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
