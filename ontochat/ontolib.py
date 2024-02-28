"""
Functions operating on the verbalisation of an ontology, providing support for
generating documentation, extracting competency questions, and preliminarly
testing an ontology via competency questions.
"""
import re
import config
from openai import OpenAI
from tqdm import tqdm

cqe_prompt_a = "You are asked to provide a comprehensive list of competency "\
               "questions describing all the possible requirements that can be "\
               "addressed by the ontology described before."

cqt_prompt_a = "You are asked to infer if the ontology described before can "\
               "address the following competency question: \"{}\" "\
               "Valid answers are: Yes, No."

cqt_prompt_b = "You are asked to infer if the ontology described before can "\
               "address the following competency question: \"{}\" "\
               "Only reply: 'Yes', 'No' and provide an explanation after a comma."


class ChatInterface:

    def __init__(self,
                 api_key: str,
                 model_name: str = config.DEFAULT_MODEL,
                 sampling_seed: int = config.DEFAULT_SEED,
                 temperature: int = config.DEFAULT_TEMPERATURE):
        # Save client configuration for all calls
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.sampling_seed = sampling_seed
        self.temperature = temperature

    def chat_completion(self, messages, **kwargs):

        model = kwargs["model"] if "model" in kwargs else self.model_name
        temperature = kwargs["temperature"] if "temperature" in kwargs \
            else self.temperature  # this do not alter the class defaults

        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            seed=self.sampling_seed,
            temperature=temperature,
        )
        return completion.choices[0].message.content


def extract_competency_questions(onto_verbalisation: str,
                                 chat_interface: ChatInterface,
                                 prompt: str = cqe_prompt_a):
    """
    Extract competency questions from the verbalisation of an ontology.

    Parameters
    ----------
    onto_verbalisation : str
        A string expressing the ontology verbalisation as output from a
        supported method in the `verbaliser` module.
    chat_interface : ChatInterface
        An instance of a chat interface holding the API session.
    prompt : str, optional
        CQ extraction prompt, by default cqe_prompt_a

    Returns
    -------
    competency_questions : str
        A list of competency questions induced from the verbalisation.

    """    
    full_prompt = onto_verbalisation + "\n" + prompt
    conversation_history = [
        {"role": "system", "content": "You are an ontology expert."},
        {"role": "user", "content": full_prompt}
    ]

    competency_questions = chat_interface.chat_completion(
        conversation_history, model="gpt-3.5-turbo-16k")

    return competency_questions


def test_competency_questions(onto_verbalisation: str,
                              competency_questions: list[str],
                              chat_interface: ChatInterface,
                              cq_prompt: str = cqt_prompt_a):
    """
    Performs a preliminary test of the ontology to assess whether its
    verbalisation allows for addressing each competency questions given.

    Parameters
    ----------
    onto_verbalisation : str
        A string expressing the ontology verbalisation as output from a
        supported method in the `verbaliser` module.
    competency_questions: list[str]
        A list of competency questions to use for preliminary testing.
    chat_interface : ChatInterface
        An instance of a chat interface holding the API session.
    cq_prompt : str, optional
        CQ test prompt, by default cqt_prompt_a

    Returns
    -------
    cq_test_dict : dict
        A dictionary holding an outcome (yes/no) as a preliminary test of each
        competency question. Keys correspond to CQs.

    """    
    cq_test_dict = {}
    for cq in tqdm(competency_questions):
        full_prompt = onto_verbalisation + "\n" + cq_prompt.format(cq)
        conversation_history = [
            {"role": "system", "content": "You are an ontology engineer."},
            {"role": "user", "content": full_prompt}
        ]
        outcome = chat_interface.chat_completion(
            conversation_history, model="gpt-3.5-turbo-16k")
        match = re.search(r"^(Yes|No)(.*)", outcome)
        explanation = match.group(2) if match is not None else None
        cq_test_dict[cq] = (match.group(1), explanation)

    return cq_test_dict


def split_cq_test_data(cq_test_dict: dict):
    """
    Returns two lists to split input and output data.
    In doing so, `Yes` gets 1 and `No` receives 0.
    """
    cq_x, cq_y, cq_e = [], [], []
    for cq, outcome in cq_test_dict.items():
        cq_x.append(cq)
        if outcome[0] not in ["Yes", "No"]:
            raise ValueError(f"Invalid test outcome: {outcome}")
        cq_y.append(1 if outcome[0] == "Yes" else 0)
    return cq_x, cq_y
