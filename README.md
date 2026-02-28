# 📄 Minimalist RenderCV Portfolio

A clean, data-driven personal portfolio built with **Streamlit** and powered by **RenderCV**. This project serves as a web-based companion to your professional CV, rendering data directly from YAML files to maintain a single source of truth.

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-black?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-App-black?style=flat-square&logo=streamlit)](https://streamlit.io/)
[![RenderCV](https://img.shields.io/badge/RenderCV-Framework-black?style=flat-square)](https://github.com/sinaatalay/rendercv)

---

## ✨ Key Features

- **RenderCV Integration:** Uses the standardized [RenderCV](https://github.com/sinaatalay/rendercv) YAML schema. One file updates both your LaTeX PDF and this web portfolio.
- **Dynamic Language Detection:** Automatically detects and serves content in English or Spanish based on browser settings.
- **Minimalist Aesthetic:** Focused on typography (_Exo 2_ & _Orbitron_) and clean spacing. No clutter, just information.
- **Interactive Elements:** Collapsible experience sections and tech stacks displayed as modern tags.
- **Direct Downloads:** Quick access to the latest PDF versions of your CV in multiple languages.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **CV Engine:** [RenderCV](https://github.com/sinaatalay/rendercv)
- **Data:** YAML (PyYAML)
- **Styling:** Custom CSS Injection (Minimalist / High-Contrast)

---

## 📂 Project Structure

```text
├── main.py                          # Application logic & UI
├── language_detection.py            # Browser language utility
├── requirements.txt                 # Dependencies
├── JuanFranMartin_English_CV.yaml   # RenderCV Source (EN)
├── JuanFranMartin_Spanish_CV.yaml   # RenderCV Source (ES)
```

## 🚀 Commands

- **Generate CVs:** `python render_cvs.py`
- **Run streamlit:** `streamlit run main.py`
