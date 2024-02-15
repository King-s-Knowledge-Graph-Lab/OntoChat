from openai import OpenAI


client = OpenAI()
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
SEED = 1234


def chat_completion(messages):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        seed=SEED,
        temperature=TEMPERATURE,
    )
    return completion.choices[0].message.content


def build_history(messages):
    """
    convert OpenAI client messages to gradio.Chatbot history
    :param messages:
    :return:
    """
    message_list = [None, ]
    for item in messages:
        message_list.append(item["content"])
    history = [[message_list[i], message_list[i + 1]] for i in range(0, len(message_list), 2)]
    return history


def build_messages(history):
    """
    convert gardio.Chatbot history to OpenAI client messages
    :param history:
    :return:
    """
    messages = list()
    for item in history:
        messages.append({"role": "user", "content": item[0]})
        messages.append({"role": "system", "content": item[1]})
    return messages[1:]
