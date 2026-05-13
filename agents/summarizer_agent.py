import asyncio

from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from prompts.summary_prompts import (
    SUMMARY_SYSTEM_PROMPT
)


async def summarize_single_paper(
    paper,
    llm
):

    response = await llm.ainvoke([

        SystemMessage(
            content=SUMMARY_SYSTEM_PROMPT
        ),

        HumanMessage(
            content=f"""
            Paper Title:
            {paper['title']}

            Abstract:
            {paper['summary']}
            """
        )
    ])

    return {

        "title": paper["title"],

        "summary": response.content,

        "link": paper["link"]
    }


async def summarize_papers_node(state):

    llm = state["llm"]

    tasks = [

        summarize_single_paper(
            paper,
            llm
        )

        for paper in state["extracted_data"]
    ]

    summaries = await asyncio.gather(*tasks)

    return {
        "summaries": summaries
    }