def summariser(history: list[dict]) -> dict:
    """
    Compresses a conversation history into a dense summary string.
    Use this when the context window is getting long.
    Returns a dict with a 'summary' key containing the compressed history.
    """
    if not history:
        return {"summary": ""}

    # Measure only the actual content, not Python repr noise
    raw_text = " ".join(
        msg.get("content", "") for msg in history if isinstance(msg, dict)
    )

    char_budget = max(200, int(len(raw_text) * 0.2))  # floor of 200 chars

    summariser_system_prompt = f"""You are a conversation compression engine.

                                Summarise the following chat history between a user and an assistant into at most {char_budget} characters.

Strict rules:
- Preserve key facts, user intent, constraints, and important context
- Remove filler, repetition, greetings, and irrelevant details
- Keep it concise, dense, and information-rich
- Use plain text (no markdown, no bullet points)
- Do NOT add new information or explanations

Output only the summary text."""

    messages_for_summarisation = (
        [{"role": "system", "content": summariser_system_prompt}]
        + history
        + [{"role": "user", "content": "Please summarise the text above."}]
    )

    try:
        summarised_history = (
            client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_for_summarisation,
            )
            .choices[0]
            .message.content
        )
    except Exception as e:
        # Fail gracefully — return the last few messages as a fallback
        fallback = " | ".join(
            msg.get("content", "")[:100]
            for msg in history[-4:]
            if isinstance(msg, dict)
        )
        print(f"Summariser failed ({e}), using fallback.")
        return {"summary": fallback}

    print("Summarised history:", summarised_history)
    return {"summary": summarised_history}
