import chromadb


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="research_blogs"
)


def store_blog(topic, blog):

    collection.add(
        documents=[blog],
        ids=[topic]
    )