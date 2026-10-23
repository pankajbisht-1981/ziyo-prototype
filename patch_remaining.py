"""Fix 4 remaining untranslated strings — exact keys now match actual HTML text."""
PATH = '/Users/I039603/Downloads/ZiyoForum/Ziyo_App_Prototype.html'

with open(PATH) as f:
    content = f.read()

en_dict_start = content.find('const EN_DICT')
en_dict_end = content.find('\n};', en_dict_start)
assert en_dict_end >= 0

en_dict_section = content[en_dict_start:en_dict_end]

PAIRS = [
    # exact HTML texts (verified by grep)
    (
        "Jonli + yozib olingan darslar",
        "Live + recorded lessons"
    ),
    (
        "HTML, CSS, JavaScript'dan React va Node.js'gacha — zamonaviy web ilovalarni noldan quring. Har hafta amaliy loyiha va mentor bilan jonli sessiya.",
        "From HTML, CSS, JavaScript to React and Node.js — build modern web apps from scratch. Every week: a practical project and live session with a mentor."
    ),
    (
        "O'zbekistondagi eng yirik IT karyera kuni! 40+ kompaniya, jonli suhbatlar, amaliyot va ish o'rinlari. CV'ingizni oling va bevosita HR mutaxassislari bilan tanishing.",
        "Uzbekistan's largest IT career day! 40+ companies, live sessions and job opportunities. Bring your CV and meet HR specialists directly."
    ),
    (
        "DAAD — Germaniyada magistratura uchun to'liq stipendiya: o'quv to'lovi, oylik nafaqa (~992€), sayohat va sug'urta. Ariza onlayn topshiriladi.",
        "DAAD — Full scholarship for Master’s in Germany: tuition fee, monthly allowance (~€992), travel and insurance. Apply online."
    ),
]

new_entries = ""
added = []
for uz, en in PAIRS:
    if f'"{uz}"' not in en_dict_section:
        uz_esc = uz.replace('\\', '\\\\').replace('"', '\\"')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"')
        new_entries += f'\n  "{uz_esc}": "{en_esc}",'
        added.append(uz[:60])

content = content[:en_dict_end] + new_entries + content[en_dict_end:]

with open(PATH, 'w') as f:
    f.write(content)

print(f'Added {len(added)} entries:')
for a in added:
    print(f'  + {a}')
