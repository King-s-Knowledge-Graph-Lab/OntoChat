from openai import OpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#Mongo DB set-up
uri = "mongodb+srv://OntoChatAdmin:DkAvUZF03TbAlp6H@ontochatdb.tawiqmm.mongodb.net/?retryWrites=true&w=majority"
client_mongo = MongoClient(uri, server_api=ServerApi('1'))
db = client_mongo.get_database('OntoChatDB')
global collection
collection = db['userChatHistory']
global instance_id
instance_id = id(object())

#Local data logging
with open('chatHistory.txt', "w") as file:
    file.write("===Your chatHistory===\n")



#OpenAI Set-up
MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0
SEED = 1234
global client



def client_import(client_away):
    global client
    client = client_away
    

def chat_completion(messages):
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        seed=SEED,
        temperature=TEMPERATURE,
    )
    document = {
    'id': instance_id ,
    'input_sequence': messages,
    'output': completion.choices[0].message.content
    }
    #Write chat data to mongodb and .txt in local machine
    collection.insert_one(document)
    with open('chatHistory.txt', "a") as file:
        file.write(str(document))
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
