from openai import OpenAI
from openai import APIConnectionError, APITimeoutError, AuthenticationError, RateLimitError

from ontochat.config import DEFAULT_MODEL, DEFAULT_SEED, DEFAULT_TEMPERATURE


def chat_completion(api_key, messages):
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            seed=DEFAULT_SEED,
            temperature=DEFAULT_TEMPERATURE,
        )
    except APITimeoutError as e:
        return f"Request timed out. Retry your request after a brief wait. Error information: {e}"
    except APIConnectionError as e:
        return f"Issue connecting to our services. Check your network settings, proxy configuration, " \
               f"SSL certificates, or firewall rules. Error information: {e}"
    except AuthenticationError as e:
        return f"Your API key or token was invalid, expired, or revoked. Error information: {e}"
    except RateLimitError as e:
        return f"You have hit your assigned rate limit. Error information: {e}"
    return response.choices[0].message.content


def build_messages(history):
    """
    Convert Gradio Chatbot history to OpenAI client messages
    :param history: List of dictionaries with 'role' and 'content' keys
    :return: List of OpenAI client messages
    """
    messages = []
    for item in history:
        messages.append({"role": item["role"], "content": item["content"]})
    return messages
