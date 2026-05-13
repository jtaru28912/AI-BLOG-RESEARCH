from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import BlogState

from agents import (
    research_agent,
    extractor_agent,
    summarizer_agent,
    insight_agent,
    blog_agent,
    seo_agent
)

workflow = StateGraph(BlogState)

workflow.add_node(
    "research",
    research_agent.fetch_papers_node
)

workflow.add_node(
    "extract",
    extractor_agent.extract_metadata_node
)

workflow.add_node(
    "summarize",
    summarizer_agent.summarize_papers_node
)

workflow.add_node(
    "insights",
    insight_agent.generate_insights_node
)

workflow.add_node(
    "blog",
    blog_agent.create_blog_node
)

workflow.add_node(
    "seo",
    seo_agent.optimize_seo_node
)

workflow.add_node(
    "faq",
    seo_agent.generate_faq_node
)

workflow.set_entry_point("research")

workflow.add_edge("research", "extract")

workflow.add_edge("extract", "summarize")

workflow.add_edge("summarize", "insights")

workflow.add_edge("insights", "blog")

workflow.add_edge("blog", "seo")

workflow.add_edge("seo", "faq")

workflow.add_edge("faq", END)

app_workflow = workflow.compile()