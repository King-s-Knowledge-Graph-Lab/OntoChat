import gradio as gr

from ontochat.functions import *


with gr.Blocks() as user_story_interface:
    gr.Markdown(
        """
        # OntoChat 
        Hello! I am OntoChat, your conversational ontology engineering assistant, to help you generate 
        user stories, elicit requirements, and extract and analyze competency questions. In ontology engineering, 
        a user story contains all the requirements from the perspective of an end user of the ontology. It is a way 
        of capturing what a user needs to achieve with the ontology while also providing context and value. This demo 
        will guide you step-by-step to create a user story and generate competency questions from it. Once you are 
        ready, start inputting your persona, objective (goal), and sample data and chat with the chatbot. Once you 
        find the generated user story satisfactory, please copy the generated user story and go to the next step (
        tab)."""
    )

    with gr.Group():
        api_key = gr.Textbox(
            label="OpenAI API Key",
            info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note that "
                 "the key will only be used for this demo and will not be uploaded or used anywhere else."
        )
        api_key_btn = gr.Button(value="Set API Key")
        api_key_btn.click(fn=set_openai_api_key, inputs=api_key, outputs=api_key)

    with gr.Row():
        with gr.Column():
            user_story_chatbot = gr.Chatbot([
                [None, "Hello! I am OntoChat, your conversational ontology engineering assistant."],
                ["I am a domain expert trying to create a user story to be used by ontology engineers. You are the "
                 "ontology expert. Only ask the following question once I have responded. Ask for the specifications "
                 "to generate a user story as a user of the system, which should include: 1. The Persona: What are "
                 "the name, occupation, skills and interests of the user? 2. The Goal: What is the goal of the user? "
                 "Are they facing specific issues? 3. Example Data: Do you have examples of the specific data "
                 "available? Make sure you have answers to all three questions before providing a user story. Only "
                 "ask the next question once I have responded.", "Sure. Let's start with the persona. What are the "
                 "name, occupations, skills, interests of the user?"]
            ])
            user_story_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
        user_story = gr.TextArea(
            label="User story",
            interactive=True
        )
    user_story_input.submit(
        fn=user_story_generator,
        inputs=[
            user_story_input, user_story_chatbot
        ],
        outputs=[
            user_story, user_story_chatbot, user_story_input
        ]
    )


with gr.Blocks() as cq_interface:
    gr.Markdown(
        """
        # OntoChat 
        This is the second step of OntoChat. Please copy the generated user story from the previous 
        step and use it here. You can also modify the user story before using it for generating competency questions. 
        **Recommended prompt workflow:** 
        1. Obtain competency questions from the user story. 
        - Zero-shot learning:
            - Prompt template: Given the user story: {user story}, generate {number} competency questions base on it. 
        - Few-shot learning (i.e., provide examples to give more instructions on how to generate competency questions):
            - Prompt template: Here are some good examples of competency questions generated from example data. 
              Formatted in {"Example data": "Competency questions"}. 
              {"Yesterday was performed by Armando Rocca.": "Who performs the song?"},
              {"The Church was built in 1619.": "When (what year) was the building built?"},
              {"The Church is located in a periurban context.": "In which context is the building located?"},
              {"The mounting system of the bells is the falling clapper.": "Which is the mounting system of the bell?"}
        2. Clean and refine competency questions. 
        - Obtain multiple competency questions. 
            - Prompt template: Take the generated competency questions and check if any of them can be divided into 
              multiple questions. If they do, split the competency question into multiple competency questions. If it 
              does not, leave the competency question as it is. For example, the competency question "Who wrote The 
              Hobbit and in what year was the book written?" must be split into two competency questions: "Who wrote 
              the book?" and "In what year was the book written?". Another example is the competency question, "When 
              was the person born?". This competency question cannot be divided into multiple questions.
        - Remove specific named entities.
            - Prompt template: Take the competency questions and check if they contain real-world entities, like 
              "Freddy Mercury" or "1837". If they do, change those real-world entities from these competency questions 
              to more general concepts. For example, the competency question "Which is the author of Harry Potter?" 
              should be changed to "Which is the author of the book?". Similarly, the competency question "Who wrote 
              the book in 2018?" should be changed to "Who wrote the book, and in what year was the book written?"
        """
    )

    with gr.Row():
        with gr.Column():
            cq_chatbot = gr.Chatbot([
                [None, "I am OntoChat, your conversational ontology engineering assistant. Here is the second step of "
                 "the system. Please give me your user story and tell me how many competency questions you want."]
            ])
            cq_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
        cq_output = gr.TextArea(
            label="Competency questions",
            interactive=True
        )
    cq_input.submit(
        fn=cq_generator,
        inputs=[
            cq_input, cq_chatbot
        ],
        outputs=[
            cq_output, cq_chatbot, cq_input
        ]
    )


clustering_interface = gr.Interface(
    fn=clustering_generator,
    inputs=[
        gr.TextArea(
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
    description="This is the third step of OntoChat. Please copy the generated competency questions from the previous "
                "step and run the clustering algorithm to group the competency questions based on their topics. From "
                "our experience, LLM clustering has the best performance.",
    allow_flagging="never"
)


with gr.Blocks() as testing_interface:
    gr.Markdown(
        """
        # OntoChat 
        This is the final part of OntoChat which performs ontology testing based on the input ontology file and CQs. 
        """
    )
    ontology_file = gr.File(label="Ontology file")
    ontology_desc = gr.Textbox(
        label="Ontology description",
        placeholder="Please provide a description of the ontology uploaded to provide basic information and "
                    "additional context."
    )
    cq_testing_input = gr.Textbox(
        label="Competency questions",
        placeholder="Please provide the competency questions that you want to test with."
    )
    testing_btn = gr.Button(value="Test")
    testing_output = gr.TextArea(label="Ontology testing output")
    testing_btn.click(
        fn=ontology_testing,
        inputs=[
            ontology_file, ontology_desc, cq_testing_input
        ],
        outputs=[
            testing_output
        ]
    )


demo = gr.TabbedInterface(
    [user_story_interface, cq_interface, clustering_interface, testing_interface],
    ["User Story Generation", "Competency Question Extraction", "Competency Question Analysis", "Ontology Testing"]
)


if __name__ == "__main__":
    demo.launch()
