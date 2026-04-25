import streamlit as st
import folium
from streamlit_folium import st_folium
import base64
import pathlib

_dir = pathlib.Path(__file__).parent
LOGO_B64    = (_dir / "logo.b64").read_text().strip()
PATTERN_B64 = (_dir / "pattern.b64").read_text().strip()

st.set_page_config(page_title="Massilia", page_icon="🥃", layout="wide", initial_sidebar_state="collapsed")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap');

html, body, [class*="css"], .stApp, p, div, span, label, h1, h2, h3 {
    font-family: 'Nunito', sans-serif !important;
}

/* ── Background ── */
.stApp {
    background-color: #FAF3E8 !important;
}

/* ── Padding ── */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 40px !important;
    max-width: 1280px !important;
}

/* ── Header ── */
.m-header {
    background: #FAF3E8;
    border-bottom: 2px solid #29B6F6;
    padding: 16px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    border-radius: 0 0 32px 32px;
    box-shadow: 0 4px 24px rgba(41,182,246,0.12);
    position: relative;
    overflow: hidden;
}
.m-header::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: rgba(41,182,246,0.06);
    pointer-events: none;
}
.m-header img { height: 100px; object-fit: contain; display: block; }
.m-tagline {
    font-size: 0.65rem; font-weight: 900;
    letter-spacing: 0.22em; color: #F5A623;
    text-transform: uppercase; margin-bottom: 6px;
}
.m-slogan { font-size: 1rem; font-weight: 800; color: #0277BD; }
.m-sub    { font-size: 0.7rem; color: #888; margin-top: 3px; }

/* ── Stat chips ── */
.stat-row { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.stat-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: white; border-radius: 40px; padding: 7px 16px;
    font-size: 0.85rem; font-weight: 700; color: #0277BD;
    border: 1.5px solid rgba(41,182,246,0.18);
    box-shadow: 0 2px 10px rgba(41,182,246,0.1);
}
.chip-val { color: #F5A623; font-weight: 900; }

/* ── Section title ── */
.s-title {
    font-size: 1.25rem; font-weight: 900; color: #0277BD;
    margin-bottom: 14px; padding-bottom: 8px;
    border-bottom: 3px solid #F5A623;
    display: inline-block;
}

/* ── Spot card ── */
.spot-card {
    background: white; border-radius: 20px; padding: 16px 18px;
    margin-bottom: 12px;
    box-shadow: 0 3px 16px rgba(41,182,246,0.09);
    border-left: 4px solid #29B6F6;
    position: relative; overflow: hidden;
}
.spot-card::after {
    content: ''; position: absolute; top: -20px; right: -20px;
    width: 70px; height: 70px; border-radius: 50%;
    background: rgba(245,166,35,0.07);
}
.spot-name { font-size: 0.97rem; font-weight: 800; color: #0277BD; margin-bottom: 5px; }
.spot-desc { font-size: 0.8rem; color: #555; margin-bottom: 8px; line-height: 1.5; }
.price-badge {
    display: inline-block;
    background: #F5A623; color: white;
    font-size: 1.05rem; font-weight: 900;
    padding: 2px 12px; border-radius: 30px;
    box-shadow: 0 3px 10px rgba(245,166,35,0.35);
}
.s-tag {
    display: inline-block; background: #EBF7FD; color: #0288D1;
    border-radius: 20px; padding: 2px 10px; font-size: 0.7rem;
    font-weight: 700; margin: 2px;
}

/* ── Pref panel ── */
.pref-panel {
    background: white; border-radius: 24px; padding: 20px 22px;
    box-shadow: 0 4px 24px rgba(41,182,246,0.10);
    border: 1.5px solid rgba(41,182,246,0.12);
    margin-bottom: 16px;
}

/* ── Community card ── */
.comm-card {
    background: white; border-radius: 20px; padding: 16px 18px;
    margin-bottom: 14px;
    box-shadow: 0 3px 16px rgba(41,182,246,0.09);
    border-left: 4px solid #F5A623;
}
.c-avatar {
    width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg,#29B6F6,#0277BD);
    color: white; font-weight: 900; font-size: 0.9rem;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(41,182,246,0.3);
}

/* ── Promo card ── */
.promo-card {
    background: linear-gradient(135deg,#29B6F6,#0277BD);
    border-radius: 22px; padding: 20px 22px; margin-bottom: 14px;
    color: white;
    box-shadow: 0 6px 28px rgba(41,182,246,0.32);
    position: relative; overflow: hidden;
}
.promo-card::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 140px; height: 140px; border-radius: 50%;
    background: rgba(255,255,255,0.07);
}
.promo-card::after {
    content: ''; position: absolute; bottom: -50px; left: -20px;
    width: 120px; height: 120px; border-radius: 50%;
    background: rgba(245,166,35,0.18);
}
.promo-num { font-size: 2.4rem; font-weight: 900; color: #F5A623; line-height: 1; }
.promo-place { font-size: 0.95rem; font-weight: 800; margin-top: 4px; position: relative; z-index: 1; }
.promo-desc  { font-size: 0.8rem; opacity: 0.85; margin-top: 3px; position: relative; z-index: 1; }
.promo-code-box {
    background: rgba(255,255,255,0.15); border-radius: 12px;
    padding: 7px 14px; display: flex; align-items: center;
    justify-content: space-between; margin-top: 12px;
    border: 1px solid rgba(255,255,255,0.22); position: relative; z-index: 1;
}
.promo-code { font-weight: 900; font-size: 0.9rem; color: #F5A623; letter-spacing: 0.08em; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white; border-radius: 40px; padding: 5px; gap: 4px;
    border: 2px solid #29B6F6;
    box-shadow: 0 4px 16px rgba(41,182,246,0.14);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 40px !important; font-weight: 800 !important;
    color: #29B6F6 !important; padding: 8px 24px !important; font-size: 0.88rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#29B6F6,#0288D1) !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(41,182,246,0.35) !important;
}

/* ── Buttons — pill shape, no emoji issues ── */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg,#29B6F6,#0277BD) !important;
    color: white !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    border: none !important;
    padding: 10px 28px !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 4px 16px rgba(41,182,246,0.32) !important;
    transition: all 0.18s ease !important;
    font-family: 'Nunito', sans-serif !important;
    width: 100% !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    box-shadow: 0 8px 28px rgba(41,182,246,0.45) !important;
    transform: translateY(-2px) !important;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox div {
    border-radius: 12px !important;
    border: 1.5px solid rgba(41,182,246,0.25) !important;
    font-family: 'Nunito', sans-serif !important;
    color: #0277BD !important;
    background: #F8FCFF !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stMultiSelect label, .stCheckbox label,
.stFileUploader label {
    color: #0277BD !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    font-family: 'Nunito', sans-serif !important;
}
/* select_slider labels */
.stSlider [data-testid="stMarkdownContainer"] p {
    color: #0277BD !important;
    font-weight: 700 !important;
}

/* ── Checkbox ── */
.stCheckbox label { color: #0277BD !important; font-weight: 700 !important; font-size: 0.85rem !important; }
.stCheckbox { margin-bottom: 4px !important; }

/* ── Welcome banner ── */
.w-banner {
    background: linear-gradient(135deg,rgba(41,182,246,0.1),rgba(245,166,35,0.07));
    border-radius: 16px; padding: 11px 16px; margin-bottom: 14px;
    border: 1px solid rgba(41,182,246,0.18);
    font-weight: 700; color: #0277BD; font-size: 0.87rem;
}
.pref-pill {
    display: inline-block; background: #EBF7FD; color: #0277BD;
    border-radius: 20px; padding: 3px 12px; font-size: 0.78rem;
    font-weight: 700; margin: 2px; border: 1px solid rgba(41,182,246,0.2);
}

/* ── Tip row ── */
.tip-row {
    background: white; border-radius: 16px; padding: 13px 16px;
    margin-bottom: 10px; display: flex; align-items: center; gap: 12px;
    box-shadow: 0 2px 12px rgba(41,182,246,0.07);
    border: 1px solid rgba(41,182,246,0.09);
}
.tip-icon { font-size: 1.5rem; flex-shrink: 0; }
.tip-title { font-size: 0.9rem; font-weight: 800; color: #0277BD; }
.tip-desc  { font-size: 0.78rem; color: #888; margin-top: 1px; }

/* ── Empty state ── */
.empty-state {
    background: #FFF3E0; border-radius: 18px; padding: 22px;
    text-align: center; color: #E65100; font-weight: 700;
    border: 1px solid rgba(230,81,0,0.15);
}

/* ── Success ── */
.ok-box {
    background: rgba(46,125,50,0.09); border-radius: 14px;
    padding: 11px 16px; color: #2E7D32; font-weight: 700;
    border: 1px solid rgba(46,125,50,0.2); margin-top: 8px;
    font-size: 0.9rem;
}

/* ── Multiselect tags ── */
[data-baseweb="tag"] { background: #29B6F6 !important; }
[data-baseweb="tag"] span { color: white !important; font-weight: 700 !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
SPOTS = [
    {"name":"Bar des 13 Coins",    "lat":43.2996,"lon":5.3697,"specialty":"Pastis",      "price":1.5,"mood":["Lively","Tradition"],"neighbourhood":"Le Panier",  "rating":4.8,"desc":"The cheapest pastis in Le Panier — pure local vibes."},
    {"name":"Chez Etienne",         "lat":43.2981,"lon":5.3712,"specialty":"Fougasse",    "price":2.5,"mood":["Tradition","Chill"], "neighbourhood":"Le Panier",  "rating":4.9,"desc":"The best fougasse in Marseille since 1943. A legend."},
    {"name":"Marche des Capucins",  "lat":43.2938,"lon":5.3791,"specialty":"Panisse",     "price":2.0,"mood":["Quick","Lively"],   "neighbourhood":"Noailles",   "rating":4.6,"desc":"Fresh panisse at 2 euros — eat standing like a real Marseillais."},
    {"name":"La Caravelle",         "lat":43.2957,"lon":5.3651,"specialty":"Pastis",      "price":2.0,"mood":["Sea view","Lively"],"neighbourhood":"Vieux-Port", "rating":4.7,"desc":"Stunning Vieux-Port view, pastis 2 euros, jazz in the evening."},
    {"name":"Cafe Populaire",       "lat":43.2916,"lon":5.3834,"specialty":"Pastis",      "price":1.8,"mood":["Chill","Tradition"],"neighbourhood":"Cours Julien","rating":4.5,"desc":"The artists hangout in Cours Julien."},
    {"name":"L Epicerie Ideale",    "lat":43.2901,"lon":5.3852,"specialty":"Fougasse",    "price":3.0,"mood":["Chill","Sea view"], "neighbourhood":"Cours Julien","rating":4.6,"desc":"Artisan fougasse and local Provencal products."},
    {"name":"Bar Longchamp",        "lat":43.2993,"lon":5.3888,"specialty":"Pastis",      "price":1.5,"mood":["Tradition","Quick"],"neighbourhood":"Longchamp",  "rating":4.4,"desc":"Pastis 1.50 euros — authentic neighbourhood, no tourists."},
    {"name":"Pizzeria Etienne",     "lat":43.2978,"lon":5.3718,"specialty":"Panisse",     "price":2.5,"mood":["Lively","Tradition"],"neighbourhood":"Le Panier", "rating":4.8,"desc":"Panisse and pizza — a true institution of Le Panier."},
    {"name":"Le Glacier du Port",   "lat":43.2948,"lon":5.3638,"specialty":"Navette",     "price":1.0,"mood":["Quick","Sea view"], "neighbourhood":"Vieux-Port", "rating":4.3,"desc":"Navettes and sweet treats with a view of the ferry."},
    {"name":"Bar de la Marine",     "lat":43.2952,"lon":5.3660,"specialty":"Pastis",      "price":2.0,"mood":["Sea view","Lively"],"neighbourhood":"Vieux-Port", "rating":4.7,"desc":"Made famous by Marcel Pagnol — the authentic pastis experience."},
]
PROMOS = [
    {"place":"Bar des 13 Coins",   "discount":"20%",   "desc":"On your 2nd pastis on Friday evenings", "code":"MASSILIA20"},
    {"place":"Marche des Capucins","discount":"- 0.50","desc":"Off panisse after 2pm",                  "code":"PANISSE50"},
    {"place":"Chez Etienne",       "discount":"15%",   "desc":"On fougasse with student ID",           "code":"ETUDIANT15"},
    {"place":"Bar Longchamp",      "discount":"1 + 1", "desc":"Buy one pastis, get one free on Sunday","code":"LONGCHAMP11"},
]
MOODS         = ["Lively","Chill","Sea view","Tradition","Quick","Terrace"]
SPECIALTIES   = ["Pastis","Panisse","Fougasse","Bouillabaisse","Navette","Socca"]
NEIGHBOURHOODS= ["All","Vieux-Port","Le Panier","Noailles","Cours Julien","Longchamp"]
PRICE_COLORS  = {1.0:"#2ECC71",1.5:"#27AE60",1.8:"#F5A623",2.0:"#F5A623",2.5:"#E67E22",3.0:"#E74C3C"}

# ── Session state ─────────────────────────────────────────────────────────────
if "prefs" not in st.session_state:
    st.session_state.prefs = {"budget":5.0,"neighbourhood":"All","moods":[],"specialties":[],"name":""}
if "comments" not in st.session_state:
    st.session_state.comments = [
        {"user":"Sophie M.","initials":"SM","text":"Bar des 13 Coins pastis at 1.50 euros with a view of Le Panier — absolutely perfect!","specialty":"Pastis","place":"Bar des 13 Coins","rating":5,"time":"2h ago"},
        {"user":"Theo B.",  "initials":"TB","text":"Panisse at Marche des Capucins for 2 euros — crispy and fresh. This is the life!",   "specialty":"Panisse","place":"Marche des Capucins","rating":5,"time":"5h ago"},
        {"user":"Lea R.",   "initials":"LR","text":"La Caravelle for apero with port views — magic. Pastis 2 euros, terrace, sunshine.", "specialty":"Pastis","place":"La Caravelle","rating":5,"time":"Yesterday"},
        {"user":"Karim D.", "initials":"KD","text":"Fougasse at Chez Etienne — a true institution. 2.50 euros a slice, can not stop.",   "specialty":"Fougasse","place":"Chez Etienne","rating":5,"time":"Yesterday"},
    ]

# ── Header ────────────────────────────────────────────────────────────────────
logo_src = f"data:image/jpeg;base64,{LOGO_B64}"
st.markdown(f"""
<div class="m-header">
  <img src="{logo_src}" alt="Massilia"/>
  <div style="text-align:right;">
    <div class="m-tagline">PANIS &middot; PASTIS &middot; FOUGASSE</div>
    <div class="m-slogan">Pas fache avec le plaisir !</div>
    <div class="m-sub">Marseille</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Stat bar ──────────────────────────────────────────────────────────────────
n_reviews = len(st.session_state.comments)
st.markdown(f"""
<div class="stat-row">
  <div class="stat-chip">Pastis <span class="chip-val">from 1.50 euros</span></div>
  <div class="stat-chip">Panisse <span class="chip-val">from 2.00 euros</span></div>
  <div class="stat-chip">Spots <span class="chip-val">{len(SPOTS)} verified</span></div>
  <div class="stat-chip">Reviews <span class="chip-val">{n_reviews} locals</span></div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  Map & Spots  ", "  Community  ", "  Deals  "])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — MAP + PREFS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    prefs = st.session_state.prefs

    # Filter
    filtered = [s for s in SPOTS if s["price"] <= prefs["budget"]]
    if prefs["neighbourhood"] != "All":
        filtered = [s for s in filtered if s["neighbourhood"] == prefs["neighbourhood"]]
    if prefs["specialties"]:
        filtered = [s for s in filtered if s["specialty"] in prefs["specialties"]]
    if prefs["moods"]:
        filtered = [s for s in filtered if any(md in s["mood"] for md in prefs["moods"])]

    col_map, col_right = st.columns([3, 2])

    # ── Right column: prefs + spot list ───────────────────────────────────────
    with col_right:

        # Prefs panel
        st.markdown('<div class="pref-panel">', unsafe_allow_html=True)
        st.markdown('<div class="s-title">My Preferences</div>', unsafe_allow_html=True)

        with st.form("pref_form", clear_on_submit=False):
            name = st.text_input("Your name", value=prefs.get("name",""), placeholder="e.g. Sophie")
            neighbourhood = st.selectbox(
                "Neighbourhood",
                NEIGHBOURHOODS,
                index=NEIGHBOURHOODS.index(prefs.get("neighbourhood","All"))
            )
            budget = st.slider("Max budget (euros)", 1.0, 10.0, prefs.get("budget",5.0), 0.5)

            st.markdown("**Mood**")
            mood_cols = st.columns(2)
            sel_moods = []
            for i, mood in enumerate(MOODS):
                with mood_cols[i % 2]:
                    if st.checkbox(mood, value=(mood in prefs.get("moods",[])), key=f"m_{mood}"):
                        sel_moods.append(mood)

            st.markdown("**Specialities**")
            spec_cols = st.columns(2)
            sel_specs = []
            for i, spec in enumerate(SPECIALTIES):
                with spec_cols[i % 2]:
                    if st.checkbox(spec, value=(spec in prefs.get("specialties",[])), key=f"s_{spec}"):
                        sel_specs.append(spec)

            if st.form_submit_button("Find my spots", use_container_width=True):
                st.session_state.prefs = {
                    "name": name, "budget": budget,
                    "neighbourhood": neighbourhood,
                    "moods": sel_moods, "specialties": sel_specs,
                }
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

        # Spot list
        st.markdown(f'<div class="s-title">{len(filtered)} Spots Found</div>', unsafe_allow_html=True)

        if not filtered:
            st.markdown(
                '<div class="empty-state">No spots match your filters.<br>'
                '<span style="font-weight:400;font-size:0.85rem;">Try a higher budget or fewer filters.</span></div>',
                unsafe_allow_html=True
            )
        else:
            for spot in sorted(filtered, key=lambda x: x["price"]):
                tags = "".join([
                    f'<span class="s-tag">{spot["specialty"]}</span>',
                    f'<span class="s-tag">{spot["neighbourhood"]}</span>',
                    f'<span class="s-tag">Rating: {spot["rating"]}</span>',
                ] + [f'<span class="s-tag">{md}</span>' for md in spot["mood"]])
                st.markdown(
                    f'<div class="spot-card">'
                    f'  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">'
                    f'    <div class="spot-name">{spot["name"]}</div>'
                    f'    <div class="price-badge">{spot["price"]} eur</div>'
                    f'  </div>'
                    f'  <div class="spot-desc">{spot["desc"]}</div>'
                    f'  <div>{tags}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ── Left column: map ──────────────────────────────────────────────────────
    with col_map:
        if prefs.get("name"):
            pills = [f"Max {prefs['budget']:.1f} eur"]
            pills += prefs.get("moods",[])[:2]
            pills += prefs.get("specialties",[])[:2]
            pills_html = " ".join(f'<span class="pref-pill">{p}</span>' for p in pills)
            st.markdown(
                f'<div class="w-banner">Hey {prefs["name"]}! Your spots: {pills_html}</div>',
                unsafe_allow_html=True
            )

        m = folium.Map(location=[43.2965, 5.3698], zoom_start=14, tiles="CartoDB Positron")
        for spot in SPOTS:
            is_match = spot in filtered
            color = PRICE_COLORS.get(spot["price"], "#29B6F6") if is_match else "#CCCCCC"
            popup_html = (
                "<div style='font-family:sans-serif;padding:8px;min-width:190px;'>"
                f"<b style='color:#0277BD;font-size:1rem;'>{spot['name']}</b><br/>"
                f"<span style='font-size:1.3rem;font-weight:900;color:#F5A623;'>{spot['price']} eur</span><br/>"
                f"<span style='background:#E1F5FE;border-radius:10px;padding:2px 8px;"
                f"font-size:0.75rem;font-weight:700;color:#0277BD;'>{spot['specialty']}</span><br/>"
                f"<span style='font-size:0.78rem;color:#555;'>{spot['desc']}</span><br/>"
                f"<span style='font-size:0.8rem;'>Rating {spot['rating']} &nbsp; {spot['neighbourhood']}</span>"
                "</div>"
            )
            folium.CircleMarker(
                location=[spot["lat"], spot["lon"]],
                radius=20 if is_match else 10,
                color=color, fill=True, fill_color=color,
                fill_opacity=0.9 if is_match else 0.3,
                popup=folium.Popup(popup_html, max_width=230),
                tooltip=f"{'OK ' if is_match else ''}{spot['name']} — {spot['price']} eur",
            ).add_to(m)
            if is_match:
                folium.Marker(
                    location=[spot["lat"], spot["lon"]],
                    icon=folium.DivIcon(
                        html=(
                            f"<div style='font-family:sans-serif;background:white;"
                            f"border:2.5px solid {color};border-radius:20px;"
                            f"padding:2px 8px;font-size:0.72rem;font-weight:900;"
                            f"color:{color};white-space:nowrap;"
                            f"box-shadow:0 3px 10px rgba(0,0,0,0.18);'>"
                            f"{spot['price']} eur</div>"
                        ),
                        icon_size=(64, 22), icon_anchor=(32, 11),
                    ),
                ).add_to(m)
        st_folium(m, width=None, height=620, returned_objects=[])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — COMMUNITY
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="s-title">The Massilia Community</div>', unsafe_allow_html=True)
    col_form, col_feed = st.columns([2, 3])

    with col_form:
        st.markdown('<div class="pref-panel">', unsafe_allow_html=True)
        st.markdown('<div class="s-title">Share your experience</div>', unsafe_allow_html=True)
        with st.form("comm_form", clear_on_submit=True):
            c_name   = st.text_input("Your name", placeholder="Sophie")
            c_place  = st.selectbox("Where were you?", [s["name"] for s in SPOTS])
            c_spec   = st.selectbox("Speciality", SPECIALTIES)
            c_rating = st.select_slider("Your rating", options=[1,2,3,4,5], value=5)
            c_text   = st.text_area("Your review", placeholder="Best pastis in Marseille!", max_chars=200)
            c_photo  = st.file_uploader("Add a photo (optional)", type=["jpg","jpeg","png"])
            if st.form_submit_button("Post my review", use_container_width=True):
                if c_name.strip() and c_text.strip():
                    initials = "".join([p[0].upper() for p in c_name.strip().split()[:2]])
                    new_c = {
                        "user": c_name.strip(), "initials": initials,
                        "text": c_text.strip(), "specialty": c_spec,
                        "place": c_place, "rating": c_rating, "time": "Just now",
                    }
                    if c_photo:
                        new_c["photo_b64"]  = base64.b64encode(c_photo.read()).decode()
                        new_c["photo_type"] = c_photo.type
                    st.session_state.comments.insert(0, new_c)
                    st.markdown('<div class="ok-box">Thank you for sharing!</div>', unsafe_allow_html=True)
                else:
                    st.error("Name and review are required.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_feed:
        n = len(st.session_state.comments)
        st.markdown(
            f'<p style="color:#888;font-weight:700;margin-bottom:14px;">'
            f'{n} review{"s" if n != 1 else ""} from locals</p>',
            unsafe_allow_html=True
        )
        for c in st.session_state.comments:
            rating_val = c.get("rating", 5)
            star_str = ("★" * rating_val) + ("☆" * (5 - rating_val))
            photo_block = ""
            if c.get("photo_b64"):
                photo_block = (
                    f'<img src="data:{c["photo_type"]};base64,{c["photo_b64"]}" '
                    f'style="width:100%;border-radius:14px;margin:10px 0;max-height:200px;'
                    f'object-fit:cover;display:block;"/>'
                )
            parts = [
                '<div class="comm-card">',
                '  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">',
                f'    <div class="c-avatar">{c["initials"]}</div>',
                '    <div style="flex:1;">',
                f'      <div style="font-weight:800;color:#0277BD;font-size:0.95rem;">{c["user"]}</div>',
                f'      <div style="font-size:0.7rem;color:#aaa;">{c["time"]} &nbsp;&middot;&nbsp; {c["place"]}</div>',
                '    </div>',
                f'    <div style="color:#F5A623;font-size:0.9rem;letter-spacing:1px;">{star_str}</div>',
                '  </div>',
                photo_block,
                f'  <div style="font-size:0.87rem;color:#333;line-height:1.6;margin-bottom:10px;">{c["text"]}</div>',
                f'  <span class="s-tag">{c.get("specialty","")}</span>',
                '</div>',
            ]
            st.markdown("\n".join(parts), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DEALS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="s-title">Exclusive Deals</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#666;font-weight:600;margin-bottom:22px;">'
        'Special offers for the Massilia community — just for students and young locals!</p>',
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)
    for i, promo in enumerate(PROMOS):
        col = col_a if i % 2 == 0 else col_b
        with col:
            parts = [
                '<div class="promo-card">',
                f'  <div class="promo-num">{promo["discount"]}</div>',
                f'  <div class="promo-place">{promo["place"]}</div>',
                f'  <div class="promo-desc">{promo["desc"]}</div>',
                '  <div class="promo-code-box">',
                '    <span style="font-size:0.72rem;opacity:0.82;color:white;">Promo code</span>',
                f'    <span class="promo-code">{promo["code"]}</span>',
                '  </div>',
                '</div>',
            ]
            st.markdown("\n".join(parts), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="s-title" style="font-size:1.1rem;">How to get more deals?</div>', unsafe_allow_html=True)
    tips = [
        ("Show your student card",      "Valid at all Massilia partner spots"),
        ("Share a photo in the community","Earn points and unlock exclusive promos"),
        ("Come back regularly",          "Loyal regulars get weekly special offers"),
        ("Invite your friends",          "Refer a friend and get a free pastis"),
    ]
    icons = ["Diploma", "Camera", "Refresh", "People"]
    icon_chars = ["🎓", "📸", "🔁", "👥"]
    for (title, desc), icon in zip(tips, icon_chars):
        st.markdown(
            f'<div class="tip-row">'
            f'  <div class="tip-icon">{icon}</div>'
            f'  <div>'
            f'    <div class="tip-title">{title}</div>'
            f'    <div class="tip-desc">{desc}</div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;padding:32px 0 16px;">
  <img src="data:image/jpeg;base64,{LOGO_B64}"
       style="height:60px;opacity:0.5;display:inline-block;" alt="Massilia"/>
  <div style="color:#bbb;font-size:0.7rem;font-weight:700;
              margin-top:10px;letter-spacing:0.12em;">
    PANIS &middot; PASTIS &middot; FOUGASSE &middot; MARSEILLE
  </div>
</div>
""", unsafe_allow_html=True)
