# ═══════════════════════════════════════════════════════════════════════════
#  NeuroGlueAI v6.0 — Sharp Cinematic Dashboard
#  TEKNOFEST 2026 | Sağlık & AI
#
#  Bağımlılıklar:
#    streamlit, pandas, numpy, plotly
#    streamlit-extras, streamlit-option-menu, py3Dmol
# ═══════════════════════════════════════════════════════════════════════════

import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

# 3D molekül
try:
    import py3Dmol
    from streamlit.components.v1 import html as st_html
    HAS_3D = True
except ImportError:
    HAS_3D = False

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA KONFİGÜRASYONU
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NeuroGlueAI — Molecular Glue Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════
# KESKİN DARK THEME — Blur YOK, Net Renkler
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ═══ ANA ARKA PLAN — Keskin solid ═══ */
.stApp {
    background: #050810;
    color: #E8F1F8;
}

html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ═══ ANA BAŞLIK ═══ */
.main-title {
    font-size: 4rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00E5FF 0%, #7C4DFF 50%, #FF4081 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    letter-spacing: -2px;
    text-align: center;
    margin-bottom: 0.3rem;
}

.subtitle {
    font-size: 1.25rem;
    color: #00E5FF;
    text-align: center;
    font-style: italic;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.3rem;
    font-weight: 600;
}

/* ═══ HERO CARD ═══ */
.hero-card {
    background: #0A1024;
    padding: 2.2rem 2.5rem;
    border-radius: 16px;
    border: 1px solid #00E5FF;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.25);
    text-align: center;
    margin: 1.5rem 0;
}

/* ═══ KPI KARTLARI ═══ */
.kpi-neon {
    background: #0A1024;
    padding: 1.4rem 1.5rem;
    border-radius: 12px;
    border: 1px solid #00E5FF;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.15);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-neon::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: #00E5FF;
}
.kpi-neon:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 35px rgba(0, 229, 255, 0.5);
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 900;
    line-height: 1;
    background: linear-gradient(135deg, #00E5FF, #FF4081);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}
.kpi-label {
    font-size: 0.78rem;
    color: #00E5FF;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.6rem;
    font-weight: 700;
}
.kpi-sub {
    font-size: 0.72rem;
    color: #8899AA;
    margin-top: 0.3rem;
}

/* ═══ BÖLÜM BAŞLIKLARI ═══ */
.section-neon {
    font-size: 1.5rem;
    font-weight: 800;
    color: #FFFFFF;
    padding: 0.7rem 0 0.7rem 1.2rem;
    margin: 1.8rem 0 1rem 0;
    border-left: 4px solid #00E5FF;
    background: #0A1024;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

/* ═══ INFO KUTULARI ═══ */
.info-glass {
    padding: 1.2rem 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    background: #0A1024;
    border-left: 4px solid #00E5FF;
    color: #E8F1F8;
    line-height: 1.7;
}
.info-glass.s { border-left-color: #27AE60; color: #B8E6C9; }
.info-glass.w { border-left-color: #F39C12; color: #FCE4B6; }
.info-glass.d { border-left-color: #FF4081; color: #FFB3C6; }
.info-glass.i { border-left-color: #00E5FF; color: #B3E5FC; }

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: #050810;
    border-right: 1px solid #00E5FF;
}
[data-testid="stSidebar"] * { color: #E8F1F8 !important; }
[data-testid="stSidebar"] hr {
    border-color: rgba(0, 229, 255, 0.3);
}

/* ═══ METRIC ═══ */
[data-testid="stMetricValue"] {
    color: #00E5FF !important;
    font-weight: 900 !important;
}
[data-testid="stMetricLabel"] {
    color: #7CB9E8 !important;
}

/* ═══ BUTONLAR ═══ */
.stButton > button {
    background: #00E5FF;
    color: #050810 !important;
    border: none;
    font-weight: 700;
    padding: 0.6rem 1.5rem;
    border-radius: 8px;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #FF4081;
    color: #FFFFFF !important;
    box-shadow: 0 0 20px rgba(255, 64, 129, 0.6);
}

/* ═══ PROGRESS BAR ═══ */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00E5FF, #FF4081);
}

/* ═══ TABS ═══ */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: #0A1024;
    border-radius: 8px;
    color: #00E5FF !important;
    padding: 0.5rem 1rem;
    font-weight: 600;
    border: 1px solid rgba(0, 229, 255, 0.3);
}
.stTabs [aria-selected="true"] {
    background: #00E5FF !important;
    color: #050810 !important;
    box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
}

/* ═══ DATAFRAME ═══ */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 8px;
}

/* ═══ CODE BLOCK ═══ */
.stCodeBlock, pre, code {
    background: #0A1024 !important;
    border: 1px solid rgba(0, 229, 255, 0.3);
    color: #00E5FF !important;
}

/* ═══ EXPANDER ═══ */
.streamlit-expanderHeader {
    background: #0A1024 !important;
    color: #E8F1F8 !important;
    border-radius: 8px;
    border: 1px solid rgba(0, 229, 255, 0.3);
}

/* ═══ HEADINGS ═══ */
h1, h2, h3, h4, h5, h6 { color: #E8F1F8 !important; }

/* ═══ PULSE ANIMASYONU (minimal) ═══ */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.pulse-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #27AE60;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s ease-in-out infinite;
}

/* ═══ SCROLLBAR ═══ */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #050810; }
::-webkit-scrollbar-thumb {
    background: #00E5FF;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover { background: #FF4081; }

/* ═══ BLUR KALDIRILDI ═══ */
/* Hiçbir backdrop-filter, blur, animated gradient yok */
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════════════
HOME = Path.home()
PROJECT = HOME / "NeuroGlue_Project"
PLATFORM = HOME / "NeuroGlueAI_Platform"

P = {
    # ═══ REPO İÇİ (Streamlit Cloud + Yerel uyumlu) ═══
    "pfig": PLATFORM / "assets" / "figures",
    "pdata": PLATFORM / "data",
    
    # Beyin
    "brain_anim": PLATFORM / "assets" / "figures" / "brain_animated.svg",
    "brain_static": PLATFORM / "assets" / "figures" / "brain_animated.svg",
    
    # 3D molekül
    "d049_sdf": PLATFORM / "assets" / "d049" / "d049_3D.sdf",
    "d049_pdb": PLATFORM / "assets" / "d049" / "d049_3D.pdb",
    
    # Üçlü kompleks
    "ternary_dodger": PLATFORM / "assets" / "figures" / "ternary_20260927_030510.png",
    "ternary_dodger_alt": PLATFORM / "assets" / "figures" / "ternary_20260927_030510.png",
    "ternary_old": PLATFORM / "assets" / "figures" / "ternary_20260927_030510.png",
    
    # Video
    "video": PLATFORM / "assets" / "videos" / "md_real_loop.mp4",
    "video_alt": PLATFORM / "assets" / "videos" / "md_100ns_30fps.mp4",
    "video_preview": PLATFORM / "assets" / "videos" / "md_preview.gif",
    
    # Poster görselleri
    "steric_wide": PLATFORM / "assets" / "poster" / "01_structure" / "01_steric_wide.png",
    "steric_interface": PLATFORM / "assets" / "poster" / "01_structure" / "03_steric_interface.png",
    "docking_compare": PLATFORM / "assets" / "poster" / "02_docking" / "crbn_pocket_comparison.png",
    "orca": PLATFORM / "assets" / "poster" / "03_quantum" / "orca_dft_full_analysis.png",
    "md_panel": PLATFORM / "assets" / "poster" / "04_md" / "md_production_5panel.png",
    "mmgbsa": PLATFORM / "assets" / "poster" / "04_md" / "mmgbsa_250frame_analysis.png",
    "d049_2d": PLATFORM / "assets" / "poster" / "05_summary" / "d049_2D.png",
    "kbb_radar": PLATFORM / "assets" / "poster" / "05_summary" / "kbb_radar.png",
    "roadmap": PLATFORM / "assets" / "poster" / "05_summary" / "roadmap_4step.png",
    "platform_exp": PLATFORM / "assets" / "poster" / "05_summary" / "platform_expansion.png",
    
    # Yaygın etki (varsa)
    "impact_clinical": PLATFORM / "assets" / "poster" / "05_summary" / "01_klinik_etki.png",
    "impact_economic": PLATFORM / "assets" / "poster" / "05_summary" / "02_ekonomik_etki.png",
    "impact_platform": PLATFORM / "assets" / "poster" / "05_summary" / "03_platform_vizyon_v2.png",
}

# ═══════════════════════════════════════════════════════════════════════════
# VERİ SABİTLERİ
# ═══════════════════════════════════════════════════════════════════════════
D049 = {
    "MW": 356.30, "TPSA": 73.32, "cLogP": 2.23, "CNS_MPO": 5.8,
    "SA": 3.09, "HBD": 2, "HBA": 5, "Formula": "C16H15F3N2O4",
    "SMILES": "Cc1cn([C@H]2C[C@@H](COc3ccc(C(F)(F)F)cc3)O2)c(=O)[nH]c1=O",
    "steps": 4, "yield": 52.1,
}

M = {
    "vina": -8.67, "iptm": 0.947, "plddt": 92.3,
    "haddock": -117.86, "contact": 100.0,
    "dG": -21.54, "dG_std": 7.67, "orca": -1327.018,
}

# ═══════════════════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════════════════════
def kpi(label, value, sub="", color="#00E5FF"):
    st.markdown(f"""
    <div class="kpi-neon">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def info(text, kind="i"):
    st.markdown(f'<div class="info-glass {kind}">{text}</div>', unsafe_allow_html=True)

def section(title, icon="◆"):
    st.markdown(f'<div class="section-neon">{icon}  {title}</div>', unsafe_allow_html=True)

def style_fig(fig, title="", h=450):
    fig.update_layout(
        title=dict(text=title, font=dict(size=17, color="#E8F1F8")),
        height=h,
        paper_bgcolor="#050810",
        plot_bgcolor="#0A1024",
        font=dict(size=12, color="#B3E5FC"),
        margin=dict(l=60, r=40, t=70, b=60),
        xaxis=dict(gridcolor="rgba(0,229,255,0.15)", zerolinecolor="rgba(0,229,255,0.3)"),
        yaxis=dict(gridcolor="rgba(0,229,255,0.15)", zerolinecolor="rgba(0,229,255,0.3)"),
        hoverlabel=dict(bgcolor="#0A1024", font=dict(color="#E8F1F8")),
    )
    return fig

def show_img(path_key, caption="", use_container=True):
    """Güvenli görsel göster."""
    p = P.get(path_key)
    if p and p.exists():
        st.image(str(p), caption=caption, use_container_width=use_container)
        return True
    return False

def show_3d(animate=True):
    """py3Dmol ile interaktif 3D molekül (auto-spin)"""
    if not HAS_3D:
        info("⚠️ py3Dmol yüklü değil. `pip install py3Dmol`", "w")
        return
    f = P["d049_sdf"] if P["d049_sdf"].exists() else P["d049_pdb"]
    if not f.exists():
        info("⚠️ D-049 3D dosyası bulunamadı.", "w")
        return
    try:
        data = open(f).read()
        fmt = "sdf" if f.suffix == ".sdf" else "pdb"
        view = py3Dmol.view(width=900, height=550)
        view.addModel(data, fmt)
        view.setStyle({
            "stick": {"radius": 0.15, "colorscheme": "cyanCarbon"},
            "sphere": {"scale": 0.25}
        })
        view.setBackgroundColor("#050810")
        if animate:
            view.spin("y", 0.5)
        view.zoomTo()
        view.zoom(1.1)
        st_html(view._make_html(), height=560, scrolling=False)
    except Exception as e:
        info(f"⚠️ 3D hatası: {e}", "w")

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.2rem 0;'>
        <div style='font-size: 3rem;'>🧬</div>
        <h1 style='background: linear-gradient(135deg, #00E5FF, #FF4081);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 1.5rem; margin: 0.4rem 0; font-weight: 900;
                   letter-spacing: 1px;'>NeuroGlueAI</h1>
        <p style='color: #00E5FF; font-size: 0.7rem; letter-spacing: 3px;
                  text-transform: uppercase; font-weight: 600;'>
            Molecular Glue
        </p>
        <p style='color: #7C4DFF; background: #0A1024;
                  padding: 0.2rem 0.6rem; border-radius: 4px;
                  display: inline-block; font-size: 0.65rem;
                  border: 1px solid #7C4DFF; margin-top: 0.4rem;'>
            v6.0 • SHARP
        </p>
    </div>
    """, unsafe_allow_html=True)

    page = option_menu(
        menu_title=None,
        options=[
            "Ana Sayfa", "Problem", "D-049", "AI Pipeline", "Yapısal",
            "MD Simülasyonu", "ORCA Kuantum", "CRISPR", "Sterik Takoz",
            "Klinik & Ekonomik", "Platform", "Yol Haritası"
        ],
        icons=[
            "house", "bullseye", "capsule", "cpu", "diagram-3",
            "activity", "atom", "dna", "exclamation-triangle",
            "currency-dollar", "rocket-takeoff", "map"
        ],
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#00E5FF", "font-size": "16px"},
            "nav-link": {
                "font-size": "13px", "text-align": "left",
                "margin": "3px 0", "border-radius": "8px",
                "color": "#B3E5FC", "background-color": "transparent",
                "font-weight": "600",
                "--hover-color": "#0A1024",
            },
            "nav-link-selected": {
                "background": "#00E5FF",
                "color": "#050810",
                "font-weight": "800",
            },
        }
    )
    st.markdown("---")
    st.markdown("""
    <div style='background: #0A1024; padding: 1rem; border-radius: 10px;
                font-size: 0.75rem; border: 1px solid #00E5FF;'>
        <p style='margin: 0; color: #27AE60; font-weight: 600;'>
            <span class="pulse-dot"></span>İn silico ✓
        </p>
        <p style='margin: 0.5rem 0 0 0; color: #F39C12; font-weight: 600;'>● THS 4 hazır</p>
        <p style='margin: 0.5rem 0 0 0; color: #00E5FF; font-weight: 600;'>● 500+ veri</p>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: ANA SAYFA
# ═══════════════════════════════════════════════════════════════════════════
if page == "Ana Sayfa":
    st.markdown('<h1 class="main-title">NeuroGlueAI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">✦ AI-Destekli Moleküler Tutkal Platformu ✦</p>',
                unsafe_allow_html=True)

    # Beyin SVG
    c1, c2, c3 = st.columns([1.5, 1.2, 1.5])
    with c2:
        brain_key = "brain_anim" if P["brain_anim"].exists() else "brain_static"
        show_img(brain_key)

    # Hero
    st.markdown("""
    <div class="hero-card">
        <h2 style='color: #00E5FF; margin: 0 0 1rem 0; font-size: 1.5rem;
                   letter-spacing: 1px;'>
            IDH1-R132H Glioblastoma — Hedeflenmiş Protein Yıkımı
        </h2>
        <p style='color: #E8F1F8; font-size: 1rem; max-width: 850px;
                  margin: 0 auto; line-height: 1.8;'>
            KBB-geçirgen, linker içermeyen
            <b style='color:#00E5FF;'>monovalent moleküler tutkal D-049</b>'un
            uçtan uca <b style='color:#FF4081;'>yapay zeka destekli</b> tasarımı ve
            <b style='color:#FFB74D;'>THS 4 (wet-lab) hazırlığı</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI
    section("Anahtar Metrikler", "◈")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi("Boltz-2 ipTM", f"{M['iptm']:.3f}", "Yüksek güven")
    with c2: kpi("MM/GBSA ΔG", f"{M['dG']}", "kcal/mol")
    with c3: kpi("Vina Afinitesi", f"{M['vina']}", "kcal/mol")
    with c4: kpi("MD Temas", f"{M['contact']:.0f}%", "500/500")
    with c5: kpi("Molekül Ağırlığı", f"{D049['MW']:.1f}", "Da")

    # MD Video
    section("100 ns MD Simülasyonu", "▶")
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        vfound = False
        for vk in ["video", "video_alt"]:
            if P[vk].exists():
                st.video(str(P[vk]), autoplay=True, loop=True, muted=True)
                st.caption("🎬 100 ns production MD • 500 frame")
                vfound = True
                break
        if not vfound and P["video_preview"].exists():
            st.image(str(P["video_preview"]), use_container_width=True)
            vfound = True
        if not vfound:
            info("📽️ MD videosu hazırlanıyor.", "i")

    # 3D molekül
    section("D-049 İnteraktif 3D Yapı", "⬢")
    info("🖱️ <b>Sol tık + sürükle</b> = Döndür • <b>Tekerlek</b> = Zoom • Otomatik salınım aktif", "i")
    show_3d(animate=True)

    # Gauges
    section("Çok Katmanlı Kanıt Özeti", "▲")
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Vina ΔG", "Boltz-2 ipTM", "MM/GBSA |ΔG|"),
        specs=[[{"type": "indicator"}] * 3]
    )
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=abs(M['vina']),
        number={"font": {"color": "#00E5FF", "size": 44}},
        gauge={"axis": {"range": [0, 12], "tickcolor": "#00E5FF"},
               "bar": {"color": "#00E5FF"},
               "bgcolor": "#0A1024"}), row=1, col=1)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=M['iptm'],
        number={"valueformat": ".3f", "font": {"color": "#27AE60", "size": 44}},
        gauge={"axis": {"range": [0, 1], "tickcolor": "#27AE60"},
               "bar": {"color": "#27AE60"},
               "bgcolor": "#0A1024"}), row=1, col=2)
    fig.add_trace(go.Indicator(
        mode="gauge+number", value=abs(M['dG']),
        number={"font": {"color": "#FF4081", "size": 44}},
        gauge={"axis": {"range": [0, 40], "tickcolor": "#FF4081"},
               "bar": {"color": "#FF4081"},
               "bgcolor": "#0A1024"}), row=1, col=3)
    fig.update_layout(
        height=320,
        paper_bgcolor="#050810",
        font=dict(color="#B3E5FC"),
        margin=dict(l=20, r=20, t=80, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Üçlü kompleks — YENİ RENDER
    section("Üçlü Kompleks Render", "◉")
    c1, c2, c3 = st.columns([1, 2.5, 1])
    with c2:
        # Cache buster: dosya modifikasyon zamanını kullan
        render_path = Path(str(PROJECT) + "//STREAMLIT_RENDER/DODGER_FINAL.png")
        if not render_path.exists():
            render_path = P["ternary_dodger"] if P.get("ternary_dodger") and P["ternary_dodger"].exists() else Path(__file__).parent.parent / "assets" / "figures" / "ternary_20260927_030510.png"
        
        if render_path.exists():
            # Dosya boyutunu ve mtime'ı cache buster olarak kullan
            mtime = render_path.stat().st_mtime
            size = render_path.stat().st_size
            st.image(
                str(render_path),
                caption=f"mIDH1 (dodgerblue) • CRBN (deeppink) • D-049 (sarı) • {size//1024}KB",
                use_container_width=True,
                key=f"ternary_{mtime}_{size}"  # ← Cache buster
            )
        else:
            info(f"⚠️ Render bulunamadı: {render_path}", "w")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: PROBLEM
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Problem":
    section("Problem & Pazar Analizi", "◈")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        info("""<table style='width:100%; line-height:2.2;'>
            <tr><td><b>Hastalık</b></td><td>Glioblastoma Multiforme</td></tr>
            <tr><td><b>Alt tip</b></td><td>IDH1-R132H mutant, WHO Grade 4</td></tr>
            <tr><td><b>5-yıllık sağkalım</b></td><td style='color:#FF4081;'><b>%3,4</b></td></tr>
            <tr><td><b>Direnç</b></td><td>Adaptif: pSTAT3-Y705</td></tr>
            <tr><td><b>Bariyer</b></td><td>Kan-Beyin Bariyeri (KBB)</td></tr>
            <tr><td><b>PROTAC limiti</b></td><td>&gt; 800 Da → KBB geçemez</td></tr>
        </table>""", "d")
    with c2:
        fig = go.Figure(go.Bar(
            x=["Standart", "Direnç Sonrası", "NeuroGlueAI"],
            y=[3.4, 1.5, 12.5],
            marker_color=["#5A7A9A", "#FF4081", "#27AE60"],
            text=["%3,4", "%1,5", "%12,5"],
            textposition="outside",
            textfont=dict(size=16, color="#E8F1F8"),
            width=0.55,
        ))
        fig = style_fig(fig, "5-Yıllık Sağkalım", 350)
        fig.update_yaxes(range=[0, 15])
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: D-049
# ═══════════════════════════════════════════════════════════════════════════
elif page == "D-049":
    section("D-049 — Lider Aday Molekül", "◈")
    c1, c2 = st.columns([1, 1.3])
    with c1:
        info(f"""
        <h4 style='color: #00E5FF; margin-top: 0;'>🧪 Moleküler Kimlik</h4>
        <table style='width: 100%; line-height: 2.1;'>
            <tr><td><b>MW</b></td><td><b style='color:#00E5FF;'>{D049['MW']} Da</b></td></tr>
            <tr><td><b>Formula</b></td><td>{D049['Formula']}</td></tr>
            <tr><td><b>TPSA</b></td><td>{D049['TPSA']} Å²</td></tr>
            <tr><td><b>cLogP</b></td><td>{D049['cLogP']}</td></tr>
            <tr><td><b>CNS MPO</b></td><td><b style='color:#FF4081;'>{D049['CNS_MPO']}</b> / 6</td></tr>
            <tr><td><b>HBD/HBA</b></td><td>{D049['HBD']} / {D049['HBA']}</td></tr>
            <tr><td><b>SA Score</b></td><td>{D049['SA']} (4 adım)</td></tr>
            <tr><td><b>Verim</b></td><td>%{D049['yield']}</td></tr>
        </table>
        """, "i")
    with c2:
        cats = ['MW', 'TPSA', 'cLogP', 'HBD', 'HBA', 'CNS MPO']
        vals = [
            1 - (D049['MW'] / 500),
            1 - (D049['TPSA'] / 120),
            1 - abs(D049['cLogP'] - 2.0) / 3.0,
            0.85, 0.75,
            D049['CNS_MPO'] / 6
        ]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]], theta=cats + [cats[0]],
            fill='toself', fillcolor='rgba(0,229,255,0.2)',
            line=dict(color='#00E5FF', width=3)
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="#0A1024",
                radialaxis=dict(range=[0, 1], gridcolor="rgba(0,229,255,0.2)",
                                tickfont=dict(color="#B3E5FC")),
                angularaxis=dict(gridcolor="rgba(0,229,255,0.2)",
                                 tickfont=dict(color="#B3E5FC"))
            ),
            height=400, paper_bgcolor="#050810", showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    section("İnteraktif 3D Yapı", "⬢")
    show_3d(animate=True)

    section("2D Kimyasal Yapı", "◉")
    show_img("d049_2d", "D-049 kimyasal yapısı")

    section("SMILES", "◈")
    st.code(D049['SMILES'], language="text")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: AI PIPELINE
# ═══════════════════════════════════════════════════════════════════════════
elif page == "AI Pipeline":
    section("AI Pipeline — De Novo Tasarım", "◈")
    c1, c2 = st.columns(2)
    with c1:
        f = P["pfig"] / "filtreleme_funnel.png"
        if f.exists():
            st.image(str(f), caption="Filtreleme Funnel", use_container_width=True)
    with c2:
        f = P["pfig"] / "chemberta_CV.png"
        if f.exists():
            st.image(str(f), caption="ChemBERTa 5-Fold CV", use_container_width=True)
    c3, c4 = st.columns(2)
    with c3:
        f = P["pfig"] / "reinvent4_egitim.png"
        if f.exists():
            st.image(str(f), caption="REINVENT 4 Eğitim", use_container_width=True)
    with c4:
        f = P["pfig"] / "retroscore_sentez.png"
        if f.exists():
            st.image(str(f), caption="RetroScore Sentez", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: YAPISAL
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Yapısal":
    section("Yapısal Analizler", "◈")
    c1, c2, c3 = st.columns(3)
    with c1: kpi("Boltz-2 ipTM", f"{M['iptm']:.3f}", "Yüksek güven")
    with c2: kpi("Vina ΔG", f"{M['vina']}", "kcal/mol")
    with c3: kpi("HADDOCK", f"{M['haddock']}", "a.u. (best-4)")

    section("Yapısal Görseller", "🖼️")
    c1, c2 = st.columns(2)
    with c1:
        show_img("steric_interface", "Arayüz detayı")
    with c2:
        show_img("docking_compare", "Klasik vs yeni cep")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: MD
# ═══════════════════════════════════════════════════════════════════════════
elif page == "MD Simülasyonu":
    section("Moleküler Dinamik Simülasyonu", "▶")
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi("Simülasyon", "100 ns", "Production")
    with c2: kpi("Temas", "100%", "500/500")
    with c3: kpi("Ligand RMSD", "1.37 Å", "Ortalama")
    with c4: kpi("MM/GBSA", f"{M['dG']}", "kcal/mol")

    section("Sinematik MD Videosu", "▶")
    c1, c2, c3 = st.columns([1, 3, 1])
    with c2:
        vfound = False
        for vk in ["video", "video_alt"]:
            if P[vk].exists():
                st.video(str(P[vk]), autoplay=True, loop=True, muted=True)
                vfound = True
                break
        if not vfound:
            info("Video hazırlanıyor.", "i")

    section("MD Grafikleri", "🖼️")
    c1, c2 = st.columns(2)
    with c1:
        show_img("md_panel", "MD Production 5-panel")
    with c2:
        show_img("mmgbsa", "MM/GBSA 250 frame")

    section("MM/GBSA Enerji Dekompozisyonu", "⚡")
    d = {
        "van der Waals": -39.10,
        "Elektrostatik": -19.02,
        "Polar solvation": 43.97,
        "Nonpolar solvation": -6.40
    }
    fig = go.Figure(go.Bar(
        x=list(d.keys()), y=list(d.values()),
        marker_color=["#00E5FF" if v < 0 else "#FF4081" for v in d.values()],
        text=[f"{v:+.2f}" for v in d.values()],
        textposition="outside",
        textfont=dict(size=13, color="#E8F1F8")
    ))
    fig.add_hline(y=0, line_color="#00E5FF")
    fig = style_fig(fig, "MM/GBSA Enerji Bileşenleri", 400)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: ORCA
# ═══════════════════════════════════════════════════════════════════════════
elif page == "ORCA Kuantum":
    section("ORCA Kuantum (DFT)", "◉")
    c1, c2 = st.columns([1, 1.3])
    with c1:
        info(f"""<table style='width:100%; line-height:2;'>
            <tr><td><b>Yöntem</b></td><td>B3LYP/def2-SVP + D3BJ</td></tr>
            <tr><td><b>Atom Sayısı</b></td><td>43</td></tr>
            <tr><td><b>Final Enerji</b></td><td>{M['orca']:.4f} Ha</td></tr>
            <tr><td><b>Geometri</b></td><td>65 adım</td></tr>
            <tr><td><b>Yakınsama</b></td><td style='color:#27AE60;'>✓ Başarılı</td></tr>
        </table>""", "i")
    with c2:
        it = [1, 2, 3, 4, 5]
        e = [-1326.329, -1326.618, -1326.721, -1326.788, -1326.936]
        fig = go.Figure(go.Scatter(
            x=it, y=e, mode="lines+markers",
            line=dict(color="#00E5FF", width=3),
            marker=dict(size=14, color="#FF4081")
        ))
        fig = style_fig(fig, "SCF Yakınsama Profili", 350)
        st.plotly_chart(fig, use_container_width=True)

    section("ORCA DFT Analizi", "🖼️")
    show_img("orca", "ORCA DFT 3-panel")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: CRISPR
# ═══════════════════════════════════════════════════════════════════════════
elif page == "CRISPR":
    section("CRISPR / DepMap Validasyonu", "◉")
    info("① IDH1 nötr → inhibitör etkisiz &nbsp;&nbsp; ② CRBN nötr → glue güvenli &nbsp;&nbsp; ③ DDB1 essential → glue dokunmaz", "i")

    genes = ["CRBN", "IDH1", "IDH2", "CUL4A", "CUL4B", "KEAP1", "MDM2", "VHL", "RBX1", "DDB1"]
    medians = [0.056, -0.076, 0.005, -0.026, -0.047, 0.038, -0.404, -0.793, -1.362, -1.831]
    cols = [
        "#27AE60" if m > -0.2
        else "#F39C12" if m > -0.5
        else "#FF4081" if m > -1.0
        else "#C0392B"
        for m in medians
    ]
    fig = go.Figure(go.Bar(
        y=genes, x=medians, orientation="h",
        marker_color=cols,
        text=[f"{m:+.3f}" for m in medians],
        textposition="outside",
        textfont=dict(size=11, color="#E8F1F8")
    ))
    fig.add_vline(x=0, line_color="#00E5FF", line_width=1.5)
    fig.add_vline(x=-0.5, line_dash="dash", line_color="#F39C12")
    fig.add_vline(x=-1.0, line_dash="dash", line_color="#C0392B")
    fig = style_fig(fig, "Chronos Gen Etkisi (median, GBM n=50)", 500)
    fig.update_xaxes(range=[-2.2, 0.5])
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1: info("<b>CRBN +0,056</b><br>Nötr adaptör → glue güvenli", "s")
    with c2: info("<b>IDH1 −0,076</b><br>Nötr enzim → inhibitör etkisiz", "s")
    with c3: info("<b>DDB1 −1,831</b><br>Essential scaffold → glue dokunmaz", "d")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: STERİK TAKOZ
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Sterik Takoz":
    section("Sterik Takoz Analizi", "⚠")
    st.markdown("""
    <div class="hero-card">
        <h2 style='color: #FFB74D; margin: 0 0 1rem 0; font-size: 1.5rem;'>
            ⚡ Yüksek Skor ≠ Üretkenlik ⚡
        </h2>
        <p style='color: #E8F1F8; font-size: 1rem; max-width: 700px;
                  margin: 0 auto; line-height: 1.8;'>
            Vina, Boltz-2 ve MM/GBSA yüksek güven gösterir. Ancak apo CRBN-mIDH1
            arayüzü TRP92/LYS217 hattını işgal eder →
            <b style='color: #FF4081;'>kompleks çöker</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        info("<h4 style='color: #27AE60; margin-top:0;'>✓ Yüksek Skorlar</h4>"
             "<table style='width:100%; line-height:2;'>"
             "<tr><td>Vina</td><td align='right'><b>−8,67 kcal/mol</b></td></tr>"
             "<tr><td>Boltz-2 ipTM</td><td align='right'><b>0,947</b></td></tr>"
             "<tr><td>MM/GBSA ΔG</td><td align='right'><b>−21,54 kcal/mol</b></td></tr>"
             "</table>", "s")
    with c2:
        info("<h4 style='color: #FF4081; margin-top:0;'>✗ Gerçek Geometri</h4>"
             "<table style='width:100%; line-height:2;'>"
             "<tr><td>Min mesafe</td><td align='right'><b>&lt; 2,5 Å</b></td></tr>"
             "<tr><td>Çakışma</td><td align='right'><b>8 atom çifti</b></td></tr>"
             "<tr><td>Kompleks</td><td align='right'><b>ÇÖKER</b></td></tr>"
             "</table>", "d")

    section("Sterik Takoz Görselleri", "🖼️")
    show_img("steric_wide", "Sterik takoz — geniş görünüm")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: KLİNİK & EKONOMİK
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Klinik & Ekonomik":
    section("Klinik & Ekonomik Etki", "◈")
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=["Standart", "Direnç", "NeuroGlueAI"],
            y=[3.4, 1.5, 12.5],
            marker_color=["#5A7A9A", "#FF4081", "#27AE60"],
            text=["%3,4", "%1,5", "%12,5"],
            textposition="outside",
            textfont=dict(size=14, color="#E8F1F8"),
            width=0.55
        ))
        fig = style_fig(fig, "5-Yıllık Sağkalım", 350)
        fig.update_yaxes(range=[0, 15])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        c1a, c2a = st.columns(2)
        with c1a: kpi("Zaman", "2×", "18→9 yıl")
        with c2a: kpi("Maliyet", "58×", "$2,6B→$45K")

    section("Yaygın Etki Görselleri", "🖼️")
    c1, c2, c3 = st.columns(3)
    with c1: show_img("impact_clinical", "Klinik")
    with c2: show_img("impact_economic", "Ekonomik")
    with c3: show_img("impact_platform", "Platform")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: PLATFORM
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Platform":
    section("Platform Vizyonu — Ölçeklenebilirlik", "▲")
    st.markdown("""
    <div class="hero-card">
        <h2 style='color: #7C4DFF; margin: 0 0 0.8rem 0; font-size: 1.5rem;'>
            Uçtan Uca Tasarım Altyapısı
        </h2>
        <p style='color: #E8F1F8; font-size: 1rem; max-width: 800px;
                  margin: 0 auto; line-height: 1.8;'>
            KBB-geçirgen mimari; sadece mIDH1 için değil, tüm zorlu nörolojik ve
            onkolojik hedefler için uyarlanabilir evrensel altyapı.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        info("<h4 style='color: #00E5FF;'>🧠 Nörodejeneratif</h4>"
             "<ul><li>Alzheimer</li><li>Parkinson</li><li>ALS</li><li>Huntington</li></ul>", "i")
    with c2:
        info("<h4 style='color: #FF4081;'>🎯 Onkoloji</h4>"
             "<ul><li>KRAS</li><li>p53</li><li>c-Myc</li><li>BRAF</li></ul>", "d")
    with c3:
        info("<h4 style='color: #27AE60;'>🩺 Diğer</h4>"
             "<ul><li>Otoimmün</li><li>Enfeksiyöz</li><li>Nadir</li><li>Kardiyo</li></ul>", "s")

    section("Platform Genişleme Şeması", "🖼️")
    show_img("platform_exp", "Platform genişleme")

# ═══════════════════════════════════════════════════════════════════════════
# SAYFA: YOL HARİTASI
# ═══════════════════════════════════════════════════════════════════════════
elif page == "Yol Haritası":
    section("Yol Haritası — THS 3 → THS 4", "▸")
    for phase, prog in [
        ("İn silico (THS 3)", 100),
        ("Kimyasal Sentez", 20),
        ("In Vitro", 0),
        ("In Vivo", 0)
    ]:
        c1, c2 = st.columns([1, 4])
        with c1:
            st.markdown(f"**{phase}**")
        with c2:
            st.progress(prog / 100)
            if prog > 0:
                st.caption(f"%{prog} tamamlandı")

    section("4 Aşamalı Deneysel Doğrulama", "🧪")
    c1, c2, c3, c4 = st.columns(4)
    steps = [
        ("1. SENTEZ", "4 adım, %52,1 verim", "#3498DB"),
        ("2. SPR/TR-FRET", "Bağlanma kinetiği", "#9B59B6"),
        ("3. WESTERN BLOT", "Hücresel degradasyon", "#FF4081"),
        ("4. FAREDE", "Ortotopik in vivo", "#27AE60")
    ]
    for col, (t, d, color) in zip([c1, c2, c3, c4], steps):
        with col:
            st.markdown(f"""
            <div style='text-align:center; padding:1.2rem;
                        background:#0A1024; border-radius:10px;
                        border-top:4px solid {color};'>
                <h4 style='color:{color}; margin:0;'>{t}</h4>
                <p style='font-size:0.85rem; color:#B3E5FC;
                          margin:0.5rem 0 0 0;'>{d}</p>
            </div>
            """, unsafe_allow_html=True)

    section("Yol Haritası Görseli", "🖼️")
    show_img("roadmap", "4 Aşamalı Yol Haritası")

# ═══════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1.5rem 0; color: #5A7A9A; font-size: 0.8rem;'>
    <p><b style='color:#00E5FF;'>NeuroGlueAI</b> — AI-Destekli Moleküler Tutkal Tasarım Platformu</p>
    <p style='color: #7C4DFF; letter-spacing: 2px;'>v6.0 • SHARP EDITION | TEKNOFEST 2026</p>
</div>
""", unsafe_allow_html=True)
