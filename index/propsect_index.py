import os

from elasticsearch_dsl import Document, Keyword, Text, connections, DenseVector, Search

from llm.aiclient import AIClient


class ProspectIndex(Document):
    name = Text()
    email = Keyword()
    phone = Keyword()
    category = Keyword()
    url = Keyword()
    bio = Text(analyzer='snowball')
    bio_embedding = DenseVector(dims=1536)
    interest = Text(analyzer='snowball')
    interest_embedding = DenseVector(dims=1536)

    class Index:
        name = 'new-prospect-index'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        openai_client = AIClient()
        self.bio_embedding = openai_client.embedding(self.bio)
        return super(ProspectIndex, self).save(**kwargs)


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


if __name__ == '__main__':
    # Connect to localhost:9200 by default.
    es_host = os.environ.get('ES_HOST', 'localhost')
    es_port = os.environ.get('ES_PORT', '9200')
    connections.create_connection(hosts=[f'http://{es_host}:{es_port}'])

    # Create the mappings in Elasticsearch
    ProspectIndex.init()

    # Delete all documents from the index and start fresh
    # Prospect._index.delete(ignore=404)

    # Create and save and prospect
    ProspectIndex(meta={'id': 1}, name='John Doe', interest='haha',
                  email='john@doe.com', phone='123456789', bio='John Doe was a great investor').save()

    ProspectIndex(meta={'id': 2}, name='Jack Done', interest='haha',
                  email='john@doe.com', phone='123456789', bio='John Doe was a great golfer').save()

    # Display cluster health
    print(connections.get_connection().cluster.health())

    # Try searching
    prospects = ProspectIndex.search().filter('term', name='john')
    print(f'Found {prospects.count()} prospects')
    for prospect in prospects:
        print(f'Found {prospect.name} with id {prospect.meta.id}')

    # Query 2:
    response = search_similar_bio('Golfer')
    print(f'Found {response.hits.total.value} prospects')
    for prospect in response:
        print(f'Found {prospect.name} with id {prospect.meta.id}')
