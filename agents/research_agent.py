import arxiv


def fetch_papers_node(state):

    topic = state["topic"]

    num_papers = state["num_papers"]

    search = arxiv.Search(
        query=topic,
        max_results=num_papers,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in search.results():

        papers.append({

            "title": result.title,

            "authors": [
                author.name
                for author in result.authors
            ],

            "summary": result.summary,

            "published": str(
                result.published
            ),

            "link": result.entry_id
        })

    return {
        "papers": papers
    }