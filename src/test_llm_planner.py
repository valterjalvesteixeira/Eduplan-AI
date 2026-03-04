from dotenv import load_dotenv
from src.llm_planner import generate_plan_llm


def main():
    load_dotenv()

    plan = generate_plan_llm(
        goal="AI-assisted learning activities to boost engagement and creativity",
        target_audience="Pre-school to Grade 12 (multicultural / multilingual classrooms)",
        duration_minutes=60,
        model="gpt-4o-mini",
    )

    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()