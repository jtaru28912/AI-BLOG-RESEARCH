from typing import TypedDict, List, Dict, Any


class BlogState(TypedDict):

    topic: str

    num_papers: int

    llm: Any

    papers: List[Dict]

    extracted_data: List[Dict]

    summaries: List[Dict]

    insights: str

    blog: str

    seo_blog: str

    faq: List[Dict]