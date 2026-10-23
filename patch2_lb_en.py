"""
Patch 2: Fix lbPeriod() to translate delta strings when in English mode,
and fix sticky rank bar 'Your rank' text.
"""
PATH = '/Users/I039603/Downloads/ZiyoForum/Ziyo_App_Prototype.html'

with open(PATH) as f:
    content = f.read()

# After the `const rows=DATA[period||'month'];` line, add a translation helper
# and fix the delta values post-render

OLD_ROWS_LINE = "  const rows=DATA[period||'month'];\n  const panel=document.getElementById('lb-coins-panel');"

NEW_ROWS_LINE = """  const rows=DATA[period||'month'];
  // translate delta strings when in English
  const _isEn=(typeof _lang!=='undefined'&&_lang==='en')||localStorage.getItem('ziyoLang')==='en';
  const _d=(s)=>{if(!_isEn)return s;return s.replace(/▲ (\\d+) o'rin/,'▲ $1 places').replace(/▼ (\\d+) o'rin/,'▼ $1 places').replace("— o'zgarishsiz","— no change");};
  rows.forEach(r=>{r.delta=_d(r.delta);});
  const panel=document.getElementById('lb-coins-panel');"""

content = content.replace(OLD_ROWS_LINE, NEW_ROWS_LINE, 1)
print('Step 1 done: added delta translation helper in lbPeriod()')

# Also fix the sticky "Sizning o'rningiz" to translate to "Your rank"
# The sticky bar has hardcoded Uzbek - it's in a static div that applyEnglish()
# should handle since "Sizning o'rningiz" should be in EN_DICT
# Let's verify it's in EN_DICT
if "Sizning o'rningiz" in content:
    # It's in the HTML - check if it's in EN_DICT
    en_dict_start = content.find('const EN_DICT')
    en_dict_end = content.find('\n};', en_dict_start)
    en_dict = content[en_dict_start:en_dict_end]
    if "Sizning o'rningiz" in en_dict:
        print("Step 2: 'Sizning o'rningiz' already in EN_DICT - OK")
    else:
        print("Step 2: Need to add 'Sizning o'rningiz' to EN_DICT")
        # Add to EN_DICT
        new_entry = '\n  "Sizning o\'rningiz": "Your rank",'
        content = content[:en_dict_end] + new_entry + content[en_dict_end:]
        print('Step 2 done: added to EN_DICT')
else:
    print("Step 2: 'Sizning o'rningiz' not found in content")

# Also fix "Top 3 gacha 290 🪙 qoldi" if not already in EN_DICT
en_dict_start = content.find('const EN_DICT')
en_dict_end = content.find('\n};', en_dict_start)
en_dict = content[en_dict_start:en_dict_end]
if '"Top 3 gacha' not in en_dict:
    new_entry = '\n  "Top 3 gacha 290 🪙 qoldi": "290 🪙 to reach Top 3",'
    content = content[:en_dict_end] + new_entry + content[en_dict_end:]
    print('Step 3 done: added "Top 3 gacha" to EN_DICT')

with open(PATH, 'w') as f:
    f.write(content)
print('Patch 2 applied!')
