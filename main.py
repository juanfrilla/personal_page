import os
from pathlib import Path

import streamlit as st
import yaml
from language_detection import detect_browser_language

# 1. Aseguramos que el idioma exista en session_state antes de usarlo
if "lang" not in st.session_state:
    # Intentamos detectar, si falla o es None, usamos "en" por defecto
    try:
        browser_lang = detect_browser_language()
        st.session_state.lang = (
            "es" if (browser_lang or "en").lower().startswith("es") else "en"
        )
    except Exception:
        st.session_state.lang = "en"

lang_key = st.session_state.get("lang", "en")

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
    path = Path(file_path)
    if path.exists():
        return path.read_bytes()
    return b""


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


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

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

pdf_bits = get_pdf_bytes(output_pdf)

_, col_btn, _ = st.columns([1, 2, 1])

with col_btn:
    if pdf_bits is not None:
        st.download_button(
            label=L["download"],
            data=pdf_bits,
            file_name=os.path.basename(output_pdf),
            mime="application/pdf",
            type="primary",
            key=f"dl_btn_{st.session_state.lang}",
            use_container_width=True,
        )
    else:
        st.warning(L.get("no_pdf", "PDF no disponible"))

# TODO quitar color negro en hover en el movil
# TODO revisar cambiar de idioma en el movil
# TODO poco mas
