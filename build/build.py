import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                PageBreak, Table, TableStyle, Flowable, KeepTogether, NextPageTemplate)

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "fonts")
for n in ["Roboto-Regular", "Roboto-Medium", "Roboto-Bold", "RobotoSlab-Bold", "RobotoSlab-Regular"]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(F, n + ".ttf")))
pdfmetrics.registerFontFamily("Roboto-Regular", normal="Roboto-Regular", bold="Roboto-Bold",
                              italic="Roboto-Regular", boldItalic="Roboto-Bold")

GREEN = HexColor("#008142"); YELLOW = HexColor("#FFCF01"); LIME = HexColor("#8DC63F")
INK = HexColor("#1d2a24"); MUTED = HexColor("#55645c"); TINT = HexColor("#eef6f1")
LINE = HexColor("#d3e0d8"); YTINT = HexColor("#fff6cc"); DKGREEN = HexColor("#00693a")

PW, PH = letter
M = 0.75 * inch
W = PW - 2 * M
CHECKED = "Last updated November 16, 2026"
TITLE = "Web Developer Job Search Guide"

SECTIONS = [("start", "Start here"), ("career", "Free career help"), ("training", "Training"),
            ("meetups", "Meetups"), ("employers", "Employers"), ("jobs", "Job leads"),
            ("freelance", "Freelancing"), ("portfolio", "Portfolio"), ("plan", "30-day plan")]

def S(name, **kw):
    base = dict(fontName="Roboto-Regular", fontSize=10, leading=14.6, textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(name, **base)

body = S("body")
small = S("small", fontSize=8.6, leading=12, textColor=MUTED)
intro = S("intro", fontSize=11, leading=16, textColor=MUTED, spaceAfter=10)
h1 = S("h1", fontName="RobotoSlab-Bold", fontSize=25, leading=29, textColor=GREEN)
h2 = S("h2", fontName="RobotoSlab-Bold", fontSize=14, leading=18, textColor=GREEN, spaceBefore=14, spaceAfter=7, keepWithNext=1)
ctitle = S("ctitle", fontName="Roboto-Bold", fontSize=11.2, leading=14.5, spaceAfter=2)
tagst = S("tag", fontName="Roboto-Bold", fontSize=7.4, leading=10.5, textColor=GREEN, spaceAfter=3)
cbody = S("cbody", spaceBefore=3)
bullet = S("bullet", leftIndent=11, bulletIndent=1, spaceBefore=2)
links = S("links", fontName="Roboto-Medium", fontSize=9.6, leading=14, spaceBefore=5)
th = S("th", fontName="Roboto-Bold", fontSize=8.4, leading=11, textColor=white)
td = S("td", fontSize=9.4, leading=13)
tdb = S("tdb", fontName="Roboto-Bold", fontSize=9.4, leading=13)
datest = S("date", fontName="Roboto-Bold", fontSize=10, leading=13, textColor=INK)
datesub = S("datesub", fontName="Roboto-Medium", fontSize=8.4, leading=11.5, textColor=INK)
week = S("week", fontName="Roboto-Bold", fontSize=8.6, leading=12, textColor=GREEN, spaceBefore=8, spaceAfter=4)

def A(url, text):
    return '<a href="%s" color="#008142"><u>%s</u></a>' % (url.replace("&", "&amp;"), text)

def linkline(*pairs):
    return Paragraph(' &nbsp;<font color="#9fb3a8">|</font>&nbsp; '.join(A(u, t) for u, t in pairs), links)

def tags(*t):
    return Paragraph(" &nbsp;•&nbsp; ".join(x.upper() for x in t), tagst)

class Rule(Flowable):
    def __init__(self, color=YELLOW, thick=2.2, width=W):
        super().__init__(); self.color = color; self.thick = thick; self.width = width; self.height = thick + 6
    def draw(self):
        self.canv.setStrokeColor(self.color); self.canv.setLineWidth(self.thick)
        self.canv.line(0, 3, self.width, 3)

class Mark(Flowable):
    """Records which section the page belongs to, for the tab bar."""
    def __init__(self, key):
        super().__init__(); self.key = key; self.width = 0; self.height = 0
    def draw(self):
        self.canv._section = self.key

class Check(Flowable):
    n = 0
    def __init__(self):
        super().__init__(); self.width = 13; self.height = 13
        Check.n += 1; self.name = "check%d" % Check.n
    def draw(self):
        self.canv.acroForm.checkbox(name=self.name, x=0, y=0, size=12, relative=True, buttonStyle="check",
                                    borderColor=GREEN, fillColor=white, textColor=GREEN, borderWidth=1,
                                    forceBorder=True, tooltip="Done")

def section(key, title, lead):
    return [PageBreak(), Mark(key), Paragraph('<a name="%s"/>%s' % (key, title), h1), Rule(),
            Spacer(1, 4), Paragraph(lead, intro)]

def card(title, tg=None, *content, stripe=GREEN):
    inner = []
    if tg: inner.append(tags(*tg))
    inner.append(Paragraph(title, ctitle))
    for c in content:
        inner.append(Paragraph(c, cbody) if isinstance(c, str) else c)
    t = Table([[inner]], colWidths=[W])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, LINE), ("LINEBEFORE", (0, 0), (0, -1), 3, stripe),
        ("LEFTPADDING", (0, 0), (-1, -1), 13), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), white)]))
    return [t, Spacer(1, 6)]

def B(text):
    return Paragraph(text, bullet, bulletText="•")

def event(day, sub, title, text, link):
    left = [Paragraph(day, datest), Paragraph(sub, datesub)]
    right = [Paragraph(title, ctitle), Paragraph(text, cbody), linkline(link)]
    t = Table([[left, right]], colWidths=[1.25 * inch, W - 1.25 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), YELLOW), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 11),
        ("RIGHTPADDING", (0, 0), (-1, -1), 11), ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10)]))
    return [t, Spacer(1, 7)]

def grid(header, rows, widths):
    data = [[Paragraph(h.upper(), th) for h in header]]
    for r in rows:
        data.append([Paragraph(r[0], tdb)] + [Paragraph(c, td) for c in r[1:]])
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), GREEN), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
          ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
          ("BOX", (0, 0), (-1, -1), 0.6, LINE), ("LINEBELOW", (0, 1), (-1, -2), 0.5, LINE)]
    for i in range(1, len(data)):
        if i % 2 == 0: st.append(("BACKGROUND", (0, i), (-1, i), TINT))
    t.setStyle(TableStyle(st))
    return [t, Spacer(1, 8)]

def note(text):
    t = Table([[Paragraph(text, body)]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), YTINT), ("LINEBEFORE", (0, 0), (0, -1), 3, YELLOW),
                           ("LEFTPADDING", (0, 0), (-1, -1), 13), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return [t, Spacer(1, 9)]

def paths(items):
    cw = (W - 8) / 2
    cells = []
    for title, text, key, label in items:
        cells.append([Paragraph(title, ctitle), Paragraph(text, S("p", fontSize=9.5, leading=13.5, textColor=MUTED)),
                      Paragraph('<a href="#%s" color="#008142"><u>%s</u></a>' % (key, label), links)])
    rows = [[cells[i], "", cells[i + 1]] for i in range(0, len(cells), 2)]
    out = []
    for r in rows:
        t = Table([r], colWidths=[cw, 8, cw])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), TINT), ("BACKGROUND", (2, 0), (2, 0), TINT),
                               ("LINEABOVE", (0, 0), (0, 0), 3, GREEN), ("LINEABOVE", (2, 0), (2, 0), 3, GREEN),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 12),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 7),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                               ("LEFTPADDING", (1, 0), (1, 0), 0), ("RIGHTPADDING", (1, 0), (1, 0), 0)]))
        out += [t, Spacer(1, 6)]
    return out

def checks(items):
    data = [[Check(), Paragraph(i, body)] for i in items]
    t = Table(data, colWidths=[24, W - 24])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3.2),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2)]))
    return [t]

# ---------------------------------------------------------------- content
CS = "https://careersourcetampabay.com"
TSN = "https://www.meetup.com/techsuccessnetwork/"
SCORE = "https://www.score.org/fl/pinellas-county/"
story = [NextPageTemplate("main"), Spacer(1, 1)]

# START
story += section("start", "Start with the path that fits you",
    "Junior web developer openings are scarce right now, and many ask for a degree or years of experience. "
    "The graduates who get hired usually do three things at once: get free help with their résumé, show up where "
    "local developers gather, and apply to nearby roles as well as developer roles.")
story += paths([
    ("I need help with my résumé and interviews", "CareerSource offers free workshops and one-on-one help in Clearwater, St. Petersburg and Tarpon Springs.", "career", "Go to Free career help"),
    ("I have been searching for months", "A paid training program with a built-in internship, or an apprenticeship, can get you past the “experience required” wall.", "training", "Go to Training"),
    ("I do not know anyone in tech", "Local meetups are free, and most welcome beginners. One room of developers beats a hundred cold applications.", "meetups", "Go to Meetups"),
    ("I just want to see openings", "Saved searches for junior roles, plus the job titles that hire web skills under another name.", "jobs", "Go to Job leads"),
    ("I want to apply straight to local employers", "Direct links to the job pages of local cities, counties, schools and companies.", "employers", "Go to Employers"),
    ("I freelance or want my own business", "Free mentors and workshops at the Greenhouse, SCORE and the Small Business Development Center.", "freelance", "Go to Freelancing"),
])
story.append(Paragraph("Three things to do this week", h2))
story += card("1. Register with Employ Florida", None, "CareerSource workshops and job referrals require it. It takes about 20 minutes.", linkline(("https://www.employflorida.com/vosnet/default.aspx", "employflorida.com")))
story += card("2. Join Tampa Devs and pick one event", None, 'The largest local developer community, and free. Browse the events calendar, RSVP to one event from the <a href="#meetups" color="#008142"><u>Meetups section</u></a>, and ask an organizer there for an invite to the members\' Slack. Online sessions count if getting to Tampa is hard.', linkline(("https://tampa.dev/", "tampa.dev")))
story += card("3. Get feedback on your résumé or LinkedIn", None, "Send the link or file to Marianne Shaffer, Web Development instructor, at <b>SHAFFERMA@pcsb.org</b>. Say what kind of role you are applying for.")

# CAREER
story += section("career", "Free career help", "You should never pay for résumé help or job placement. These services cost nothing.")
story.append(Paragraph("CareerSource (Pinellas and Hillsborough)", h2))
story.append(Paragraph("The county workforce boards merged in 2024. You may see the names CareerSource Pinellas, CareerSource Tampa Bay and CareerSource Hillsborough Pinellas. They are the same organization.", S("x", textColor=MUTED, spaceAfter=8)))
story += grid(["Career center", "Address", "Phone"], [
    ["Gulf to Bay (Clearwater)", "2312 Gulf to Bay Blvd, Clearwater, FL 33765", "(727) 524-4344"],
    ["St. Petersburg", "3420 8th Ave S, St. Petersburg, FL 33711", "(727) 524-4344"],
    ["Tarpon Springs", "682 E Klosterman Rd, Tarpon Springs, FL 34689 (closed 12 to 1)", "(727) 524-4344"],
    ["Tampa", "9215 N Florida Ave, Tampa, FL 33612", "(813) 930-7400"]], [1.75 * inch, W - 3.05 * inch, 1.3 * inch])
story.append(Paragraph("Open Monday to Friday, 8 a.m. to 5 p.m. Closed November 26 and 27 for Thanksgiving. " + A(CS + "/career-centers/", "All career centers"), small))
story.append(Spacer(1, 10))
story += card("Workshops on résumés, interviews and job search", ["Free", "In person and online"], "Sessions run most weeks at the centers. Register through the calendar.",
    linkline((CS + "/career-training-resources/employability-skills-training/", "Free workshops"), (CS + "/events/month/?tribe_eventcategory%5B0%5D=344", "Workshop calendar")))
story += card("Hiring events and job fairs", ["Free"], "Employers come to the centers to interview on the spot. Coffee and Careers events are planned for December and January.",
    linkline((CS + "/events/month/?tribe_eventcategory%5B0%5D=136", "Hiring events calendar"), (CS + "/job-boards/hot-jobs/", "Hot Jobs")))
story += card("Professional Networking Group", ["Free"], "A regular group for job seekers to trade leads and practice introducing themselves.",
    linkline((CS + "/job-seekers/professional-networking-group/", "Professional Networking Group")))
story += card("Youth Connection", ["Free", "Ages 16 to 24"], "Job training, paid work experience and apprenticeships for young adults. If you are in this age range, ask about it first, because it comes with more one-on-one support.",
    linkline((CS + "/youth-services/", "Youth Connection"), (CS + "/youth-services/paid-work-experience/", "Paid Work Experience")))
story += card("Training funds", ["Ask a counselor"], "CareerSource can sometimes pay for approved training, including IT certifications. Ask what you qualify for before paying for any course yourself.",
    linkline((CS + "/career-training-resources/", "Career training and resources"), (CS + "/explore-programs/", "All programs")))

# TRAINING
story += section("training", "Training and apprenticeships", "These programs add experience and employer connections to the skills you already have. Each has eligibility rules, so check them before you apply.")
story += card("Year Up United, Tampa Bay", ["Tuition-free", "Stipend", "Ages 18 to 29"],
    "About a year long: classroom training first, then an internship at a large employer. Tampa Bay currently offers two tracks, <b>Banking</b> and <b>Customer Success</b>. "
    "Neither is a developer track, but both are a paid way into large companies that also have tech teams. "
    "Students receive an educational stipend, and Tampa listings have put the internship-phase stipend at $525 a week.",
    B("<b>You qualify if you are</b> 18 to 29, have a high school diploma or GED, do not have a bachelor's degree, have low to moderate income, can work in the U.S., and are available Monday to Friday."),
    B("<b>Next start:</b> April 2027. Training is in person 3 to 4 days a week at 2101 E Palm Ave, Tampa."),
    B("<b>Questions:</b> 855-932-7871 or admissions@yearupunited.org"),
    linkline(("https://www.yearup.org/locations/tampa-bay-fl", "Year Up United Tampa Bay"), ("https://www.yearup.org/get-started", "Apply"), ("https://www.yearup.org/students/how-it-works", "Eligibility"), ("https://www.yearup.org/students/student-faqs", "Student FAQs")))
story += card("Tampa Bay Tech Apprentice Network", ["Paid", "No degree required"],
    "Local tech employers hiring apprentices: on-the-job training, classes, certifications and a wage. The network is aimed at adults entering or changing into tech. "
    "Openings are posted on its apprenticeship job board. The board can be empty between hiring rounds, so sign up there for email alerts.",
    linkline(("https://tampabay.tech/apprenticeship-board/", "Apprenticeship job board"), ("https://tampabay.tech/foundation/", "About the network")))
story += card("Computer Coach Training Center", ["Paid courses", "Tampa and online", "Free events"],
    "IT and business bootcamps with certification prep, at 5005 N Hesperides St, Tampa, and live online. Phone (813) 947-0552. "
    "The courses cost money, but the school appears on the state's approved training provider list, so ask CareerSource whether funding can cover it. "
    'Its free career meetups are open to everyone and listed in the <a href="#meetups" color="#008142"><u>Meetups section</u></a>.',
    linkline(("https://www.computercoach.com", "computercoach.com")))

# MEETUPS
story += section("meetups", "Meetups and community", "Go to learn, and tell people you are looking. Bring a link to your portfolio on your phone. All of these are free unless noted.")
story.append(Paragraph("Coming up", h2))
story += note("<b>Confirm before you go.</b> These dates were on the organizers' pages between November 13 and 16, 2026. Times and rooms change.")
story += event("TUE, NOV 17", "10 AM • Online", "Career Clarity", "A Tech Success Network session on weighing your career options.", (TSN, "Tech Success Network"))
story += event("TUE, NOV 17", "6 PM • St. Petersburg", "Crafting a Compelling Elevator Pitch", "A free SCORE workshop on speaking with confidence and telling your story. Useful practice for interviews and meetups. In person at the Greenhouse, 440 2nd Ave N.", (SCORE, "SCORE Pinellas County"))
story += event("THU, NOV 19", "Evening • Tampa", "TECHAPALOOZA", "A large gathering of Tampa Bay tech groups at SOFWERX. Calendars list the start as 4 PM or 5 PM, so check the event page.", ("https://tampa.dev/events/6155e1d7-f6c5-4251-b661-c358f93d0af1", "Event page"))
story += event("WED, DEC 2", "5 PM • Tampa", "End of Year Tech Meetup Extravaganza", "Hosted by Computer Coach at 802 E Whiting St, Tampa. Many local tech groups in one room. Attendees are asked to bring a gift or donation for Joshua's House.", (TSN, "Tech Success Network"))
story += event("MON, DEC 7", "6 PM • St. Petersburg or online", "Commanding the Room", "A free SCORE workshop on explaining what you do so people remember you, and sounding confident without sounding rehearsed. At the Greenhouse, 440 2nd Ave N, or online.", (SCORE, "SCORE Pinellas County"))
story += event("TUE, DEC 8", "10 AM • Online", "Networking Intentionally", "How to network on LinkedIn with a purpose.", (TSN, "Tech Success Network"))
story += event("THU, DEC 10", "See event page", "Building 2D Web Games with Flutter and Flame", "A Google Developer Group Tampa Bay session with free registration. The time and place are on the group page.", ("https://gdg.community.dev/gdg-tampa-bay/", "GDG Tampa Bay"))
story += card("Every week", ["Recurring"],
    B("<b>Wednesdays, 9 to 10 AM, St. Petersburg:</b> 1 Million Cups. Two local founders present and the room gives feedback. Free, with no registration. See " + '<a href="#freelance" color="#008142"><u>Freelancing</u></a>' + "."),
    B("<b>Wednesdays, 6 PM, St. Petersburg:</b> St. Pete Dev Nights. Confirm the date on the group page below."),
    B("<b>Mondays:</b> check the Global Nerdy list below for everything happening that week."))
story.append(Paragraph("Groups to join", h2))
story += card("Tampa Devs", ["Tampa Bay", "Job board"],
    "The largest local developer community. Monthly meetups with talks and food, workshops, and a calendar that collects events from every local tech group. Its job board works in reverse: you post a profile and employers find you. Members also have a Slack workspace, so ask for an invite at an event.",
    linkline(("https://tampa.dev/", "Events calendar"), ("https://talent.tampa.dev", "Job board"), ("https://tampa.dev/groups", "All local groups")))
story += card("Pinellas Tech Network", ["Palm Harbor"],
    "The closest tech meetup to Clearwater. It meets at Geographic Solutions' main campus in Palm Harbor, with food, networking and a speaker. Past sessions have covered web trends and how to break into tech, with résumé reviewers on site. Join the group to be notified when the next event is posted.",
    linkline(("https://www.meetup.com/pinellas-tech-network/", "Pinellas Tech Network")))
story += card("St. Pete Dev Nights", ["St. Petersburg", "Wednesdays"],
    "A Wednesday evening gathering for developers of all levels at Steep Station, a tea and kava cafe at 2235 1st Ave S, starting at 6 PM. Bring a laptop and work on something. Confirm the next date on the group page.",
    linkline(("https://www.meetup.com/st-pete-dev-nights/", "St. Pete Dev Nights")))
story += card("Tech Success Network", ["Online and Tampa", "Career focused"],
    "About 5,000 members, run by the CEO of Computer Coach. Regular online sessions on job search, LinkedIn and changing careers into tech.", linkline((TSN, "Tech Success Network")))
story += card("Google Developer Group (GDG) Tampa Bay", ["Tampa and online", "Free events"],
    "Workshops and talks on web, mobile and AI, many of them online and free. It also runs the yearly DevFest conference at USF.",
    linkline(("https://gdg.community.dev/gdg-tampa-bay/", "GDG Tampa Bay")))
story += card("Global Nerdy weekly events list", ["Updated weekly"], "Every tech, entrepreneur and hobby event in Tampa Bay for the coming week, in one post. Check it each Monday.",
    linkline(("https://www.globalnerdy.com/category/tampa-bay/", "globalnerdy.com")))

# EMPLOYERS
def L(url, text): return A(url, text)
story += section("employers", "Local employers", "Each link goes straight to that employer's own job page, so what you see is always current. Openings change every week.")
story += note("<b>How to use this page.</b> Open a job page and search for “web”, “digital”, “communications”, “marketing”, “IT” and “support”. Most of these sites let you create a job alert, so set one and let the openings come to you. Check back weekly.")
c1 = 1.95 * inch; c3 = 1.6 * inch; c2 = W - c1 - c3
story.append(Paragraph("Cities and counties", h2))
story.append(Paragraph("Public employers hire for websites, communications, IT support and office technology. They list pay up front, offer strong benefits, and many roles ask for experience or a certificate in place of a degree.", S("e1", textColor=MUTED, spaceAfter=8)))
story += grid(["Employer", "Good to know", "Job page"], [
    ["Pinellas County", "One site covers county departments and also the Clerk of Court, Property Appraiser, Supervisor of Elections and Business Technology Services.", L("https://pinellas.gov/jobs", "pinellas.gov/jobs")],
    ["City of Clearwater", "Listings open in the city's GovernmentJobs portal. Create an account once and reuse it.", L("https://www.myclearwater.com/Jobs", "myclearwater.com/Jobs")],
    ["City of St. Petersburg", "Large city with its own marketing, technology and library systems teams.", L("https://www.stpete.org/jobs", "stpete.org/jobs")],
    ["City of Largo", "Openings are posted in Workday.", L("https://www.largo.com/jobs", "largo.com/jobs")],
    ["City of Pinellas Park", "Smaller city, shorter list, less competition.", L("https://www.pinellaspark.gov/apply", "pinellaspark.gov/apply")],
    ["Pinellas County Sheriff's Office", "More than 1,100 civilian staff, including IT and administrative roles. Expect a background check that can take up to six weeks.", L("https://pinellassheriff.gov/current-openings", "Current openings")],
    ["Pinellas County Tax Collector", "Mostly customer service roles in branch offices. A steady way into county government.", L("https://www.pinellastaxcollector.gov/careers", "Careers")],
    ["PSTA (county bus system)", "Office, technology and internship postings.", L("https://psta.net/careers/join-our-team/", "psta.net careers")],
    ["City of Tampa", "Worth it if you can commute across the bay.", L("https://www.tampa.gov/guide/careers", "tampa.gov careers")],
    ["Hillsborough County", "County departments in Tampa and Brandon.", L("https://hcfl.gov/about-hillsborough/jobs-and-benefits", "hcfl.gov jobs")]], [c1, c2, c3])
story.append(Paragraph("Schools and colleges", h2))
story += grid(["Employer", "Good to know", "Job page"], [
    ["Pinellas County Schools", "Look under support and technology positions for web, help desk and school technology roles.", L("https://www.pcsb.org/jobs", "pcsb.org/jobs")],
    ["St. Petersburg College", "Staff roles in web, marketing, online learning and IT support across several campuses.", L("https://hr.spcollege.edu/work-at-spc/prospective-employees", "Work at SPC")],
    ["University of South Florida", "Hundreds of staff jobs in Tampa and St. Petersburg. Search “web” and “digital”.", L("https://www.usf.edu/work-at-usf/careers/", "USF careers")],
    ["Hillsborough County Public Schools", "One of the largest districts in the country, with its own technology department.", L("https://www.hillsboroughschools.org/Domain/293", "HCPS jobs")]], [c1, c2, c3])
story.append(Paragraph("Tech, web and marketing companies", h2))
story.append(Paragraph("Local companies that hire for web, content, SEO, support and testing. The roles named here were posted in November 2026 or earlier and will change, so use them as a guide to what each company hires for.", S("e2", textColor=MUTED, spaceAfter=8)))
story += grid(["Company", "Good to know", "Job page"], [
    ["KnowBe4<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Clearwater</font>", "Security training software, headquartered downtown. Known for entry-level technical support, support intern and sales roles.", L("https://www.knowbe4.com/careers?filter=Clearwater%2C%20Florida", "Clearwater openings")],
    ["PostcardMania<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Clearwater</font>", "Marketing company that has posted web services, SEO and web copywriting roles, some with training on the job. Holds hiring open houses. Requires a drug and nicotine screen.", L("https://www.postcardmania.com/jobs", "postcardmania.com/jobs")],
    ["Geographic Solutions<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Palm Harbor</font>", "Builds the software behind Employ Florida. Runs its own apprenticeships, and hosts the Pinellas Tech Network meetup.", L("https://www.geographicsolutions.com/Careers/Current-Openings", "Openings") + " &nbsp;|&nbsp; " + L("https://www.geographicsolutions.com/Careers/Apprenticeships-GSI", "Apprenticeships")],
    ["WebstaurantStore (Clark Associates)<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Tampa and remote</font>", "Large online store with a Tampa office. Has posted IT support, remote content roles and a summer testing internship. Scan the list for “Tampa” and “Remote”.", L("https://www.webstaurantstore.com/careers/", "Careers")],
    ["The HOTH<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>St. Petersburg</font>", "SEO and digital marketing company downtown. Posts junior marketing, design and support roles, and accepts open applications.", L("https://www.thehoth.com/careers/", "thehoth.com/careers")],
    ["Focus School Software<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>St. Petersburg</font>", "Makes the student information system many Florida schools use. Has posted support technician, software tester and trainer roles.", L("https://focusschoolsoftware.com/careers", "Careers")],
    ["TD SYNNEX<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Clearwater</font>", "One of the largest tech distributors in the world. Filter by Clearwater for support, operations and e-commerce roles.", L("https://synnex.wd5.myworkdayjobs.com/tdsynnexcareers", "Job search")],
    ["Jabil<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>St. Petersburg</font>", "Global manufacturer with its headquarters here. Search by St. Petersburg for IT and digital roles.", L("https://jobs.jabil.com/en", "jobs.jabil.com")],
    ["Raymond James<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>St. Petersburg</font>", "Big technology department. Most developer roles are senior, so look at the early career and support paths.", L("https://www.raymondjames.com/careers", "Careers")],
    ["BayCare<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Clearwater</font>", "Hospital system with a large IT and digital team. Help desk and application support roles are the usual way in.", L("https://baycare.org/careers", "baycare.org/careers")],
    ["Bayshore Solutions<br/><font name='Roboto-Regular' size='8.4' color='#55645c'>Tampa</font>", "Web design and digital marketing agency. The list is often short, so check back.", L("https://www.bayshoresolutions.com/careers", "Careers")]], [c1, c2, c3])
story += note("<b>Applying direct works best with a person attached.</b> After you apply, look for someone from that employer at a meetup or on LinkedIn and send a short, polite note with your portfolio link.")

# JOBS
story += section("jobs", "Job leads", "These are live searches, so the results change daily. Save each one and turn on email alerts.")
story.append(Paragraph("Junior developer searches", h2))
ZR = "https://www.ziprecruiter.com/Jobs/"
story += card("ZipRecruiter", None, "Recent results have included Tampa junior developer roles from about $23 an hour to $60,000 to $70,000 a year, and a remote entry-level role at $40,000.",
    linkline((ZR + "Junior-Web-Developer/-in-Clearwater,FL", "Junior web developer, Clearwater"), (ZR + "Entry-Level-Web-Developer/-in-Clearwater,FL", "Entry-level web developer, Clearwater")))
story += card("Glassdoor, Built In, Indeed and LinkedIn", None, "Built In lists tech companies and startups only.",
    linkline(("https://www.glassdoor.com/Job/clearwater-junior-web-developer-jobs-SRCH_IL.0,10_IC1154388_KO11,31.htm", "Glassdoor, Clearwater"), ("https://www.glassdoor.com/Job/tampa-junior-web-developer-jobs-SRCH_IL.0,5_IC1154429_KO6,26.htm", "Glassdoor, Tampa"), ("https://builtin.com/jobs/tampa-bay/entry-level", "Built In entry level")),
    linkline(("https://www.indeed.com/jobs?q=junior+web+developer&l=Clearwater%2C+FL", "Indeed, near Clearwater"), ("https://www.linkedin.com/jobs/search/?keywords=junior%20web%20developer&location=Tampa%20Bay%20Area", "LinkedIn, Tampa Bay Area")))
story += card("Local boards", None, "Smaller boards with less competition.",
    linkline(("https://talent.tampa.dev", "Tampa Devs job board"), (CS + "/job-boards/", "CareerSource job boards"), ("https://www.employflorida.com/vosnet/default.aspx", "Employ Florida")))
story.append(Paragraph("Search these titles too", h2))
story.append(Paragraph("Plenty of jobs use HTML, CSS, JavaScript and WordPress every day without “developer” in the title. They are easier to land, and they count as experience for your next application.", S("y", textColor=MUTED, spaceAfter=8)))
story += grid(["Title to search", "What you would do"], [
    ["Web content specialist, web coordinator", "Update pages, fix layouts and post content in a CMS"],
    ["WordPress or Shopify support specialist", "Troubleshoot client sites, themes and plugins"],
    ["Email developer, marketing operations", "Build HTML emails and landing pages"],
    ["Digital marketing coordinator", "Run the website, SEO and analytics for a small business"],
    ["QA tester, quality assurance analyst", "Test websites and apps and write up bugs"],
    ["Technical support specialist, help desk", "Solve customer and staff tech problems. A common first step into IT."],
    ["Implementation or onboarding specialist", "Set up software for new customers at a tech company"]    ], [2.75 * inch, W - 2.75 * inch])
story.append(Paragraph("Where web skills get hired locally", h2))
story += card("Marketing and web agencies", None, "Small agencies in St. Petersburg, Clearwater and Tampa hire juniors and freelancers for WordPress work. Many never post the job. Meet them at local meetups, or send a short email with your portfolio link.")
story += card("Cities, counties, schools and local companies", None, 'Each one posts openings on its own job page, often before they reach the big job sites. The <a href="#employers" color="#008142"><u>Employers section</u></a> links straight to more than 25 of them.')
story += card("Staffing firms", None, "Robert Half, TEKsystems and Vaco all place web and IT contractors in Tampa Bay. A recruiter there costs you nothing, and contract work is often how the first job happens.")
story += note("<b>Avoid scams. Real employers do not charge you.</b> Walk away from any “job” that asks you to pay for training or equipment, cash a check and send money back, or interview only by text message.")

# FREELANCE
GH = "https://stpetegreenhouse.com"
story += section("freelance", "Freelancing and your own business", "Building sites for clients is real experience, whether it is your whole plan or a way to earn while you job hunt. Every service here is free unless noted.")
story += card("The Greenhouse, St. Petersburg", ["Free", "In person and online"],
    "The city's front door for small business, run by the City of St. Petersburg and the St. Petersburg Area Chamber of Commerce at <b>440 2nd Ave N</b>. Start here if you are not sure where to start.",
    B("<b>One-on-one help:</b> free appointments with business consultants and mentors. Request one online or call (727) 893-7146."),
    B("<b>Workshops:</b> free and low-cost sessions on starting up, marketing, pricing and money, most of them in the evening and many online too."),
    B("<b>1 Million Cups:</b> every Wednesday from 9 to 10 AM. Two founders present and the room gives feedback. Free, with no registration. A good room for meeting small business owners who need websites."),
    linkline((GH + "/start/", "Starting a business"), (GH + "/assistance/", "Request an appointment"), (GH + "/1mc/", "1 Million Cups")))
story += card("SCORE Pinellas County", ["Free", "Mentoring"],
    "Volunteer mentors who have run businesses. Mentoring is free and confidential, and you can keep the same mentor as long as you like. Use the “Request a mentor” button on the chapter page. The chapter office is at 4707 140th Ave N, Clearwater, and its workshops are held with the Greenhouse.",
    linkline((SCORE, "SCORE Pinellas County")))
story.append(Paragraph("SCORE workshops coming up", h2))
story.append(Paragraph("All free, 90 minutes, at the Greenhouse. Register on the SCORE Pinellas County page.", S("f1", textColor=MUTED, spaceAfter=8)))
story += grid(["Date", "Workshop", "How to attend"], [
    ["Tue, Nov 17, 6 PM", "Crafting a Compelling Elevator Pitch and Becoming a Better Storyteller", "In person"],
    ["Thu, Nov 19, 6 PM", "Real Talk About Financing Your Business", "In person or online"],
    ["Mon, Dec 7, 6 PM", "Commanding the Room", "In person or online"],
    ["Tue, Dec 8, 6 PM", "Three AI tools worth having for a small business", "In person or online"]], [1.5 * inch, W - 3.1 * inch, 1.6 * inch])
story += card("Florida Small Business Development Center at Pinellas County", ["Free consulting", "Clearwater and St. Petersburg"],
    "No-cost, confidential consulting and low-cost training, including “How to Start a Business” workshops. Offices at 13805 58th St N, Clearwater (by appointment, 727-453-7200) and at USF St. Petersburg.",
    linkline(("https://pced.org/start-ups", "Start-up help"), ("https://pced.org/consulting", "Request consulting")))
story += card("Set it up properly", None,
    "Florida has no general state business license. The rules are local, so check the city you live in. A mentor from SCORE or the Small Business Development Center will walk you through this for free.",
    B("<b>Register your business name</b> with the state at " + A("https://dos.fl.gov/sunbiz/", "Sunbiz") + " if you form an LLC or work under a name other than your own."),
    B("<b>Get a local business tax receipt</b> if your city requires one. This applies to home-based businesses too. " + A("https://www.myclearwater.com/BTR", "Clearwater") + " &nbsp;|&nbsp; " + A("https://www.stpete.org/businesstax", "St. Petersburg") + " &nbsp;|&nbsp; " + A("https://www.pced.org/permits-licenses-taxes/", "Other Pinellas cities")),
    B("<b>Keep business money separate</b> and set some aside for taxes. Ask your mentor what applies to you."))
story += card("Finding your first clients", None,
    B("Start with people who already know you: family businesses, churches, clubs and local nonprofits."),
    B("Go to 1 Million Cups and Greenhouse workshops. The room is full of new business owners who need a website."),
    B("Tell local web and marketing agencies you take overflow WordPress work."),
    B("Put every project in writing: what you will build, the price, the deadline, and a deposit before you start."),
    B("Add each finished client site to your portfolio. It counts as experience on a job application."))

# PORTFOLIO
story += section("portfolio", "Portfolio and skills", "For a junior developer the portfolio does the work a degree does for other applicants. A hiring manager gives it about a minute.")
story += card("What to show", None,
    B("Three finished projects are better than ten half-done ones."),
    B("Each project needs a live link, a link to the code on GitHub, and two or three sentences on what it does and what you built."),
    B("Include at least one project that solves a real problem for a real person or business."),
    B("List the certifications you earned in your program, with the exact names."))
story += card("Check before you send it", None,
    B("It works on a phone."), B("Every link works and nothing says “coming soon”."),
    B("Images have alt text and you can reach everything with the keyboard."),
    B("Run it through " + A("https://pagespeed.web.dev/", "PageSpeed Insights") + " and fix what it flags."),
    B("Your name, email and LinkedIn are easy to find."))
story += card("Keep building while you search", None, "Gaps worry employers less when your GitHub shows recent work.",
    B(A("https://www.frontendmentor.io/", "Frontend Mentor") + ": build real designs and get feedback."),
    B(A("https://www.freecodecamp.org/", "freeCodeCamp") + ": free courses and certifications in JavaScript and more."),
    B(A("https://www.theodinproject.com/", "The Odin Project") + ": a free full-stack curriculum with projects."),
    B(A("https://developer.mozilla.org/en-US/docs/Learn_web_development", "MDN Learn") + ": the reference professionals use."))
story += card("Get feedback", ["Free", "PTC"], "Marianne Shaffer, your Web Development instructor, is glad to review your résumé, LinkedIn profile or portfolio. Email a link or attachment to <b>SHAFFERMA@pcsb.org</b> and say what kind of role you are applying for. You can also ask for a portfolio review at a Tampa Devs meetup.")
story += card("Real experience without a job", None, "Build or fix a site for a local nonprofit, a family business or a community group. Treat it like client work, with a short write-up of the problem and the result, and it belongs on your résumé as experience.")

# PLAN
story += section("plan", "30-day plan", "Work through one week at a time. You can tick the boxes on screen, or print this page.")
for wk, items in [
    ("WEEK 1: GET SET UP", ["Register at Employ Florida", "Call or visit a CareerSource center and ask about résumé help and training funds", "RSVP to a Tampa Devs event and introduce yourself there", "Email your résumé or LinkedIn link to Marianne Shaffer for feedback"]),
    ("WEEK 2: FIX YOUR MATERIALS", ["Attend one résumé workshop and update your résumé", "Run the portfolio checklist and fix what fails", "Update LinkedIn with your program, certifications and portfolio link", "Post a profile on the Tampa Devs job board"]),
    ("WEEK 3: MEET PEOPLE", ["Attend one in-person or online meetup", "Ask one person there to look at your portfolio", "Check Year Up United and apprenticeship eligibility, and apply if you qualify", "If you freelance, request a free SCORE mentor or a Greenhouse appointment"]),
    ("WEEK 4: APPLY WIDELY", ["Set up job alerts for junior developer roles and at least three nearby titles", "Send 10 applications, each with a short note written for that employer", "Apply directly to two employers from the Employers section", "Email three local agencies or small businesses with your portfolio link", "Start one new project so your GitHub shows recent work"])]:
    story.append(KeepTogether([Paragraph(wk, week)] + checks(items)))
story.append(Spacer(1, 8))
story += note("<b>Found a broken link or something out of date?</b> Email Marianne Shaffer at <b>SHAFFERMA@pcsb.org</b> so it can be fixed for everyone.")
story.append(Rule(LINE, 0.6))
story.append(Paragraph("<b>Pinellas Technical College</b> &nbsp;•&nbsp; Clearwater Campus, 6100 154th Ave N, Clearwater, FL 33760, 727.538.7167 &nbsp;•&nbsp; myptc.edu", small))
story.append(Spacer(1, 4))
story.append(Paragraph("Programs listed here set their own eligibility rules and dates. Confirm details with each organization.", S("fine", fontSize=7.4, leading=10.2, textColor=MUTED)))

# ---------------------------------------------------------------- page furniture
LOGO = os.path.join(HERE, "logo.png")

def cover(c, doc):
    c.saveState()
    lw = 4.6 * inch; lh = lw * 127 / 945
    c.drawImage(LOGO, M, PH - 0.85 * inch - lh, width=lw, height=lh, mask="auto")
    top = PH - 2.35 * inch; bot = 4.55 * inch
    c.setFillColor(GREEN); c.rect(0, bot, PW, top - bot, stroke=0, fill=1)
    c.setFillColor(YELLOW); c.rect(0, top, PW, 9, stroke=0, fill=1)
    c.setFillColor(LIME); c.rect(0, bot - 5, PW, 5, stroke=0, fill=1)
    c.setFillColor(YELLOW); c.setFont("Roboto-Bold", 10.5)
    c.drawString(M, top - 0.62 * inch, "FOR WEB DEVELOPMENT GRADUATES  •  TAMPA BAY")
    c.setFillColor(white); c.setFont("RobotoSlab-Bold", 44)
    c.drawString(M, top - 1.42 * inch, "Web Developer")
    c.drawString(M, top - 2.08 * inch, "Job Search Guide")
    c.setFont("Roboto-Regular", 13.5)
    c.drawString(M, top - 2.62 * inch, "Free career help, paid training, meetups and job leads")
    c.drawString(M, top - 2.88 * inch, "for landing a first role in web or a nearby field.")
    # contents
    y = bot - 0.62 * inch
    c.setFillColor(GREEN); c.setFont("RobotoSlab-Bold", 14); c.drawString(M, y, "Inside this guide")
    c.setStrokeColor(YELLOW); c.setLineWidth(2.2); c.line(M, y - 9, PW - M, y - 9)
    desc = {"start": "Pick your path and three things to do this week", "career": "CareerSource centers, workshops and hiring events",
            "training": "Year Up United, apprenticeships and funded training", "meetups": "Upcoming events and groups to join",
            "jobs": "Saved searches and the titles that hire web skills", "employers": "Direct links to local employers' own job pages",
            "freelance": "Free mentors, workshops and how to set up", "portfolio": "What to show and how to keep building",
            "plan": "A week-by-week checklist"}
    y -= 34
    for i, (k, label) in enumerate(SECTIONS):
        c.setFillColor(YELLOW); c.circle(M + 9, y + 4, 9.5, stroke=0, fill=1)
        c.setFillColor(INK); c.setFont("Roboto-Bold", 10); c.drawCentredString(M + 9, y + 0.6, str(i + 1))
        c.setFillColor(GREEN); c.setFont("Roboto-Bold", 11.5); c.drawString(M + 28, y, label)
        c.setFillColor(MUTED); c.setFont("Roboto-Regular", 10.5); c.drawString(M + 2.05 * inch, y, desc[k])
        c.linkRect("", k, (M, y - 6, PW - M, y + 14), relative=0, thickness=0)
        y -= 21.5
    c.setFillColor(MUTED); c.setFont("Roboto-Regular", 8.6)
    c.setFont("Roboto-Bold", 8.6); c.drawString(M, 0.74 * inch, CHECKED)
    c.setFont("Roboto-Regular", 8.6)
    c.drawString(M, 0.56 * inch, "Every underlined link is clickable. Found a broken link? Email SHAFFERMA@pcsb.org.")
    c.setFillColor(GREEN); c.setFont("RobotoSlab-Bold", 11); c.drawRightString(PW - M, 0.6 * inch, "myptc.edu")
    c.restoreState()

class Doc(BaseDocTemplate):
    def afterPage(self):
        c = self.canv
        if self.page == 1: return
        cur = getattr(c, "_section", "start")
        c.saveState()
        # tab bar
        gap = 4; font = "Roboto-Medium"; size = 7.9
        tw = sum(pdfmetrics.stringWidth(l, font, size) for _, l in SECTIONS)
        pad = min(8.5, (W - tw - gap * (len(SECTIONS) - 1)) / (2 * len(SECTIONS)))
        widths = [pdfmetrics.stringWidth(l, font, size) + 2 * pad for _, l in SECTIONS]
        x = M; y = PH - 0.62 * inch; h = 17
        for (k, label), w in zip(SECTIONS, widths):
            if k == cur:
                c.setFillColor(GREEN); c.roundRect(x, y, w, h, 8.5, stroke=0, fill=1); c.setFillColor(white)
            else:
                c.setFillColor(TINT); c.roundRect(x, y, w, h, 8.5, stroke=0, fill=1); c.setFillColor(DKGREEN)
            c.setFont(font, size); c.drawCentredString(x + w / 2, y + 5.4, label)
            c.linkRect("", k, (x, y, x + w, y + h), relative=0, thickness=0)
            x += w + gap
        c.setStrokeColor(LINE); c.setLineWidth(0.6); c.line(M, y - 8, PW - M, y - 8)
        # footer
        c.setStrokeColor(YELLOW); c.setLineWidth(1.6); c.line(M, 0.62 * inch, PW - M, 0.62 * inch)
        c.setFillColor(MUTED); c.setFont("Roboto-Regular", 8)
        c.drawString(M, 0.43 * inch, "Pinellas Technical College  |  " + TITLE + "  |  " + CHECKED)
        c.drawRightString(PW - M, 0.43 * inch, "Page %d" % self.page)
        c.restoreState()

out = os.path.join(HERE, "PTC-Web-Developer-Job-Search-Guide.pdf")
doc = Doc(out, pagesize=letter, title=TITLE, author="Pinellas Technical College",
          subject="Career and job search resources for Web Development graduates")
full = Frame(M, M, W, PH - 2 * M, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
main = Frame(M, 0.8 * inch, W, PH - 0.8 * inch - 0.95 * inch, id="main", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="cover", frames=[full], onPage=cover), PageTemplate(id="main", frames=[main])])
doc.build(story)
print(out)
