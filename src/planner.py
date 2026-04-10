import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv


def generate_plan(
    theme: str,
    goal: str,
    audience: str,
    duration: int,
    language: str,
    school_name: str = "",
    activity_type: str = "",
    subject_area: str = "",
    teacher_name: str = "",
    emergency_contact: str = "",
    meeting_time: str = "",
    materials_needed: str = "",
    student_materials: str = "",
    price_per_student: float = 0.0,
    student_count: int = 0,
) -> str:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no ficheiro .env")

    client = OpenAI(api_key=api_key)

    total_cost = round(price_per_student * student_count, 2)

    if language == "pt":
        prompt = f"""
Cria um plano de atividade educativa em português de Portugal, com tom profissional, claro e útil para contexto escolar.

Dados:
- Tema: {theme}
- Objetivo: {goal}
- Público-alvo: {audience}
- Duração: {duration} minutos
- Nome da escola: {school_name}
- Tipo de atividade: {activity_type}
- Área / disciplina principal: {subject_area}
- Professor responsável: {teacher_name}
- Contacto de emergência: {emergency_contact}
- Hora indicativa / opcional: {meeting_time}
- Materiais já conhecidos: {materials_needed}
- Materiais que os alunos poderão trazer: {student_materials}
- Preço por aluno: {price_per_student}
- Número de alunos: {student_count}
- Custo total estimado: {total_cost}

Quero um plano estruturado nas seguintes secções, exatamente com estes títulos:

RESUMO
OBJETIVOS
DISCIPLINAS ENVOLVIDAS
COMPETÊNCIAS DESENVOLVIDAS
MATERIAIS
PASSO A PASSO
AVALIAÇÃO / REFLEXÃO
INFORMAÇÃO LOGÍSTICA
CUSTOS

Regras:
- Em "DISCIPLINAS ENVOLVIDAS", sugere disciplinas realistas para a atividade.
- Em "PASSO A PASSO", cria etapas claras e numeradas.
- Em "INFORMAÇÃO LOGÍSTICA", adapta ao tipo de atividade.
- Não assumas horas exatas como obrigatórias, especialmente com crianças pequenas.
- Se houver hora, trata-a como indicativa.
- Usa sempre o público-alvo de forma clara, por exemplo "12 anos" ou "12.º ano".
- Não uses linguagem demasiado genérica.
- Escreve como se fosse um documento útil para uma professora.

No final, acrescenta uma pequena nota final de enquadramento pedagógico.

Acrescenta também no fim uma linha separada com:
PROMPT_ILUSTRACAO:
seguida de um prompt curto, visual e claro para gerar uma imagem ilustrativa desta atividade.
"""
    else:
        prompt = f"""
Create an educational activity plan in English, with a professional, clear, school-ready tone.

Data:
- Theme: {theme}
- Goal: {goal}
- Target audience: {audience}
- Duration: {duration} minutes
- School name: {school_name}
- Activity type: {activity_type}
- Main subject area: {subject_area}
- Responsible teacher: {teacher_name}
- Emergency contact: {emergency_contact}
- Indicative / optional time: {meeting_time}
- Known materials: {materials_needed}
- Materials students may bring: {student_materials}
- Price per student: {price_per_student}
- Number of students: {student_count}
- Estimated total cost: {total_cost}

I want the plan structured with exactly these section titles:

SUMMARY
OBJECTIVES
SUBJECTS INVOLVED
SKILLS DEVELOPED
MATERIALS
STEP BY STEP
ASSESSMENT / REFLECTION
LOGISTICAL INFORMATION
COSTS

Rules:
- In "SUBJECTS INVOLVED", suggest realistic school subjects connected to the activity.
- In "STEP BY STEP", create clear numbered stages.
- In "LOGISTICAL INFORMATION", adapt to the activity type.
- Do not assume exact times are mandatory, especially with younger students.
- If time is included, treat it as indicative.
- Always make the audience explicit, such as "12 years old" or "12th grade".
- Avoid generic writing.
- Write as if this were a useful teacher-facing document.

At the end, add a short pedagogical framing note.

Also add one separate final line with:
ILLUSTRATION_PROMPT:
followed by a short, visual, clear prompt to generate an illustrative image for this activity.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()