import ast

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from prompts.seo_prompts import (
    SEO_SYSTEM_PROMPT
)


async def optimize_seo_node(state):

    llm = state["llm"]

    response = await llm.ainvoke([

        SystemMessage(
            content=SEO_SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
            Optimize this blog.

            Topic:
            {state['topic']}

            Blog:
            {state['blog']}
            """
        )
    ])

    return {
        "seo_blog": response.content
    }


async def generate_faq_node(state):

    llm = state["llm"]

    response = await llm.ainvoke([

        SystemMessage(
            content="""
            You are an expert educational FAQ generator.

            Generate highly relevant FAQs from the blog.

            Rules:
            - no hallucinations
            - concise answers
            - beginner friendly
            - factual correctness

            Return ONLY valid Python list format.
            """
        ),

        HumanMessage(
            content=f"""
            Blog:
            {state['seo_blog']}
            """
        )
    ])

    try:

        faq = ast.literal_eval(
            response.content
        )

    except Exception:

        faq = []

    return {
        "faq": faq
    }