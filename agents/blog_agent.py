from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from prompts.blog_prompts import (
    BLOG_SYSTEM_PROMPT
)


async def create_blog_node(state):

    llm = state["llm"]

    summaries_text = "\n\n".join([

        f"""
        Title:
        {summary['title']}

        Summary:
        {summary['summary']}
        """

        for summary in state["summaries"]
    ])

    response = await llm.ainvoke([

        SystemMessage(
            content=BLOG_SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
            Topic:
            {state['topic']}

            Research Summaries:
            {summaries_text}

            Insights:
            {state['insights']}

            Generate a detailed blog article.
            """
        )
    ])

    return {
        "blog": response.content
    }