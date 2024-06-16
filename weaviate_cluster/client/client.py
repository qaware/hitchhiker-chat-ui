import os
import weaviate
import streamlit as st

from weaviate_cluster.client.st_weaviate_connection import WeaviateConnection


def get_env_vars():
    connect_config = {}
    for env_var in ["WEAVIATE_URL", "WEAVIATE_API_KEY", "OPENAI_KEY"]:
        if env_var not in os.environ:
            raise ValueError('Environment variable "%s" was not set' % env_var)
        connect_config[env_var] = os.environ.get(env_var)
    return connect_config


def connect_to_cluster():
    config = get_env_vars()

    print("host is "+config["WEAVIATE_URL"])
    return weaviate.connect_to_custom(http_host=config["WEAVIATE_URL"],
                                      http_port=8080,
                                      http_secure=False,
                                      grpc_host=config["WEAVIATE_URL"],
                                      grpc_port=50051,
                                      grpc_secure=False,
                                      auth_credentials=weaviate.auth.AuthApiKey(config["WEAVIATE_API_KEY"]),
                                      headers={'X-OpenAI-Api-key': config["OPENAI_KEY"]},
                                      additional_config=weaviate.config.AdditionalConfig(
                                          timeout=weaviate.config.Timeout(init=10))
                                      )


def connect_to_cluster_as_streamlit():
    config = get_env_vars()

    return st.connection(
        "weaviate",
        type=WeaviateConnection,
        url="http://" + config["WEAVIATE_URL"] + ":8080",
        api_key=config["WEAVIATE_API_KEY"],
        additional_headers={"X-OpenAI-Api-Key": config["OPENAI_KEY"]},
        max_entries=10,
        startup_period=25
    )
