"""
Interface functions
"""

import json

from ontochat.chatbot import chat_completion
from ontochat.analysis import compute_embeddings, agglomerative_clustering, hdbscan_clustering, llm_cq_clustering


def user_story_generator(message, history):
    """

    :param message:
    :param history:
    :return:
    """
    if len(history) == 1:
        bot_message = "What is the goal of the user? Are they facing specific issues?"  # goal
    elif len(history) == 2:
        bot_message = "Do you have examples of data?"  # example
    else:
        client_messages = [{
            "role": "system",
            "content": "Hello! I am OntoChat, your conversational ontology engineering assistant, to help you "
                       "generate user stories, elicit requirements, and extract and analyze competency questions. In "
                       "ontology engineering, a user story contains all the requirements from the perspective of an "
                       "end user of the ontology. It is a way of capturing what a user needs to achieve with the "
                       "ontology while also providing context and value. This demo will guide you step-by-step to "
                       "create a user story and generate competency questions from it."
        }]
        for conversation in history[1:]:
            client_messages.append({"role": "user", "content": conversation[0]})
            client_messages.append({"role": "system", "content": conversation[1]})
        client_messages.append({"role": "user", "content": "Can you wrtie a user story for ontology?"})
        bot_message = chat_completion(client_messages)
    return bot_message


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
    response = chat_completion(messages)
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
        cq_clusters, cluster_image = llm_cq_clustering(cqs, n_clusters)

    print(cq_clusters)
    return cluster_image, json.dumps(cq_clusters, indent=4)
