def extract_metadata_node(state):

    extracted_data = []

    for paper in state["papers"]:

        extracted_data.append({

            "title": paper["title"],

            "authors": paper["authors"],

            "summary": paper["summary"],

            "published": paper["published"],

            "link": paper["link"]
        })

    return {
        "extracted_data": extracted_data
    }