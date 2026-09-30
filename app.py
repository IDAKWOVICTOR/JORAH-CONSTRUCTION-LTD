"""JORAH CONSTRUCTION LTD - interactive company profile (Streamlit)."""
import base64
import csv
from datetime import datetime
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

# --------------------------------------------------------------------------- #
# Editable company facts. Leave a contact field empty to hide it.
# --------------------------------------------------------------------------- #
COMPANY = {
    "name": "JORAH CONSTRUCTION LTD",
    "tagline": "Building a Sustainable Tomorrow",
    "type": "A Private Company Limited by Shares",
    "rc": "9896662",
    "office": "Federal Republic of Nigeria",
    "phone": "+234 806 726 0801",
    "email": "lakijohn1@gmail.com",
    "website": "",
    "linkedin": "https://www.linkedin.com/in/bldr-john-laki-mniob-014194261/",
}
FOUNDER = {
    "name": "Bldr. John Ndi Laki",
    "role": "Founder & Chief Executive Officer",
    "credential": "Registered Builder",
}

SERVICES = [
    ("travel_explore", "Drone Survey & Mapping", "Accurate data. Better decisions.",
     ["Aerial mapping & photogrammetry", "Topographic surveys", "Progress monitoring"]),
    ("view_in_ar", "BIM Services", "Smarter design. Efficient construction. Greater value.",
     ["3D modelling & coordination", "Clash detection", "Lifecycle management"]),
    ("layers", "GIS & Spatial Analysis", "Data-driven insights for better planning.",
     ["Spatial data analysis", "Thematic mapping", "Decision support systems"]),
    ("straighten", "Land Survey & Mapping", "Precision. Accuracy. Reliability.",
     ["Boundary & cadastral surveys", "Control surveys", "As-built surveys"]),
    ("engineering", "Construction & Engineering", "From concept to completion.",
     ["Building & infrastructure", "Project management", "Civil engineering solutions"]),
]

VALUES = [
    ("verified", "Quality Delivery", "Workmanship checked at every stage, from foundation to finishes."),
    ("schedule", "On-Time Execution", "Planned programmes and disciplined site management."),
    ("eco", "Sustainable Solutions", "Designs and methods built for a resilient future."),
    ("groups", "Professional Team", "Registered, experienced people on every project."),
]

PROCESS = [
    ("01", "Survey & Plan", "Drone, GNSS and total-station data establish the ground truth."),
    ("02", "Model & Design", "BIM coordination resolves clashes before they reach site."),
    ("03", "Build", "Supervised construction to specification, programme and budget."),
    ("04", "Monitor & Hand Over", "Progress mapping, as-built surveys and clean handover."),
]

PORTFOLIO = {
    "Residential & Apartments": (
        "residential",
        "Multi-storey apartment blocks and private residences, taken from structure through roofing, "
        "plastering and finishes.",
    ),
    "Institutional & Estate Developments": (
        "estates",
        "Large-footprint estate and institutional works: reinforced-concrete frames, ring beams, "
        "timber and steel roof trusses, and pitched roofing.",
    ),
    "Civil & Substructure Works": (
        "civil",
        "Excavation, blockwork foundations, septic and underground tanks, columns, stairs and "
        "structural detailing.",
    ),
    "Survey & Site Supervision": (
        "supervision",
        "Setting-out with survey instruments, and on-site inspections with clients, "
        "stakeholders and regulators.",
    ),
}

st.set_page_config(
    page_title="JORAH CONSTRUCTION LTD | Building a Sustainable Tomorrow",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()


def html(block: str) -> None:
    """Render raw HTML; collapse whitespace so markdown never treats it as a code block."""
    st.markdown(" ".join(line.strip() for line in block.splitlines()), unsafe_allow_html=True)


def icon(name: str) -> str:
    return f'<span class="ms">{name}</span>'


def head_html(kicker: str, title: str, sub: str = "", anchor: str = "") -> str:
    return " ".join(l.strip() for l in f"""
    <div class="sec-head" id="{anchor}">
      <div class="kicker">{kicker}</div>
      <h2>{title}</h2>
      {f'<p>{sub}</p>' if sub else ''}
    </div>""".splitlines())


def section_head(*args, **kwargs) -> None:
    st.markdown(head_html(*args, **kwargs), unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Styles
# --------------------------------------------------------------------------- #
hero_bg = b64(str(ASSETS / "hero.jpg"))

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap');

:root {{
  --g900:#06301B; --g800:#0B4D2A; --g700:#0F6B38; --g600:#1E8C45; --g100:#E6F3EA; --g50:#F3F7F4;
  --gold:#F5B800; --ink:#10281A; --muted:#5B6E62; --line:#DCE7DF;
}}
html, body, [class*="css"], .stMarkdown, p, li {{ font-family:'Plus Jakarta Sans',sans-serif; }}
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"],
[data-testid="stDecoration"] {{ display:none !important; }}
.block-container {{ padding:0 !important; max-width:100% !important; }}
[data-testid="stAppViewContainer"] {{ background:#fff; }}
html {{ scroll-behavior:smooth; }}
.ms {{ font-family:'Material Symbols Outlined'; font-weight:400; font-style:normal; font-size:inherit;
  line-height:1; display:inline-block; letter-spacing:normal; text-transform:none; white-space:nowrap;
  -webkit-font-feature-settings:'liga'; font-feature-settings:'liga'; vertical-align:middle; }}

/* ---------- nav ---------- */
.nav {{ position:sticky; top:0; z-index:999; display:flex; align-items:center; justify-content:space-between;
  padding:14px 6vw; background:rgba(255,255,255,.92); backdrop-filter:blur(14px);
  border-bottom:1px solid var(--line); }}
.nav .brand {{ font-family:'Sora',sans-serif; font-weight:800; color:var(--g800); font-size:1.15rem;
  letter-spacing:.2px; display:flex; align-items:center; gap:10px; }}
.nav .brand i {{ width:34px; height:34px; border-radius:9px; background:linear-gradient(135deg,var(--g800),var(--g600));
  color:#fff; display:grid; place-items:center; font-style:normal; font-size:1.25rem; }}
.nav .links a {{ color:var(--ink); text-decoration:none; font-weight:600; font-size:.9rem; margin-left:26px;
  padding:6px 0; border-bottom:2px solid transparent; transition:.2s; }}
.nav .links a:hover {{ color:var(--g600); border-color:var(--gold); }}
@media (max-width:900px) {{ .nav .links {{ display:none; }} }}

/* ---------- hero ---------- */
.hero {{ position:relative; min-height:88vh; display:flex; align-items:center; padding:90px 6vw 130px;
  background:linear-gradient(100deg,rgba(6,48,27,.96) 0%,rgba(6,48,27,.85) 42%,rgba(6,48,27,.35) 100%),
  url(data:image/jpeg;base64,{hero_bg}) center/cover; color:#fff; overflow:hidden; }}
.hero::after {{ content:""; position:absolute; right:-8%; top:-30%; width:55%; height:160%;
  background:linear-gradient(135deg,transparent 48%,rgba(245,184,0,.9) 48.3%,rgba(245,184,0,.9) 49%,
  rgba(30,140,69,.55) 49.3%,transparent 75%); transform:skewX(-8deg); pointer-events:none; }}
.hero .inner {{ position:relative; z-index:2; max-width:780px; animation:rise .9s ease both; }}
.pill {{ display:inline-flex; gap:8px; align-items:center; background:rgba(255,255,255,.12);
  border:1px solid rgba(255,255,255,.3); padding:7px 16px; border-radius:99px; font-size:.78rem;
  font-weight:600; letter-spacing:.6px; margin-bottom:22px; }}
.pill b {{ color:var(--gold); }}
.hero h1 {{ font-family:'Sora',sans-serif; font-weight:800; font-size:clamp(2.4rem,5.6vw,4.6rem);
  line-height:1.04; margin:0 0 20px; color:#fff; }}
.hero h1 em {{ font-style:normal; color:var(--gold); }}
.hero p.lead {{ font-size:1.15rem; line-height:1.65; color:#DCEEE2; max-width:600px; margin-bottom:34px; }}
.btns a {{ display:inline-block; padding:14px 28px; border-radius:10px; font-weight:700; text-decoration:none;
  margin:0 12px 12px 0; transition:.25s; font-size:.95rem; }}
.btn-gold {{ background:var(--gold); color:var(--g900) !important; }}
.btn-gold:hover {{ transform:translateY(-3px); box-shadow:0 12px 26px rgba(245,184,0,.4); }}
.btn-ghost {{ border:1.5px solid rgba(255,255,255,.6); color:#fff !important; }}
.btn-ghost:hover {{ background:rgba(255,255,255,.14); transform:translateY(-3px); }}
.cert {{ position:absolute; right:6vw; bottom:96px; z-index:3; background:#fff; color:var(--ink);
  border-radius:14px; padding:14px 20px; display:flex; gap:14px; align-items:center;
  box-shadow:0 18px 40px rgba(0,0,0,.3); animation:rise 1.1s .2s ease both; }}
.cert .ms {{ font-size:2.2rem; color:var(--g600); }}
.cert small {{ display:block; color:var(--muted); font-size:.68rem; letter-spacing:1px; font-weight:700; }}
.cert strong {{ font-family:'Sora',sans-serif; color:var(--g800); font-size:1.05rem; }}
@media (max-width:700px) {{ .cert {{ position:relative; right:auto; bottom:auto; margin-top:10px; }}
  .hero {{ flex-direction:column; align-items:flex-start; justify-content:center; padding-bottom:60px; }} }}
@keyframes rise {{ from {{ opacity:0; transform:translateY(28px); }} to {{ opacity:1; transform:none; }} }}

/* ---------- stats band ---------- */
.stats {{ margin:-56px 6vw 0; position:relative; z-index:5; display:grid; grid-template-columns:repeat(4,1fr);
  background:#fff; border-radius:18px; box-shadow:0 20px 50px rgba(6,48,27,.16); overflow:hidden; }}
.stat {{ padding:28px 24px; text-align:center; border-right:1px solid var(--line); }}
.stat:last-child {{ border:none; }}
.stat b {{ display:block; font-family:'Sora',sans-serif; font-size:1.9rem; color:var(--g700); }}
.stat span {{ font-size:.82rem; color:var(--muted); font-weight:600; letter-spacing:.4px; }}
@media (max-width:800px) {{ .stats {{ grid-template-columns:1fr 1fr; }} .stat {{ border-bottom:1px solid var(--line); }} }}

/* ---------- sections ---------- */
.sec-head {{ text-align:center; max-width:720px; margin:0 auto 42px; padding:0 20px; scroll-margin-top:80px; }}
.sec-head .kicker {{ color:var(--g600); font-weight:800; letter-spacing:3px; font-size:.76rem; text-transform:uppercase; }}
.sec-head h2 {{ font-family:'Sora',sans-serif; font-size:clamp(1.8rem,3.4vw,2.6rem); color:var(--g800);
  margin:10px 0 12px; font-weight:800; }}
.sec-head h2::after {{ content:""; display:block; width:64px; height:4px; background:var(--gold);
  border-radius:4px; margin:14px auto 0; }}
.sec-head p {{ color:var(--muted); font-size:1.02rem; line-height:1.7; }}
.pad {{ padding:96px 6vw 10px; }}

.about {{ display:grid; grid-template-columns:1.1fr 1fr; gap:48px; align-items:center; padding:0 6vw; }}
.about p {{ color:#33483B; line-height:1.85; font-size:1.05rem; }}
.about .mission {{ background:linear-gradient(135deg,var(--g800),var(--g600)); color:#fff; border-radius:20px;
  padding:34px; position:relative; overflow:hidden; }}
.about .mission::after {{ content:""; position:absolute; right:-40px; bottom:-40px; width:160px; height:160px;
  border-radius:50%; background:rgba(245,184,0,.22); }}
.about .mission h3 {{ font-family:'Sora',sans-serif; margin:0 0 10px; color:var(--gold); font-size:1.15rem; }}
.about .mission p {{ color:#E3F2E8; margin:0 0 18px; }}
.about .mission ul {{ list-style:none; padding:0; margin:0; position:relative; z-index:2; }}
.about .mission li {{ padding:7px 0; color:#fff; font-weight:600; }}
.about .mission li .ms {{ color:var(--gold); margin-right:10px; }}
@media (max-width:900px) {{ .about {{ grid-template-columns:1fr; }} }}

.values {{ display:grid; grid-template-columns:repeat(4,1fr); gap:18px; padding:48px 6vw 0; }}
.val {{ padding:26px; border-radius:16px; background:var(--g50); border:1px solid var(--line); transition:.3s; }}
.val:hover {{ transform:translateY(-6px); background:#fff; box-shadow:0 18px 36px rgba(6,48,27,.12); }}
.val .ms {{ font-size:2rem; color:var(--g600); }}
.val h4 {{ font-family:'Sora',sans-serif; color:var(--g800); margin:12px 0 6px; font-size:1rem; }}
.val p {{ margin:0; color:var(--muted); font-size:.9rem; line-height:1.6; }}
@media (max-width:1000px) {{ .values {{ grid-template-columns:1fr 1fr; }} }}
@media (max-width:560px) {{ .values {{ grid-template-columns:1fr; }} }}

/* ---------- services ---------- */
.svc-wrap {{ background:linear-gradient(180deg,#fff,var(--g50)); padding-bottom:90px; margin-top:80px; }}
.services {{ display:grid; grid-template-columns:repeat(5,1fr); gap:18px; padding:0 6vw; }}
.svc {{ background:#fff; border-radius:18px; padding:28px 22px 26px; border:1px solid var(--line);
  position:relative; overflow:hidden; transition:.35s; }}
.svc::before {{ content:""; position:absolute; left:0; top:0; height:4px; width:100%;
  background:linear-gradient(90deg,var(--g600),var(--gold)); transform:scaleX(0); transform-origin:left; transition:.4s; }}
.svc:hover {{ transform:translateY(-8px); box-shadow:0 24px 44px rgba(6,48,27,.15); }}
.svc:hover::before {{ transform:scaleX(1); }}
.svc .ic {{ width:58px; height:58px; border-radius:16px; background:var(--g100); color:var(--g700);
  display:grid; place-items:center; font-size:1.9rem; margin-bottom:18px; transition:.3s; }}
.svc:hover .ic {{ background:var(--g700); color:#fff; }}
.svc h3 {{ font-family:'Sora',sans-serif; font-size:1.02rem; color:var(--g800); margin:0 0 6px; }}
.svc .tag {{ color:var(--g600); font-weight:600; font-size:.82rem; margin-bottom:14px; }}
.svc ul {{ list-style:none; padding:0; margin:0; }}
.svc li {{ font-size:.86rem; color:#3c5145; padding:5px 0 5px 20px; position:relative; }}
.svc li::before {{ content:"\\2713"; position:absolute; left:0; color:var(--g600); font-weight:800; }}
@media (max-width:1200px) {{ .services {{ grid-template-columns:repeat(3,1fr); }} }}
@media (max-width:760px) {{ .services {{ grid-template-columns:1fr; }} }}

/* ---------- process ---------- */
.process {{ display:grid; grid-template-columns:repeat(4,1fr); gap:0; padding:0 6vw; position:relative; }}
.step {{ padding:0 22px; position:relative; text-align:center; }}
.step .n {{ width:64px; height:64px; margin:0 auto 18px; border-radius:50%; background:var(--g800); color:var(--gold);
  font-family:'Sora',sans-serif; font-weight:800; font-size:1.2rem; display:grid; place-items:center;
  border:5px solid var(--g100); position:relative; z-index:2; }}
.step::before {{ content:""; position:absolute; top:31px; left:-50%; width:100%; height:3px;
  background:repeating-linear-gradient(90deg,var(--g600) 0 8px,transparent 8px 16px); }}
.step:first-child::before {{ display:none; }}
.step h4 {{ font-family:'Sora',sans-serif; color:var(--g800); margin:0 0 6px; }}
.step p {{ color:var(--muted); font-size:.9rem; line-height:1.6; margin:0; }}
@media (max-width:800px) {{ .process {{ grid-template-columns:1fr 1fr; row-gap:34px; }} .step::before {{ display:none; }} }}

/* ---------- founder ---------- */
.founder-wrap {{ background:var(--g900); margin-top:96px; padding:90px 6vw; position:relative; overflow:hidden; }}
.founder-wrap::before {{ content:""; position:absolute; left:-10%; top:-40%; width:45%; height:200%;
  background:linear-gradient(135deg,rgba(30,140,69,.35),transparent 60%); transform:skewX(-10deg); }}
.founder {{ position:relative; z-index:2; display:grid; grid-template-columns:380px 1fr; gap:60px; align-items:center;
  max-width:1100px; margin:0 auto; }}
.founder .photo {{ border-radius:22px; overflow:hidden; border:4px solid var(--gold); box-shadow:0 26px 60px rgba(0,0,0,.45); }}
.founder .photo img {{ width:100%; display:block; }}
.founder .kicker {{ color:var(--gold); font-weight:800; letter-spacing:3px; font-size:.76rem; }}
.founder h2 {{ font-family:'Sora',sans-serif; color:#fff; font-size:clamp(1.9rem,3.6vw,2.8rem); margin:10px 0 4px; }}
.founder .role {{ color:#B5D9C2; font-weight:600; margin-bottom:20px; }}
.founder .badge {{ display:inline-flex; gap:8px; align-items:center; background:var(--gold); color:var(--g900);
  padding:8px 18px; border-radius:99px; font-weight:800; font-size:.85rem; margin:0 10px 18px 0; }}
.founder .badge.alt {{ background:rgba(255,255,255,.12); color:#fff; border:1px solid rgba(255,255,255,.3); }}
.founder blockquote {{ border-left:4px solid var(--gold); margin:18px 0 0; padding:4px 0 4px 20px; color:#E3F2E8;
  font-size:1.1rem; line-height:1.7; }}
@media (max-width:900px) {{ .founder {{ grid-template-columns:1fr; gap:34px; }} .founder .photo {{ max-width:340px; }} }}

.founder a.li {{ display:inline-flex; gap:8px; align-items:center; color:#fff; text-decoration:none; font-weight:700;
  border-bottom:2px solid var(--gold); padding:2px 0; margin-bottom:6px; }}
.founder a.li:hover {{ color:var(--gold); }}

/* ---------- portfolio (tabs + images) ---------- */
.stTabs [data-baseweb="tab-list"] {{ gap:8px; justify-content:center; flex-wrap:wrap; border-bottom:none; padding:0 6vw; }}
.stTabs [data-baseweb="tab"] {{ background:var(--g50); border-radius:99px; padding:10px 22px; height:auto;
  font-weight:700; border:1px solid var(--line); }}
.stTabs [aria-selected="true"] {{ background:var(--g800) !important; color:#fff !important; border-color:var(--g800); }}
.stTabs [aria-selected="true"] p {{ color:#fff !important; }}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display:none; }}
.stTabs [data-baseweb="tab-panel"] {{ padding:26px 6vw 0; }}
.tab-blurb {{ text-align:center; color:var(--muted); max-width:720px; margin:0 auto 26px; line-height:1.7; }}
[data-testid="stImage"] img {{ border-radius:14px; transition:.35s; box-shadow:0 6px 18px rgba(6,48,27,.14); }}
[data-testid="stImage"]:hover img {{ transform:scale(1.025); box-shadow:0 18px 34px rgba(6,48,27,.28); }}
[data-testid="stHorizontalBlock"] {{ gap:14px; }}
[data-testid="stVerticalBlock"] {{ gap:14px; }}
[data-testid="stExpander"] {{ border:1px solid var(--line); border-radius:14px; margin:0 6vw; }}

/* ---------- contact ---------- */
.contact-card {{ background:linear-gradient(135deg,var(--g800),var(--g600)); color:#fff; border-radius:20px; padding:36px; }}
.contact-card h3 {{ font-family:'Sora',sans-serif; color:var(--gold); margin:0 0 18px; }}
.ci {{ display:flex; gap:14px; align-items:flex-start; padding:12px 0; border-top:1px solid rgba(255,255,255,.18); }}
.ci:first-of-type {{ border-top:none; }}
.ci .ms {{ font-size:1.6rem; color:var(--gold); }}
.ci small {{ display:block; color:#BFE3CB; font-size:.72rem; letter-spacing:1px; font-weight:700; text-transform:uppercase; }}
.ci span.v {{ font-weight:600; }}
.ci a {{ color:#fff; }}
.stForm {{ border:1px solid var(--line) !important; border-radius:20px !important; padding:26px !important; background:var(--g50); }}
.stFormSubmitButton button {{ background:var(--g700); color:#fff; border:none; border-radius:10px; font-weight:700; padding:10px 26px; }}
.stFormSubmitButton button:hover {{ background:var(--gold); color:var(--g900); }}
[data-testid="stDownloadButton"] button {{ background:var(--g700); color:#fff; border:none; border-radius:10px; font-weight:700; }}

[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] {{ background:#fff !important;
  border:1px solid #C5D6CA !important; border-radius:10px !important; }}
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {{ background:#fff !important; color:var(--ink) !important; }}
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within {{ border-color:var(--g600) !important; }}

/* ---------- footer ---------- */
.footer {{ margin-top:90px; background:var(--g900); color:#BFE3CB; padding:44px 6vw 26px; position:relative; }}
.footer::before {{ content:""; position:absolute; top:0; left:0; right:0; height:5px;
  background:linear-gradient(90deg,var(--g600),var(--gold),var(--g600)); }}
.footer .row {{ display:flex; flex-wrap:wrap; justify-content:space-between; gap:20px; align-items:center; }}
.footer .b {{ font-family:'Sora',sans-serif; color:#fff; font-weight:800; font-size:1.2rem; }}
.footer .m {{ letter-spacing:3px; font-weight:700; color:var(--gold); font-size:.8rem; }}
.footer hr {{ border:none; border-top:1px solid rgba(255,255,255,.14); margin:22px 0 14px; }}
.footer .c {{ font-size:.8rem; }}
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------- #
# Navigation + hero
# --------------------------------------------------------------------------- #
html(f"""
<div class="nav">
  <div class="brand"><i>{icon('apartment')}</i>{COMPANY['name']}</div>
  <div class="links">
    <a href="#about">About</a><a href="#services">Services</a><a href="#process">Approach</a>
    <a href="#leadership">Leadership</a><a href="#projects">Projects</a><a href="#contact">Contact</a>
  </div>
</div>
<div class="hero">
  <div class="inner">
    <div class="pill">{icon('flag')} FEDERAL REPUBLIC OF NIGERIA &nbsp;|&nbsp; <b>RC {COMPANY['rc']}</b></div>
    <h1>Innovative solutions for <em>modern infrastructure.</em></h1>
    <p class="lead">We deliver high-quality construction, engineering and technology-driven solutions
    for a sustainable and resilient future.</p>
    <div class="btns"><a class="btn-gold" href="#projects">View Our Projects</a>
    <a class="btn-ghost" href="#contact">Start a Project</a></div>
  </div>
  <div class="cert">{icon('workspace_premium')}<div><small>CERTIFICATE OF INCORPORATION</small>
  <strong>No. {COMPANY['rc']}</strong></div></div>
</div>
<div class="stats">
  <div class="stat"><b>5</b><span>CORE SERVICE LINES</span></div>
  <div class="stat"><b>BIM + GIS</b><span>TECHNOLOGY-DRIVEN</span></div>
  <div class="stat"><b>Registered</b><span>BUILDER-LED</span></div>
  <div class="stat"><b>{COMPANY['rc']}</b><span>CORPORATE REG. NO.</span></div>
</div>
""")

# --------------------------------------------------------------------------- #
# About
# --------------------------------------------------------------------------- #
html('<div class="pad" style="padding-bottom:0"></div>')
section_head("Who we are", "Construction, engineered with technology",
             "", anchor="about")
html(f"""
<div class="about">
  <div>
    <p><strong>{COMPANY['name']}</strong> is a Nigerian {COMPANY['type'].lower().replace('a private', 'private')}
    that brings construction, engineering and geospatial technology under one roof.</p>
    <p>We combine site-proven building expertise with drone surveys, BIM coordination and GIS analysis,
    so every decision, from land acquisition to lifecycle management, is backed by accurate data.
    The result is infrastructure that is precise, cost-effective and delivered on time.</p>
    <p style="font-weight:700;color:var(--g800)">From concept to completion, we build with precision,
    technology and integrity.</p>
  </div>
  <div class="mission">
    <h3>Why clients choose JORAH</h3>
    <p>Innovation. Integrity. Impact.</p>
    <ul>
      <li>{icon('check_circle')}Modern equipment &amp; technology</li>
      <li>{icon('check_circle')}Experienced professionals</li>
      <li>{icon('check_circle')}Cost-effective solutions</li>
      <li>{icon('check_circle')}Timely project delivery</li>
    </ul>
  </div>
</div>
<div class="values">
  {''.join(f'<div class="val">{icon(i)}<h4>{t}</h4><p>{d}</p></div>' for i, t, d in VALUES)}
</div>
""")

# --------------------------------------------------------------------------- #
# Services
# --------------------------------------------------------------------------- #
cards = "".join(
    f'<div class="svc"><div class="ic">{icon(ic)}</div><h3>{t}</h3><div class="tag">{tag}</div>'
    f'<ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>'
    for ic, t, tag, items in SERVICES
)
html('<div class="svc-wrap"><div class="pad" style="padding-bottom:0"></div>'
     + head_html("What we do", "Our Services",
                 "Five integrated service lines covering the full project lifecycle.", "services")
     + f'<div class="services">{cards}</div></div>')

# --------------------------------------------------------------------------- #
# Process
# --------------------------------------------------------------------------- #
html('<div class="pad"></div>')
section_head("How we work", "From concept to completion",
             "A data-first workflow that removes surprises from site.", anchor="process")
html('<div class="process">' + "".join(
    f'<div class="step"><div class="n">{n}</div><h4>{t}</h4><p>{d}</p></div>' for n, t, d in PROCESS
) + "</div>")

# --------------------------------------------------------------------------- #
# Founder
# --------------------------------------------------------------------------- #
founder_img = b64(str(ASSETS / "people" / "founder.jpg"))
html(f"""
<div class="founder-wrap" id="leadership">
  <div class="founder">
    <div class="photo"><img alt="{FOUNDER['name']}" src="data:image/jpeg;base64,{founder_img}"></div>
    <div>
      <div class="kicker">LEADERSHIP</div>
      <h2>{FOUNDER['name']}</h2>
      <div class="role">{FOUNDER['role']}</div>
      <span class="badge">{icon('verified')} {FOUNDER['credential']}</span>
      <span class="badge alt">{icon('school')} Corporate Member, NIOB</span><br>
      <a class="li" href="{COMPANY['linkedin']}" target="_blank" rel="noopener">{icon('open_in_new')} Connect on LinkedIn</a><br>
      <blockquote>As a Registered Builder, he leads JORAH in delivering construction, engineering and
      geospatial solutions with precision, technology and integrity.</blockquote>
    </div>
  </div>
</div>
""")

# --------------------------------------------------------------------------- #
# Projects
# --------------------------------------------------------------------------- #
html('<div class="pad"></div>')
section_head("Track record", "Projects We Have Executed",
             "A selection of work from our sites. Hover an image and use the expand icon for full size.",
             anchor="projects")

tabs = st.tabs(list(PORTFOLIO))
for tab, (label, (key, blurb)) in zip(tabs, PORTFOLIO.items()):
    with tab:
        html(f'<div class="tab-blurb">{blurb}</div>')
        photos = sorted((ASSETS / "projects").glob(f"{key}_*.jpg"))
        cols = st.columns(3)
        for n, p in enumerate(photos):
            with cols[n % 3]:
                st.image(str(p), width="stretch")

html('<div style="height:40px"></div>')
with st.expander("View the company flyer"):
    st.image(str(ASSETS / "flyer.png"), width="stretch")
    st.download_button("Download flyer (PNG)", (ASSETS / "flyer.png").read_bytes(),
                       file_name="JORAH-Construction-Flyer.png", mime="image/png")

# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #
html('<div class="pad"></div>')
section_head("Get in touch", "Let's build something lasting",
             "Tell us about your project and we will respond promptly.", anchor="contact")

_, left, right, _ = st.columns([0.45, 4.4, 5.6, 0.45], gap="large")
with left:
    rows = [("location_on", "Head Office", COMPANY["office"]),
            ("apartment", "Company Registration No.", COMPANY["rc"])]
    if COMPANY["phone"]:
        tel = COMPANY["phone"].replace(" ", "")
        rows.append(("call", "Phone / WhatsApp",
                     f'<a href="tel:{tel}">{COMPANY["phone"]}</a> &nbsp;&middot;&nbsp; '
                     f'<a href="https://wa.me/{tel.lstrip("+")}" target="_blank" rel="noopener">WhatsApp</a>'))
    if COMPANY["email"]:
        rows.append(("mail", "Email", f'<a href="mailto:{COMPANY["email"]}">{COMPANY["email"]}</a>'))
    if COMPANY["linkedin"]:
        rows.append(("share", "LinkedIn",
                     f'<a href="{COMPANY["linkedin"]}" target="_blank" rel="noopener">Bldr. John Laki, MNIOB</a>'))
    if COMPANY["website"]:
        rows.append(("language", "Website", f'<a href="{COMPANY["website"]}">{COMPANY["website"]}</a>'))
    html('<div class="contact-card"><h3>JORAH CONSTRUCTION LTD</h3>' + "".join(
        f'<div class="ci">{icon(i)}<div><small>{k}</small><span class="v">{v}</span></div></div>'
        for i, k, v in rows) + "</div>")
with right:
    with st.form("enquiry", clear_on_submit=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full name*")
        contact = c2.text_input("Phone or email*")
        interest = st.selectbox("I am interested in", [s[1] for s in SERVICES])
        message = st.text_area("Project details", height=120)
        if st.form_submit_button("Send enquiry"):
            if name.strip() and contact.strip():
                path = ROOT / "enquiries.csv"
                new = not path.exists()
                with path.open("a", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    if new:
                        w.writerow(["timestamp", "name", "contact", "service", "message"])
                    w.writerow([datetime.now().isoformat(timespec="seconds"), name, contact, interest, message])
                st.success("Thank you. Your enquiry has been received.")
            else:
                st.warning("Please provide your name and a phone number or email.")

# --------------------------------------------------------------------------- #
# Footer
# --------------------------------------------------------------------------- #
html(f"""
<div class="footer">
  <div class="row">
    <div><div class="b">{COMPANY['name']}</div><div>{COMPANY['tagline']} &middot; {COMPANY['type']}</div></div>
    <div class="m">INNOVATION &nbsp;|&nbsp; INTEGRITY &nbsp;|&nbsp; IMPACT</div>
  </div>
  <hr>
  <div class="c">&copy; {datetime.now().year} {COMPANY['name']}. RC {COMPANY['rc']}. All rights reserved.</div>
</div>
""")
