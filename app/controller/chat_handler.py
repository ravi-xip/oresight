import logging

from elasticsearch_dsl import Search

from llm.aiclient import AIClient


def search_similar_bio(query_text: str):
    openai_client = AIClient()
    query_embedding = openai_client.embedding(query_text)

    s = Search(index="new-prospect-index").query(
        {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'bio_embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }
    )
    return s.execute()


def get_prospect_page_url(name: str) -> str:
    # Remove /u/ from the start of the name if it exists
    name = name.replace("/u/", "").replace("/user/", "").replace("u/", "").replace("user/", "")
    return f"https://www.reddit.com/user/{name}/"


def create_chunk(hit) -> str:
    chunk = "\n--------------------------------------------------------------\n"
    chunk += f"Prospect Name {hit.name} Prospect Bio {hit.bio} is a {hit.category}"
    chunk += "\n--------------------------------------------------------------\n"
    chunk += f"URL: {get_prospect_page_url(hit.name)}\n"
    chunk += "\n--------------------------------------------------------------\n"
    return chunk


class ChatController:
    def __init__(self):
        self.ai_client = AIClient()

    def chat(self, query: str, conversation: str):
        # Step I: Search for similar bios
        response = search_similar_bio(query)

        # Step II: Create a list of chunks from the response
        chunks = []
        for hit in response:
            try:
                chunks.append(create_chunk(hit))
            except Exception as e:
                logging.error(f"Error while creating a chunk: {e}")
                continue

        # Step III: Trigger an LLM query for all the chunks combined
        response = self.ai_client.explain(query, conversation, chunks)
        logging.debug(f"response: {response}")

        # Step IV: Return the response
        return response
