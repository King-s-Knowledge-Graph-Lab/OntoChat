import gradio as gr
# from ontochat.functions import set_openai_api_key, user_story_generator, cq_generator, load_example_user_story, clustering_generator, ontology_testing, load_example
from ontochat.functions import set_openai_api_key, user_story_generator, load_example

user_story_template = """**Persona:**\n\n- Name: -\n- Age: -\n- Occupation: -\n- Skills: -\n- Interests: -\n\n**Goal:**\n\n- Description: -\n- Keywords: -\n\n**Scenario:**\n\n- Before: -\n- During: -\n- After: -\n\n**Example Data:**\n\n- Category: -\n- Data: -\n\n**Resources:**\n\n- Resource Name: -\n- Link: -"""

with gr.Blocks() as set_api_key:
    gr.Markdown(
        """
        # Welcome to OntoChat! 👋

        Hi there! I'm OntoChat, your conversational assistant for collaborative ontology engineering. (1) 📋 I assist with ontology requirements elicitation by asking targeted questions, collecting user inputs, providing example answers, and recommending prompt templates to guide you. (2) 📝 I offer customizable prompts designed for different interaction stages, ensuring structured guidance throughout the process. (3) ⚙️ You can edit placeholders within these templates to refine constraints and shape my responses to fit your specific needs. (4) 🔄 I continuously improve my responses based on your feedback until you're satisfied. Let's make ontology development smoother and more interactive! 🚀 For more details, visit 🌐 [OntoChat on GitHub](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat).
        """
    )

    # ### Citations
        
    # [1] Zhang B, Carriero VA, Schreiberhuber K, Tsaneva S, González LS, Kim J, de Berardinis J. OntoChat: a Framework for Conversational Ontology Engineering using Language Models. arXiv preprint arXiv:2403.05921. 2024 Mar 9.
    
    # [2] Zhao Y, Zhang B, Hu X, Ouyang S, Kim J, Jain N, de Berardinis J, Meroño-Peñuela A, Simperl E. Improving Ontology Requirements Engineering with OntoChat and Participatory Prompting. InProceedings of the AAAI Symposium Series 2024 Nov 8 (Vol. 4, No. 1, pp. 253-257).

    with gr.Group():
        api_key = gr.Textbox(
            label="OpenAI API Key",
            info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note that "
                 "the key will only be used for this demo and will not be uploaded or used anywhere else."
        )
        api_key_btn = gr.Button(value="Set API Key")
        api_key_btn.click(fn=set_openai_api_key, inputs=api_key, outputs=api_key)

with gr.Blocks() as user_story_interface:
    with gr.Row():
        with gr.Column(scale=1):
            user_story_chatbot = gr.Chatbot(
                value=[
                    {"role": "assistant", "content": ( 
                        "Hello! I'm OntoChat 😊. I'll help you create an ontology user story!\n\n 1. I will ask you one **elicitation question** at a time, present an **example answer** to support your understanding, and recommend a **prompt template** 📄 for answering.\n\n 2. Don't worry about prompting—find the **template** 📄 I recommended and edit the **placeholders** 📝 to craft an effective response 👍.\n\n 3. Within a prompt template:\n   - **\*\*[]\*\*** placeholders are **mandatory**.\n   - **\*[]\*** placeholders are **optional**.\n\n 4. I will **refine** my generation iteratively based on your input 🔄 until you are satisfied ✅.\n\nLet's get started! **Which domain is this ontology for?**\n\n**For example:** *Healthcare, Wine, Music, etc.*\n\nUse template **[Create Domain]** to answer. 🚀"
                    )}
                ],
                height="472px",
                type="messages"
            )
            user_story_input = gr.Textbox(
                label="Message OntoChat",
                placeholder="Please type your message here and press Enter to interact with the chatbot:",
                max_lines = 20,
                lines = 1
            )
            elicitation_questions_dataset = gr.Dataset(
                components=[user_story_input],
                label="Prompt Templates",
                type="index",
                samples=[
                    ["Create Domain"],
                    ["Create Persona"],
                    ["Create User Goal"],
                    ["Create Actions"],
                    ["Create Keywords"],
                    ["Create Current Methods"],
                    ["Create Challenges"],
                    ["Create New Methods"],
                    ["Create Outcomes"]
                ],
                samples_per_page = 10
            )

    user_story_input.submit(
        fn=user_story_generator,
        inputs=[user_story_input, user_story_chatbot],
        outputs=[user_story_chatbot, user_story_input]
    )
    elicitation_questions_dataset.click(
        fn=load_example, 
        inputs=[elicitation_questions_dataset], 
        outputs=[user_story_input]
    ) 

# with gr.Blocks() as cq_interface:
#     with gr.Row():
#         with gr.Column():
#             cq_chatbot = gr.Chatbot(
#                 value=[
#                     {
#                         "role": "assistant",
#                         "content": (
#                             "I am OntoChat, your conversational ontology engineering assistant. Here is the second step of "
#                             "the system. Please give me your user story and tell me how many competency questions you want "
#                             "me to generate from the user story."
#                         )
#                     }
#                 ],
#                 type="messages" 
#             )
#             cq_input = gr.Textbox(
#                 label="Chatbot input",
#                 placeholder="Please type your message here and press Enter to interact with the chatbot:"
#             )
#             gr.Markdown(
#                 """
#                 ### User story examples
#                 Click the button below to use an example user story from 
#                 [Linka](https://github.com/polifonia-project/stories/tree/main/Linka_Computer_Scientist) in Polifonia.
#                 """
#             )
#             example_btn = gr.Button(value="Use example user story")
#             example_btn.click(
#                 fn=load_example_user_story,
#                 inputs=[],
#                 outputs=[cq_input]
#             )
#         cq_output = gr.TextArea(
#             label="Competency questions",
#             interactive=True
#         )
#     cq_input.submit(
#         fn=cq_generator,
#         inputs=[
#             cq_input, cq_chatbot
#         ],
#         outputs=[
#             cq_output, cq_chatbot, cq_input
#         ]
#     )

# clustering_interface = gr.Interface(
#     fn=clustering_generator,
#     inputs=[
#         gr.TextArea(
#             label="Competency questions",
#             info="Please copy the previously generated competency questions and paste it here. You can also modify "
#                  "the questions before submitting them."
#         ),
#         gr.Dropdown(
#             value="LLM clustering",
#             choices=["LLM clustering", "Agglomerative clustering"],
#             label="Clustering method",
#             info="Please select the clustering method."
#         ),
#         gr.Textbox(
#             label="Number of clusters (optional for LLM clustering)",
#             info="Please input the number of clusters you want to generate. And please do not input a number that "
#                  "exceeds the total number of competency questions."
#         )
#     ],
#     outputs=[
#         gr.Image(label="Visualization"),
#         gr.Code(
#             language='json',
#             label="Competency Question clusters"
#         )
#     ],
#     title="OntoChat",
#     description="This is the third step of OntoChat. Please copy the generated competency questions from the previous "
#                 "step and run the clustering algorithm to group the competency questions based on their topics. From "
#                 "our experience, LLM clustering has the best performance.",
#     flagging_mode="never"
# )

# with gr.Blocks() as testing_interface:
#     gr.Markdown(
#         """
#         # OntoChat
#         This is the final part of OntoChat which performs ontology testing based on the input ontology file and CQs. 
#         """
#     )

#     with gr.Group():
#         api_key = gr.Textbox(
#             label="OpenAI API Key",
#             placeholder="If you have set the key in other tabs, you don't have to set it again.",
#             info="Please input your OpenAI API Key if you don't have it set up on your own machine. Please note that "
#                  "the key will only be used for this demo and will not be uploaded or used anywhere else."
#         )
#         api_key_btn = gr.Button(value="Set API Key")
#         api_key_btn.click(fn=set_openai_api_key, inputs=api_key, outputs=api_key)

#     ontology_file = gr.File(label="Ontology file")
#     ontology_desc = gr.Textbox(
#         label="Ontology description",
#         placeholder="Please provide a description of the ontology uploaded to provide basic information and "
#                     "additional context."
#     )
#     cq_testing_input = gr.Textbox(
#         label="Competency questions",
#         placeholder="Please provide the competency questions that you want to test with."
#     )
#     testing_btn = gr.Button(value="Test")
#     testing_output = gr.TextArea(label="Ontology testing output")
#     testing_btn.click(
#         fn=ontology_testing,
#         inputs=[
#             ontology_file, ontology_desc, cq_testing_input
#         ],
#         outputs=[
#             testing_output
#         ]
#     )

demo = gr.TabbedInterface(
    # [set_api_key, user_story_interface, cq_interface, clustering_interface, testing_interface],
    [set_api_key, user_story_interface],
    ["Set API Key", "User Story Generation", "Competency Question Extraction", "Competency Question Analysis", "Ontology Testing"]
)

if __name__ == "__main__":
    demo.launch(share=True)
