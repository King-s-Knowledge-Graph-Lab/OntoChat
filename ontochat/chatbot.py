from openai import OpenAI


MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
SEED = 1234


def chat_completion(api_key, messages):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        seed=SEED,
        temperature=TEMPERATURE,
    )
    return completion.choices[0].message.content


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
