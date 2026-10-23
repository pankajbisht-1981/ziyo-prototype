"""
Patch Ziyo_App_Prototype.html:
1. Remove duplicate Doston row (rank 5 DT initials)
2. Fix Doston photo avatar size (add width/height to container)
3. Renumber ranks 6→5, 7→6, 8→7, 9→8, 10→9
4. Add ZiyoCoins / Faollik type switcher tab
5. Add Activity leaderboard panel
6. Add lbType() JS function
"""

PATH = '/Users/I039603/Downloads/ZiyoForum/Ziyo_App_Prototype.html'

with open(PATH) as f:
    content = f.read()

# ── 1. Fix photo avatar size (rank-4 Doston in the list) ──────────────────
# The container has no width/height, so the img stretches. Add explicit size.
content = content.replace(
    '<div class="lb-rank">4</div><div class="avatar xs" style="background:none;overflow:hidden;padding:0;">',
    '<div class="lb-rank">4</div><div class="avatar xs" style="width:36px;height:36px;background:none;overflow:hidden;padding:0;">',
    1  # only first occurrence (the list row, not the sticky bar)
)

# ── 2. Remove duplicate Doston DT row (rank 5) ────────────────────────────
DUPE_ROW = ('\n          <div class="lb-row"><div class="lb-rank">5</div>'
            '<div class="avatar xs">DT</div><div style="flex:1;">'
            '<div style="font-weight:700;">Doston Toshmatov</div>'
            '<div class="xs delta-up">▲ 1 o\'rin</div></div>'
            '<div style="font-weight:800;">🪙 1,080</div></div>')
content = content.replace(DUPE_ROW, '', 1)

# ── 3. Renumber remaining ranks 6→5, 7→6, 8→7, 9→8, 10→9 ─────────────────
for old_init, old_rank, new_rank in [
    ('AN', '6', '5'),
    ('MY', '7', '6'),
    ('BQ', '8', '7'),
    ('ZS', '9', '8'),
    ('JT', '10', '9'),
]:
    old_str = f'<div class="lb-rank">{old_rank}</div><div class="avatar xs">{old_init}</div>'
    new_str = f'<div class="lb-rank">{new_rank}</div><div class="avatar xs">{old_init}</div>'
    content = content.replace(old_str, new_str, 1)

# ── 4. Wrap existing scroll div with id="lb-coins-panel" ──────────────────
content = content.replace(
    '<div class="scroll no-tab" style="padding-top:0;padding-bottom:120px;">',
    '<div id="lb-coins-panel" class="scroll no-tab" style="padding-top:0;padding-bottom:120px;">',
    1
)

# ── 5. Add ZiyoCoins/Faollik type seg before period seg ───────────────────
TYPE_SEG = '''        <div class="seg mt20" id="lb-type-seg" style="max-width:260px;margin:16px auto 0;background:rgba(255,255,255,.22);">
          <div class="on" onclick="lbType(this,\'coins\')">🪙 ZiyoCoins</div>
          <div onclick="lbType(this,\'activity\')">📊 Faollik</div>
        </div>
        '''
OLD_PERIOD_SEG_OPEN = '        <div class="seg mt20" style="max-width:280px;margin:20px auto 0;background:rgba(255,255,255,.22);">'
NEW_PERIOD_SEG_OPEN = TYPE_SEG + '        <div id="lb-period-seg" class="seg" style="max-width:280px;margin:10px auto 0;background:rgba(255,255,255,.22);">'
content = content.replace(OLD_PERIOD_SEG_OPEN, NEW_PERIOD_SEG_OPEN, 1)

# ── 6. Add activity panel after the coins panel (before sticky rank bar) ──
ACTIVITY_ROWS = '''
          <div style="display:flex;align-items:center;gap:12px;padding:6px 14px 4px;font-size:10px;font-weight:700;color:var(--muted);">
            <div style="width:24px;"></div><div style="width:36px;"></div>
            <div style="flex:1;padding-left:4px;">Talaba</div>
            <div style="min-width:50px;text-align:center;">⏱ Vaqt</div>
            <div style="min-width:40px;text-align:center;">🎟 Tadbir</div>
            <div style="min-width:40px;text-align:center;">📹 Video</div>
          </div>'''

def act_row(rank, init, name, you=False, hours=0, events=0, videos=0, last=False):
    you_cls = ' you' if you else ''
    you_badge = ' <span class="xs" style="color:var(--green-d);">· Siz</span>' if you else ''
    border = ' style="border-bottom:none;"' if last else ''
    return (
        f'\n          <div class="lb-row{you_cls}"{border}>'
        f'<div class="lb-rank">{rank}</div>'
        f'<div class="avatar xs">{init}</div>'
        f'<div style="flex:1;"><div style="font-weight:700;">{name}{you_badge}</div></div>'
        f'<div style="min-width:50px;text-align:center;"><div style="font-weight:800;font-size:13px;">{hours}</div><div class="xs muted">soat</div></div>'
        f'<div style="min-width:40px;text-align:center;"><div style="font-weight:800;font-size:13px;">{events}</div><div class="xs muted">tadbir</div></div>'
        f'<div style="min-width:40px;text-align:center;"><div style="font-weight:800;font-size:13px;">{videos}</div><div class="xs muted">video</div></div>'
        f'</div>'
    )

students = [
    ('JA', 'Jasur A.',    False, 18, 12, 35, False),
    ('SU', 'Sardor U.',   False, 15, 10, 28, False),
    ('NK', 'Nilufar K.',  False, 14,  9, 31, False),
    ('DT', 'Doston T.',   True,  12,  8, 24, False),
    ('AN', 'Asilbek N.',  False, 11,  7, 20, False),
    ('MY', 'Malika Y.',   False, 10,  6, 18, False),
    ('BQ', 'Bobur Q.',    False,  8,  5, 14, False),
    ('ZS', 'Zarina S.',   False,  7,  4, 11, False),
    ('JT', 'Jahongir T.', False,  5,  3,  8, True),
]

rows_html = ACTIVITY_ROWS
for rank, (init, name, you, hours, events, videos, last) in enumerate(students, 1):
    rows_html += act_row(rank, init, name, you, hours, events, videos, last)

ACTIVITY_PANEL = f'''      </div>
      <!-- activity leaderboard panel -->
      <div id="lb-activity-panel" class="scroll no-tab" style="padding-top:0;padding-bottom:120px;display:none;">
        <div class="card" style="margin:-50px 14px 0;border-radius:22px;padding:8px 6px;position:relative;">{rows_html}
        </div>
        <div class="card" style="margin:14px 14px 0;border-radius:18px;padding:14px 16px;background:var(--green-ll);">
          <div class="row gap12" style="align-items:center;">
            <div style="font-size:22px;">🔥</div>
            <div class="sm" style="color:var(--ink2);line-height:1.5;">Har kuni ilovaga kiring, videolar ko'ring va tadbirlarda qatnashing — faolligingiz oshadi!</div>
          </div>
        </div>
      </div>
      <!-- sticky your rank -->'''

OLD_STICKY = '      </div>\n      <!-- sticky your rank -->'
content = content.replace(OLD_STICKY, ACTIVITY_PANEL, 1)

# ── 7. Add lbType() JS function after lbPeriod ────────────────────────────
OLD_LB_PERIOD = ('function lbPeriod(el){ [...el.parentNode.children].forEach(c=>c.classList.remove(\'on\')); '
                 'el.classList.add(\'on\'); toast(\'Reyting: \'+el.textContent); }')
NEW_LB_PERIOD = (OLD_LB_PERIOD + '''
function lbType(el,type){
  [...el.parentNode.children].forEach(c=>c.classList.remove('on')); el.classList.add('on');
  const coins=document.getElementById('lb-coins-panel');
  const act=document.getElementById('lb-activity-panel');
  const periodSeg=document.getElementById('lb-period-seg');
  if(type==='activity'){
    coins.style.display='none'; act.style.display='block'; if(periodSeg) periodSeg.style.display='none';
  } else {
    coins.style.display='block'; act.style.display='none'; if(periodSeg) periodSeg.style.display='';
  }
}''')
content = content.replace(OLD_LB_PERIOD, NEW_LB_PERIOD, 1)

with open(PATH, 'w') as f:
    f.write(content)

print('Done. Leaderboard patched.')
