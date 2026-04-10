def score_plan(plan_text: str) -> dict:
    text = plan_text.lower()

    score = 0
    strengths = []
    improvements = []

    if len(plan_text) > 400:
        score += 25
        strengths.append("O plano tem bom nível de detalhe.")
    else:
        improvements.append("O plano pode ser mais desenvolvido e específico.")

    if any(word in text for word in ["objetivo", "objective", "learn", "aprender"]):
        score += 20
        strengths.append("Inclui intenção pedagógica clara.")
    else:
        improvements.append("Falta explicitar melhor os objetivos de aprendizagem.")

    if any(word in text for word in ["materiais", "materials", "recursos", "resources"]):
        score += 15
        strengths.append("Identifica materiais ou recursos.")
    else:
        improvements.append("Seria útil indicar materiais ou recursos necessários.")

    if any(word in text for word in ["passo", "steps", "etapa", "activity", "dinâmica"]):
        score += 20
        strengths.append("Apresenta estrutura de execução.")
    else:
        improvements.append("O plano deve mostrar etapas mais claras de execução.")

    if any(word in text for word in ["avaliação", "evaluation", "reflexão", "reflection"]):
        score += 20
        strengths.append("Inclui componente de reflexão ou avaliação.")
    else:
        improvements.append("Convém acrescentar um momento final de reflexão ou avaliação.")

    score = min(score, 100)

    if not strengths:
        strengths.append("O plano já oferece uma base útil para desenvolvimento.")

    if not improvements:
        improvements.append("O plano está equilibrado e pronto para uso inicial.")

    return {
        "score": score,
        "strengths": strengths,
        "improvements": improvements,
    }