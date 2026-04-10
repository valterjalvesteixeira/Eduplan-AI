import time
import re
import streamlit as st
from pathlib import Path

from src.i18n import get_text
from src.planner import generate_plan
from src.image_generator import generate_activity_image
from src.pdf_generator import (
    generate_paa_pdf,
    generate_parents_materials_pdf,
    generate_parents_authorization_pdf,
)

st.set_page_config(page_title="EduPlan AI", layout="wide")

ASSETS_DIR = Path("assets")
THEMES_DIR = ASSETS_DIR / "themes"

theme_files = {
    "food": THEMES_DIR / "food.png",
    "history": THEMES_DIR / "history.png",
    "science": THEMES_DIR / "science.png",
    "environment": THEMES_DIR / "environment.png",
    "arts": THEMES_DIR / "arts.png",
    "heritage": THEMES_DIR / "heritage.png",
    "sport": THEMES_DIR / "sport.png",
    "technology": THEMES_DIR / "technology.png",
}

THEME_LABELS = {
    "pt": {
        "food": "Food",
        "history": "History",
        "science": "Science",
        "environment": "Environment",
        "arts": "Arts",
        "heritage": "Heritage",
        "sport": "Sport",
        "technology": "Technology",
    },
    "en": {
        "food": "Food",
        "history": "History",
        "science": "Science",
        "environment": "Environment",
        "arts": "Arts",
        "heritage": "Heritage",
        "sport": "Sport",
        "technology": "Technology",
    },
    "es": {
        "food": "Food",
        "history": "History",
        "science": "Science",
        "environment": "Environment",
        "arts": "Arts",
        "heritage": "Heritage",
        "sport": "Sport",
        "technology": "Technology",
    },
    "fr": {
        "food": "Food",
        "history": "History",
        "science": "Science",
        "environment": "Environment",
        "arts": "Arts",
        "heritage": "Heritage",
        "sport": "Sport",
        "technology": "Technology",
    },
}

if "language" not in st.session_state:
    st.session_state.language = "pt"

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "food"

if "generated_plan" not in st.session_state:
    st.session_state.generated_plan = None

if "generated_banner" not in st.session_state:
    st.session_state.generated_banner = None

if "illustration_prompt" not in st.session_state:
    st.session_state.illustration_prompt = None

if "generated_post_visit" not in st.session_state:
    st.session_state.generated_post_visit = None


def inject_css():
    st.markdown(
        """
        <style>
        .section-card {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px;
            background: rgba(255,255,255,0.03);
            margin-bottom: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def suggest_subjects(theme: str, language: str):
    mapping_pt = {
        "food": ["Ciências Naturais", "Português", "Cidadania e Desenvolvimento"],
        "history": ["História", "Português", "Cidadania e Desenvolvimento"],
        "science": ["Ciências Naturais", "Físico-Química", "Matemática"],
        "environment": ["Ciências Naturais", "Geografia", "Cidadania e Desenvolvimento"],
        "arts": ["Educação Visual", "Português", "História"],
        "heritage": ["História", "Português", "Educação Visual"],
        "sport": ["Educação Física", "Ciências Naturais", "Cidadania e Desenvolvimento"],
        "technology": ["TIC", "Matemática", "Ciências"],
    }

    mapping_en = {
        "food": ["Science", "Language", "Citizenship"],
        "history": ["History", "Language", "Citizenship"],
        "science": ["Science", "Math", "Technology"],
        "environment": ["Science", "Geography", "Citizenship"],
        "arts": ["Arts", "Language", "History"],
        "heritage": ["History", "Arts", "Language"],
        "sport": ["Physical Education", "Science", "Citizenship"],
        "technology": ["Technology", "Math", "Science"],
    }

    mapping_es = {
        "food": ["Ciencias Naturales", "Lengua", "Ciudadanía"],
        "history": ["Historia", "Lengua", "Ciudadanía"],
        "science": ["Ciencias", "Matemáticas", "Tecnología"],
        "environment": ["Ciencias", "Geografía", "Ciudadanía"],
        "arts": ["Artes", "Lengua", "Historia"],
        "heritage": ["Historia", "Artes", "Lengua"],
        "sport": ["Educación Física", "Ciencias", "Ciudadanía"],
        "technology": ["Tecnología", "Matemáticas", "Ciencias"],
    }

    mapping_fr = {
        "food": ["Sciences", "Langue", "Citoyenneté"],
        "history": ["Histoire", "Langue", "Citoyenneté"],
        "science": ["Sciences", "Mathématiques", "Technologie"],
        "environment": ["Sciences", "Géographie", "Citoyenneté"],
        "arts": ["Arts", "Langue", "Histoire"],
        "heritage": ["Histoire", "Arts", "Langue"],
        "sport": ["Éducation Physique", "Sciences", "Citoyenneté"],
        "technology": ["Technologie", "Mathématiques", "Sciences"],
    }

    maps = {
        "pt": mapping_pt,
        "en": mapping_en,
        "es": mapping_es,
        "fr": mapping_fr,
    }

    return maps.get(language, mapping_en).get(theme, [])


def get_theme_label(theme_key: str, language: str) -> str:
    return THEME_LABELS.get(language, THEME_LABELS["en"]).get(theme_key, theme_key.title())


def split_plan_and_illustration(raw_text: str) -> tuple[str, str | None]:
    markers = [
        "PROMPT_ILUSTRACAO:",
        "ILLUSTRATION_PROMPT:",
        "PROMPT_ILUSTRACION:",
        "PROMPT_ILLUSTRATION:",
    ]

    for marker in markers:
        if marker in raw_text:
            plan, prompt = raw_text.split(marker, 1)
            return plan.strip(), prompt.strip()

    return raw_text.strip(), None


def extract_post_visit_section(plan_text: str, language: str) -> tuple[str, str | None]:
    headings = {
        "pt": "SUGESTÕES PÓS-VISITA / PÓS-ATIVIDADE",
        "en": "POST-VISIT / POST-ACTIVITY SUGGESTIONS",
        "es": "SUGERENCIAS POSTERIORES A LA VISITA / ACTIVIDAD",
        "fr": "SUGGESTIONS APRÈS LA VISITE / ACTIVITÉ",
    }

    heading = headings.get(language, headings["en"])
    pattern = rf"(?:^|\n)##\s*{re.escape(heading)}\s*\n(.+)$"

    match = re.search(pattern, plan_text, flags=re.DOTALL)
    if not match:
        return plan_text, None

    suggestions = match.group(1).strip()
    cleaned = re.sub(pattern, "", plan_text, flags=re.DOTALL).strip()
    return cleaned, suggestions


def render_theme_selector(t: dict):
    st.subheader(t.get("theme", "Tema"))

    lang = st.session_state.language
    theme_options = list(theme_files.keys())
    theme_labels = THEME_LABELS[lang]

    current_index = theme_options.index(st.session_state.selected_theme)

    selected_label = st.radio(
        label=t.get("theme", "Tema"),
        options=[theme_labels[key] for key in theme_options],
        index=current_index,
        horizontal=True,
        label_visibility="collapsed",
    )

    selected_key = None
    for key, label in theme_labels.items():
        if label == selected_label:
            selected_key = key
            break

    if selected_key:
        st.session_state.selected_theme = selected_key

    image_path = theme_files[st.session_state.selected_theme]
    preview_col1, preview_col2, preview_col3 = st.columns([1.4, 1.2, 1.4])

    with preview_col2:
        if image_path.exists():
            st.image(str(image_path), width=300)

    st.caption(
        f"{t.get('selected_theme', 'Tema selecionado')}: "
        f"{theme_labels[st.session_state.selected_theme]}"
    )


def render_plan_block(plan_text: str, t: dict):
    st.subheader(t.get("generated_plan", "Plano gerado"))
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(plan_text.replace("\n", "  \n"))
    st.markdown("</div>", unsafe_allow_html=True)


inject_css()

top_left, top_right = st.columns([6, 1])

with top_right:
    language = st.selectbox(
        "Idioma / Language",
        options=["pt", "en", "es", "fr"],
        index=["pt", "en", "es", "fr"].index(st.session_state.language),
    )
    st.session_state.language = language

t = get_text(st.session_state.language)

banner_path = ASSETS_DIR / "banner.png"
if banner_path.exists():
    st.image(str(banner_path), width="stretch")

st.title(t.get("app_title", "EduPlan AI"))
st.caption(t.get("app_subtitle", "Planeador inteligente de atividades educativas"))

render_theme_selector(t)

st.markdown(f"### {t.get('main_details', 'Dados principais')}")

left_col, right_col = st.columns(2)

with left_col:
    school_name = st.text_input(t.get("school_name", "Nome da escola"))
    goal = st.text_area(
        t.get("goal", "Objetivo da atividade"),
        placeholder=t.get("goal_placeholder", "Example"),
    )
    audience = st.text_input(
        t.get("audience_age_year", "Faixa etária / ano"),
        placeholder=t.get("audience_age_year_placeholder", "Example"),
    )
    subject_area = st.text_input(t.get("subject_area", "Disciplina / área principal"))
    duration = st.slider(
        t.get("duration", "Duração total (minutos)"),
        min_value=15,
        max_value=180,
        value=60,
        step=15,
    )

with right_col:
    activity_type = st.radio(
        t.get("activity_type", "Tipo de atividade"),
        options=[
            t.get("activity_type_visit", "Visita de estudo"),
            t.get("activity_type_classroom", "Atividade em sala de aula"),
        ],
    )
    teacher_name = st.text_input(t.get("teacher_name", "Professor responsável"))
    emergency_contact = st.text_input(t.get("emergency_contact", "Contacto de emergência"))
    meeting_time = st.text_input(t.get("meeting_time_optional", "Hora indicativa / opcional"))

st.markdown(f"### {t.get('transport_section', 'Transporte')}")

transport_mode = st.selectbox(
    t.get("transport_type", "Tipo de transporte"),
    options=[
        t.get("transport_none", "Sem transporte"),
        t.get("transport_private_bus", "Autocarro alugado"),
        t.get("transport_public", "Transporte público"),
        t.get("transport_other", "Outro"),
    ],
)

departure_time = ""
return_time = ""
public_transport_type = ""

transport_col1, transport_col2 = st.columns(2)

if transport_mode == t.get("transport_private_bus", "Autocarro alugado"):
    with transport_col1:
        departure_time = st.text_input(
            t.get("bus_departure_time_optional", "Hora indicativa de partida")
        )
    with transport_col2:
        return_time = st.text_input(
            t.get("estimated_return_time_optional", "Hora prevista / opcional de chegada")
        )

elif transport_mode == t.get("transport_public", "Transporte público"):
    public_transport_type = st.selectbox(
        t.get("public_transport_mode", "Meio de transporte público"),
        options=[
            t.get("public_transport_bus", "Autocarro"),
            t.get("public_transport_train", "Comboio"),
            t.get("public_transport_metro", "Metro"),
            t.get("public_transport_other", "Outro"),
        ],
    )

st.markdown(f"### {t.get('materials_and_participants', 'Materiais e participantes')}")

materials_needed = st.text_area(
    t.get("known_materials", "Observações logísticas / materiais já conhecidos")
)

student_materials = st.text_area(
    t.get("student_materials", "Materiais a trazer pelos alunos")
)

st.markdown(f"### {t.get('costs_and_participants', 'Custos e participantes')}")

cost_col1, cost_col2, cost_col3 = st.columns(3)

with cost_col1:
    student_count = st.number_input(
        t.get("student_count", "Número de alunos"),
        min_value=0,
        value=25,
        step=1,
    )

with cost_col2:
    price_per_student = st.number_input(
        t.get("price_per_student", "Valor por aluno (€)"),
        min_value=0.0,
        value=0.0,
        step=0.5,
    )

with cost_col3:
    total_cost = round(student_count * price_per_student, 2)
    st.metric(t.get("total_cost", "Custo total (€)"), f"{total_cost:.2f}")

suggested_subjects = suggest_subjects(st.session_state.selected_theme, st.session_state.language)
if suggested_subjects:
    st.markdown(f"### {t.get('suggested_subjects', 'Disciplinas sugeridas')}")
    st.markdown(", ".join(suggested_subjects))

if st.button(t.get("generate", "Gerar plano"), width="stretch"):
    if not goal.strip():
        st.error(t.get("error_missing_goal", "Erro"))
    elif not audience.strip():
        st.error(t.get("error_missing_audience", "Erro"))
    else:
        progress_bar = st.progress(0, text=t.get("progress_generating", "A gerar plano..."))
        progress_bar.progress(20, text=t.get("progress_analysing", "A analisar contexto..."))
        time.sleep(0.2)
        progress_bar.progress(50, text=t.get("progress_structuring", "A estruturar pedido..."))
        time.sleep(0.2)

        try:
            theme_label = get_theme_label(
                st.session_state.selected_theme,
                st.session_state.language,
            )

            raw_plan = generate_plan(
                theme=theme_label,
                goal=goal,
                audience=audience,
                duration=duration,
                language=st.session_state.language,
                school_name=school_name,
                activity_type=activity_type,
                subject_area=subject_area,
                teacher_name=teacher_name,
                emergency_contact=emergency_contact,
                meeting_time=meeting_time,
                materials_needed=materials_needed,
                student_materials=student_materials,
                price_per_student=price_per_student,
                student_count=student_count,
            )

            plan_with_suggestions, illustration_prompt = split_plan_and_illustration(raw_plan)
            clean_plan, post_visit_suggestions = extract_post_visit_section(
                plan_with_suggestions,
                st.session_state.language,
            )

            st.session_state.illustration_prompt = illustration_prompt
            st.session_state.generated_plan = clean_plan
            st.session_state.generated_post_visit = post_visit_suggestions

            if illustration_prompt:
                try:
                    banner_output = generate_activity_image(
                        illustration_prompt,
                        Path("generated") / "activity_banner.png",
                    )
                    st.session_state.generated_banner = banner_output
                except Exception:
                    st.session_state.generated_banner = None

            progress_bar.progress(100, text=t.get("progress_done", "Concluído."))
            time.sleep(0.2)
            progress_bar.empty()

        except Exception as e:
            progress_bar.empty()
            st.error(f"{t.get('error_generate_plan', 'Erro ao gerar plano')}: {e}")

if st.session_state.generated_plan:
    if st.session_state.generated_banner:
        banner_col1, banner_col2, banner_col3 = st.columns([1.2, 2.6, 1.2])
        with banner_col2:
            st.image(st.session_state.generated_banner, width=560)

    render_plan_block(st.session_state.generated_plan, t)

    if st.session_state.get("generated_post_visit"):
        st.subheader(t.get("post_visit_suggestions", "Sugestões pós-visita / pós-atividade"))
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(st.session_state.generated_post_visit.replace("\n", "  \n"))
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"### {t.get('pdf_section', 'PDFs')}")

    theme_label = get_theme_label(
        st.session_state.selected_theme,
        st.session_state.language,
    )

    paa_pdf = generate_paa_pdf(
        school_name=school_name,
        activity_type=activity_type,
        theme=theme_label,
        subject_area=subject_area,
        audience=audience,
        duration=duration,
        plan_text=st.session_state.generated_plan,
        total_cost=total_cost,
        banner_path=st.session_state.generated_banner,
        language=st.session_state.language,
    )

    pdf_col1, pdf_col2 = st.columns(2)

    with pdf_col1:
        st.download_button(
            t.get("download_paa_pdf", "Descarregar PDF PAA"),
            data=paa_pdf,
            file_name=t.get("paa_file", "documento_paa.pdf"),
            mime="application/pdf",
            width="stretch",
        )

    with pdf_col2:
        if activity_type == t.get("activity_type_classroom", "Atividade em sala de aula"):
            parents_pdf = generate_parents_materials_pdf(
                school_name=school_name,
                teacher_name=teacher_name,
                theme=theme_label,
                audience=audience,
                student_materials=student_materials,
                meeting_time=meeting_time,
                emergency_contact=emergency_contact,
                banner_path=st.session_state.generated_banner,
                language=st.session_state.language,
            )

            st.download_button(
                t.get("download_parents_materials_pdf", "Lista de materiais para pais"),
                data=parents_pdf,
                file_name=t.get("parents_materials_file", "materiais_para_pais.pdf"),
                mime="application/pdf",
                width="stretch",
            )

        else:
            transport_description = public_transport_type if public_transport_type else transport_mode

            parents_pdf = generate_parents_authorization_pdf(
                school_name=school_name,
                theme=theme_label,
                audience=audience,
                meeting_time=meeting_time,
                transport_mode=transport_description,
                departure_time=departure_time,
                return_time=return_time,
                price_per_student=price_per_student,
                emergency_contact=emergency_contact,
                banner_path=st.session_state.generated_banner,
                language=st.session_state.language,
            )

            st.download_button(
                t.get("download_parents_authorization_pdf", "Autorização para pais"),
                data=parents_pdf,
                file_name=t.get("parents_authorization_file", "autorizacao_pais.pdf"),
                mime="application/pdf",
                width="stretch",
            )