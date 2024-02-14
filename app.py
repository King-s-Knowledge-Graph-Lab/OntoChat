import gradio as gr

from ontochat.functions import *


with gr.Blocks() as user_story_interface:
    gr.Markdown(
        """# OntoChat Hello! I am OntoChat, your conversational ontology engineering assistant, to help you generate 
        user stories, elicit requirements, and extract and analyze competency questions. In ontology engineering, 
        a user story contains all the requirements from the perspective of an end user of the ontology. It is a way 
        of capturing what a user needs to achieve with the ontology while also providing context and value. This demo 
        will guide you step-by-step to create a user story and generate competency questions from it. Once you are 
        ready, start inputting your persona, objective (goal), and sample data and chat with the chatbot. Once you 
        find the generated user story satisfactory, please copy the generated user story and go to the next step (
        tab)."""
    )
    with gr.Row():
        with gr.Column():
            api_key = gr.Textbox(
                label="OpenAI API Key",
                info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note "
                     "that the key will only be used for this demo and will not be uploaded or used anywhere else."
            )
            persona = gr.Textbox(
                label="Persona",
                placeholder="Please input the persona of the user, including the name, occupations, skills, interests.",
                info="Example: The user, Mark, is an experienced musicologist. He's an expert in western music, "
                     "and plays piano and guitar."
            )
            goal = gr.Textbox(
                label="Goal",
                placeholder="Please input the goal of the user and any specific issues faced.",
                info="Example: The goal of the user is to analyse analogies and simmetries between music scores, "
                     "with a particular focus on harmony and the lyrics of the music piece."
            )
            sample_data = gr.Textbox(
                label="Sample of Data",
                placeholder="Please input a sample of data.",
                info="Example: An example of data would be: - 'Let it be' by 'The Beatles' has a sequence of chords "
                     "composed by 'F, Amin, F' that is recurring every time the lyrics say 'Let it be'; - The lyrics "
                     "of 'Running with the Devil' by 'Van Halen' have a recurring chord sequence for the chorus and a "
                     "recurring chord sequence for the bridge."
            )
            generate_btn = gr.Button(value="Generate")
            user_story_chatbot = gr.Chatbot(

            )
            chatbot_input = gr.Textbox(
                placeholder="Please tell me what improvements I should make to the user story :)"
            )
        user_story = gr.TextArea(
            label="User story",
            interactive=True
        )
    generate_btn.click(
        fn=user_story_init_generator,
        inputs=[
            api_key, persona, goal, sample_data
        ],
        outputs=[
            user_story, user_story_chatbot
        ]
    )
    chatbot_input.submit(
        fn=user_story_generator,
        inputs=[chatbot_input, user_story_chatbot],
        outputs=[user_story, user_story_chatbot]
    )

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
    demo.launch()
