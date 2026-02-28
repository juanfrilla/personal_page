from pathlib import Path

import streamlit as st
import yaml
from language_detection import detect_browser_language

# --- CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Juan Francisco Martin", page_icon="💻", layout="wide")

if "lang" not in st.session_state:
    browser_lang = detect_browser_language()
    st.session_state.lang = (
        "es" if (browser_lang or "en").lower().startswith("es") else "en"
    )

# --- CONSTANTES ---
YAML_FILES = {
    "en": "JuanFranMartin_English_CV.yaml",
    "es": "JuanFranMartin_Spanish_CV.yaml",
}
PDF_FILES = {
    "en": "JuanFranMartin_English_CV.pdf",
    "es": "JuanFranMartin_Spanish_CV.pdf",
}

LABELS = {
    "en": {
        "about": "About Me",
        "experience": "Experience",
        "education": "Education",
        "languages": "Languages",
        "download": "⬇️ Download CV (PDF)",
        "no_pdf": "PDF not found.",
        "switch": "🇪🇸 Español",
        "new_lang": "es",
        "present": "present",
        "tech": "Tech Stack",
    },
    "es": {
        "about": "Sobre mí",
        "experiencia": "Experiencia",
        "educación": "Educación",
        "lenguajes": "Idiomas",
        "download": "⬇️ Descargar CV (PDF)",
        "no_pdf": "PDF no encontrado.",
        "switch": "🇬🇧 English",
        "new_lang": "en",
        "present": "presente",
        "tech": "Tecnologías",
    },
}


# --- FUNCIONES ---
@st.cache_data
def load_cv_data(lang):
    file_path = YAML_FILES[lang]
    if not Path(file_path).exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["cv"]


def render_tags(techs_string):
    """Convierte string de tecnologías en tags HTML"""
    tags = techs_string.replace("·", ",").split(",")
    return "".join(f'<span class="tag">{t.strip()}</span>' for t in tags if t.strip())


# --- CARGA DE DATOS ---
cv = load_cv_data(st.session_state.lang)
L = LABELS[st.session_state.lang]

sections = cv.get("sections", {})

edu_key = next((k for k in sections if k.lower().startswith("educ")), None)

lang_key = next(
    (
        k
        for k in sections
        if k.lower().startswith("lang") or k.lower().startswith("leng")
    ),
    None,
)

exp_key = next((k for k in sections if k.lower().startswith("exp")), None)

sum_key = next(
    (k for k in sections if k.lower().startswith("sum") or k.lower().startswith("res")),
    None,
)

if not cv:
    st.error("CV data not found.")
    st.stop()

st.markdown(
    """
<style>
    /* Importamos fuentes: Inter para lectura y JetBrains Mono para ese toque de "código" */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Fondo claro y limpio estilo GitHub Light */
    .stApp {
        background-color: #ffffff;
        color: #1f2328;
    }

    /* Tipografía general */
    html, body, [class*="css"], .stMarkdown, p, li, label {
        font-family: 'Inter', sans-serif !important;
        color: #444d56 !important; /* Gris oscuro profesional */
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* Títulos principales: Limpios y negros */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #1f2328 !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0px !important;
    }

    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #1f2328 !important;
    }

    /* Títulos de sección estilo "Editor de Código" en modo claro */
    .section-title {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #0969da !important; /* Azul software GitHub */
        border-bottom: 1px solid #d0d7de;
        padding-bottom: 8px !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    /* Expanders estilo Cards nítidas */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        background-color: #f6f8fa !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
        color: #1f2328 !important;
    }

    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #d0d7de !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }

    /* Tags minimalistas claros */
    .tag {
        display: inline-block;
        background: #ddf4ff;
        color: #0969da !important;
        border: 1px solid #54aeff66;
        border-radius: 12px;
        padding: 0px 10px;
        margin: 2px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Metadatos (fechas, lugares) */
    .entry-meta {
        color: #636c76 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    /* Botones de acción minimalistas */
    .stDownloadButton > button, .stButton > button {
        background-color: #f6f8fa !important;
        color: #24292f !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        transition: 0.2s;
    }

    .stDownloadButton > button:hover, .stButton > button:hover {
        background-color: #ebf0f4 !important;
        border-color: #afb8c1 !important;
    }

    /* Info de contacto */
    .contact-info {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #0969da !important;
        margin: 10px 0px;
    }

    /* Imagen de perfil */
    img {
        border-radius: 50%;
        border: 2px solid #d0d7de !important;
    }

    /* Scrollbar minimalista claro */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #ffffff; }
    ::-webkit-scrollbar-thumb { background: #d0d7de; border-radius: 10px; }

    hr { border-color: #d0d7de !important; }
    
    #MainMenu, footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# --- HEADER & NAVIGATION ---
col_head, col_sw = st.columns([4, 1])

with col_sw:
    if st.button(L["switch"]):
        st.session_state.lang = L["new_lang"]
        st.rerun()

with col_head:
    st.title(cv["name"])
    st.subheader(cv.get("headline", ""))

# --- COLUMNAS PRINCIPALES ---
col1, col2 = st.columns([3, 1])

# --- INFORMACIÓN DE CONTACTO (Debajo del Título/Subheader) ---
st.markdown(
    f"""
    <div class="contact-info">
        📍 {cv.get("location", "")} &nbsp; | &nbsp; ✉️ {cv.get("email", "")}
    </div>
    """,
    unsafe_allow_html=True,
)

# --- LINKS Y FOTO ---
col_links, col_photo = st.columns([3, 1])
with col_links:
    links = []
    for sn in cv.get("social_networks", []):
        links.append(
            f"[{sn['network']}](https://{sn['network'].lower()}.com/{sn['username']})"
        )
    st.markdown("  |  ".join(links))

with col_photo:
    if cv.get("photo") and Path(cv["photo"].lstrip("./")).exists():
        st.image(cv["photo"].lstrip("./"), width=180)

# --- BOTÓN DE DESCARGA ---
pdf_path = Path(PDF_FILES[st.session_state.lang])
if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        st.download_button(
            L["download"], f, file_name=pdf_path.name, mime="application/pdf"
        )

st.markdown("---")

# --- SECCIONES DINÁMICAS ---
sections = cv.get("sections", {})

# Sobre mí
if sum_key in sections:
    st.markdown(
        f'<div class="section-title">{L["about"]}</div>', unsafe_allow_html=True
    )
    st.write(" ".join(sections[sum_key]))


# Experiencia y Educación (Lógica unificada)
def render_timeline_section(section_key, title):
    if section_key in sections:
        st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
        for item in sections[section_key]:
            start = item.get("start_date", "")
            end = item.get("end_date", L["present"])
            name = item.get("company") or item.get("institution")
            role = item.get("position") or item.get("degree", "")

            with st.expander(f"**{role}** @ {name}  ({start} — {end})"):
                if item.get("location"):
                    st.markdown(
                        f'<div class="entry-meta">📍 {item["location"]}</div>',
                        unsafe_allow_html=True,
                    )

                for h in item.get("highlights", []):
                    # Detectar si es línea de tecnologías
                    if any(
                        h.startswith(prefix)
                        for prefix in ["Technologies", "Tecnologías"]
                    ):
                        techs = h.split(":", 1)[-1]
                        st.markdown(
                            f"**{L['tech']}:** {render_tags(techs)}",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(f"- {h}")


render_timeline_section(exp_key, L[exp_key])
render_timeline_section(edu_key, L[edu_key])

# Idiomas
if lang_key in sections:
    st.markdown(
        f'<div class="section-title">{L[lang_key]}</div>', unsafe_allow_html=True
    )
    cols = st.columns(len(sections[lang_key]))
    for idx, lang_item in enumerate(sections[lang_key]):
        cols[idx].markdown(f"**{lang_item}**")
