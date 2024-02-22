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
                [None, "Hello! I am OntoChat, your conversational ontology engineering assistant. I will guide you step"
                       " by step in the creation of a user story. Let's start with the persona. What are the name, "
                       "occupations, skills, interests of the user?"],
            ])
            user_story_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
            # gr.Markdown(
            #     """
            #     ### User story generation prompt
            #     Click the button below to use a user story generation prompt that provides better instructions to the chatbot.
            #     """
            # )
            # prompt_btn = gr.Button(value="User story generation prompt")
            # prompt_btn.click(
            #     fn=load_user_story_prompt,
            #     inputs=[],
            #     outputs=[user_story_input]
            # )
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
        This is the second step of OntoChat. This functionality provides support for the extraction of competency 
        questions from a user story. Please, provide a user story to start extracting competency questions with the 
        chatbot, or simply load the example story below.
        """
    )

    with gr.Group():
        api_key = gr.Textbox(
            label="OpenAI API Key",
            placeholder="If you have set the key in other tabs, you don't have to set it again.",
            info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note that "
                 "the key will only be used for this demo and will not be uploaded or used anywhere else."
        )
        api_key_btn = gr.Button(value="Set API Key")
        api_key_btn.click(fn=set_openai_api_key, inputs=api_key, outputs=api_key)

    with gr.Row():
        with gr.Column():
            cq_chatbot = gr.Chatbot([
                [None, "I am OntoChat, your conversational ontology engineering assistant. Here is the second step of "
                       "the system. Please give me your user story and tell me how many competency questions you want "
                       "me to generate from the user story."]
            ])
            cq_input = gr.Textbox(
                label="Chatbot input",
                placeholder="Please type your message here and press Enter to interact with the chatbot :)"
            )
            gr.Markdown(
                """
                ### User story examples
                Click the button below to use an example user story from 
                [Linka](https://github.com/polifonia-project/stories/tree/main/Linka_Computer_Scientist) in Polifonia.
                """
            )
            # TODO: could add more examples using Dropdown or CheckboxGroup
            example_btn = gr.Button(value="Use example user story")
            example_btn.click(
                fn=load_example_user_story,
                inputs=[],
                outputs=[cq_input]
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
            value="LLM clustering",
            choices=["LLM clustering", "Agglomerative clustering"],
            label="Clustering method",
            info="Please select the clustering method."
        ),
        gr.Textbox(
            label="Number of clusters (optional for LLM clustering)",
            info="Please input the number of clusters you want to generate. And please do not input a number that "
                 "exceeds the total number of competency questions."
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

    with gr.Group():
        api_key = gr.Textbox(
            label="OpenAI API Key",
            placeholder="If you have set the key in other tabs, you don't have to set it again.",
            info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note that "
                 "the key will only be used for this demo and will not be uploaded or used anywhere else."
        )
        api_key_btn = gr.Button(value="Set API Key")
        api_key_btn.click(fn=set_openai_api_key, inputs=api_key, outputs=api_key)

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
