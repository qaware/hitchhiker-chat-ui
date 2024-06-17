import weaviate
from weaviate_cluster.client.client import connect_to_cluster, connect_to_cluster_as_streamlit


def query_ai_solutions(text):
    with connect_to_cluster() as client:
        solutions = client.collections.get("Solutions")
        solution_query_result = solutions.query.near_text(
            limit = 1,
            query=text,
            return_metadata=weaviate.classes.query.MetadataQuery(certainty=True, distance=True)
        )
        print("in query_ai_solutions")
        print(solution_query_result.objects[0])
        return solution_query_result.objects[0]


def query_talks(text):
    with connect_to_cluster() as client:
        talks = client.collections.get("ConferenceTalks")
        talk_query_result = talks.query.near_text(
            limit=3,
            query=text,
            return_metadata=weaviate.classes.query.MetadataQuery(certainty=True, distance=True)
        )
        print(talk_query_result.objects[0])
        return talk_query_result.objects


def query_using_graphql(text):
    ai_solutions_query = """
    {{
        Get {{
            Solutions(
                nearText: {{ concepts: "{input}" }}
            ) 
            {{
                phase
                question
                answer
                categories
                solution
                link
                price
                _additional {{
                    distance
                    certainty
                    score
                    distance
                }}
            }}
        }}
    }}
    """
    conference_query = """
    {{
        Get {{
            ConferenceTalks(
                nearText: {{ concepts: "{input}" }}
            ) 
            {{
                title
                time
                speaker
                company
                keywords
                abstract
                _additional {{
                    distance
                    certainty
                    score
                    distance
                }}
            }}
        }}
    }}
    """
    gql = ai_solutions_query.format(input=text)

    conn = connect_to_cluster_as_streamlit()
    # return pandas Dataframe
    return conn.query(gql, ttl=None)
