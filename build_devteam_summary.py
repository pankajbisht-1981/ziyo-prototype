#!/usr/bin/env python3
"""
ZiyoForum × SAP Social Sabbatical
Meeting Summary — External Development Team (Tech Partner)
Same format as all previous Ziyo Forum stakeholder summaries.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

DST = '/Users/I039603/Downloads/ZiyoForum/Sync_with_DevTeam_Minutes.docx'

# ─── Colours ─────────────────────────────────────────────────────────────────
NAVY    = RGBColor(0x00, 0x33, 0x66)
NAVY2   = RGBColor(0x00, 0x1A, 0x44)
TEAL    = RGBColor(0x1D, 0xCE, 0xAF)
GOLD    = RGBColor(0xF0, 0xAB, 0x00)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
LGREY   = RGBColor(0xF2, 0xF4, 0xF7)
DGREY   = RGBColor(0x22, 0x22, 0x22)
MUTED   = RGBColor(0x6B, 0x77, 0x85)
RED     = RGBColor(0xC0, 0x00, 0x00)
AMBER   = RGBColor(0x9A, 0x68, 0x00)
GREEN   = RGBColor(0x00, 0x6B, 0x3C)
ORANGE  = RGBColor(0xD2, 0x47, 0x26)

doc = Document()

# ─── Page margins ─────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(1.8)
    section.bottom_margin = Cm(1.8)
    section.left_margin   = Cm(2.2)
    section.right_margin  = Cm(2.2)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def shd_para(para, hex_colour):
    pPr = para._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_colour)
    pPr.append(shd)

def shd_cell(cell, hex_colour):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_colour)
    tcPr.append(shd)

def set_col_width(cell, width_cm):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), str(int(width_cm * 567)))
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)

def section_title(doc, text):
    p = doc.add_paragraph()
    shd_para(p, '003366')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after  = Pt(0)
    p.paragraph_format.left_indent  = Cm(0)
    run = p.add_run(f'  {text}')
    run.bold = True
    run.font.size = Pt(10.5)
    run.font.color.rgb = WHITE
    run.font.name = 'Calibri'

def sub(doc, text, bold=False, colour=None, size=10.5, before=4, after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after  = Pt(after)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Calibri'
    if colour:
        run.font.color.rgb = colour
    return p

def bullet(doc, text, bold_prefix=None, indent=0.4):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent   = Cm(indent)
    p.paragraph_format.space_before  = Pt(2)
    p.paragraph_format.space_after   = Pt(2)
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.size = Pt(10.5)
        r1.font.name = 'Calibri'
        r2 = p.add_run(text)
        r2.font.size = Pt(10.5)
        r2.font.name = 'Calibri'
    else:
        r = p.add_run(text)
        r.font.size = Pt(10.5)
        r.font.name = 'Calibri'

def callout(doc, text, bg='FFF8E1', left_bar='F0AB00', bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    p.paragraph_format.left_indent  = Cm(0.3)
    shd_para(p, bg)
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.bold = True
        r1.font.size = Pt(10.5)
        r1.font.name = 'Calibri'
        r2 = p.add_run(text)
        r2.font.size = Pt(10.5)
        r2.font.name = 'Calibri'
    else:
        r = p.add_run(text)
        r.font.size = Pt(10.5)
        r.font.name = 'Calibri'

def two_col(doc, left_items, right_items, header_left='', header_right=''):
    table = doc.add_table(rows=1 + max(len(left_items), len(right_items)), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.LEFT

    for ci, hdr in enumerate([header_left, header_right]):
        cell = table.rows[0].cells[ci]
        shd_cell(cell, '003366')
        p = cell.paragraphs[0]
        run = p.add_run(hdr)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.size = Pt(10)
        run.font.name = 'Calibri'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_col_width(cell, 7.8)

    for ri in range(max(len(left_items), len(right_items))):
        row = table.rows[ri + 1]
        for ci, items in enumerate([left_items, right_items]):
            cell = row.cells[ci]
            shd_cell(cell, 'F2F4F7' if ri % 2 == 0 else 'FFFFFF')
            if ri < len(items):
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after  = Pt(2)
                run = p.add_run(items[ri])
                run.font.size = Pt(10)
                run.font.name = 'Calibri'

def findings_table(doc, rows):
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Table Grid'

    headers = ['#', 'Finding', 'Implication for SAP Recommendation']
    widths   = [0.6, 7.5, 7.5]
    for ci, (hdr, w) in enumerate(zip(headers, widths)):
        cell = table.rows[0].cells[ci]
        shd_cell(cell, '003366')
        p = cell.paragraphs[0]
        run = p.add_run(hdr)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.size = Pt(10)
        run.font.name = 'Calibri'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_col_width(cell, w)

    for ri, (num, severity, finding, implication) in enumerate(rows):
        row = table.add_row()
        bg = 'F2F4F7' if ri % 2 == 0 else 'FFFFFF'

        # Number + severity dot
        c0 = row.cells[0]
        shd_cell(c0, bg)
        p = c0.paragraphs[0]
        dot = p.add_run(severity + '\n')
        dot.font.size = Pt(11)
        dot.font.name = 'Calibri'
        n = p.add_run(str(num))
        n.font.size = Pt(9)
        n.font.name = 'Calibri'
        n.font.color.rgb = MUTED
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

        c1 = row.cells[1]
        shd_cell(c1, bg)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        r1 = p1.add_run(finding)
        r1.font.size = Pt(10)
        r1.font.name = 'Calibri'

        c2 = row.cells[2]
        shd_cell(c2, bg)
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(2)
        r2 = p2.add_run(implication)
        r2.font.size = Pt(10)
        r2.font.name = 'Calibri'
        r2.font.color.rgb = MUTED

def actions_table(doc, rows):
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'
    headers = ['#', 'Action', 'Owner', 'Deadline']
    widths  = [0.5, 9.5, 3.5, 2.1]
    for ci, (hdr, w) in enumerate(zip(headers, widths)):
        cell = table.rows[0].cells[ci]
        shd_cell(cell, '003366')
        p = cell.paragraphs[0]
        run = p.add_run(hdr)
        run.bold = True
        run.font.color.rgb = WHITE
        run.font.size = Pt(10)
        run.font.name = 'Calibri'
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        set_col_width(cell, w)

    for ri, (num, action, owner, deadline) in enumerate(rows):
        row = table.add_row()
        bg = 'F2F4F7' if ri % 2 == 0 else 'FFFFFF'
        data = [str(num), action, owner, deadline]
        for ci, (cell_text, w) in enumerate(zip(data, widths)):
            cell = row.cells[ci]
            shd_cell(cell, bg)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after  = Pt(2)
            run = p.add_run(cell_text)
            run.font.size = Pt(10)
            run.font.name = 'Calibri'
            if ci == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.font.color.rgb = MUTED
            if ci == 3:
                run.font.bold = True


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER BLOCK
# ═══════════════════════════════════════════════════════════════════════════════
header = doc.add_table(rows=1, cols=1)
header.alignment = WD_TABLE_ALIGNMENT.LEFT
cell = header.rows[0].cells[0]
shd_cell(cell, '001A44')

p = cell.add_paragraph()
r = p.add_run('MEETING MINUTES  ·  EXTERNAL DEVELOPMENT TEAM')
r.font.size = Pt(9)
r.font.color.rgb = TEAL
r.font.name = 'Calibri'
r.bold = True
p.paragraph_format.space_before = Pt(10)
p.paragraph_format.space_after  = Pt(2)

p2 = cell.add_paragraph()
r2 = p2.add_run('Tech Partner Interview  —  ZEO App Development Team')
r2.font.size = Pt(18)
r2.font.color.rgb = WHITE
r2.font.name = 'Calibri'
r2.bold = True
p2.paragraph_format.space_after = Pt(4)

p3 = cell.add_paragraph()
r3 = p3.add_run('SAP Social Sabbatical × Ziyo Forum  ·  Tashkent, Uzbekistan  ·  October 2026')
r3.font.size = Pt(10)
r3.font.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
r3.font.name = 'Calibri'
p3.paragraph_format.space_after = Pt(10)


# ═══════════════════════════════════════════════════════════════════════════════
#  STAT ROW
# ═══════════════════════════════════════════════════════════════════════════════
doc.add_paragraph()
stats_table = doc.add_table(rows=2, cols=4)
stats_table.alignment = WD_TABLE_ALIGNMENT.LEFT

stats = [
    ('10+', 'App Versions Released'),
    ('Flutter / Node.js', 'Tech Stack  (iOS / Android)'),
    ('~2 Weeks', 'Feature Delivery TAT'),
    ('0', 'Formal Requirements Documents'),
]
for ci, (num, label) in enumerate(stats):
    top_cell = stats_table.rows[0].cells[ci]
    bot_cell = stats_table.rows[1].cells[ci]
    shd_cell(top_cell, 'F0F4FA')
    shd_cell(bot_cell, 'F0F4FA')
    set_col_width(top_cell, 3.9)

    p_num = top_cell.paragraphs[0]
    p_num.paragraph_format.space_before = Pt(6)
    p_num.paragraph_format.space_after  = Pt(0)
    r_num = p_num.add_run(num)
    r_num.bold = True
    r_num.font.size = Pt(18)
    r_num.font.color.rgb = NAVY
    r_num.font.name = 'Calibri'

    p_lbl = bot_cell.paragraphs[0]
    p_lbl.paragraph_format.space_before = Pt(0)
    p_lbl.paragraph_format.space_after  = Pt(6)
    r_lbl = p_lbl.add_run(label)
    r_lbl.font.size = Pt(9)
    r_lbl.font.color.rgb = MUTED
    r_lbl.font.name = 'Calibri'


# ═══════════════════════════════════════════════════════════════════════════════
#  1. CONTEXT
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '1.  CONTEXT')
sub(doc,
    'The SAP Social Sabbatical team met with Ziyo Forum\'s external development partner — the outsourced '
    'software team currently responsible for building and maintaining the ZEO app. This interview was '
    'conducted to understand the technical landscape, development workflow, current constraints, and the '
    'team\'s own perspective on what is needed to improve the product.',
    before=8, after=4)
sub(doc,
    'Bug reporting contact on the dev team side is Esmina, who relays issues to Azam. The dev team '
    'communicates requirements directly with Akobir. They have no formal relationship with Aksana '
    '(UX Designer) and have not received structured design handoffs.',
    before=2, after=4)


# ═══════════════════════════════════════════════════════════════════════════════
#  2. TEAM BACKGROUND & HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '2.  TEAM BACKGROUND & PROJECT HISTORY')
sub(doc, 'History', bold=True, before=8, after=2)
bullet(doc, 'A previous development team worked on the app originally.')
bullet(doc, 'The current team inherited the codebase, rebuilt it, and then extended it to support event capture and audience engagement features.')
bullet(doc, 'The team has released more than 10 versions of the app (v1.01 through v1.1), with 6–7 additional minor regression versions.')
bullet(doc, 'Releases happen on a monthly cadence — though the most recent month had no release.')

sub(doc, 'UX Designer Relationship', bold=True, before=8, after=2)
bullet(doc, 'The dev team does not work with Aksana (UX Designer) directly.')
bullet(doc, 'All design direction flows through Akobir. When mockups are needed, the dev team uses Figma.')
bullet(doc, 'The team flagged that they need proper design (Figma files) before they can build new features effectively.')


# ═══════════════════════════════════════════════════════════════════════════════
#  3. TECH STACK & ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '3.  TECH STACK & ARCHITECTURE')

two_col(doc,
    [
        'iOS:  Flutter framework',
        'Android:  Node.js (backend / app layer)',
        'Mockup tool:  Figma',
        'No documented architecture overview',
        'No shared technical specification documents (yet)',
    ],
    [
        'Feature TAT:  ~2 weeks (depends on complexity)',
        'App Store release (iOS):  ~4 days review',
        'Play Store release (Android):  ~4 days review',
        'Bug fix TAT:  ~4 days',
        'Azam to send written technical document (pending)',
    ],
    header_left='Stack & Tools',
    header_right='Turnaround Times (TAT)'
)
doc.add_paragraph()


# ═══════════════════════════════════════════════════════════════════════════════
#  4. REQUIREMENTS & WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '4.  REQUIREMENTS & WORKFLOW')
sub(doc, 'How requirements currently flow', bold=True, before=8, after=2)
bullet(doc, 'No formal requirements process exists. The dev team has no idea what a structured process looks like in this engagement.')
bullet(doc, 'Akobir verbally discusses items with the dev team — no written brief, no ticket system, no sprint planning.')
bullet(doc, 'Azam is supposed to send a written document for new features, but this has not been consistently done.')
bullet(doc, 'There is no backlog, no prioritisation framework, and no story points.')
bullet(doc, 'Bug reporting: Esmina is the point of contact on the dev team side. Reports come in → Esmina relays to Azam → Azam relays to the dev team.')
bullet(doc, 'The dev team only acts on improvements when instruction comes from Akobir. They do not proactively suggest or prioritise.')

sub(doc, 'Deployment process', bold=True, before=8, after=2)
bullet(doc, 'New versions are pushed monthly when there is a release. Last month had no release.')
bullet(doc, 'iOS and Android store review each takes approximately 4 days after submission.')
bullet(doc, '10+ app versions released to date; 6–7 minor/regression releases within those versions.')
bullet(doc, 'No documented deployment checklist or QA sign-off process was mentioned.')


# ═══════════════════════════════════════════════════════════════════════════════
#  5. FEEDBACK & STORE MONITORING
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '5.  USER FEEDBACK & APP STORE MONITORING')
sub(doc, 'Current state', bold=True, before=8, after=2)
bullet(doc, 'The dev team does not actively monitor App Store or Google Play reviews.')
bullet(doc, 'No negative ratings have been reported — but this is not the result of active monitoring.')
bullet(doc, 'There is no process for surfacing user feedback from the stores to the product or dev team.')
bullet(doc, 'Improvements are only made when Akobir specifically requests them, not in response to user data.')

callout(doc,
    'The dev team is flying blind on user sentiment. No active monitoring, no feedback loop, '
    'no mechanism to surface what users dislike before it compounds.',
    bg='FFF8E1', bold_prefix='Note:  ')


# ═══════════════════════════════════════════════════════════════════════════════
#  6. WHAT THE DEV TEAM WANTS
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '6.  WHAT THE DEV TEAM WANTS (THEIR OWN ASKS)')
sub(doc,
    'The dev team expressed several unprompted requests for process and product improvements:',
    before=8, after=4)

bullet(doc, 'Monthly structured product review meeting  — they explicitly asked for a regular cadence with the Ziyo Forum side. "Once a month is good."', bold_prefix='Monthly sync:  ')
bullet(doc, 'Story points and task tracking  — they want to move to a structured sprint model with story-point estimation. Currently no sprint structure exists.', bold_prefix='Sprint model:  ')
bullet(doc, 'Story / interactive videos  — they proposed a short-video content feature (1–2 minutes, similar to Instagram Reels) for educational or opportunity content within the app.', bold_prefix='Video content feature:  ')
bullet(doc, 'Proper design files before build  — they highlighted that they need Figma mockups or clear design handoffs before starting development. They should not be designing as they build.', bold_prefix='Design-first process:  ')


# ═══════════════════════════════════════════════════════════════════════════════
#  7. CRITICAL FINDINGS
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '7.  CRITICAL FINDINGS')
sub(doc,
    '🔴 = Critical risk  ·  🟡 = Important gap  ·  🟢 = Opportunity or positive signal',
    colour=MUTED, size=9.5, before=6, after=6)

findings_table(doc, [
    (1, '🔴', 'No formal requirements process — verbal only',
     'Any feature built without a written spec is unverifiable. Scope creep, misalignment, and rework are inevitable. The SLA and process playbook (Week 3 deliverable) must include a written spec requirement before any build begins.'),
    (2, '🔴', 'Dev team has never worked directly with the UX designer',
     'Aksana and the dev team have never collaborated. All design direction flows through Akobir informally. This is a structural gap: design and build are disconnected. Fixing this is a prerequisite for any meaningful product improvement.'),
    (3, '🔴', 'No QA or testing process mentioned',
     'Monthly releases happen with no documented QA checklist or sign-off step. The 6–7 regression versions suggest bugs are escaping to production. The operating model must include a QA gate before any release.'),
    (4, '🟡', 'No IP / codebase ownership clarity',
     'Confirmed from the IT interview: the dev team holds the source code and there is no written agreement on IP ownership. This must be resolved in writing this week (Quick Win, already assigned).'),
    (5, '🟡', 'No app store feedback monitoring',
     'The dev team does not watch ratings or reviews. User sentiment issues will not surface until they become significant. A simple weekly review of store feedback should be part of the operating model.'),
    (6, '🟡', 'No sprint structure or task tracking',
     'Work is handed over verbally with no prioritisation, no story points, no sprint cadence. The dev team themselves asked for this. The operating model deliverable must include a Trello-based sprint process starting Week 4.'),
    (7, '🟢', 'Dev team is willing to improve',
     'The team proactively asked for monthly meetings, a sprint model, and better design handoffs. This is a strong signal — they are not resistant to structure, they have simply never been given it. This makes the operating model easier to implement.'),
    (8, '🟢', 'Figma is already in use',
     'The dev team already uses Figma for mockups. Combined with Aksana\'s Figma skills, there is a clear path to a proper design-to-dev handoff workflow — it just needs to be formalised and connected.'),
])
doc.add_paragraph()


# ═══════════════════════════════════════════════════════════════════════════════
#  8. SAP TEAM PRELIMINARY FINDINGS
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '8.  SAP TEAM PRELIMINARY FINDINGS')
sub(doc,
    'The dev team interview confirms and deepens the picture from the IT and UX interviews. '
    'The core problem is not capability — it is process. The team can build, they use modern tools, '
    'they release regularly, and they want structure. What is missing is the connective tissue: '
    'written specs, design handoffs, a QA gate, a sprint cadence, and a direct channel to the designer.',
    before=8, after=4)
sub(doc,
    'The tech stack split (Flutter for iOS, Node.js for Android) is worth noting — this is an unusual '
    'combination and may introduce maintenance complexity as the codebase grows. It was not flagged as '
    'a problem by the dev team, but it should be explored in the operating model conversations.',
    before=2, after=4)
callout(doc,
    'The dev team\'s request for a structured sprint, design files, and a monthly sync is '
    'effectively a request for exactly what the Week 3 Operating Model deliverable will provide. '
    'This is a clear mandate — the team is ready for it.',
    bg='E8F5E9', bold_prefix='Key signal:  ')


# ═══════════════════════════════════════════════════════════════════════════════
#  9. ACTION REGISTER
# ═══════════════════════════════════════════════════════════════════════════════
section_title(doc, '9.  ACTION REGISTER')
sub(doc, '', before=4, after=2)
actions_table(doc, [
    (1,  'Azam to send written technical document to SAP team (architecture, stack details, current feature list)',
         'Azam',                'This week — OVERDUE'),
    (2,  'Confirm IP / source code ownership with tech partner in writing (already assigned as Quick Win)',
         'Akobir + Azam',       'This week — URGENT'),
    (3,  'Aksana and dev team to be introduced and aligned on Figma-based design handoff process',
         'Akobir + Aksana',     'Week 2'),
    (4,  'Establish bug-reporting channel: Trello card template or Telegram bot → Esmina → Azam → dev team',
         'Akobir + Azam',       'Week 2'),
    (5,  'Set up first monthly product review meeting (dev team + Akobir + Product Owner)',
         'Akobir',              'Week 2 — recurring'),
    (6,  'Define QA checklist and sign-off requirement before any release (input to Operating Model)',
         'SAP Team + Azam',     'Week 3'),
    (7,  'Include dev team in Operating Model sprint design — agree story point process and Trello workflow',
         'SAP Team + Akobir',   'Week 3'),
    (8,  'Add App Store and Google Play review monitoring to weekly rhythm (assign to Akobir or media team)',
         'Akobir',              'Week 3'),
    (9,  'Assess Flutter / Node.js stack split — document maintenance implications for roadmap',
         'SAP Team + Azam',     'Week 3'),
    (10, 'Evaluate short-video (Reels-style) feature request for inclusion in Product & UX backlog',
         'SAP Team + Aksana',   'Week 2–3'),
])

doc.add_paragraph()
sub(doc,
    'Ziyo Forum × SAP Social Sabbatical  ·  Tashkent, Uzbekistan  ·  October 2026        '
    'SAP Team  ·  Interview Summary  ·  External Development Team  ·  v1.0',
    colour=MUTED, size=8.5, before=10, after=4)

doc.save(DST)
print(f'Saved: {DST}')
