"""
Contains function get_llm() that lets user choose which LLM to run this model on. It is flexible since different businesses have access to different APIs
"""
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(max_tokens: int = 4096):
    provider = os.getenv("LLM_PROVIDER", "gemini").strip().lower() #default provider is gemini
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Check your .env file.")
        model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        return ChatGoogleGenerativeAI(model=model, google_api_key=api_key)

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set. Check your .env file.")
        model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
        return ChatAnthropic(model=model, api_key=api_key)

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set. Check your .env file.")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(model=model, api_key=api_key)
    
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}'. Use 'gemini', 'anthropic', or 'openai'.")