import gradio as gr
from openai import OpenAI
from ontochat.functions import *
from ontochat.chatbot import client_import

with gr.Blocks() as user_story_interface:
    with gr.Row():
        gr.Markdown("## OntoChat")
    with gr.Row():
        gr.Markdown("""
        Hello! I am OntoChat, your conversational ontology engineering assistant, to help you generate user 
        stories, elicit requirements, and extract and analyze competency questions. In ontology engineering, 
        a user story contains all the requirements from the perspective of an end user of the ontology. It 
        is a way of capturing what a user needs to achieve with the ontology while also providing context 
        and value. This demo will guide you step-by-step to create a user story and generate competency 
        questions from it. Once you are ready, start inputting your persona, objective (goal), and sample 
        data and chat with the chatbot. Once you find the generated user story satisfactory, please copy the 
        generated user story and go to the next step (tab).
        """)
    #API key set
    with gr.Row():
        def API_key_set(API_KEY):
            global client
            client = OpenAI(api_key = API_KEY)
            client_import(client)
            return "API Key set successfully!"
        API_KEY = gr.Textbox(label='Input your API-KEY of OpenAI', placeholder='e.g. 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')
        key_status = gr.Textbox(label='key status',visible=True)
        set_btn = gr.Button("Set API key")
        set_btn.click(fn=API_key_set, inputs=API_KEY, outputs=key_status)

    #User story generator
    persona_q = "What are the name and occupation of the user, and what are their skills and interests?"
    goal_q = "What is the goal of the user? Are they facing specific issues?"
    example_q = "Do you have examples of data?"
    persona = gr.Textbox(label=persona_q)
    goal = gr.Textbox(label=goal_q)
    example = gr.Textbox(label=example_q)
    output = gr.Textbox(label="Generated user story")
    generate_btn = gr.Button("Generate")
    generate_btn.click(fn=user_story_generator, inputs=[persona, goal, example], outputs=output, api_name="Generate")

    #User stroy refinement chatbot
    gr.Markdown("Copy the generated user story above and paste it here to refine it with the chatbot.")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="What you would like to refine?")
    clear = gr.ClearButton([msg, chatbot])
    client_messages = [{"role": "system", "content": "Hello! I'm here to guide you through refining your user stories, ensuring they're clear, concise, and ready to drive your project forward. User stories are a fundamental part of developing an ontology that truly meets your users' needs, and getting them right is crucial."}]

    def respond(message, chat_history):
        client_messages.append({"role": "user", "content": message})
        bot_message = chat_completion(client_messages)
        chat_history.append((message, bot_message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

cq_interface = gr.Interface(
    fn=cq_generator,
    inputs=[
        gr.Textbox(
            label="User story",
            info="Please copy the previously generated user story and paste it here. You can also modify the user "
                 "story before submitting it."
        ),
        gr.Slider(
            minimum=5,
            maximum=50,
            step=1,
            label="Number of competency questions",
            info="Please select the number of competency questions you want to generate."
        )
    ],
    outputs=[
        gr.Textbox(label="Competency questions")
    ],
    title="OntoChat",
)

clustering_interface = gr.Interface(
    fn=clustering_generator,
    inputs=[
        gr.Textbox(
            label="Competency questions",
            info="Please copy the previously generated competency questions and paste it here. You can also modify "
                 "the questions before submitting them."
        ),
        gr.Dropdown(
            choices=["Agglomerative clustering", "HDBSCAN", "LLM clustering"],
            label="Clustering method",
            info="Please select the clustering method."
        ),
        gr.Slider(
            minimum=2,
            maximum=50,
            step=1,
            label="Number of clusters",
            info="Please select the number of clusters you want to generate. Please note that for HDBSCAN, this value "
                 "is used as the minimum size of a cluster. And please do not input a number that exceeds the total "
                 "number of competency questions."
        )
    ],
    outputs=[
        gr.Image(label="Visualization"),
        gr.Code(
            language='json',
            label="Competency Question clusters"
        )
    ],
    title="OntoChat",
)

demo = gr.TabbedInterface(
    [user_story_interface, cq_interface, clustering_interface],
    ["User Story Generation", "Competency Question Extraction", "Competency Question Analysis"]
)

if __name__ == "__main__":
    # demo.launch(share=True)
    demo.launch(share=True)
