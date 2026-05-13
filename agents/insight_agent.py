from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from prompts.insight_prompts import (
    INSIGHT_SYSTEM_PROMPT
)


async def generate_insights_node(state):

    llm = state["llm"]

    combined_summaries = "\n\n".join([
        summary["summary"]
        for summary in state["summaries"]
    ])

    response = await llm.ainvoke([

        SystemMessage(
            content=INSIGHT_SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
            Analyze these research summaries carefully.

            Research Summaries:
            {combined_summaries}
            """
        )
    ])

    return {
        "insights": response.content
    }