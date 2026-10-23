"""
Final EN_DICT patch — add all remaining untranslated strings found across all 26 screens.
"""
PATH = '/Users/I039603/Downloads/ZiyoForum/Ziyo_App_Prototype.html'

with open(PATH) as f:
    content = f.read()

# Find EN_DICT end
en_dict_start = content.find('const EN_DICT')
en_dict_end = content.find('\n};', en_dict_start)
assert en_dict_end >= 0, "Could not find EN_DICT end"

en_dict_section = content[en_dict_start:en_dict_end]

def already_has(key):
    return f'"{key}"' in en_dict_section

NEW_ENTRIES = ""

# ── v-home ────────────────────────────────────────────────────────────────────
pairs_home = [
    ("CV yozish sirlari", "CV writing secrets"),
    ("Suhbatga tayyorlanish", "Interview preparation"),
    ("Suhbatga tayyorlanish sirlari", "Interview preparation secrets"),
    ("60s: Grantga ariza", "60s: Grant application"),
]

# ── v-courses ─────────────────────────────────────────────────────────────────
pairs_courses = [
    ("1 kun", "1 day"),
    ("2 kun", "2 days"),
    ("6 hafta", "6 weeks"),
    ("8 hafta", "8 weeks"),
    ("10 hafta", "10 weeks"),
    ("Public Speaking Treningi", "Public Speaking Training"),
    ("Ziyo Academy · Boshlang'ich", "Ziyo Academy · Beginner"),
    ("Ziyo Academy · O'rta", "Ziyo Academy · Intermediate"),
    ("Kurslar", "Courses"),
]

# ── v-course (detail) ─────────────────────────────────────────────────────────
pairs_course = [
    ("Kurs haqida", "About this course"),
    ("Kursni tugatganingizda beriladi", "Awarded on course completion"),
    ("Oldindan tajriba shart emas", "No prior experience required"),
    ("8 hafta · haftasiga 3 dars", "8 weeks · 3 lessons per week"),
    ("Boshlang'ich daraja", "Beginner level"),
    ("Senior Engineer · 6 yil tajriba", "Senior Engineer · 6 years experience"),
    ("Kursga yozilish", "Enrol in course"),
    ("📚 KURS · 8 hafta", "📚 COURSE · 8 weeks"),
]

# ── v-event (detail) ──────────────────────────────────────────────────────────
pairs_event = [
    ("+30 🪙 qatnashganlik uchun", "+30 🪙 for attending"),
    ("Tadbir chati", "Event chat"),
    ("O'zbekistondagi eng yirik IT karyera kuni! 40+ kompaniya, jonli suhbatlar, amaliy sessiyalar.", "Uzbekistan's largest IT career day! 40+ companies, live interviews, practical sessions."),
]

# ── v-register ────────────────────────────────────────────────────────────────
pairs_register = [
    ("12-noyabr · Tashkent IT Park", "Nov 12 · Tashkent IT Park"),
    ("To'liq ism", "Full name"),
    ("Ziyo Forum qoidalari va maxfiylik siyosatiga roziman", "I agree to Ziyo Forum terms and privacy policy"),
]

# ── v-ticket ──────────────────────────────────────────────────────────────────
pairs_ticket = [
    ("Chiptangiz tayyor. Tadbir kuni QR kodni ko'rsating.", "Your ticket is ready. Show the QR code on event day."),
    ("Ro'yxatdan o'tdingiz!", "You're registered!"),
    ("TADBIR CHIPTASI", "EVENT TICKET"),
    ("📅 12-noyabr · 10:00", "📅 Nov 12 · 10:00"),
]

# ── v-scan ────────────────────────────────────────────────────────────────────
pairs_scan = [
    ("QR kodni skanerlash (demo)", "Scan QR code (demo)"),
    ("Tadbir yoki kurs QR kodini skanerlang", "Scan the event or course QR code"),
    ("Tadbirga kelganingizni tasdiqlang va ZiyoCoin yutib oling 🪙", "Confirm attendance and earn ZiyoCoin 🪙"),
    ("kodni qo'lda kiriting", "enter code manually"),
]

# ── v-grants ──────────────────────────────────────────────────────────────────
pairs_grants = [
    ("Grantlar & stipendiyalar", "Grants & scholarships"),
    ("Grantlar &amp; stipendiyalar", "Grants & scholarships"),
    ("Magistratura · 1 yillik", "Master's · 1 year"),
    ("Chevening Scholarship (UK)", "Chevening Scholarship (UK)"),
    ('"Chevening tajribam"', '"My Chevening experience"'),
    ('"DAAD\'ni qanday yutdim"', '"How I won DAAD"'),
    ('"Fulbright yo\'lim"', '"My Fulbright journey"'),
    ('"Germaniyaga qanday bordim"', '"How I went to Germany"'),
    ('"Boshida imkonsiz tuyuldi. Ziyo menga yo\'l ko\'rsatdi — hujjatlardan suhbatgacha."', '"It seemed impossible at first. Ziyo guided me — from documents to the interview."'),
]

# ── v-grant (detail) ──────────────────────────────────────────────────────────
pairs_grant = [
    ("🎓 GRANT · Magistratura", "🎓 GRANT · Master's"),
    ("Siz uchun mosligi yuqori", "High match for you"),
    ("Profilingiz talablarga mos keladi", "Your profile matches the requirements"),
    ("Motivatsion xatni qanday yozish kerak", "How to write a motivation letter"),
    ("G'olib tajribasi 🎬", "Winner's experience 🎬"),
    ('"DAAD\'ni qanday yutdim" — Nodira', '"How I won DAAD" — Nodira'),
    ("DAAD — Germaniyada magistratura uchun to'liq stipendiya: o'quv to'lovi, oylik nafaqa va boshqa imtiyozlar.", "DAAD — Full scholarship for Master's in Germany: tuition fee, monthly allowance and other benefits."),
    ("Ariza topshirish", "Apply now"),
]

# ── v-jobs ────────────────────────────────────────────────────────────────────
pairs_jobs = [
    ("Ishlar & amaliyot", "Jobs & internships"),
    ("Ishlar &amp; amaliyot", "Jobs & internships"),
    ("Bolalarga ta'lim", "Education for children"),
]

# ── v-job (detail) ────────────────────────────────────────────────────────────
pairs_job = [
    ("6 oy", "6 months"),
    ("Kurs ›", "Course ›"),
    ("Ariza yuborish", "Submit application"),
    ("Mentorlar juda yordam berdi. 6 oydan keyin ishga taklif qilishdi 🙌", "The mentors were very helpful. They offered me a job after 6 months 🙌"),
    ("Yaxshi tajriba, lekin tempi tez. Oldindan React o'rganib boring.", "Good experience, but the pace is fast. Learn React beforehand."),
]

# ── v-bytes ───────────────────────────────────────────────────────────────────
pairs_bytes = [
    ("60 soniyada grantga qanday ariza beriladi 🎓", "How to apply for a grant in 60 seconds 🎓"),
    ("Mukammal CV yozishning 3 siri 📄", "3 secrets to writing a perfect CV 📄"),
    ("Suhbatda ko'p so'raladigan 5 savol 🎤", "5 most common interview questions 🎤"),
    ("#grant #tahsil #ziyotips", "#grant #education #ziyotips"),
]

# ── v-podcasts ────────────────────────────────────────────────────────────────
pairs_podcasts = [
    ("Nol'dan birinchi mahsulotgacha", "From zero to first product"),
    ("2-qism · Grantlar olami", "Part 2 · World of grants"),
    ("Xalqaro stipendiyalar bo'yicha qo'llanma", "Guide to international scholarships"),
    ("Professional aloqalar qanday quriladi", "How to build professional connections"),
    ("▶ 19 daqiqa", "▶ 19 min"),
    ("▶ 27 daqiqa", "▶ 27 min"),
    ("▶ 31 daqiqa", "▶ 31 min"),
]

# ── v-podcast (detail) ────────────────────────────────────────────────────────
pairs_podcast = [
    ("Mehmonimiz — Google'da ishlaydigan muhandis. U birinchi ishga kirish, portfolio tuzish va xalqaro arenaga chiqish haqida so'zlaydi.", "Our guest is an engineer working at Google. They talk about landing the first job, building a portfolio and entering the international stage."),
]

# ── v-profile ─────────────────────────────────────────────────────────────────
pairs_profile = [
    ("Ko'nikmalar qo'shing · CV biriktiring", "Add skills · Attach CV"),
]

# ── v-notifications ───────────────────────────────────────────────────────────
pairs_notifs = [
    ("Bugun · 18:42 · 12 ta yangi xabar", "Today · 18:42 · 12 new messages"),
    ("Ertaga tadbir!", "Event tomorrow!"),
    ("IT Career Day 2026 — 12-noyabr, soat 10:00. Tashkent IT Park. Tayyormisiz?", "IT Career Day 2026 — Nov 12, 10:00. Tashkent IT Park. Are you ready?"),
    ("IT Career Day chatida yangi xabarlar", "New messages in IT Career Day chat"),
    ("Asilbek: \"Kim ertaga Google stendiga boradi? 👀\"", "Asilbek: \"Who's going to the Google stand tomorrow? 👀\""),
    ("+30 ZiyoCoin qo'shildi!", "+30 ZiyoCoin added!"),
    ("UX/UI Bootcamp tadbirida qatnashganingiz uchun mukofot. Balansingiz: 🪙 1,250", "Reward for attending UX/UI Bootcamp. Your balance: 🪙 1,250"),
    ("Python Hackathon sertifikatingiz tayyorlandi. Yuklab olish uchun bosing.", "Your Python Hackathon certificate is ready. Tap to download."),
    ("Haftalik reytingda #6-o'rindan #4-o'ringa ko'tarildingiz. Top 3 gacha 290 🪙 qoldi!", "You moved from #6 to #4 in the weekly ranking. 290 🪙 to reach Top 3!"),
    ("IT Career Day 2026 ga muvaffaqiyatli ro'yxatdan o'tdingiz. Chiptangiz tayyor!", "You've successfully registered for IT Career Day 2026. Your ticket is ready!"),
    ("18-noyabr kuni Startup Weekend boshlanadi. Ro'yxatdan o'ting va +50 🪙 yig'ing!", "Startup Weekend starts Nov 18. Register and earn +50 🪙!"),
    ("2-noyabr · 09:00", "Nov 2 · 09:00"),
    ("Yangi tadbir: Startup Weekend", "New event: Startup Weekend"),
    ("Ro'yxatga olindi", "Registered"),
]

# ── v-leaderboard ─────────────────────────────────────────────────────────────
pairs_lb = [
    ("🎟 Tadbir", "🎟 Events"),
]

# ── v-feedback ────────────────────────────────────────────────────────────────
pairs_feedback = [
    ("Yuborish · +10 🪙", "Send · +10 🪙"),
]

# ── v-chatroom ────────────────────────────────────────────────────────────────
pairs_chatroom = [
    ("Salom! Kim ertaga Google stendiga boradi? 👀", "Hello! Who's going to the Google stand tomorrow? 👀"),
    ("Men boraman! CV tayyorlab qo'ydim 📄", "I'm going! Got my CV ready 📄"),
    ("Men ham! 10:00 da kirish eshigida uchrashamizmi?", "Me too! Shall we meet at the entrance at 10:00?"),
    ("Zo'r g'oya 🙌 Kelishdik!", "Great idea 🙌 Deal!"),
]

# ── v-mocktests ───────────────────────────────────────────────────────────────
pairs_mocktests = [
    ("— keyin qayta tiklanadi. Gaming oldini olish uchun.", "— resets later. To prevent gaming."),
]

# ── v-skills ─────────────────────────────────────────────────────────────────
pairs_skills = [
    ("+ Qo'shish", "+ Add"),
    ("🇺🇿 O'zbek", "🇺🇿 Uzbek"),
    ("da quloqchin, sichqoncha, sumka va boshqa sovg'alarga almashtiring.", "redeem for earphones, mouse, bags and other gifts."),
]

# Combine all
all_pairs = (
    pairs_home + pairs_courses + pairs_course + pairs_event +
    pairs_register + pairs_ticket + pairs_scan + pairs_grants +
    pairs_grant + pairs_jobs + pairs_job + pairs_bytes + pairs_podcasts +
    pairs_podcast + pairs_profile + pairs_notifs + pairs_lb +
    pairs_feedback + pairs_chatroom + pairs_mocktests + pairs_skills
)

added = []
for uz, en in all_pairs:
    if not already_has(uz):
        # Escape for JS string
        uz_esc = uz.replace('\\', '\\\\').replace('"', '\\"')
        en_esc = en.replace('\\', '\\\\').replace('"', '\\"')
        NEW_ENTRIES += f'\n  "{uz_esc}": "{en_esc}",'
        added.append(uz)
    else:
        print(f'  already has: {uz[:50]}')

# Insert before closing }; of EN_DICT
content = content[:en_dict_end] + NEW_ENTRIES + content[en_dict_end:]

with open(PATH, 'w') as f:
    f.write(content)

print(f'\nAdded {len(added)} new EN_DICT entries:')
for a in added:
    print(f'  + {a[:60]}')
print('\nPatch applied!')
