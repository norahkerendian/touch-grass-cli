def generate_plan(prompt: str) -> str:
    """Generate a Touch Grass plan using the default mock AI provider."""
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    return """Touch Grass Plan

1. Balboa Park Garden Walk
   Duration: 45 minutes
   Estimated cost: Free
   Reason: A relaxed outdoor start with plenty of shade, open space, and easy photo stops.

2. Spanish Village Art Center Browse
   Duration: 35 minutes
   Estimated cost: Free
   Reason: Adds a creative stop without using the budget, and it is easy to explore at your own pace.

3. Picnic Snack Break
   Duration: 30 minutes
   Estimated cost: $8
   Reason: Keeps the afternoon casual while leaving room in the budget for one more stop.

4. Waterfront Stroll at Seaport Village
   Duration: 50 minutes
   Estimated cost: Free
   Reason: A scenic walk fits the sunny weather and keeps the plan flexible.

5. Sunset Treat
   Duration: 30 minutes
   Estimated cost: $6-$10
   Reason: Ends the outing with something small and budget-friendly before the free-time window closes.

Total estimated cost: $14-$18"""


def generate_plan_real(prompt: str) -> str:
    """Placeholder for a future real AI provider integration."""
    raise NotImplementedError(
        "Real AI integration is not configured. Use generate_plan() for offline mock output."
    )
