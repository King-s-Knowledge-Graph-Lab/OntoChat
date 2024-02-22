"""
Interface functions
"""

import json

from ontochat.chatbot import chat_completion, build_messages
from ontochat.analysis import compute_embeddings, agglomerative_clustering, llm_cq_clustering
from ontochat.verbaliser import verbalise_ontology


def set_openai_api_key(api_key: str):
    global openai_api_key
    openai_api_key = api_key
    return "API key has been set! Now you can chat with the chatbot. Enjoy :)"


def user_story_generator(message, history):
    instructions = [{
        "role": "system",
        "content": "You are a conversational ontology engineering assistant."
    }, {
        "role": "user",
        "content": "I am a domain expert trying to create a user story to be used by ontology engineers. You are the "
                   "ontology expert. Only ask the following question once I have responded. Ask for the"
                   "specifications to generate a user story as a user of the system, which should include: 1. The "
                   "Persona: What are the name, occupation, skills and interests of the user? 2. The Goal: What is "
                   "the goal of the user? Are they facing specific issues? 3. Example Data: Do you have examples of "
                   "the specific data available? Make sure you have answers to all three questions before providing "
                   "a user story. Only ask the next question once I have responded. And you should also ask questions "
                   "to elaborate on more information after the user provides the initial information, and ask for "
                   "feedback and suggestions after the user story is generated."
    }]
    messages = build_messages(history)
    messages.append({
        "role": "user",
        "content": message
    })
    bot_message = chat_completion(openai_api_key, instructions + messages)
    # post-processing response
    history.append([message, bot_message])
    print(history)
    return bot_message, history, ""


# def load_user_story_prompt():
#     """
#
#     :return:
#     """
#     prompt = """
#     Now create the full user story.The user story should be written in the following structure:
#
#     Title: Which topics are covered by the user story?
#
#     Persona: What is the occupation of the user and what are their goals?
#
#     Goal:
#     Keywords: provide 5-10 keywords related to the user story
#     Provide the issues a user is facing and how our application can help reach their goals.
#
#     Scenario:
#     Write out a scenario, where the user could use a structured knowledge base to help with their work.
#
#     Example Data:
#
#     Think of a list of requirements and provide example data for each requirement. Structure the example data by requirements
#     Example data should by simple sentences.
#     These are possible formats:
#     One sonata is a “Salmo alla Romana”.
#     A concert played in San Pietro di Sturla for exhibition was recorded by ethnomusicologist Mauro Balma in 1994.
#     The Church of San Pietro di Sturla is located in Carasco, Genova Province.
#     The Sistema Ligure is described in the text “Campanari, campane e campanili di Liguria” By Mauro Balma, 1996.
#     """
#     return prompt


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


def load_example_user_story():
    """
    load example user story
    TODO: more examples
    :return:
    """
    f = open("data/Linka#1_MusicKnowledge.md", "r")
    return f.read()


def clustering_generator(cqs, cluster_method, n_clusters):
    """

    :param cqs:
    :param cluster_method:
    :param n_clusters: default ''
    :return:
    """
    if n_clusters:
        n_clusters = int(n_clusters)

    cqs, cq_embeddings = compute_embeddings(cqs)

    if cluster_method == "Agglomerative clustering":
        cq_clusters, cluster_image = agglomerative_clustering(cqs, cq_embeddings, n_clusters)
    else:  # cluster_method == "LLM clustering"
        cq_clusters, cluster_image = llm_cq_clustering(cqs, n_clusters, openai_api_key)

    return cluster_image, json.dumps(cq_clusters, indent=4)


def ontology_testing(ontology_file, ontology_desc, cqs):
    """

    :param ontology_file:
    :param ontology_desc:
    :param cqs:
    :return:
    """
    verbalisation = verbalise_ontology(ontology_file, ontology_desc, "")
    messages = [{
        "role": "system",
        "content": "Please (1) provide a description of the ontology uploaded to provide basic information and "
                   "additional context, (2) give the competency questions (CQs) that you want to test with."
    }, {
        "role": "user",
        "content": verbalisation + "\n" + f"Given the above ontology, please label each competency question: {cqs} to "
                                          f"determine whether it is addressed properly or not. Format your response in"
                                          f" ['yes': 'CQ1', 'no': 'CQ2', ...]."
    }]
    bot_message = chat_completion(openai_api_key, messages)
    return bot_message
