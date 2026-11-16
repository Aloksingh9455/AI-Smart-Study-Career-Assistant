from openai import OpenAI

def get_client(api_key: str) -> OpenAI:
    if not api_key or not api_key.strip():
        raise ValueError("OpenAI API key is missing.")
    return OpenAI(api_key=api_key.strip())

def ask_ai(api_key: str, model: str, prompt: str, history=None,
           extra_context: str = "", system_prompt: str = "") -> str:
    client = get_client(api_key)
    default_system = (
        "You are a helpful study and career assistant. Explain clearly, use examples, "
        "and adapt to a student audience. Be honest when uncertain."
    )
    system = system_prompt or default_system
    if extra_context:
        system += "\n\nUse this retrieved context where relevant:\n" + extra_context
    messages = [{"role": "system", "content": system}]
    for item in (history or [])[-10:]:
        if item.get("role") in ("user", "assistant"):
            messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.4,
    )
    return response.choices[0].message.content or "The model returned an empty response."
