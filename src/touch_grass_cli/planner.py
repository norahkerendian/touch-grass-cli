def build_context(budget: int) -> dict[str, object]:
    return {
        "location": "San Diego",
        "weather": "75°F and sunny",
        "free_time": "2pm-6pm",
        "budget": budget,
    }


def build_prompt(context: dict[str, object]) -> str:
    return (
        "Plan a Touch Grass adventure with these details:\n"
        f"- Location: {context['location']}\n"
        f"- Weather: {context['weather']}\n"
        f"- Free time: {context['free_time']}\n"
        f"- Budget: ${context['budget']}\n\n"
        "Suggest an outdoor-friendly plan that fits the time window and budget."
    )
