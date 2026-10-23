#!/usr/bin/env python3
"""
ZiyoForum × SAP Social Sabbatical
Week 1 Wrap-Up & Plan Forward — CEO Presentation
Built on SAP template: 20260928_IntroCall_Ziyo-SAP.pptx
"""
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

SRC = '/Users/I039603/Downloads/20260928_IntroCall_Ziyo-SAP.pptx'
DST = '/Users/I039603/Downloads/ZiyoForum/ZiyoForum_Week1_CEO_Presentation.pptx'

shutil.copy(SRC, DST)
prs = Presentation(DST)

# Remove all existing slides
sli = prs.slides._sldIdLst
while len(sli):
    sli.remove(sli[0])

LY = {l.name: l for l in prs.slide_master.slide_layouts}

# ─── Minimal colour palette (SAP black + gold only) ──────────────────────────
GOLD  = RGBColor(0xF0, 0xAB, 0x00)
BLACK = RGBColor(0x00, 0x00, 0x00)
DARK  = RGBColor(0x1A, 0x1A, 0x1A)
MID   = RGBColor(0x55, 0x55, 0x55)
LGREY = RGBColor(0xF2, 0xF2, 0xF2)
MGREY = RGBColor(0xCC, 0xCC, 0xCC)
HDR_C = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

# ─── Layout-derived constants (from template inspection) ─────────────────────
# "Title Only" PH 0: pos=(0.551, 1.18), size=(12.23, 0.404)
TITLE_Y  = 1.18
TITLE_H  = 0.404
GOLD_Y   = TITLE_Y + TITLE_H + 0.02   # 1.604
CONT_Y   = GOLD_Y + 0.04 + 0.07       # 1.714  (no subtitle)
CONT_Y_S = CONT_Y + 0.30              # 2.014  (with subtitle)
CX       = 0.551
CW       = 12.23

# ─── Helpers ─────────────────────────────────────────────────────────────────

def AS(name):
    return prs.slides.add_slide(LY[name])

def PH(slide, idx):
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == idx:
            return ph
    return None

def TXB(sl, x, y, w, h, text='', sz=11, bold=False, col=BLACK,
        align=PP_ALIGN.LEFT, italic=False):
    box = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(sz)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = col
    return box, tf

def ALINE(tf, text, sz=11, bold=False, col=BLACK, after=3, before=0,
          align=PP_ALIGN.LEFT):
    p = tf.add_paragraph()
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(sz)
    r.font.bold = bold
    r.font.color.rgb = col
    if after:
        p.space_after = Pt(after)
    if before:
        p.space_before = Pt(before)
    return p

def RC(sl, x, y, w, h, fill=None, line_col=None):
    s = sl.shapes.add_shape(1, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    else:
        s.fill.background()
    if line_col:
        s.line.color.rgb = line_col
        s.line.width = Pt(0.5)
    else:
        s.line.fill.background()
    return s

def set_title(slide, text, sub=None):
    """Set placeholder title + gold bar. Returns content start y."""
    ph = PH(slide, 0)
    if ph:
        ph.text = text
    RC(slide, CX, GOLD_Y, CW, 0.035, fill=GOLD)
    if sub:
        TXB(slide, CX, GOLD_Y + 0.05, CW, 0.25, sub, sz=10, col=MID)
        return CONT_Y_S
    return CONT_Y

def tbl(sl, rows, col_widths, x, y, row_h=0.40):
    """Draw table using rectangles + textboxes."""
    cy = y
    for ri, row in enumerate(rows):
        is_hdr = ri == 0
        row_fill = HDR_C if is_hdr else (LGREY if ri % 2 == 0 else WHITE)
        txt_col  = WHITE if is_hdr else DARK
        cur_x = x
        for cell, cw in zip(row, col_widths):
            RC(sl, cur_x, cy, cw, row_h, fill=row_fill)
            TXB(sl, cur_x + 0.06, cy + 0.04, cw - 0.12, row_h - 0.06,
                cell, sz=10 if is_hdr else 9.5, bold=is_hdr, col=txt_col)
            cur_x += cw
        cy += row_h
    return cy

def divider(sl, x, y, h, col=MGREY):
    RC(sl, x, y, 0.02, h, fill=col)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1  TITLE
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('4_Cover C')
ph = PH(s, 0)
if ph:
    tf = ph.text_frame
    tf.paragraphs[0].text = 'Week 1 Complete'
    p2 = tf.add_paragraph()
    p2.text = 'What We Found & The Plan Forward'
    for r in p2.runs:
        r.font.size = Pt(26)
TXB(s, 0.55, 4.67, 9.0, 0.28,
    'Stefanie, Anja, Pankaj  ·  SAP Social Sabbatical', sz=12, col=WHITE)
TXB(s, 0.55, 4.97, 9.0, 0.28,
    '10 October 2026  ·  Tashkent, Uzbekistan', sz=12, col=WHITE)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2  AGENDA
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Agenda')

agenda = [
    ('01', 'Week 1 Recap',           'What we did, who we spoke to, and what we found'),
    ('02', 'Top Findings',           'Key insights from 6 discovery interviews'),
    ('03', 'Quick Wins',             'Urgent actions already identified and assigned'),
    ('04', 'The Plan Forward',       'Weeks 2–4: 6 pillars, deliverables, session schedule'),
    ('05', 'What We Need From You',  'Commitments that make the next 3 weeks work'),
]
for i, (num, title, desc) in enumerate(agenda):
    y = cy + i * 0.98
    RC(s, CX, y, 0.54, 0.67, fill=GOLD)
    TXB(s, CX, y + 0.14, 0.54, 0.4, num, sz=16, bold=True,
        col=BLACK, align=PP_ALIGN.CENTER)
    TXB(s, CX + 0.65, y + 0.09, CW - 0.70, 0.28, title, sz=13, bold=True, col=BLACK)
    TXB(s, CX + 0.65, y + 0.37, CW - 0.70, 0.25, desc, sz=10.5, col=MID)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3  DIVIDER — WEEK 1
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Divider Page A')
ph = PH(s, 0)
if ph:
    tf = ph.text_frame
    tf.paragraphs[0].text = 'Week 1  ·  Discovery Complete'
    p2 = tf.add_paragraph()
    p2.text = '6 interviews done  ·  6 summaries delivered  ·  Quick wins assigned'
    for r in p2.runs:
        r.font.size = Pt(16)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4  WHAT WE DID
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'What We Did in Week 1', '6–10 October 2026')

done = [
    ('6 Discovery Interviews',
     'Bobur (CEO)  ·  Sirojiddin (Events)  ·  Azam (IT)  ·  Alim (PR)  ·  Akobir (Media & App)  ·  Aksana (UX Designer)'),
    ('6 Meeting Summaries',
     'Full branded Word document for every interview — shared with each stakeholder this week'),
    ('Student Survey Drafted',
     'Uzbek-language 8-question Telegram poll ready for Sirojiddin / Akobir to distribute'),
    ('Quick Wins Identified & Assigned',
     '4 urgent actions: data privacy notice, IP ownership confirmation, design file transfer, survey launch'),
    ('ZEO Cup Attendance',
     'SAP team attended ZEO Cup — observed real student users, validated platform energy'),
    ('Delivery Plan Shared',
     'Initial SOW sent to Akobir on Friday 9 Oct as committed at start of engagement'),
]
for title, desc in done:
    RC(s, CX, cy + 0.08, 0.06, 0.06, fill=GOLD)
    TXB(s, CX + 0.13, cy, CW - 0.15, 0.27, title, sz=12, bold=True, col=BLACK)
    TXB(s, CX + 0.13, cy + 0.27, CW - 0.15, 0.24, desc, sz=10.5, col=MID)
    cy += 0.61


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5  WHO WE SPOKE TO
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Who We Spoke To',
               '6 stakeholders across all departments  ·  Discovery interviews totalling 3–8 hours')

rows5 = [
    ['Stakeholder', 'Role', 'Key Finding'],
    ['Bobur',       'Founder & CEO',
     'App stuck in demo state; no single agreed vision; team stretched; no dedicated product owner'],
    ['Sirojiddin',  'Head of Events / Youth Centre',
     '8 staff, 1,000+ volunteers; events not connected to app; QR check-in not used; no shared workflow'],
    ['Azam',        'Head of IT',
     'Data loss incident; no SLA with outsource dev; IP ownership unconfirmed; no documentation'],
    ['Alim',        'Head of PR & Partnerships',
     'University relationships exist but no model; clear path to subscription and employer revenue'],
    ['Akobir',      'Head of Media & App Lead',
     'App is events + media; no data privacy notice; no analytics; events / media teams siloed'],
    ['Aksana',      'UX Designer',
     'Never designed app UI — only banners; all UI source files locked with Azam; 1 year since last UI work'],
]
tbl(s, rows5, [1.8, 2.5, 7.93], CX, cy, row_h=0.76)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6  TOP FINDINGS
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'What We Found — Top Findings',
               'Synthesised across all 6 interviews')

HALF = 5.90
DIV_X = CX + HALF + 0.33
RX    = DIV_X + 0.04

findings_l = [
    ('No data privacy / consent notice in the app',
     'Users register without informed consent. Legal risk that must be fixed immediately.'),
    ('No SLA with outsource developer',
     'Any bug or feature could take any amount of time. No QA. IP ownership unconfirmed.'),
    ('No agreed product vision',
     'Bobur, Azam, Akobir, and Aksana describe different apps. No written vision statement.'),
    ('Events and media teams are siloed',
     'Content is not coordinated. Users see stale or incomplete event information.'),
]
findings_r = [
    ('No dedicated product owner',
     'Akobir runs media AND product. No single person accountable for the app as a product.'),
    ('UX designer never designed the app UI',
     'Aksana designed banners only. App UI was outsourced. All source files are locked with Azam.'),
    ('Strong raw potential',
     '7,000+ registered users, 1,000+ volunteers, genuine energy around ZEO Cup.'),
    ('Untapped partnership revenue',
     'Alim has university relationships with no monetisation model. Clear near-term opportunity.'),
]

cy_l = cy_r = cy
for title, desc in findings_l:
    RC(s, CX, cy_l + 0.06, 0.06, 0.06, fill=GOLD)
    TXB(s, CX + 0.14, cy_l, HALF - 0.15, 0.25, title, sz=11, bold=True, col=BLACK)
    TXB(s, CX + 0.14, cy_l + 0.25, HALF - 0.15, 0.28, desc, sz=10, col=MID)
    cy_l += 0.66

for title, desc in findings_r:
    RC(s, RX, cy_r + 0.06, 0.06, 0.06, fill=GOLD)
    TXB(s, RX + 0.14, cy_r, HALF - 0.15, 0.25, title, sz=11, bold=True, col=BLACK)
    TXB(s, RX + 0.14, cy_r + 0.25, HALF - 0.15, 0.28, desc, sz=10, col=MID)
    cy_r += 0.66

divider(s, DIV_X - 0.01, cy, 5.3)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7  QUICK WINS
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Quick Wins — Urgent Actions Already Assigned',
               'All identified in Week 1 — cannot wait for the main plan')

qw = [
    ['Action', 'Owner', 'Deadline', 'Status'],
    ['Add data privacy / consent notice to app registration',       'Akobir + Azam',       'This week', 'In progress'],
    ['Confirm IP / source code ownership with tech partner',        'Akobir + Azam',       'This week', 'In progress'],
    ['Transfer ZEO app UI source files from Azam to Aksana',        'Azam + Aksana',       'This week', 'In progress'],
    ['Launch student survey via Telegram channel',                  'Sirojiddin / Akobir', 'This week', 'In progress'],
    ['Designate dedicated Product Owner (interim: Akobir)',         'Bobur',               'Week 2',    'To confirm'],
    ['Events calendar to media team 2 weeks in advance (ongoing)',  'Sirojiddin + Akobir', 'Ongoing',   'To start'],
]
tbl(s, qw, [5.60, 2.15, 1.65, 2.83], CX, cy, row_h=0.69)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8  WEEK 1 IN PICTURES
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Week 1 in Pictures')

photos = [
    'Working Session',
    'Whiteboard / Miro Board',
    'Team Moments',
    'ZEO Cup',
]
PW, PH2 = 5.90, 2.63
positions = [(CX, cy), (CX + 6.32, cy), (CX, cy + 2.75), (CX + 6.32, cy + 2.75)]

for (px, py), cap in zip(positions, photos):
    RC(s, px, py, PW, PH2, fill=LGREY)
    RC(s, px, py + PH2 - 0.34, PW, 0.34, fill=MGREY)
    TXB(s, px + 0.1, py + PH2 - 0.30, PW - 0.2, 0.28,
        cap, sz=10.5, bold=True, col=DARK)

TXB(s, CX, cy + 5.55, CW, 0.22,
    'Add photos before sharing — drag and drop your own images into the grey boxes above.',
    sz=9, italic=True, col=MID)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9  DIVIDER — PLAN FORWARD
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Divider Page A')
ph = PH(s, 0)
if ph:
    tf = ph.text_frame
    tf.paragraphs[0].text = 'The Plan Forward'
    p2 = tf.add_paragraph()
    p2.text = 'Weeks 2–4  ·  13–31 October 2026'
    for r in p2.runs:
        r.font.size = Pt(18)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10  6 PILLARS
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, "Ziyo Forum's 6 Expectations — Our Organising Principle",
               'Every deliverable, session, and recommendation maps to one of these 6 expectations')

pillars = [
    ('①', 'Growth Strategy',    'Attract, activate, and retain young users at scale',                     'Week 2'),
    ('②', 'Product & UX',       'Identify and rank the most important product improvements',              'Week 2'),
    ('③', 'Partner Strategy',   'Scalable approach to universities, employers, and NGOs',                 'Week 3'),
    ('④', 'Analytics & KPIs',   'The 8 metrics that tell Ziyo Forum if it is growing',                   'Week 3'),
    ('⑤', 'Operating Model',    'How the team runs the app after SAP leaves',                             'Week 3'),
    ('⑥', '3-Year Roadmap',     'NOW / NEXT / LATER milestones with ownership and dependencies',          'Week 4'),
]
for num, title, desc, week in pillars:
    TXB(s, CX,        cy + 0.07, 0.54, 0.44, num, sz=20, bold=True, col=GOLD, align=PP_ALIGN.CENTER)
    TXB(s, CX + 0.65, cy + 0.04, 3.8, 0.30, title, sz=13, bold=True, col=BLACK)
    TXB(s, CX + 0.65, cy + 0.34, 10.5, 0.22, desc, sz=10, col=MID)
    TXB(s, 11.8,      cy + 0.13, 1.0, 0.28, week, sz=10, col=MID, align=PP_ALIGN.RIGHT)
    RC(s, CX, cy + 0.78, CW, 0.01, fill=MGREY)
    cy += 0.83


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 11  WEEK 2
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Week 2  ·  13–17 October  ·  Growth Strategy + Product & UX',
               'From listening to making — workshops and working sessions with tech and design leads')

CL = 5.965
GAP = 0.30
CR_X = CX + CL + GAP

TXB(s, CX,  cy, CL, 0.27, '① Growth Strategy',  sz=12.5, bold=True, col=BLACK)
RC(s,  CX,  cy + 0.28, CL, 0.03, fill=GOLD)
TXB(s, CR_X, cy, CL, 0.27, '② Product & UX', sz=12.5, bold=True, col=BLACK)
RC(s,  CR_X, cy + 0.28, CL, 0.03, fill=GOLD)

cy2 = cy + 0.37
growth_items = [
    'Analyse student survey results — motivation gaps, channel preferences, barriers',
    'Map registration → event → return visit funnel; identify largest drop-off',
    'Assess Zeocoin gamification — meaningful reward? Right cadence?',
    'Identify 2 highest-ROI acquisition channels given team capacity',
    'Map Ministry of Education merger opportunity (1M+ school-age students)',
    'Working session with Alim — draft university subscription value proposition',
]
ux_items = [
    'Session with Aksana — homepage redesign, referencing OneFit + SAP examples',
    'Map registration & onboarding flow; identify highest-friction moment',
    'Redesign event discovery & RSVP — most-cited user complaint (Sirojiddin)',
    'Define content feed minimum — what appears, in what order, how fresh',
    'Review Zeocoin UX — is earning visible and motivating?',
    'Feature priority matrix: 2×2 impact vs. effort — top-right = roadmap',
]
_, tf_l = TXB(s, CX,   cy2, CL, 0.27, f'• {growth_items[0]}', sz=10.5, col=DARK)
for it in growth_items[1:]:
    ALINE(tf_l, f'• {it}', sz=10.5, col=DARK, after=4)

_, tf_r = TXB(s, CR_X, cy2, CL, 0.27, f'• {ux_items[0]}', sz=10.5, col=DARK)
for it in ux_items[1:]:
    ALINE(tf_r, f'• {it}', sz=10.5, col=DARK, after=4)

# Sessions box
RC(s, CX, 6.22, CW, 1.02, fill=LGREY)
TXB(s, CX + 0.12, 6.27, CW - 0.24, 0.26, 'Week 2 Mandatory Sessions:', sz=10.5, bold=True, col=BLACK)
TXB(s, CX + 0.12, 6.54, CW - 0.24, 0.60,
    'SAP Masterclass (all staff · 1.5–2 hrs)   ·   Vision Workshop (CEO + all dept heads · 2 hrs)   ·   '
    'Growth Strategy Working Session   ·   Product & UX Session with Aksana   ·   Informal team gathering (Friday evening)',
    sz=10, col=DARK)

divider(s, CX + CL + GAP * 0.5, cy, 5.5)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 12  WEEK 3
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Week 3  ·  20–24 October  ·  Partner Strategy + Analytics + Operating Model',
               'Building the infrastructure Ziyo Forum needs to grow sustainably after this engagement')

c3w = 3.943
c1x, c2x, c3x = CX, CX + 4.143, CX + 8.286
c3gap = 0.15

cols3 = [
    ('③ Partner Strategy', [
        'Partner type matrix: universities, employers, NGOs, cultural institutions',
        'University subscription model with sample pricing tiers',
        'Employer partnership template — job listings + Zeocoin sponsorship',
        'NGO content partnership — listings in exchange for supply',
    ], 'Deliverable: partner framework document', c1x),
    ('④ Analytics & KPIs', [
        'Define the 8 metrics Ziyo Forum needs to track growth',
        'Map data source for each (app, app store, Trello, manual count)',
        'Build Excel dashboard pre-filled with current knowns',
        'Workshop: agree definitions, targets, and review cadence',
    ], 'Deliverable: KPI framework + Excel dashboard', c2x),
    ('⑤ Operating Model', [
        'Core team org chart: Product Owner, Designer, Tech Liaison, Content',
        'Weekly rhythm: Mon–Fri 15-min meeting cadence',
        'Feature request + bug fix: 7-step process from Trello to release',
        'Tech partner SLA: P1=48hr · P2=1wk · P3=next sprint',
    ], 'Deliverable: process playbook (Word, printable)', c3x),
]

for pillar_title, items, deliv, col_x in cols3:
    TXB(s, col_x, cy, c3w, 0.26, pillar_title, sz=12, bold=True, col=BLACK)
    RC(s, col_x, cy + 0.27, c3w, 0.03, fill=GOLD)
    cy3 = cy + 0.36
    _, tf3 = TXB(s, col_x, cy3, c3w, 0.27, f'• {items[0]}', sz=10, col=DARK)
    for it in items[1:]:
        ALINE(tf3, f'• {it}', sz=10, col=DARK, after=5)
    ALINE(tf3, '', sz=4)
    ALINE(tf3, deliv, sz=9.5, bold=True, col=MID, after=0)

divider(s, c1x + c3w + c3gap, cy, 5.1)
divider(s, c2x + c3w + c3gap, cy, 5.1)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 13  WEEK 4
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Week 4  ·  27–31 October  ·  3-Year Roadmap + Final Presentation',
               'Translating everything into one coherent plan — presented to the full team')

CL4 = 6.0
CR4X = CX + CL4 + 0.23

TXB(s, CX,  cy, CL4, 0.27, '⑥ 3-Year Roadmap',   sz=12.5, bold=True, col=BLACK)
RC(s,  CX,  cy + 0.28, CL4, 0.03, fill=GOLD)
TXB(s, CR4X, cy, CL4, 0.27, 'Final Presentation',  sz=12.5, bold=True, col=BLACK)
RC(s,  CR4X, cy + 0.28, CL4, 0.03, fill=GOLD)

roadmap = [
    ['Phase', 'Period', 'Theme & Key Milestones'],
    ['NOW',   'Oct–Dec 2026', 'Stabilise the foundation\nData privacy live  ·  IP confirmed  ·  Op model running'],
    ['NEXT',  'Q1–Q2 2027',  'Build the product that retains users\nHomepage redesigned  ·  Event RSVP flow live  ·  3 university partners'],
    ['LATER', 'H2 2027–2028','Scale with data and partnerships\n5+ universities  ·  Employer pipeline  ·  Revenue model'],
]
tbl(s, roadmap, [1.2, 1.8, 3.0], CX, cy + 0.36, row_h=0.95)

final_items = [
    'Format: 2 hours — Bobur + full Ziyo Forum team, Thursday or Friday Week 4',
    'Structure: Findings (30 min) → Growth (15) → Product (15) → Partners (15) → Analytics (10) → Op Model (10) → Roadmap (10) → Q&A',
    'Leave-behind: printed summary card + USB with all 14 deliverable documents',
    'First sprint can start 27 Oct if Operating Model is agreed in Week 3',
]
cy_r4 = cy + 0.36
_, tf_f = TXB(s, CR4X, cy_r4, CL4, 0.28, f'• {final_items[0]}', sz=10.5, col=DARK)
for it in final_items[1:]:
    ALINE(tf_f, f'• {it}', sz=10.5, col=DARK, after=7)

divider(s, CX + CL4 + 0.11, cy, 5.1)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 14  DELIVERABLES
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'What You Will Receive — 14 Deliverables',
               "All documents and sessions mapped to Ziyo Forum's 6 expectations")

left_d = [
    ['Deliverable', 'Pillar(s)', 'Week'],
    ['6 × Discovery Interview Summaries',         '—',     'Week 1 ✓'],
    ['Student Survey (Uzbek · Telegram)',          '① ④',   'Week 1 ✓'],
    ['This SOW Document',                          'All',   'Week 1 ✓'],
    ['SAP Masterclass Deck + Session',             '⑤',     'Week 2'],
    ['Vision Workshop Output',                     '① ②',   'Week 2'],
    ['Growth Strategy Document',                   '①',     'Week 3'],
    ['Product & UX Backlog + Wireframe Sketches',  '②',     'Week 3'],
]
right_d = [
    ['Deliverable', 'Pillar(s)', 'Week'],
    ['Partner Framework Document',                 '③',     'Week 3'],
    ['KPI Framework + Excel Dashboard',            '④',     'Week 3'],
    ['Process Playbook (Operating Model)',          '⑤',     'Week 3'],
    ['3-Year Roadmap Document',                    '⑥',     'Week 4'],
    ['Final Presentation Deck',                    'All',   'Week 4'],
    ['Printed One-Page Summary',                   'All',   'Week 4'],
    ['Leave-Behind USB / Shared Drive',            'All',   'Week 4'],
]

LTW = 6.10
RTX = CX + LTW + 0.13
tbl(s, left_d,  [3.8, 0.9, 1.4], CX,  cy, row_h=0.42)
tbl(s, right_d, [3.7, 0.9, 1.4], RTX, cy, row_h=0.42)
divider(s, CX + LTW + 0.05, cy, len(left_d) * 0.42)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 15  MUTUAL EXPECTATIONS
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Mutual Expectations — What Makes This Work',
               'This engagement succeeds when both sides commit')

SAP_W = 5.90
ZF_X  = CX + SAP_W + 0.43

sap_c = [
    'Deliver all 14 documents and sessions within the 4-week schedule',
    'Be present and on time for every agreed session',
    'Raise blockers early — if we need something, we say so within 24 hours',
    'Recommendations will be realistic for your team size and resources',
    'Share all work in editable formats (Word, Excel, PowerPoint)',
    'Maintain confidentiality of everything shared during the engagement',
]
zf_c = [
    'Fix the two urgent Week 1 items this week: data privacy + IP confirmation',
    'Confirm a dedicated Product Owner by Week 2 (interim: Akobir)',
    'All 6 department heads attend the Vision Workshop — no proxies',
    'Give honest, direct feedback — recommendations improve with pushback',
    'Distribute the student survey via Telegram this week',
    'Share events calendar with media team 2 weeks in advance from now on',
]

TXB(s, CX, cy, SAP_W, 0.28, 'SAP Team Commits To Ziyo Forum:', sz=12, bold=True, col=BLACK)
RC(s, CX,  cy + 0.29, SAP_W, 0.03, fill=GOLD)
_, tf_s = TXB(s, CX, cy + 0.38, SAP_W, 0.28, f'• {sap_c[0]}', sz=10.5, col=DARK)
for c in sap_c[1:]:
    ALINE(tf_s, f'• {c}', sz=10.5, col=DARK, after=5)

TXB(s, ZF_X, cy, SAP_W, 0.28, 'Ziyo Forum Commits To SAP Team:', sz=12, bold=True, col=BLACK)
RC(s, ZF_X, cy + 0.29, SAP_W, 0.03, fill=GOLD)
_, tf_z = TXB(s, ZF_X, cy + 0.38, SAP_W, 0.28, f'• {zf_c[0]}', sz=10.5, col=DARK)
for c in zf_c[1:]:
    ALINE(tf_z, f'• {c}', sz=10.5, col=DARK, after=5)

divider(s, CX + SAP_W + 0.2, cy, 5.2)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 16  NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Title Only')
cy = set_title(s, 'Next Steps & Key Dates', 'What happens after this meeting')

next_rows = [
    ['When',               'Session',                          'Who',                                     'Format'],
    ['Mon 13 Oct',         'SAP Masterclass',                  'All Ziyo Forum staff (mandatory)',         '1.5–2 hrs'],
    ['Mon–Tue 13–14 Oct',  'Vision Workshop',                  'CEO + all 6 dept heads (mandatory)',       '2 hrs'],
    ['Tue–Thu 13–16 Oct',  'Growth Strategy Sessions',         'SAP + Alim + Akobir',                     'Working sessions'],
    ['Wed–Thu 14–16 Oct',  'Product & UX Sessions',            'SAP + Aksana + Azam',                     'Working sessions'],
    ['Fri 17 Oct',         'Informal Team Gathering',          'SAP + Ziyo Forum team',                   'Evening social'],
    ['Week of 20 Oct',     'Partner, Analytics & Op Model',    'SAP + relevant dept leads',                'Working sessions'],
    ['Week of 27 Oct',     '3-Year Roadmap + Final Prep',      'SAP + Bobur',                             'Workshop + rehearsal'],
    ['Thu–Fri 30–31 Oct',  'Final Presentation',               'Bobur + full Ziyo Forum team',            '2 hours'],
]
tbl(s, next_rows, [2.10, 3.70, 4.15, 2.28], CX, cy, row_h=0.54)


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 17  THANK YOU
# ═══════════════════════════════════════════════════════════════════════════════
s = AS('Thank you B')
ph = PH(s, 0)
if ph:
    ph.text = 'Thank you!'
TXB(s, 3.0, 5.65, 7.5, 0.28,
    'Stefanie, Anja, Pankaj  ·  SAP Social Sabbatical Team',
    sz=12, col=WHITE, align=PP_ALIGN.CENTER)
TXB(s, 3.0, 5.93, 7.5, 0.28,
    'October 2026  ·  Tashkent, Uzbekistan',
    sz=12, col=WHITE, align=PP_ALIGN.CENTER)


# ─── Save ─────────────────────────────────────────────────────────────────────
prs.save(DST)
print(f'Saved: {DST}')
print(f'Slides: {len(prs.slides)}')
