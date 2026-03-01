import os
from pathlib import Path

import streamlit as st
import yaml
from language_detection import detect_browser_language

if "lang" not in st.session_state:
    browser_lang = detect_browser_language()
    st.session_state.lang = (
        "es" if (browser_lang or "en").lower().startswith("es") else "en"
    )

YAML_FILES = {
    "en": "JuanFranMartin_English_CV.yaml",
    "es": "JuanFranMartin_Spanish_CV.yaml",
}

LABELS = {
    "en": {
        "about": "About Me",
        "experience": "Experience",
        "education": "Education",
        "languages": "Languages",
        "download": "⬇️ Download CV (PDF)",
        "generating": "Generating PDF...",
        "download_ready": "⬇️ Save PDF",
        "no_pdf": "PDF not found.",
        "switch": "🇪🇸 Español",
        "new_lang": "es",
        "present": "present",
        "tech": "Tech Stack",
        "pdf_path": "./rendercv_output/JuanFranMartin_English_CV.pdf",
    },
    "es": {
        "about": "Sobre mí",
        "experience": "Experiencia",
        "education": "Educación",
        "languages": "Idiomas",
        "download": "⬇️ Descargar CV (PDF)",
        "generating": "Generando PDF...",
        "download_ready": "⬇️ Guardar PDF",
        "no_pdf": "PDF no encontrado.",
        "switch": "🇬🇧 English",
        "new_lang": "en",
        "present": "presente",
        "tech": "Tecnologías",
        "pdf_path": "./rendercv_output/JuanFranMartin_Spanish_CV.pdf",
    },
}

os.makedirs("rendercv_output", exist_ok=True)
yaml_file = YAML_FILES[st.session_state.lang]
output_pdf = f"rendercv_output/JuanFranMartin_{'English' if st.session_state.lang == 'en' else 'Spanish'}_CV.pdf"


def get_pdf_bytes(file_path):
    """Lee el PDF generado previamente por GitHub Actions."""
    path = Path(file_path)
    if path.exists():
        return path.read_bytes()
    return None


@st.cache_data
def load_cv_data(lang):
    file_path = YAML_FILES[lang]
    if not Path(file_path).exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["cv"]


def render_tags(techs_string):
    tags = techs_string.replace("·", ",").split(",")
    return "".join(f'<span class="tag">{t.strip()}</span>' for t in tags if t.strip())


cv = load_cv_data(st.session_state.lang)
L = LABELS[st.session_state.lang]

if not cv:
    st.error("CV data not found.")
    st.stop()

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

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp { background-color: #ffffff; color: #1f2328; }

    /* --- CENTRADO Y LIMITACIÓN DE ANCHO --- */
    .block-container {
        max-width: 1300px !important;
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
        margin: auto;
    }

    /* Aumentado de 0.95rem a 1.05rem para mejor legibilidad */
    html, body, [class*="css"], .stMarkdown, p, li, label {
        font-family: 'Inter', sans-serif !important;
        color: #444d56 !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #1f2328 !important;
        font-size: 2.5rem !important; /* Ajuste para el H1 */
        letter-spacing: -0.02em !important;
        margin-bottom: 0px !important;
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #1f2328 !important;
    }
    
    /* Aumentado de 0.8rem a 0.9rem */
    .section-title {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #0969da !important;
        border-bottom: 1px solid #d0d7de;
        padding-bottom: 8px !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        background-color: #f6f8fa !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
        color: #1f2328 !important;
        font-size: 1rem !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #d0d7de !important;
        border-top: none !important;
        border-radius: 0 0 6px 6px !important;
    }
    
    /* Aumentado de 0.75rem a 0.85rem */
    .tag {
        display: inline-block;
        background: #ddf4ff;
        color: #0969da !important;
        border: 1px solid #54aeff66;
        border-radius: 12px;
        padding: 2px 12px;
        margin: 2px;
        font-size: 0.85rem;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .entry-meta {
        color: #636c76 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }
    
    /* Botones ligeramente más grandes */
    .stDownloadButton > button, .stButton > button {
        background-color: #f6f8fa !important;
        color: #24292f !important;
        border: 1px solid #d0d7de !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        transition: 0.2s;
        width: auto;
    }
    
    .stDownloadButton > button:hover, .stButton > button:hover {
        background-color: #ebf0f4 !important;
        border-color: #afb8c1 !important;
    }
    
    .contact-info {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.95rem !important;
        color: #0969da !important;
        margin: 10px 0px;
    }
    
    img { border-radius: 50%; border: 2px solid #d0d7de !important; }
    
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #ffffff; }
    ::-webkit-scrollbar-thumb { background: #d0d7de; border-radius: 10px; }
    
    hr { border-color: #d0d7de !important; }
    
    #MainMenu, footer { visibility: hidden; }

    /* Ajuste para móviles */
    @media (max-width: 800px) {
        .block-container {
            max-width: 95% !important;
            padding: 1rem !important;
        }
        html, body, [class*="css"], .stMarkdown, p, li, label {
            font-size: 1rem !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

header_container = st.container()
with header_container:
    col_spacer, col_sw = st.columns([4, 1])
    with col_sw:
        selected_lang = st.segmented_control(
            label="Lang",
            options=["en", "es"],
            format_func=lambda x: "EN" if x == "en" else "ES",
            selection_mode="single",
            default=st.session_state.lang,
            label_visibility="collapsed",
            key="lang_selector",
        )
        if selected_lang != st.session_state.lang:
            st.session_state.lang = selected_lang
            st.rerun()


col_text, col_photo = st.columns([4, 1])

with col_text:
    st.title(cv["name"])
    st.subheader(cv.get("headline", ""))
    contact_html = (
        f"📍 {cv.get('location', '')} &nbsp; | &nbsp; ✉️ {cv.get('email', '')}"
    )
    for sn in cv.get("social_networks", []):
        contact_html += f" &nbsp; | &nbsp; [{sn['network']}](https://{sn['network'].lower()}.com/{sn['username']})"
    st.markdown(contact_html)

with col_photo:
    photo_path = cv.get("photo", "").lstrip("./")
    if photo_path and Path(photo_path).exists():
        st.image(photo_path, width="content")

st.markdown("---")

if sum_key and sum_key in sections:
    st.markdown(
        f'<div class="section-title">{L["about"]}</div>', unsafe_allow_html=True
    )
    st.write(" ".join(sections[sum_key]))


def render_timeline_section(section_key, title):
    if not section_key or section_key not in sections:
        return
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    for item in sections[section_key]:
        start = str(item.get("start_date", ""))
        end = str(item.get("end_date", L["present"]))
        name = item.get("company") or item.get("institution", "")
        role = item.get("position") or item.get("degree", "")

        with st.expander(f"**{role}** @ {name}  ({start} — {end})"):
            if item.get("location"):
                st.markdown(
                    f'<div class="entry-meta">📍 {item["location"]}</div>',
                    unsafe_allow_html=True,
                )
            for h in item.get("highlights", []):
                if any(h.startswith(p) for p in ["Technologies", "Tecnologías"]):
                    techs = h.split(":", 1)[-1]
                    st.markdown(
                        f"**{L['tech']}:** {render_tags(techs)}", unsafe_allow_html=True
                    )
                else:
                    st.markdown(f"- {h}")


render_timeline_section(exp_key, L["experience"])
render_timeline_section(edu_key, L["education"])


if lang_key and lang_key in sections:
    st.markdown(
        f'<div class="section-title">{L["languages"]}</div>', unsafe_allow_html=True
    )
    cols = st.columns(len(sections[lang_key]))
    for idx, lang_item in enumerate(sections[lang_key]):
        cols[idx].markdown(f"**{lang_item}**")
st.markdown("---")

_, col_btn, _ = st.columns([1, 2, 1])

with col_btn:
    st.download_button(
        label=L["download"],
        data=get_pdf_bytes(output_pdf),
        file_name=os.path.basename(output_pdf),
        mime="application/pdf",
        type="primary",
        key=f"dl_btn_{st.session_state.lang}",
        width="content",
    )

#TODO quitar color negro en hover en el movil 
# TODO revisar cambiar de idioma en el movil
#TODO poco mas