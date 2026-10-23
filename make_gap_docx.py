"""
Create Ziyo_Product_UX_Gap_Analysis.docx
matching the format of User-Research-Playbook.docx
"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.oxml.ns import qn
from lxml import etree
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# ─── Open template to inherit styles ───
doc = Document('/Users/I039603/Downloads/User-Research-Playbook.docx')

# Remove all existing content but preserve the sectPr (section/page properties)
body = doc.element.body
# Keep only the sectPr element (page size, margins) — remove everything else
sectPr = body.find(qn('w:sectPr'))
for element in list(body):
    body.remove(element)
if sectPr is not None:
    body.append(sectPr)

# ─── Helpers ───
def add_para(text, style='Normal', bold=False, italic=False):
    p = doc.add_paragraph(style=style)
    run = p.add_run(text)
    if bold:   run.bold = True
    if italic: run.italic = True
    return p

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.left_indent = Inches(0.25)
    if bold_prefix:
        run = p.add_run(bold_prefix + ': ')
        run.bold = True
        p.add_run(text)
    else:
        p.add_run(text)
    return p

# ─── Header table matching template ───
def add_header_table():
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'
    row = table.rows[0]

    c0 = row.cells[0]
    c0.text = 'SAP Social Sabbatical'
    c0.paragraphs[0].runs[0].bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(9)

    c1 = row.cells[1]
    p = c1.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('SAP Social Sabbatical x Ziyo App')
    run.bold = True
    run.font.size = Pt(10)

    c2 = row.cells[2]
    c2.text = 'October 2026'
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    c2.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# DOCUMENT
# ══════════════════════════════════════════════════════════════

add_header_table()

doc.add_heading('Product & UX Assessment / Gap Analysis', level=1)

intro = doc.add_paragraph(style='Normal')
intro.add_run(
    'This document assesses the current Ziyo App against the prototype vision, '
    'identifying feature gaps, UX shortfalls, and prioritised recommendations. '
    'Findings are grounded in user research (UX Designer and Events Head interviews), '
    'app-store analytics, and a full review of the 26-screen interactive prototype.'
)

doc.add_paragraph()

# ── Context ──
doc.add_heading('Context & Current State', level=2)
add_para(
    'The current Ziyo App (iOS and Android) serves as an event-discovery and resource hub for students '
    'in Uzbekistan. It lists events, courses, grants, and job opportunities in a minimal text/image '
    'interface. The UI has remained unchanged for over 12 months, and the Android version suffers from '
    'an active image-distortion bug. Analytics show an 83.8 % Android uninstall rate (2,018 of 2,408 '
    'installs) and an app-store rating of 3.0 stars with 5 unanswered 1-star reviews.'
)

doc.add_paragraph()

# ── Key Stats ──
doc.add_heading('Key Metrics at a Glance', level=2)
stats = [
    ('26+', 'prototype screens mapped across 8 feature categories'),
    ('9', 'feature gaps identified between current app and prototype'),
    ('83.8 %', 'Android uninstall rate — 2,018 of 2,408 installs uninstalled'),
    ('3.0 star', 'Android app-store rating (5 unanswered 1-star reviews)'),
    ('297', 'active Android users (Dec 2025)'),
]
for num, desc in stats:
    add_bullet(desc, bold_prefix=num)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# FEATURE CATEGORIES
# ══════════════════════════════════════════════════════════════

doc.add_heading('Feature Gap Analysis by Category', level=1)

categories = [
    {
        'name': '1. Home & Discovery',
        'current': (
            'Static list of events/courses with no personalisation; same feed for all users '
            'regardless of interests or role.'
        ),
        'features': [
            ('Personalised feed',
             'Match-% scoring surfaces content most relevant to each user based on interests and history.'),
            ('5 category tabs',
             'Dedicated tabs for Events, Courses, Grants, Jobs, and Podcasts replace a single undifferentiated list.'),
            ('Featured cards',
             'Rich image cards with coin-reward badges, capacity indicators, and category labels.'),
            ('Weekly rank header',
             'Leaderboard position and ZiyoCoin balance surfaced on the home screen for daily motivation.'),
            ('Interest filtering',
             'Quick-filter chips (Tech / Design / Business etc.) allow instant content narrowing.'),
            ('Onboarding flow',
             'Interest-selection and role wizard on first launch seeds the personalisation model.'),
            ('Activity nudges',
             'Smart notifications remind users of events they bookmarked or grants with upcoming deadlines.'),
        ],
    },
    {
        'name': '2. Content Formats',
        'current': (
            'Text/image cards only. No short-form video, no audio, no structured course player. '
            'Android image distortion bug active.'
        ),
        'features': [
            ('Quick Bytes',
             'TikTok-style vertical short-form video scroll — bite-sized educational clips and event highlights.'),
            ('Podcast player',
             'In-app audio player with transcript overlay, chapter markers, and playback speed control.'),
            ('Course curriculum',
             'Structured lesson list with progress bar, locked/unlocked state, and estimated duration per module.'),
            ('Event detail',
             'Rich event page: cover image, agenda, speaker cards, location map, and attendee count.'),
            ('Grant detail',
             'Grant card with eligibility criteria, deadline countdown, and one-tap Apply button.'),
            ('Job listing',
             'Job/internship card with company logo, requirements, and in-app apply flow.'),
            ('Bookmarks',
             'Save any content type to a personal library accessible offline.'),
        ],
    },
    {
        'name': '3. Events',
        'current': (
            'Event registration runs via Telegram bot and QR to Google Docs entirely outside the app. '
            'No in-app ticketing, check-in, or post-event certificate.'
        ),
        'features': [
            ('Discovery feed',
             'Upcoming and past events in a card feed with filter by category, city, and date.'),
            ('One-tap registration',
             'Native in-app register button; confirmation saved to profile with calendar export.'),
            ('Digital ticket',
             'QR-code ticket stored in a Ticket Wallet within the app; accessible offline.'),
            ('QR check-in',
             'Event staff scan attendee QR codes using the in-app camera — replaces manual Google Docs.'),
            ('Chatroom',
             'Per-event group chat auto-opens on registration for attendee networking before and after the event.'),
            ('Social proof',
             'Live attendee count, reactions, and photo gallery post-event visible to non-attendees.'),
            ('Auto certificate',
             'Attendance certificate generated automatically after QR check-in and added to profile.'),
        ],
    },
    {
        'name': '4. Learning',
        'current': (
            'No structured learning flow. Courses are listed but have no enrolment, '
            'progress tracking, or certificate issuance.'
        ),
        'features': [
            ('Enrolment',
             'Single-tap course enrolment; enrolled courses appear under an "In Progress" tab on profile.'),
            ('Progress tracking',
             'Module-level progress bar and last-lesson bookmark so users resume exactly where they left off.'),
            ('Mock tests',
             'Formative quizzes at the end of each module with instant feedback and score history.'),
            ('Completion certificate',
             'Auto-generated PDF certificate on course completion — downloadable and shareable.'),
            ('Grants listings',
             'Curated grant cards filtered by education level, field of study, and deadline proximity.'),
            ('Deadline reminders',
             'Push notifications 7 days and 24 hours before grant and application deadlines.'),
            ('Short apply form',
             'Streamlined in-app application form pre-filled from profile data (name, university, CV).'),
        ],
    },
    {
        'name': '5. ZiyoCoins & Gamification',
        'current': (
            'ZiyoCoins exist in the backend but are invisible in the UI — no balance, no earning events, no shop. '
            'Zero daily-return incentive.'
        ),
        'features': [
            ('Balance on home',
             'ZiyoCoin balance displayed prominently in the home header; tapping opens earning history.'),
            ('Earn on registration',
             'Coins awarded instantly when a user registers for an event.'),
            ('Earn on attendance',
             'Bonus coins credited after QR check-in confirms physical attendance at an event.'),
            ('Earn on course',
             'Coins awarded for each completed course module and double on certificate earn.'),
            ('Earn on referral',
             'Referral code shared to friends earns both parties a bonus on the first event attended.'),
            ('Shop',
             'Merch shop where ZiyoCoins redeem for branded items, event discounts, and premium access.'),
            ('History',
             'Transaction log showing every earn and spend event with date, source, and amount.'),
        ],
    },
    {
        'name': '6. Leaderboard & Recognition',
        'current': 'No leaderboard feature anywhere in the current app. Recognition system entirely absent.',
        'features': [
            ('Full leaderboard',
             'Global and friends-filtered leaderboard ranked by ZiyoCoin balance, updated weekly.'),
            ('Medal podium',
             'Top 3 users displayed in a visually prominent podium with gold/silver/bronze treatment.'),
            ('Weekly rank tracker',
             'Personal rank card on the home screen showing movement (up/down) vs. previous week.'),
            ('Achievement badges',
             'Unlockable badges for milestones: First Event, 10 Courses, Top 10 Leaderboard, etc.'),
            ('Rank on profile',
             'Current leaderboard position displayed on user profile, visible to other users.'),
            ('Streak system',
             'Daily app-open streak counter with bonus coins for 7-day and 30-day streaks.'),
            ('Rank notifications',
             'Push notification when a user enters the Top 10 or is overtaken by a follower.'),
        ],
    },
    {
        'name': '7. Profile & Career',
        'current': (
            'Static profile with basic user info only. No certificates, no skill tracking, no career tools.'
        ),
        'features': [
            ('Skills & CV',
             'Skill tag selection and CV file upload; displayed on profile for recruiter/organiser visibility.'),
            ('AI recommendations',
             'AI-powered gap analysis comparing current skills to target roles, surfacing relevant courses.'),
            ('Jobs board',
             'In-app job and internship listings matched to user skills and field of study.'),
            ('In-app apply',
             'One-click apply using profile data; application status tracked under an "Applied" tab.'),
            ('Certificate library',
             'All earned certificates (events + courses) stored as downloadable PDFs in the profile.'),
            ('Attendance history',
             'Full history of attended events, with dates, coin earnings, and ratings per event.'),
            ('Stats overview',
             'Dashboard showing coins earned, events attended, courses completed, and leaderboard rank.'),
        ],
    },
    {
        'name': '8. Community & Settings',
        'current': (
            'No in-app social features. No notification centre. '
            'Settings are minimal with no language or interest customisation.'
        ),
        'features': [
            ('Direct messages',
             'One-to-one and group DMs with other app users; accessible from profile or event chatroom.'),
            ('Notification centre',
             'Unified inbox for event reminders, leaderboard alerts, coin rewards, and messages.'),
            ('Event reminders',
             'Smart reminders at 1 hour and 10 minutes before events the user registered for.'),
            ('Language toggle',
             'Instant UI switch between Uzbek (Cyrillic), Uzbek (Latin), and English.'),
            ('Interest preferences',
             'Re-selectable interest tags that update the personalised home feed in real time.'),
            ('Account settings',
             'Manage profile photo, university, graduation year, notification preferences, and privacy.'),
            ('Feedback form',
             'In-app feedback form with screenshot attachment — routes directly to the product team.'),
        ],
    },
]

for cat in categories:
    doc.add_heading(cat['name'], level=2)

    p = doc.add_paragraph(style='Normal')
    r = p.add_run('Current state: ')
    r.bold = True
    p.add_run(cat['current'])

    p2 = doc.add_paragraph(style='Normal')
    p2.add_run('Prototype features:').bold = True

    for feature, desc in cat['features']:
        add_bullet(desc, bold_prefix=feature)

    doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# GAP SUMMARY TABLE
# ══════════════════════════════════════════════════════════════

doc.add_heading('Gap Summary', level=1)

add_para(
    'The table below summarises the severity of each gap against the prototype vision. '
    'Priority is rated High / Medium / Low based on user impact and implementation effort.'
)
doc.add_paragraph()

gap_table = doc.add_table(rows=1, cols=4)
gap_table.style = 'Table Grid'
gap_table.alignment = WD_TABLE_ALIGNMENT.CENTER

hdr = gap_table.rows[0].cells
for i, h in enumerate(['Category', 'Gap', 'User Impact', 'Priority']):
    hdr[i].text = h
    hdr[i].paragraphs[0].runs[0].bold = True
    hdr[i].paragraphs[0].runs[0].font.size = Pt(9)

gaps = [
    ('Home & Discovery', 'No personalisation — same feed for all users', 'High', 'HIGH'),
    ('Content Formats', 'Android image distortion bug — images appear smashed', 'High', 'HIGH'),
    ('Events', 'Registration via Telegram bot, not in-app', 'High', 'HIGH'),
    ('Learning', 'No enrolment, progress tracking, or certificates', 'High', 'HIGH'),
    ('ZiyoCoins', 'Coins invisible — no balance, no earning, no shop', 'High', 'HIGH'),
    ('Leaderboard', 'Feature entirely absent from current app', 'Medium', 'HIGH'),
    ('Profile & Career', 'No Skills & CV, no certificate download, no jobs', 'Medium', 'MEDIUM'),
    ('Community', 'No DMs, no notifications, no social features', 'Medium', 'MEDIUM'),
    ('Store Reviews', '5 unanswered 1-star reviews — no public response', 'High', 'HIGH'),
]
for category, gap, impact, priority in gaps:
    row = gap_table.add_row()
    for i, v in enumerate([category, gap, impact, priority]):
        row.cells[i].text = v
        row.cells[i].paragraphs[0].runs[0].font.size = Pt(9)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════

doc.add_heading('Priority Recommendations', level=1)

doc.add_heading('Phase 1 — Quick Wins (0–8 weeks)', level=2)
add_para(
    'Address the most visible issues that require minimal development time '
    'but have the highest user-trust impact.'
)
phase1 = [
    ('Fix Android image distortion',
     'Images appear smashed on Android — reported for months, still unfixed. '
     'Affects all 297 active Android users. Critical for store rating recovery.'),
    ('Reply to 5 unanswered 1-star reviews',
     'Public response with a V2 timeline commitment rebuilds trust, signals active development, '
     'and improves store ranking.'),
    ('In-app event registration',
     'Replace Telegram bot + QR to Google Docs flow with native in-app registration. '
     'Top request from Events Head (Sirojiddin).'),
    ('Coin balance on home screen',
     'Surface ZiyoCoin balance in the home header. Requires backend connection only — '
     'no new features. Immediately motivates daily return.'),
    ('Content category filters',
     'Add filter chips to the home feed so users can narrow to Events, Courses, '
     'Grants, or Jobs without manual scrolling.'),
]
for title, desc in phase1:
    add_bullet(desc, bold_prefix=title)

doc.add_paragraph()
doc.add_heading('Phase 2 — Core Engagement Loop (2–4 months)', level=2)
add_para('Build the features that create a daily return habit and measurable engagement.')
phase2 = [
    ('Full gamification loop',
     'ZiyoCoin earn events (registration, attendance, course), leaderboard, and merch shop.'),
    ('Personalised home feed',
     'Onboarding interest flow plus match-% ranking algorithm for events and courses.'),
    ('Native QR check-in',
     'In-app camera-based QR scanner for event attendance — enables auto certificate issuance.'),
    ('Rich content formats',
     'Quick Bytes video scroll and podcast player to increase session depth.'),
]
for title, desc in phase2:
    add_bullet(desc, bold_prefix=title)

doc.add_paragraph()
doc.add_heading('Phase 3 — Career & Community (4–6 months)', level=2)
add_para(
    'Build the differentiating features that make Ziyo a career platform, '
    'not just an event app.'
)
phase3 = [
    ('Skills & CV plus Jobs board',
     'Profile skills section, CV upload, AI gap recommendations, and in-app job apply flow.'),
    ('Achievement profile',
     'Certificate library, attendance history, badges, and leaderboard rank on profile.'),
    ('Social layer',
     'Event chatrooms, DMs, reactions, and community features.'),
    ('Language & accessibility',
     'Full Uzbek (Cyrillic/Latin) and English localisation with right-to-left layout support.'),
]
for title, desc in phase3:
    add_bullet(desc, bold_prefix=title)

doc.add_paragraph()

# ══════════════════════════════════════════════════════════════
# CONCLUSIONS
# ══════════════════════════════════════════════════════════════

doc.add_heading('Conclusions', level=1)
add_para(
    'The Ziyo App prototype demonstrates a substantially richer product than the current application — '
    '26+ interactive screens covering gamification, skills & career, social features, and rich content '
    'formats. The current app records an 83.8 % Android uninstall rate with a UI unchanged for over '
    '12 months, indicating a critical retention problem.'
)
doc.add_paragraph()
add_para(
    'Closing this gap requires: (1) an immediate fix sprint targeting the Android image bug and unanswered '
    'reviews; (2) a structured feature roadmap prioritising gamification and personalisation as the core '
    'engagement drivers; and (3) addressing the design-access constraint — the UX Designer currently '
    'cannot iterate on the interface without file access from the developer.'
)
doc.add_paragraph()
add_para(
    'This assessment serves as the foundation for the Vision Workshop (Deliverable 2) and Target User '
    'Personas (Deliverable 4) in the SAP Social Sabbatical product vision engagement.'
)

# ─── Save ───
out_path = '/Users/I039603/Downloads/ZiyoForum/Ziyo_Product_UX_Gap_Analysis.docx'
doc.save(out_path)
print(f'Saved -> {out_path}')
