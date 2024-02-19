"""
Interface functions
"""

import json

from ontochat.chatbot import chat_completion, build_messages
from ontochat.analysis import compute_embeddings, agglomerative_clustering, hdbscan_clustering, llm_cq_clustering


def set_openai_api_key(api_key: str):
    global openai_api_key
    openai_api_key = api_key
    return "API key has been set! Now you can chat with the chatbot. Enjoy :)"


def user_story_generator(message, history):
    print(history)
    if len(history) == 1:  # initial round
        messages = [{
            "role": "system",
            "content": "Hello! I am OntoChat, your conversational ontology engineering assistant."
        }, {
            "role": "user",
            "content": "I am a domain expert trying to create a user story to be used by ontology engineers. You are "
                       "the ontology expert. Only ask the following question once I have responded. Ask for the"
                       "specifications to generate a user story as a user of the system, which should include: 1. The "
                       "Persona: What are the name, occupation, skills and interests of the user? 2. The Goal: What is "
                       "the goal of the user? Are they facing specific issues? 3. Example Data: Do you have examples "
                       "of the specific data available? Make sure you have answers to all three questions before "
                       "providing a user story. Only ask the next question once I have responded."
        }, {
            "role": "system",
            "content": "Sure. Let's start with the persona. What are the name, occupations, skills, interests of the user?"
        }, {
            "role": "user",
            "content": message
        }]
    else:
        messages = build_messages(history)
        messages.append({
            "role": "user",
            "content": message
        })
    bot_message = chat_completion(openai_api_key, messages)
    history.append([message, bot_message])
    return bot_message, history, ""


def cq_generator(message, history):
    """
    generate competency questions based on the user story
    format constraint may not be necessary if we only use LLMs for clustering
    :param message:
    :param history:
    :return:
    """
    if (len(history)) == 1:  # initial round
        messages = [
            {
                "role": "system",
                "content": "I am OntoChat, your conversational ontology engineering assistant. Here is the second step "
                           "of the system. Please give me your user story and tell me how many competency questions "
                           "you want."
            }, {
                "role": "user",
                "content": message
            }
        ]
    else:
        messages = build_messages(history)
        messages.append({
            "role": "user",
            "content": message
        })
    bot_message = chat_completion(openai_api_key, messages)
    history.append([message, bot_message])
    return bot_message, history, ""


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
