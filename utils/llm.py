from langchain_openai import ChatOpenAI


def get_llm(
    model_name="gpt-4o-mini",
    temperature=0.3,
    api_key=None
):

    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=api_key
    )