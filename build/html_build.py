import os, re, base64, html as H
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build.py")).read()
a = src.index('CS = "https://careersourcetampabay.com"'); b = src.index('# ---------------------------------------------------------------- page furniture')
content = src[a:b]
CHECKED = re.search(r'CHECKED = "([^"]+)"', src).group(1)
SECTIONS = eval(re.search(r"SECTIONS = (\[.*?\])\n", src, re.S).group(1))
inch = 1; W = 1; MUTED = LINE = GREEN = YELLOW = None
class St(str): pass
body, small, intro, h1, h2, ctitle, cbody, bullet, links, week = [St(x) for x in
    ["body", "small", "intro", "h1", "h2", "ctitle", "cbody", "bullet", "links", "week"]]
def S(name, **kw): return St("fine" if name == "fine" else "muted")
def clean(t): return t.replace(' color="#008142"', '').replace('<u>', '').replace('</u>', '')
def Paragraph(text, style=body, bulletText=None):
    t = clean(text)
    if bulletText: return "<li>%s</li>" % t
    tag = {"h2": "h3", "week": "p"}.get(style, "p")
    return '<%s class="%s">%s</%s>' % (tag, style, t, tag)
def Spacer(*a): return ""
def Rule(*a, **k): return ""
def KeepTogether(x): return x
def NextPageTemplate(x): return ""
def A(url, text):
    ext = '' if url.startswith('#') else ' target="_blank" rel="noopener"'
    return '<a href="%s"%s>%s</a>' % (url.replace("&", "&amp;"), ext, text)
def linkline(*pairs): return '<p class="links">%s</p>' % ' <span class="sep">|</span> '.join(A(u, t) for u, t in pairs)
def B(text): return "<li>%s</li>" % clean(text)
def group(items):
    out = []; inlist = False
    for i in items:
        if i.startswith("<li>"):
            if not inlist: out.append("<ul>"); inlist = True
            out.append(i)
        else:
            if inlist: out.append("</ul>"); inlist = False
            out.append(i)
    if inlist: out.append("</ul>")
    return "".join(out)
first = [True]
def section(key, title, lead):
    close = "" if first[0] else "</section>"
    hidden = "" if first[0] else " hidden"
    first[0] = False
    return [close + '<section class="panel" id="%s" role="tabpanel" aria-labelledby="tab-%s"%s><h2>%s</h2><p class="intro">%s</p>' % (key, key, hidden, title, clean(lead))]
def card(title, tg=None, *content, stripe=None):
    inner = []
    if tg: inner.append('<p class="tags">%s</p>' % "".join('<span>%s</span>' % t for t in tg))
    inner.append("<h4>%s</h4>" % title)
    inner.append(group([c if c.startswith("<") else "<p>%s</p>" % clean(c) for c in content]))
    return ['<div class="card">%s</div>' % "".join(inner)]
def event(day, sub, title, text, link):
    return ['<div class="event"><div class="when"><strong>%s</strong><span>%s</span></div><div class="what"><h4>%s</h4><p>%s</p>%s</div></div>' % (day, sub, title, clean(text), linkline(link))]
def grid(header, rows, widths):
    h = "".join("<th>%s</th>" % x for x in header)
    r = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % clean(c) for c in row) for row in rows)
    return ['<div class="scroll"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (h, r)]
def note(text): return ['<div class="note">%s</div>' % clean(text)]
def paths(items):
    return ['<div class="paths">%s</div>' % "".join('<div class="path"><strong>%s</strong><span>%s</span><a href="#%s">%s</a></div>' % (t, x, k, l) for t, x, k, l in items)]
n = [0]
def checks(items):
    out = []
    for i in items:
        n[0] += 1
        out.append('<li><label><input type="checkbox" id="c%d"><span>%s</span></label></li>' % (n[0], i))
    return ['<ul class="checks">%s</ul>' % "".join(out)]
g = dict(globals())
exec(content, g)
def flat(x):
    for i in x:
        if isinstance(i, list): yield from flat(i)
        else: yield i
bodyhtml = "".join(flat(g["story"])) + "</section>"
logo = base64.b64encode(open(os.path.join(HERE, "logo.png"), "rb").read()).decode()
tabs = "".join('<button role="tab" id="tab-%s" data-tab="%s" aria-controls="%s">%s</button>' % (k, k, k, l) for k, l in SECTIONS)
page = open(os.path.join(HERE, "template.html")).read()
page = page.replace("{{TABS}}", tabs).replace("{{BODY}}", bodyhtml).replace("{{LOGO}}", logo).replace("{{CHECKED}}", CHECKED)
open(os.path.join(os.environ.get("SITE_DIR", "/home/claude/site"), "index.html"), "w").write(page)
print(len(page), page.count('class="card"'), page.count("<section"))
