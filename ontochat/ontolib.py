"""
Functions operating on the verbalisation of an ontology, providing support for
generating documentation, extracting competency questions, and preliminarly
testing an ontology via competency questions.
"""

import config
from openai import OpenAI

cqe_prompt_a = "You are asked to provide a comprehensive list of competency "\
               "questions describing all the possible requirements that can be "\
               "addressed by the ontology."

cqt_prompt_a = "You are asked to infer if the ontology described before can "\
               "address the following competency question: \"{}\" "\
               "Valid answers are: Yes, No."


class ChatInterface:

    def __init__(self,
                 api_key: str,
                 model_name: str = config.DEFAULT_MODEL,
                 sampling_seed: int = config.DEFAULT_MODEL,
                 temperature: int = config.DEFAULT_TEMPERATURE):
        # Save client configuration for all calls
        self.client = OpenAI(api_key=api_key)
        self.modmodel_nameel = model_name
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
                                 chat_interface: ChatInterface.chat_completion,
                                 prompt: str = cqe_prompt_a):
    
    full_prompt = onto_verbalisation + "\n" + prompt
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": full_prompt}
    ]

    competency_questions = chat_interface.chat_completion(
        conversation_history, model="gpt-3.5-turbo-16k")

    return competency_questions


def test_competency_questions(onto_verbalisation: str,
                              competency_questions: list[str],
                              chat_interface: ChatInterface.chat_completion,
                              cq_prompt: str = cqt_prompt_a):

    cq_test_dict = {}
    for cq in competency_questions:
        full_prompt = onto_verbalisation + "\n" + cq_prompt.format(cq)
        conversation_history = [
            {"role": "system", "content": "You are an ontology engineer."},
            {"role": "user", "content": full_prompt}
        ]
        outcome = chat_interface.chat_completion(
            conversation_history, model="gpt-3.5-turbo-16k")
        cq_test_dict[cq] = outcome

    return cq_test_dict
