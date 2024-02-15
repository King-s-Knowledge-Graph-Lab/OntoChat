from openai import OpenAI





def chat_completion(messages):
    client = OpenAI()
    MODEL_NAME = "gpt-3.5-turbo"
    TEMPERATURE = 0
    SEED = 1234
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        seed=SEED,
        temperature=TEMPERATURE,
    )
    return completion.choices[0].message.content
