def summariser(history: list[dict]) -> dict:
    """
    Compresses a conversation history into a dense summary string.
    Use this when the context window is getting long.
    Returns a dict with a 'summary' key containing the compressed history.
    """
    if not history:
        return {"summary": ""}

    chat_content = " ".join(
        msg["content"][0]["text"]
        for msg in history
        if msg.get("content")
        and len(msg["content"]) > 0
        and "text" in msg["content"][0]
    )
    char_budget = len(chat_content)

    summariser_system_prompt = f"""
    Summarise the conversation in <= {int(0.5 * char_budget)} characters.
    Preserve key facts and intent. No extra text.
    """

    def normalize(history):
        out = []
        for msg in history:
            content = msg["content"]
            if isinstance(content, list):
                content = content[0]["text"]
            out.append({"role": msg["role"], "content": content})
        return out

    messages_for_summarisation = [
        {"role": "system", "content": summariser_system_prompt}
    ] + normalize(history)

    print("Messages for summarisation:", messages_for_summarisation)

    try:
        summarised_history = (
            client.chat.completions.create(
                model=SUMMARY_MODEL,
                messages=messages_for_summarisation,
            )
            .choices[0]
            .message.content
        )
    except Exception as e:

        fallback = " | ".join(
            msg.get("content", "")[:100]
            for msg in history[-4:]
            if isinstance(msg, dict)
        )
        print(f"Summariser failed ({e}), using fallback.")
        return {"summary": fallback}

    print("Summarised history:", summarised_history)
    return {"summary": summarised_history}


def call_summariser(history: list[dict]) -> dict:
    summarised_history = summariser(history)
    print("Using summarised history:", summarised_history)
    messages = (
        [{"role": "system", "content": system}]
        + [{"role": "user", "content": summarised_history["summary"]}]
        + [{"role": "user", "content": message}]
    )
    print("\n Messages after summarisation:", messages)
    return messages
