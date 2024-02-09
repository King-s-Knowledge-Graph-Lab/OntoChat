import gradio as gr
from openai import OpenAI

#GPT setting
with open('API_key.txt', 'r') as file:
    api_key = file.readline().strip()
client = OpenAI(api_key= api_key)
def chat_with_gpt():
    global messages
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    return completion.choices[0].message

persona = "What is the name of user, what is the occupation of the user, and what are their skills and interests?"
Goal = "What is the goal of the user? Are they facing specific issues?"
Example = "Do you have examples of the specific data available?"

def interface(message, history):
    global i
    global messages
    if i==0:
        messages.append( {"role": "user", "content": f"{message}"})
        messages.append( {"role": "system", "content": f"{Goal}"})
        i+=1
        return f"{Goal}"
    elif i==1:
        messages.append( {"role": "user", "content": f"{message}"})
        messages.append( {"role": "system", "content": f"{Example}"})
        i+=1
        return f"{Example}"
    elif i==2:
        messages.append( {"role": "user", "content": f"{message}can you wrtie a user story for ontology?"})
        response = chat_with_gpt()
        messages.append( {"role": "system", "content": f"{response.content}"})
        i+=1
        return f"{response.content}"
    else:
        messages.append( {"role": "user", "content": f"{message}"})
        response = chat_with_gpt()
        messages.append( {"role": "system", "content": f"{response.content}"})
        return f"{response.content}"



chatbot = gr.Chatbot(value=[(None, persona)])

chat_interface = gr.ChatInterface(
    chatbot=chatbot,
    fn=interface,
    textbox=gr.Textbox(placeholder="Please explain your user story to me :)", container=False, scale=7),
    title="IDEA++",
    description="Hello! I am your UserStoryWizard, here to help you in all the steps to create a good user story. A user story contains all the requirements from the perspective of an end user of the system. It is a way of capturing what a user needs to achieve with a product or system, while also providing context and value. I am gonna guide you through each step and ask you question by question and then use your inputs to create a user story. Once you are ready, start answering the following questions. Once you think you provided all the information necessary, just press the corresponding button below. \n What is the name of user, what is the occupation of the user, and what are their skills and interests?",
    theme="soft",
    examples=["The user is a musicologist named Mark. He's an expert in western and an experienced musician. He plays piano and guitar.", "The goal of the user is to analyse analogies and simmetries between music score, with a particular focus on harmony and the lyrics of the music piece", 'an example of data would be: - "let it be" by "The Beatles" has a sequence of chord composed by "F, Amin, F" that is recurring every time the lyrics say "Let it be" - the lyrics of "Running with the devil" by "Van Halen" has a recurring chord sequince for the chorus and a recurring chord sequence for the bridge'],
    cache_examples=False,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
)
def CQGenerator(numbers):
    questions = f"Please {numbers} competency questions generation based on the generated user story"
    messages.append( {"role": "user", "content": f"{questions}"})
    response = chat_with_gpt()
    return f"{response.content}"

CQ= gr.Interface(fn=CQGenerator, inputs=gr.Slider(20, 60, step=1), outputs="textbox")

demo = gr.TabbedInterface([chat_interface, CQ], ["UserStoryAssistant","CompetencyQuestions"])

if __name__ == "__main__":
    global message
    global i
    instruction = "Hello! I am your UserStoryWizard, here to help you in all the steps to create a good user story. A user story contains all the requirements from the perspective of an end user of the system. It is a way of capturing what a user needs to achieve with a product or system, while also providing context and value. I am gonna guide you through each step and ask you question by question and then use your inputs to create a user story. Once you are ready, start answering the following questions. Once you think you provided all the information necessary, just press the corresponding button below. \n What is the name of user, what is the occupation of the user, and what are their skills and interests?"
    messages=[
        {"role": "system", "content": f"{instruction}"}
    ]

    i = 0
    demo.launch(share=True)