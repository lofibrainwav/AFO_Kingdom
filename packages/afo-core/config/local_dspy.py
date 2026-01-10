import os

import dspy


def configure_local_dspy():
    """
    AFO Kingdom Local DSPy/Ollama Configuration.
    Prioritizes local OLLAMA over remote OpenAI for 'Goodness/Serenity'.
    """
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    print(f"[DSPy][LOCAL] Configuring Ollama: model={ollama_model}, url={ollama_base_url}")

    try:
        lm = dspy.OllamaLocal(model=ollama_model, base_url=ollama_base_url)
        dspy.settings.configure(lm=lm)
        return True
    except Exception as e:
        print(f"[DSPy][LOCAL][ERROR] Failed to configure Ollama: {e}")
        return False


if __name__ == "__main__":
    configure_local_dspy()
