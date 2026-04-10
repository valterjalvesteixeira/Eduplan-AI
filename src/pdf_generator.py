from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image


PDF_TEXTS = {
    "pt": {
        "paa_title": "Documento PAA / Justificação | {school_name}",
        "paa_framework": "Enquadramento pedagógico",
        "paa_subject": "Área / disciplina principal",
        "paa_audience": "Público-alvo",
        "paa_duration": "Duração",
        "paa_total_cost": "Custo total estimado",
        "paa_plan": "Plano / descrição da atividade",
        "paa_justification": (
            "A presente proposta enquadra-se no desenvolvimento de uma atividade do tipo "
            "'{activity_type}', relacionada com o tema '{theme}', dirigida ao público "
            "'{audience}', com duração prevista de {duration} minutos. "
            "A atividade articula-se com a área disciplinar '{subject_area}' e contribui para "
            "o desenvolvimento de competências pedagógicas, sociais e de literacia cultural."
        ),
        "parents_materials_title": "Informação para Pais | Materiais para Atividade em Sala",
        "parents_general_info": "Informação geral",
        "parents_teacher": "Professor responsável",
        "parents_time": "Hora / referência",
        "parents_materials": "Materiais a trazer pelos alunos",
        "parents_contact": "Contacto",
        "parents_intro": (
            "A escola {school_name} informa que será dinamizada uma atividade com o tema "
            "'{theme}', destinada a '{audience}'."
        ),
        "parents_authorization_title": "Autorização para Pais / Encarregados de Educação",
        "parents_authorization": "Autorização",
        "parents_meeting": "Hora de encontro / início",
        "parents_transport": "Transporte",
        "parents_departure": "Hora de partida",
        "parents_return": "Hora prevista de chegada",
        "parents_price": "Valor por aluno",
        "parents_emergency": "Contacto de emergência",
        "parents_guardian_block_title": "Preenchimento pelo encarregado de educação",
        "parents_authorization_body": (
            "Autorizo o/a educando/a a participar na visita de estudo relacionada com o tema "
            "'{theme}', destinada a '{audience}', organizada por {school_name}."
        ),
        "parents_guardian_block": (
            "Declaro que tomei conhecimento das condições da visita e autorizo a participação do/a aluno/a.<br/><br/>"
            "Nome do aluno: _________________________________________________<br/><br/>"
            "Turma: _________________________________________________<br/><br/>"
            "Ano de escolaridade: _________________________________________________<br/><br/>"
            "Nome do Encarregado de Educação: ________________________________<br/><br/>"
            "Assinatura: _________________________________________________<br/><br/>"
            "Data: ____ / ____ / ______"
        ),
        "not_indicated": "Não indicado",
        "not_indicated_f": "Não indicada",
        "not_applicable": "Não aplicável",
        "untitled_school": "Escola",
    },
    "en": {
        "paa_title": "PAA / Institutional Justification | {school_name}",
        "paa_framework": "Pedagogical framework",
        "paa_subject": "Main subject / area",
        "paa_audience": "Target audience",
        "paa_duration": "Duration",
        "paa_total_cost": "Estimated total cost",
        "paa_plan": "Plan / activity description",
        "paa_justification": (
            "This proposal is part of an activity of type '{activity_type}', related to the theme "
            "'{theme}', aimed at '{audience}', with an expected duration of {duration} minutes. "
            "The activity is connected to the subject area '{subject_area}' and contributes to the "
            "development of pedagogical, social, and cultural literacy skills."
        ),
        "parents_materials_title": "Parent Information | Materials for Classroom Activity",
        "parents_general_info": "General information",
        "parents_teacher": "Responsible teacher",
        "parents_time": "Time / reference",
        "parents_materials": "Materials students should bring",
        "parents_contact": "Contact",
        "parents_intro": (
            "The school {school_name} informs that an activity related to the theme "
            "'{theme}' will take place for '{audience}'."
        ),
        "parents_authorization_title": "Parent / Guardian Authorization",
        "parents_authorization": "Authorization",
        "parents_meeting": "Meeting / start time",
        "parents_transport": "Transport",
        "parents_departure": "Departure time",
        "parents_return": "Estimated return time",
        "parents_price": "Price per student",
        "parents_emergency": "Emergency contact",
        "parents_guardian_block_title": "To be completed by parent / guardian",
        "parents_authorization_body": (
            "I authorize the student to participate in the study visit related to the theme "
            "'{theme}', intended for '{audience}', organized by {school_name}."
        ),
        "parents_guardian_block": (
            "I confirm that I am aware of the visit conditions and authorize the student to participate.<br/><br/>"
            "Student name: _________________________________________________<br/><br/>"
            "Class group: _________________________________________________<br/><br/>"
            "School year: _________________________________________________<br/><br/>"
            "Parent / Guardian name: ________________________________<br/><br/>"
            "Signature: _________________________________________________<br/><br/>"
            "Date: ____ / ____ / ______"
        ),
        "not_indicated": "Not indicated",
        "not_indicated_f": "Not indicated",
        "not_applicable": "Not applicable",
        "untitled_school": "School",
    },
    "es": {
        "paa_title": "Documento PAA / Justificación | {school_name}",
        "paa_framework": "Marco pedagógico",
        "paa_subject": "Asignatura / área principal",
        "paa_audience": "Público objetivo",
        "paa_duration": "Duración",
        "paa_total_cost": "Coste total estimado",
        "paa_plan": "Plan / descripción de la actividad",
        "paa_justification": (
            "La presente propuesta se enmarca en el desarrollo de una actividad del tipo "
            "'{activity_type}', relacionada con el tema '{theme}', dirigida al público "
            "'{audience}', con una duración prevista de {duration} minutos. "
            "La actividad se articula con el área disciplinar '{subject_area}' y contribuye al "
            "desarrollo de competencias pedagógicas, sociales y de alfabetización cultural."
        ),
        "parents_materials_title": "Información para Familias | Materiales para Actividad en Aula",
        "parents_general_info": "Información general",
        "parents_teacher": "Profesor responsable",
        "parents_time": "Hora / referencia",
        "parents_materials": "Materiales que deben traer los alumnos",
        "parents_contact": "Contacto",
        "parents_intro": (
            "El centro {school_name} informa que se realizará una actividad relacionada con el tema "
            "'{theme}', destinada a '{audience}'."
        ),
        "parents_authorization_title": "Autorización para Familias / Tutores",
        "parents_authorization": "Autorización",
        "parents_meeting": "Hora de encuentro / inicio",
        "parents_transport": "Transporte",
        "parents_departure": "Hora de salida",
        "parents_return": "Hora prevista de llegada",
        "parents_price": "Precio por alumno",
        "parents_emergency": "Contacto de emergencia",
        "parents_guardian_block_title": "A completar por la familia / tutor",
        "parents_authorization_body": (
            "Autorizo al alumno/a a participar en la visita de estudio relacionada con el tema "
            "'{theme}', destinada a '{audience}', organizada por {school_name}."
        ),
        "parents_guardian_block": (
            "Declaro que conozco las condiciones de la visita y autorizo la participación del alumno/a.<br/><br/>"
            "Nombre del alumno/a: _________________________________________________<br/><br/>"
            "Grupo / clase: _________________________________________________<br/><br/>"
            "Curso escolar: _________________________________________________<br/><br/>"
            "Nombre del padre, madre o tutor: ________________________________<br/><br/>"
            "Firma: _________________________________________________<br/><br/>"
            "Fecha: ____ / ____ / ______"
        ),
        "not_indicated": "No indicado",
        "not_indicated_f": "No indicada",
        "not_applicable": "No aplicable",
        "untitled_school": "Centro educativo",
    },
    "fr": {
        "paa_title": "Document PAA / Justification | {school_name}",
        "paa_framework": "Cadre pédagogique",
        "paa_subject": "Discipline / domaine principal",
        "paa_audience": "Public cible",
        "paa_duration": "Durée",
        "paa_total_cost": "Coût total estimé",
        "paa_plan": "Plan / description de l’activité",
        "paa_justification": (
            "La présente proposition s’inscrit dans le développement d’une activité de type "
            "'{activity_type}', liée au thème '{theme}', destinée au public "
            "'{audience}', avec une durée prévue de {duration} minutes. "
            "L’activité s’articule avec le domaine disciplinaire '{subject_area}' et contribue au "
            "développement de compétences pédagogiques, sociales et de culture générale."
        ),
        "parents_materials_title": "Information aux Parents | Matériel pour Activité en Classe",
        "parents_general_info": "Informations générales",
        "parents_teacher": "Enseignant responsable",
        "parents_time": "Horaire / référence",
        "parents_materials": "Matériel à apporter par les élèves",
        "parents_contact": "Contact",
        "parents_intro": (
            "L’école {school_name} informe qu’une activité liée au thème "
            "'{theme}' sera organisée pour '{audience}'."
        ),
        "parents_authorization_title": "Autorisation Parentale / Responsable Légal",
        "parents_authorization": "Autorisation",
        "parents_meeting": "Heure de rendez-vous / début",
        "parents_transport": "Transport",
        "parents_departure": "Heure de départ",
        "parents_return": "Heure prévue de retour",
        "parents_price": "Prix par élève",
        "parents_emergency": "Contact d’urgence",
        "parents_guardian_block_title": "À compléter par le parent / responsable légal",
        "parents_authorization_body": (
            "J’autorise l’élève à participer à la visite d’étude liée au thème "
            "'{theme}', destinée à '{audience}', organisée par {school_name}."
        ),
        "parents_guardian_block": (
            "Je déclare avoir pris connaissance des conditions de la visite et j’autorise la participation de l’élève.<br/><br/>"
            "Nom de l’élève: _________________________________________________<br/><br/>"
            "Classe: _________________________________________________<br/><br/>"
            "Niveau scolaire: _________________________________________________<br/><br/>"
            "Nom du parent / responsable légal: ________________________________<br/><br/>"
            "Signature: _________________________________________________<br/><br/>"
            "Date: ____ / ____ / ______"
        ),
        "not_indicated": "Non indiqué",
        "not_indicated_f": "Non indiquée",
        "not_applicable": "Non applicable",
        "untitled_school": "École",
    },
}


def _pdf_texts(language: str) -> dict:
    return PDF_TEXTS.get(language, PDF_TEXTS["en"])


def _build_pdf(title: str, sections: list[tuple[str, str]], banner_path: str | None = None) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=10,
    )

    story = []

    if banner_path and Path(banner_path).exists():
        img = Image(banner_path, width=16 * cm, height=3.8 * cm)
        story.append(img)
        story.append(Spacer(1, 0.25 * cm))

    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.35 * cm))

    for heading, content in sections:
        story.append(Paragraph(heading, heading_style))
        story.append(Spacer(1, 0.12 * cm))
        safe_content = (content or "").replace("\n", "<br/>")
        story.append(Paragraph(safe_content, body_style))
        story.append(Spacer(1, 0.25 * cm))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_paa_pdf(
    school_name: str,
    activity_type: str,
    theme: str,
    subject_area: str,
    audience: str,
    duration: int,
    plan_text: str,
    total_cost: float,
    banner_path: str | None = None,
    language: str = "pt",
) -> bytes:
    tx = _pdf_texts(language)
    safe_school = school_name or tx["untitled_school"]

    title = tx["paa_title"].format(school_name=safe_school)

    justification = tx["paa_justification"].format(
        activity_type=activity_type,
        theme=theme,
        audience=audience,
        duration=duration,
        subject_area=subject_area or tx["not_indicated"],
    )

    sections = [
        (tx["paa_framework"], justification),
        (tx["paa_subject"], subject_area or tx["not_indicated"]),
        (tx["paa_audience"], audience or tx["not_indicated"]),
        (tx["paa_duration"], f"{duration} min"),
        (tx["paa_total_cost"], f"{total_cost:.2f} €"),
        (tx["paa_plan"], plan_text),
    ]

    return _build_pdf(title, sections, banner_path=banner_path)


def generate_parents_materials_pdf(
    school_name: str,
    teacher_name: str,
    theme: str,
    audience: str,
    student_materials: str,
    meeting_time: str,
    emergency_contact: str,
    banner_path: str | None = None,
    language: str = "pt",
) -> bytes:
    tx = _pdf_texts(language)
    safe_school = school_name or tx["untitled_school"]

    title = tx["parents_materials_title"]

    intro = tx["parents_intro"].format(
        school_name=safe_school,
        theme=theme,
        audience=audience or tx["not_indicated"],
    )

    sections = [
        (tx["parents_general_info"], intro),
        (tx["parents_teacher"], teacher_name or tx["not_indicated"]),
        (tx["parents_time"], meeting_time or tx["not_applicable"]),
        (tx["parents_materials"], student_materials or tx["not_indicated"]),
        (tx["parents_contact"], emergency_contact or tx["not_indicated"]),
    ]

    return _build_pdf(title, sections, banner_path=banner_path)


def generate_parents_authorization_pdf(
    school_name: str,
    theme: str,
    audience: str,
    meeting_time: str,
    transport_mode: str,
    departure_time: str,
    return_time: str,
    price_per_student: float,
    emergency_contact: str,
    banner_path: str | None = None,
    language: str = "pt",
) -> bytes:
    tx = _pdf_texts(language)
    safe_school = school_name or tx["untitled_school"]

    title = tx["parents_authorization_title"]

    body = tx["parents_authorization_body"].format(
        theme=theme,
        audience=audience or tx["not_indicated"],
        school_name=safe_school,
    )

    sections = [
        (tx["parents_authorization"], body),
        (tx["parents_meeting"], meeting_time or tx["not_indicated_f"]),
        (tx["parents_transport"], transport_mode or tx["not_indicated"]),
        (tx["parents_departure"], departure_time or tx["not_indicated_f"]),
        (tx["parents_return"], return_time or tx["not_indicated_f"]),
        (tx["parents_price"], f"{price_per_student:.2f} €"),
        (tx["parents_emergency"], emergency_contact or tx["not_indicated"]),
        (tx["parents_guardian_block_title"], tx["parents_guardian_block"]),
    ]

    return _build_pdf(title, sections, banner_path=banner_path)