"""
Competency questions analysis functions
Partially inherited from [idea](https://github.com/polifonia-project/idea)
"""

import ast
import io
import re
from collections import defaultdict

import numpy as np

from PIL import Image
from matplotlib import pyplot as plt

from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering, HDBSCAN
from scipy.cluster.hierarchy import dendrogram

from ontochat.chatbot import chat_completion


def preprocess_competency_questions(cqs):
    # preprocess competency questions: string -> list of strings
    cqs = cqs.split("\n")
    # # keep index
    # cqs = [re.split(r'\.\s', cq, 1) for cq in cqs]
    # cqs = [{cq[0]: cq[1]} for cq in cqs]
    # cqs = [re.split(r'\.\s', cq, 1)[1] for cq in cqs]

    # clean
    cleaned_cqs = []
    for q in cqs:  # FIXME to move
        # Collapse complex questions in a sentence
        q = q.replace("\n", "; ")
        # Remove tabular occurrences for metadata
        q = q.replace("\t", " ")
        # Collapse multiple empty spaces
        q = re.sub(r"[ ]+", " ", q)
        # Discard inconsistent punctuation
        q = re.sub(r";[ ]*;", ";", q)
        cleaned_cqs.append(q)

    return cleaned_cqs


def compute_embeddings(cqs, model="all-MiniLM-L6-v2", device="cpu"):
    """
    Compute sentence-level embeddings of competency questions

    :param cqs:
    :param model:
    :param device:
    :return:
    """
    cleaned_cqs = preprocess_competency_questions(cqs)

    model = SentenceTransformer(model, device=device)
    embeddings = model.encode(cleaned_cqs)

    # Normalisation of CQ embeddings to unit length
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    return cleaned_cqs, embeddings


def agglomerative_clustering(cqs, embeddings, n_clusters=None, metric="euclidean", distance_threshold=None):
    """

    :param cqs:
    :param embeddings:
    :param n_clusters:
    :param metric:
    :param distance_threshold:
    :return:
    """
    clustering_model = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric=metric,
        distance_threshold=distance_threshold,
        compute_distances=True
    )
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    clustered_cqs = defaultdict(list)
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        clustered_cqs[str(cluster_id)].append(cqs[sentence_id])

    pil_image = plot_dendrogram(
        clustering_model,
        orientation='right',
        labels=list(range(1, len(cqs) + 1)),
        # labels=cqs,
        truncate_mode=None,
        # p=3,
        show_leaf_counts=False,
    )

    return clustered_cqs, pil_image


def plot_dendrogram(model, **kwargs):
    """ Create linkage matrix and then plot the dendrogram
    source: https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html

    :param model:
    :param kwargs:
    :return:
    """
    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    plt.tight_layout()
    # plt.figure(figsize=(40, 20))
    dendrogram(linkage_matrix, **kwargs)
    # plt.subplots_adjust(left=0.25, right=1.025, top=0.9, bottom=0.075)
    # plt.savefig(figsave_path)
    # plt.show()
    # convert the figure into a PIL image
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    return Image.open(buf)


def response_parser(response):
    try:
        response = ast.literal_eval(response)
    except (ValueError, TypeError, SyntaxError):
        response = ""
    return response


def llm_cq_clustering(cqs, n_clusters, api_key, paraphrase_detection=False):
    """

    :param cqs:
    :param n_clusters:
    :param api_key:
    :param paraphrase_detection:
    :return:
    """
    conversation_history = [
        {"role": "system", "content": "You are an ontology engineer."}
    ]
    # paraphrase detection before clustering
    if paraphrase_detection:
        # 1. paraphrase detection
        prompt_1 = "Perform paraphrase detection for the following competency questions: {}. " \
                   "Return a Python list of duplicate competency questions.".format(cqs)

        conversation_history.append({"role": "user", "content": prompt_1})
        response = chat_completion(api_key, conversation_history)
        print("{} CQs remaining after paraphrase detection.".format(len(cqs) - len(response_parser(response))))

        # 2. clustering
        if n_clusters:
            prompt_2 = f"Clustering the competency questions into {n_clusters} clusters based on their topics. " \
                        "Keep the granularity of the topic in each cluster at a similar level. " \
                        "Return in JSON format, such as: {'cluster 1 topic': " \
                        "['competency question 1', 'competency question 2']}:"
        else:
            prompt_2 = f"Clustering the competency questions into clusters based on their topics. " \
                       "Keep the granularity of the topic in each cluster at a similar level. " \
                       "Return in JSON format, such as: {'cluster 1 topic': " \
                       "['competency question 1', 'competency question 2']}:"
        conversation_history.append({"role": "assistant", "content": response})  # previous response
        conversation_history.append({"role": "user", "content": prompt_2})
        response = chat_completion(api_key, conversation_history)
        # print("Output is: \"{}\"".format(response))

    else:  # clustering only
        if n_clusters:
            prompt_2 = f"Given the competency questions: {cqs}, clustering them into {n_clusters} clusters based on " \
                       f"the topics."
        else:
            prompt_2 = f"Given the competency questions: {cqs}, clustering them into clusters based on the topics."
        prompt_2 += "Keep the granularity of the topic in each cluster at a similar level. " \
                    "Return in JSON format, such as: {'cluster 1 topic': " \
                    "['competency question 1', 'competency question 2']}:"
        conversation_history.append({"role": "user", "content": prompt_2})
        response = chat_completion(api_key, conversation_history)
        # print("Output is: \"{}\"".format(response))

    # # 3. assign labels
    # prompt_2 = "Clustering the competency questions based on their topics. Return in JSON format, " \
    #            "such as: {'cluster 1 topic': ['competency question 1', 'competency question 2']}:"
    # conversation_history.append({"role": "assistant", "content": response})  # previous response
    # conversation_history.append({"role": "user", "content": prompt_2})
    # response = chat_completion(conversation_history)
    # response = response.choices[0].message.content
    # print("Output is: \"{}\"".format(response))

    return response_parser(response), Image.new("RGB", (640, 480), (255, 255, 255))
