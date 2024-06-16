import json
import weaviate
import weaviate.classes.config as wc

from weaviate_cluster.client.client import connect_to_cluster

def load_data(client: weaviate.WeaviateClient):
    with open('weaviate_cluster/data/galaxy.json', 'r') as file:
        data = json.load(file)

    solution_objs = list()
    for i, d in enumerate(data):
        solution_objs.append({
            "phase": d["Phase"],
            "question": d["Question"],
            "answer": d["Answer"],
            "categories": d["Categories"],
            "solution": d["Solution"],
            "link": d["Link"],
            "price": d["Price"],
        })

    solutions = client.collections.get("Solutions")
    solutions.data.insert_many(solution_objs)

    with open('weaviate_cluster/data/conference_talks.json', 'r') as file:
        data = json.load(file)

    conf_talk_objects = list()
    for i, d in enumerate(data):
        conf_talk_objects.append({
            "title": d["title"],
            "time": d["time"],
            "speaker": d["speaker"],
            "company": d["company"],
            "keywords": d["keywords"],
            "abstract": d["abstract"],
        })
    conf_talks = client.collections.get("ConferenceTalks")
    conf_talks.data.insert_many(conf_talk_objects)

def main() -> None:
    print("=== LOADING HITCHHIKER DATA ===")

    with connect_to_cluster() as client:
        if not client.is_ready():
            raise Exception("Weaviate cluster is not ready!")

        client.collections.delete(name="ConferenceTalks")
        client.collections.create(name="ConferenceTalks",
                                  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
                                  vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
                                  # Ensure the `generative-openai` module is used for generative queries
                                  generative_config=wc.Configure.Generative.openai())

        client.collections.delete(name="Solutions")
        client.collections.create(name="Solutions",
                                  vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
                                  generative_config=wc.Configure.Generative.openai())

        load_data(client)

if __name__ == "__main__":
    main()
