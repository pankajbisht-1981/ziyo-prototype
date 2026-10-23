"""
Patch Ziyo_App_Prototype.html:
1. Replace Doston's base64 photo avatar in rank-4 list row with text avatar DT
2. Replace Doston's base64 photo in sticky rank bar with text avatar DT
3. Make period tabs (Hafta/Oy/Umumiy) show different coin leaderboard data
4. Add EN_DICT entries for all untranslated strings
"""

PATH = '/Users/I039603/Downloads/ZiyoForum/Ziyo_App_Prototype.html'

with open(PATH) as f:
    content = f.read()

# ── 1. Replace Doston's photo in rank-4 list row ─────────────────────────────
# The row starts with lb-rank 4 + avatar xs with background:none + img tag
# Find start marker
ROW4_START = '<div class="lb-row"><div class="lb-rank">4</div><div class="avatar xs" style="width:36px;height:36px;background:none;overflow:hidden;padding:0;">'
ROW4_END_MARKER = '🪙 1,250</div></div>\n          <div class="lb-row"><div class="lb-rank">5</div>'

row4_start = content.find(ROW4_START)
assert row4_start >= 0, "Could not find rank-4 row start"

row4_end_pos = content.find(ROW4_END_MARKER, row4_start)
assert row4_end_pos >= 0, "Could not find rank-4 row end marker"
row4_end = row4_end_pos + len('🪙 1,250</div></div>')
# The end marker includes the next row, so we only replace up to row4_end which excludes the next row start

OLD_ROW4 = content[row4_start:row4_end]
NEW_ROW4 = ('<div class="lb-row you"><div class="lb-rank">4</div>'
            '<div class="avatar xs">DT</div>'
            '<div style="flex:1;">'
            '<div style="font-weight:700;">Doston Toshmatov <span class="xs" style="color:var(--green-d);">· Siz</span></div>'
            '<div class="xs delta-up">▲ 2 o\'rin</div>'
            '</div>'
            '<div style="font-weight:800;color:var(--green-d);">🪙 1,250</div></div>')

content = content[:row4_start] + NEW_ROW4 + content[row4_end:]
print('Step 1 done: replaced Doston photo in rank-4 list row')

# ── 2. Replace Doston's photo in sticky rank bar ──────────────────────────────
# The sticky bar also has a base64 img for Doston
# Find the sticky rank bar section
STICKY_START = '<!-- sticky your rank -->'
sticky_pos = content.find(STICKY_START)
assert sticky_pos >= 0

# Find the img in the sticky section
sticky_section_start = content.find('<div style="position:absolute;bottom:0', sticky_pos)
# Find the lb-row in sticky that has the photo
sticky_row_start = content.find('<div class="lb-row', sticky_section_start)

# Find "Doston" alt in sticky
sticky_doston = content.find('alt="Doston">', sticky_row_start)
assert sticky_doston >= 0, "Could not find Doston alt in sticky"

# Find the start of the avatar div in sticky (has background:none pattern)
sticky_avatar_start = content.rfind('<div class="avatar xs"', sticky_row_start, sticky_doston)
assert sticky_avatar_start >= 0

# Find end of avatar (after alt="Doston">)
sticky_avatar_end = sticky_doston + len('alt="Doston">')
# +</div> to close avatar div
sticky_avatar_close = content.find('</div>', sticky_avatar_end)
sticky_avatar_end_full = sticky_avatar_close + len('</div>')

OLD_STICKY_AVATAR = content[sticky_avatar_start:sticky_avatar_end_full]
NEW_STICKY_AVATAR = '<div class="avatar xs">DT</div>'

content = content[:sticky_avatar_start] + NEW_STICKY_AVATAR + content[sticky_avatar_end_full:]
print('Step 2 done: replaced Doston photo in sticky rank bar')

# ── 3. Make period tabs show different data ──────────────────────────────────
# Update the period seg labels: Hafta (Week), Oy (Month), Umumiy (Overall)
# Add data-period attributes and update lbPeriod() function to swap data

# Add data-period attributes to period tabs
OLD_PERIOD_SEG = '''        <div id="lb-period-seg" class="seg" style="max-width:280px;margin:10px auto 0;background:rgba(255,255,255,.22);">
          <div onclick="lbPeriod(this)">Hafta</div>
          <div class="on" onclick="lbPeriod(this)">Oy</div>
          <div onclick="lbPeriod(this)">Umumiy</div>
        </div>'''

NEW_PERIOD_SEG = '''        <div id="lb-period-seg" class="seg" style="max-width:280px;margin:10px auto 0;background:rgba(255,255,255,.22);">
          <div onclick="lbPeriod(this,'week')">Hafta</div>
          <div class="on" onclick="lbPeriod(this,'month')">Oy</div>
          <div onclick="lbPeriod(this,'all')">Umumiy</div>
        </div>'''

content = content.replace(OLD_PERIOD_SEG, NEW_PERIOD_SEG, 1)
print('Step 3a done: added period params to tabs')

# Update lbPeriod() to swap leaderboard data based on period
OLD_LB_PERIOD_FN = "function lbPeriod(el){ [...el.parentNode.children].forEach(c=>c.classList.remove('on')); el.classList.add('on'); toast('Reyting: '+el.textContent); }"

NEW_LB_PERIOD_FN = r"""function lbPeriod(el,period){
  [...el.parentNode.children].forEach(c=>c.classList.remove('on')); el.classList.add('on');
  // Different leaderboard data per period
  const DATA={
    week:[
      {rank:1,init:'DT',name:'Doston Toshmatov',you:true,delta:'▲ 3 o\'rin',cls:'delta-up',coins:'🪙 420'},
      {rank:2,init:'JA',name:'Jasur Abdullayev',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 390'},
      {rank:3,init:'NK',name:'Nilufar Karimova',delta:'▲ 1 o\'rin',cls:'delta-up',coins:'🪙 310'},
      {rank:4,init:'SU',name:'Sardor Umarov',delta:'— o\'zgarishsiz',cls:'delta-eq',coins:'🪙 280'},
      {rank:5,init:'AN',name:'Asilbek Normatov',delta:'▲ 2 o\'rin',cls:'delta-up',coins:'🪙 240'},
      {rank:6,init:'MY',name:'Malika Yusupova',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 195'},
      {rank:7,init:'BQ',name:'Bobur Qodirov',delta:'▲ 1 o\'rin',cls:'delta-up',coins:'🪙 170'},
      {rank:8,init:'ZS',name:'Zarina Saidova',delta:'▼ 2 o\'rin',cls:'delta-dn',coins:'🪙 130'},
      {rank:9,init:'JT',name:'Jahongir Toshev',delta:'— o\'zgarishsiz',cls:'delta-eq',coins:'🪙 95'}
    ],
    month:[
      {rank:1,init:'JA',name:'Jasur Abdullayev',delta:'— o\'zgarishsiz',cls:'delta-eq',coins:'🪙 2,480'},
      {rank:2,init:'NK',name:'Nilufar Karimova',delta:'▲ 1 o\'rin',cls:'delta-up',coins:'🪙 1,920'},
      {rank:3,init:'SU',name:'Sardor Umarov',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 1,540'},
      {rank:4,init:'DT',name:'Doston Toshmatov',you:true,delta:'▲ 2 o\'rin',cls:'delta-up',coins:'🪙 1,250',green:true},
      {rank:5,init:'AN',name:'Asilbek Normatov',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 960'},
      {rank:6,init:'MY',name:'Malika Yusupova',delta:'— o\'zgarishsiz',cls:'delta-eq',coins:'🪙 870'},
      {rank:7,init:'BQ',name:'Bobur Qodirov',delta:'▲ 3 o\'rin',cls:'delta-up',coins:'🪙 740'},
      {rank:8,init:'ZS',name:'Zarina Saidova',delta:'▼ 2 o\'rin',cls:'delta-dn',coins:'🪙 610'},
      {rank:9,init:'JT',name:'Jahongir Toshev',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 480'}
    ],
    all:[
      {rank:1,init:'JA',name:'Jasur Abdullayev',delta:'— o\'zgarishsiz',cls:'delta-eq',coins:'🪙 8,920'},
      {rank:2,init:'NK',name:'Nilufar Karimova',delta:'▲ 2 o\'rin',cls:'delta-up',coins:'🪙 7,340'},
      {rank:3,init:'MY',name:'Malika Yusupova',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 6,810'},
      {rank:4,init:'SU',name:'Sardor Umarov',delta:'▼ 1 o\'rin',cls:'delta-dn',coins:'🪙 5,540'},
      {rank:5,init:'AN',name:'Asilbek Normatov',delta:'▲ 1 o\'rin',cls:'delta-up',coins:'🪙 4,260'},
      {rank:6,init:'BQ',name:'Bobur Qodirov',delta:'▲ 4 o\'rin',cls:'delta-up',coins:'🪙 3,740'},
      {rank:7,init:'DT',name:'Doston Toshmatov',you:true,delta:'▲ 1 o\'rin',cls:'delta-up',coins:'🪙 3,250',green:true},
      {rank:8,init:'ZS',name:'Zarina Saidova',delta:'▼ 3 o\'rin',cls:'delta-dn',coins:'🪙 2,610'},
      {rank:9,init:'JT',name:'Jahongir Toshev',delta:'▼ 2 o\'rin',cls:'delta-dn',coins:'🪙 1,980'}
    ]
  };
  const rows=DATA[period||'month'];
  const panel=document.getElementById('lb-coins-panel');
  const card=panel.querySelector('.card');
  // rebuild rows
  let html='';
  rows.forEach(r=>{
    const youCls=r.you?' you':'';
    const youBadge=r.you?' <span class="xs" style="color:var(--green-d);">· Siz</span>':'';
    const coinColor=r.green?' style="font-weight:800;color:var(--green-d);"':' style="font-weight:800;"';
    const rankBg=r.you?' style="background:var(--green);color:#fff;"':'';
    html+=`<div class="lb-row${youCls}"><div class="lb-rank"${rankBg}>${r.rank}</div><div class="avatar xs">${r.init}</div><div style="flex:1;"><div style="font-weight:700;">${r.name}${youBadge}</div><div class="xs ${r.cls}">${r.delta}</div></div><div${coinColor}>${r.coins}</div></div>`;
  });
  card.innerHTML=html;
  // update sticky rank bar
  const me=rows.find(r=>r.you);
  if(me){
    const stickyRow=document.querySelector('.lb-row.you[style*="border:none"]')||document.querySelector('[data-sticky-rank]');
    if(stickyRow){
      const rankEl=stickyRow.querySelector('.lb-rank');
      if(rankEl) rankEl.textContent=me.rank;
      const coinEl=stickyRow.lastElementChild;
      if(coinEl) coinEl.textContent=me.coins.replace('🪙 ','🪙 ');
    }
  }
}"""

content = content.replace(OLD_LB_PERIOD_FN, NEW_LB_PERIOD_FN, 1)
print('Step 3b done: updated lbPeriod() function with real data')

# ── 4. Add EN_DICT entries for all untranslated strings ──────────────────────
# Find EN_DICT closing };
en_dict_end = content.find('\n};', content.find('const EN_DICT'))
assert en_dict_end >= 0, "Could not find EN_DICT end"

NEW_ENTRIES = """
  // ── Event detail screen ─────────────────────────────
  "12-noyabr, 2026": "Nov 12, 2026",
  "320 ishtirokchi": "320 attendees",
  "+30 🪙qatnashganlik uchun": "+30 🪙 for attending",
  "Tashkilotchi": "Organiser",
  "Rasmiy tashkilotchi · ✓ Tasdiqlangan": "Official organiser · ✓ Verified",
  "Fikringizni bildiring": "Share your reaction",
  "ta reaksiya": "reactions",
  "142 ta reaksiya": "142 reactions",
  "58 ta xabar · hozir faol": "58 messages · active now",
  "Event chati": "Event chat",
  "ANMYDT": "ANMYDT",
  "Qatnashish": "Attend",
  "Qatnashmoqchi emasman": "Not attending",
  "Ro'yxatdan o'tish": "Register",
  // ── Leaderboard ──────────────────────────────────────
  "🏆 ZiyoCoin reytingi": "🏆 ZiyoCoin Rankings",
  "Eng faol foydalanuvchilar": "Most active students",
  "📊 Faollik": "📊 Activity",
  "Hafta": "Week",
  "Oy": "Month",
  "Umumiy": "Overall",
  "Talaba": "Student",
  "⏱ Vaqt": "⏱ Time",
  "soat": "hrs",
  "tadbir": "events",
  "Har kuni ilovaga kiring, videolar ko'ring va tadbirlarda qatnashing — faolligingiz oshadi!": "Log in every day, watch videos and attend events — your activity score will grow!",
  "Sizning o'rningiz": "Your rank",
  "Top 3 gacha 290 🪙 qoldi": "290 🪙 to reach Top 3",
  "▲ 2 o'rin": "▲ 2 places",
  "▲ 1 o'rin": "▲ 1 place",
  "▼ 1 o'rin": "▼ 1 place",
  "▼ 2 o'rin": "▼ 2 places",
  "▲ 3 o'rin": "▲ 3 places",
  "▼ 3 o'rin": "▼ 3 places",
  "▲ 4 o'rin": "▲ 4 places",
  "▼ 4 o'rin": "▼ 4 places",
  "— o'zgarishsiz": "— no change",
  // ── Home screen ──────────────────────────────────────
  "Tavsiya etilgan": "Recommended",
  "Bugun": "Today",
  "Hafta reytingi": "Weekly ranking",
  "ZiyoCoin balansi": "ZiyoCoin balance",
  "Barchasi": "All",
  "Tadbirlar": "Events",
  "Kurslar": "Courses",
  "Grantlar": "Grants",
  "Ish o'rinlari": "Jobs",
  "Podkastlar": "Podcasts",
  // ── Navigation / tabs ────────────────────────────────
  "Bosh sahifa": "Home",
  "Profil": "Profile",
  "Bildirishnomalar": "Notifications",
  // ── Profile screen ───────────────────────────────────
  "Sertifikatlar": "Certificates",
  "Yutuqlar": "Achievements",
  "Ko'nikmalari": "Skills",
  "Qatnashgan tadbirlar": "Events attended",
  "Tugatilgan kurslar": "Courses completed",
  "Ishlar": "Jobs",
  "CV yuklash": "Upload CV",
  "Tahrirlash": "Edit",
  "Sozlamalar": "Settings",
  "Chiqish": "Sign out",
  "Profil tahrirlash": "Edit profile",
  "O'rni": "Rank",
  "Sertifikat": "Certificate",
  // ── Grants / Jobs ────────────────────────────────────
  "Ariza topshirish": "Apply now",
  "Muddati": "Deadline",
  "Talablar": "Requirements",
  "Ariza topshirdingiz": "Application submitted",
  "Muvaffaqiyatli ariza topshirildi": "Application submitted successfully",
  "Grant haqida": "About the grant",
  "Ish haqida": "About the job",
  "Ish joyi": "Work location",
  "Maosh": "Salary",
  "Ish turi": "Job type",
  "To'liq stavka": "Full-time",
  "Qisman stavka": "Part-time",
  "Masofaviy": "Remote",
  // ── Courses ─────────────────────────────────────────
  "Kursni boshlash": "Start course",
  "Davom ettirish": "Continue",
  "Tugatildi": "Completed",
  "Darslar": "Lessons",
  "Daraja": "Level",
  "Boshlang'ich": "Beginner",
  "O'rta": "Intermediate",
  "Ilg'or": "Advanced",
  "Davomiyligi": "Duration",
  // ── Notifications ────────────────────────────────────
  "Barcha bildirishnomalar": "All notifications",
  "O'qilmagan": "Unread",
  "O'chirib tashlash": "Delete",
  // ── Settings ────────────────────────────────────────
  "Til": "Language",
  "Hisob": "Account",
  "Maxfiylik": "Privacy",
  "Yordam": "Help",
  "Ilovani baholash": "Rate the app",
  "Versiya": "Version",
  // ── Chat ────────────────────────────────────────────
  "Xabar yozing...": "Write a message...",
  "Yuborish": "Send",
  "Chatga qo'shilish": "Join chat",
  // ── Onboarding ──────────────────────────────────────
  "Qiziqishlaringizni tanlang": "Select your interests",
  "Davom etish": "Continue",
  "O'tkazib yuborish": "Skip",
  // ── Quick bytes ─────────────────────────────────────
  "Qisqa videolar": "Quick Bytes",
  "Izoh": "Comment",
  "Ulashish": "Share",
  // ── Podcasts ────────────────────────────────────────
  "Podkast tinglash": "Listen to podcast",
  "Epizodlar": "Episodes",
  // ── Shop ────────────────────────────────────────────
  "Do'kon": "Shop",
  "Sotib olish": "Buy",
  "Narxi": "Price",
  "Balans yetarli emas": "Insufficient balance",
  // ── Skill test / Mock tests ──────────────────────────
  "Ko'nikma testi": "Skill test",
  "Sinov testlari": "Mock tests",
  "Savol": "Question",
  "Javob": "Answer",
  "Natija": "Result",
  "Tekshirish": "Check",
  "Keyingi": "Next",
  "Oldingi": "Previous",
  "Yakunlash": "Finish",
  // ── Ticket / Register ────────────────────────────────
  "Bilet": "Ticket",
  "QR kod": "QR code",
  "Ro'yxatdan o'tdingiz": "Registered successfully",
  "Tasdiqlash": "Confirm",
  "Bekor qilish": "Cancel",
  // ── Feedback ────────────────────────────────────────
  "Fikr bildirish": "Give feedback",
  "Xabar": "Message",
  "Yuborish": "Send",
  // ── General UI strings ───────────────────────────────
  "Yuklanmoqda...": "Loading...",
  "Xatolik yuz berdi": "An error occurred",
  "Qayta urinib ko'ring": "Try again",
  "Orqaga": "Back",
  "Yopish": "Close",
  "Ko'proq": "More",
  "Kamroq": "Less",
  "Hammasi": "All",
  "Sana": "Date",
  "Vaqt": "Time",
  "Joy": "Location",
  "Bepul": "Free",
  "Pullik": "Paid",
  "Yangi": "New",
  "Ommabop": "Popular","""

# Insert before the closing }; of EN_DICT
content = content[:en_dict_end] + NEW_ENTRIES + content[en_dict_end:]
print('Step 4 done: added EN_DICT entries')

with open(PATH, 'w') as f:
    f.write(content)

print('All patches applied successfully!')
