"""
Interface functions
"""

import json

from ontochat.chatbot import chat_completion, build_history, build_messages
from ontochat.analysis import compute_embeddings, agglomerative_clustering, hdbscan_clustering, llm_cq_clustering


def set_openai_api_key(api_key: str):
    global openai_api_key
    openai_api_key = api_key
    return "API key has been set!"


def user_story_init_generator(persona, goal, sample_data):
    # if os.environ.get("OPENAI_API_KEY") is None:
    #     # openai.api_key = api_key
    #     os.environ["OPENAI_API_KEY"] = api_key
    messages = [{
        "role": "system",
        "content": "I am a conversational ontology engineering assistant, to help the user generate user stories, "
                   "elicit requirements, and extract and analyze competency questions. In ontology engineering, "
                   "a user story contains all the requirements from the perspective of an end user of the ontology. "
                   "It is a way of capturing what a user needs to achieve with the ontology while also providing "
                   "context and value. I will guide the user step-by-step to create a user story and generate "
                   "competency questions from it."
    }, {
        "role": "user",
        "content": f"The persona of the user is {persona}. The goal of the user is {goal}. A sampple of data is "
                   f"{sample_data}. Write a user story for the ontology that fit into the information provided."
    }]
    bot_message = chat_completion(openai_api_key, messages)
    messages.append({
        "role": "system",
        "content": bot_message
    })
    history = build_history(messages)
    return bot_message, history


def user_story_generator(message, history):
    """

    :param message:
    :param history:
    :return:
    """
    messages = build_messages(history)
    bot_message = chat_completion(openai_api_key, messages)
    history.append((message, bot_message))
    return bot_message, history


def cq_generator(messages, numbers):
    """

    :param messages:
    :param numbers:
    :return:
    """
    messages = [
        {
            "role": "system",
            "content": "You are an ontology engineer."
        }, {
            "role": "user",
            "content": f"Please generate {numbers} competency questions based on the user story: {messages}"
        }  # TODO: format constraint
    ]
    response = chat_completion(openai_api_key, messages)
    return response


def clustering_generator(cqs, cluster_method, n_clusters):
    """

    :param cqs:
    :param cluster_method:
    :param n_clusters:
    :return:
    """
    cqs, cq_embeddings = compute_embeddings(cqs)

    if cluster_method == "Agglomerative clustering":
        cq_clusters, cluster_image = agglomerative_clustering(cqs, cq_embeddings, n_clusters)
    elif cluster_method == "HDBSCAN":
        cq_clusters, cluster_image = hdbscan_clustering(cqs, cq_embeddings, n_clusters)
    else:  # cluster_method == "LLM clustering"
        cq_clusters, cluster_image = llm_cq_clustering(cqs, n_clusters, openai_api_key)

    return cluster_image, json.dumps(cq_clusters, indent=4)
