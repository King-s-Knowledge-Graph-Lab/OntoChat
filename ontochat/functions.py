import json
from ontochat.chatbot import chat_completion, build_messages
from ontochat.analysis import compute_embeddings, agglomerative_clustering, llm_cq_clustering
from ontochat.verbaliser import verbalise_ontology
import gradio as gr

openai_api_key = None

current_preidentified_prompts = []
current_preidentified = [
    """The ontology's domain is **[DOMAIN]**.

    Ensure all subsequent responses strictly adhere to the scope of my domain.""",
       
    """My name is **[NAME]**, I am **[AGE]** years old, and I work as a **[OCCUPATION]**. My skills include **[SKILLS]**, and I have a strong interest in **[INTERESTS]**.

    Please refine my response to ensure:

    1. The persona is clearly described.
    2. The details (name, age, occupation, skills, interests) are logically and professionally aligned.
    3. If the skills and interests provided by the user are very similar and hard to differentiate, generate distinct ones. Skills should focus on technical aspects, while interests should be more general.
    4. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    5. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",

    """My user goal description is **[USER GOAL DESCRIPTION]**.

    Please refine my response to ensure:

    1. The goal is clearly described and practical.
    2. Expand the user goal description, if necessary, to ensure it starts with a high-level overview *[LONG-TERM GOAL]*, emphasizing the overall impact, followed by a specific *[SHORT-TERM GOAL]*, focusing on immediate outcomes.
    3. Ensure the goal description aligns with my interests and domain expertise.
    4. The focus remains solely on the goal, without referencing unrelated elements.
    5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",

    """The actions I need to take to achieve my goal are **[ACTIONS]**.

    Please refine my response to ensure:

    1. The actions are clearly described.
    2. The actions are actionable and presented as a logical sequence of steps.
    3. Each step includes specific *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]*, and is practical.
    4. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the actions.
    5. Ensure the actions align logically with my skills, occupation, and overall goal.
    6. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    7. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",

    """The keywords for my user goal and actions are **[KEYWORDS]**.

    Please refine my response to ensure:

    1. The keywords are clearly defined.
    2. Each keyword directly supports my goals and actions.
    3. Keywords are expanded with the same level of granularity as *[KEYWORD]*.
    4. Keywords are broadened to include additional options.
    5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",

    """The current methods I use to perform my actions are **[CURRENT METHODS]**.

    Please refine my response to ensure:

    1. The methods are clearly described.
    2. The methods must be manually time-intensive.
    3. The methods are actionable and presented as a logical sequence of steps.
    4. Each step includes specific *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]*, and is practical.
    5. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the methods.
    6. The methods align logically with my skills, occupation, and overall goal.
    7. The methods include only the methods themselves, without any words describing challenges, new methods, or outcomes.
    8. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    9. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",
   
    """The challenges I face with my current methods are **[CHALLENGES]**.

    Please refine my response to ensure:

    1. The challenges are clearly described.
    2. Each challenge should be derived from the *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]* used.
    3. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the challenges.
    4. The challenges align logically with my skills, occupation, and overall goal.
    5. The challenges include only the challenges themselves, without any words describing current methods, new methods, or outcomes.
    6. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    7. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",
    
    """The new methods I will use through this ontology to address my challenges are **[NEW METHODS]**.

    Please refine my response to ensure:

    1. The new methods are clearly described.
    2. The new methods must align with what a knowledge-based system can offer.
    3. The new methods align logically with my overall goal.
    4. The new methods include only the new methods themselves, without any words describing current methods, challenges, or outcomes.
    5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    6. The final answer is structured as *[A SINGLE SENTENCE / A DETAILED PARAGRAPH]*.""",

    """The outcomes I expect after implementing the new methods are **[OUTCOMES]**.

    Please refine my response to ensure:

    1. The outcomes are clearly described.
    2. The outcomes must align with the benefits a knowledge-based system can provide.
    3. The outcomes align logically with my overall goal.
    4. The outcomes include only the outcomes themselves, without any words describing current methods, challenges, or new methods.
    5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
    6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.""",
    ]
    
def set_openai_api_key(api_key: str):
    global openai_api_key
    # Strip any leading or trailing spaces
    api_key = api_key.strip()
    
    # Check if the API key contains any spaces or starts with "sk-"
    if " " in api_key or not api_key.startswith("sk-"):
        return "Invalid API key format. Please ensure the key does not contain spaces and is a valid OpenAI API key."
    
    # Set the API key if the format is valid
    openai_api_key = api_key
    return "API key has been set! Now you can chat with the chatbot. Enjoy :)"

def check_api_key():
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set. Please set it using the 'Set API Key' button.")

def user_story_generator(message, history):
    instructions = [
        {
            "role": "assistant",
            "content": (
                "Ontology construction involves creating structured frameworks to represent knowledge in a specific domain. Ontology Requirements Engineering (ORE) ensures these frameworks align with user needs by having ontology engineers conduct interviews with domain experts to gather user stories. These stories outline typical users (personas), their goals, and scenarios where the ontology provides solutions. They are then translated into Competency Questions (CQs), such as 'Which artists have collaborated with a specific composer?', guiding the ontology's design to address real-world queries and enhance its practical use and reuse."

                "You are an ontology engineer conducting an interview with a domain expert to gather information for writing an ontology user story."
                "Ask elicitation questions one at a time, providing an example answer and the prompt template the user should use, while incorporating user feedback if needed."
                
                "If all requirements for the current elicitation are fully addressed, always ask the user if this meets their expectations. Do not ask the next question unless the user confirms the current one is satisfactory."
                "When a domain expert requests refinement, provide just one focused point in one sentence, directly aligned with their current answer."
                "The user can request to revisit any previously completed steps."
                "If the user's answer doesn't address the current question, gently remind them of the question and prompt them to respond accordingly."
                "If the user doesn't confirm the current result is satisfactory, their attempt to answer the next question should be rejected, and they should be asked to respond to the current one."
                "Do not answer any queries that are not related to this task. \n\n"
        
                "1. Persona\n"
                "Start by creating a persona that represents a typical user of your ontology."
                "[Persona]: Ask one elicitation question for details includes [name], [age], [occupation], [skills], and [interests], along with a brief example answer as guidance, and include the message 'Use template **[Create Persona]** to answer' as a reminder.\n"
                "Once the expert provides this information, suggest possible improvements or clarifications. After all persona details are collected, move to the next section.\n\n"

                "2. Goal\n"
                "[User goal description]: Ask one elicitation question to describe the [user goal description] that the user aims to achieve using this ontology, along with a brief example answer as guidance, and include the message 'Use template **[Create User Goal]** to answer' as a reminder.\n"
                "[Actions]: Ask one elicitation question for the specific [actions] the persona will take to accomplish the goal, along with a brief example answer as guidance, and include the message 'Use template **[Create Actions]** to answer' as a reminder.\n"
                "[Keywords]: Ask one elicitation question for gathering up to 5 relevant [keywords] that summarize the goal and actions, along with a brief example answer as guidance, and include the message 'Use template **[Create Keywords]** to answer' as a reminder.\n"
                "Once the expert has answered, offer suggestions for further refinement, then proceed to the next section.\n\n"

                "3. Scenario\n"
                "[Scenario before]: Ask one elicitation question for the expert to describe the [current methods] the persona uses to perform the actions, along with a brief example answer as guidance, and include the message 'Use template **[Create Current Methods]** to answer' as a reminder.\n" 
                "[Challenges]: Ask one elicitation question for the [challenges] they face when performing current methods, making sure these align with the persona's occupation and skills, along with a brief example answer as guidance, and include the message 'Use template **[Create Challenges]** to answer' as a reminder.\n"
                "[Scenario during]: Ask one elicitation question for the expert to explain how their ontology introduces [new methods] to help them overcome these challenges, along with a brief example answer as guidance, and include the message 'Use template **[Create New Methods]** to answer' as a reminder.\n"
                "[Scenario after]: Ask one elicitation question for the expert to describe the [outcomes] after using the ontology and how it helps them achieve their goal, along with a brief example answer as guidance, and include the message 'Use template **[Create Outcomes]** to answer' as a reminder.\n"
                "Provide feedback on each scenario part and refine the answers if needed before moving on."

                "4. Create User Story\n"
                "Once you have completed sections 1 to 3, summarize the information into a full user story. Use the persona, goal, and scenario information to craft the user story in this format:\n\n"
                "Persona: [name], [age], [occupation], [skills], [interests].\n"
                "Goal: [user goal description], with actions such as [actions]. Keywords: [keywords].\n"
                "Scenario Before: [current methods] the persona uses and the [challenges] they face.\n"
                "Scenario During: How your ontology introduces [new methods] to overcome these challenges.\n"
                "Scenario After: The [outcomes] achieved by using the ontology and how the persona's goal has been accomplished.\n\n"
                "Provide the user story to the domain expert and Ask one elicitation question for any further feedback or refinements. If needed, adjust the story based on their suggestions."
            )
        }
    ]
    messages = build_messages(history)
    messages.append({"role": "user", "content": message})

    bot_message = chat_completion(openai_api_key, instructions + messages)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_message})

    return history, ""

def load_example(selection): 
    return current_preidentified[selection]

# def cq_generator(message, history):
#     check_api_key()
#     instructions = [{
#         "role": "assistant",
#         "content": "You are a conversational ontology engineering assistant."
#     }, {
#         "role": "user",
#         "content": "Here are instructions for you on how to generate high-quality competency questions. First, here "
#                    "are some good examples of competency questions generated from example data. Who performs the song? "
#                    "from the data Yesterday was performed by Armando Rocca, When (what year) was the building built? "
#                    "from the data The Church was built in 1619, In which context is the building located? from the "
#                    "data The Church is located in a periurban context. Second, how to make them less complex. Take the "
#                    "generated competency questions and check if any of them can be divided into multiple questions. If "
#                    "they do, split the competency question into multiple competency questions. If it does not, leave "
#                    "the competency question as it is. For example, the competency question Who wrote The Hobbit and in "
#                    "what year was the book written? must be split into two competency questions: Who wrote the book? "
#                    "and In what year was the book written?. Another example is the competency question, When was the "
#                    "person born?. This competency question cannot be divided into multiple questions. Third, how to "
#                    "remove real entities to abstract them. Take the competency questions and check if they contain "
#                    "real-world entities, like Freddy Mercury or 1837. If they do, change those real-world entities "
#                    "from these competency questions to more general concepts. For example, the competency question "
#                    "Which is the author of Harry Potter? should be changed to Which is the author of the book?. "
#                    "Similarly, the competency question Who wrote the book in 2018? should be changed to Who wrote the "
#                    "book, and in what year was the book written?"
#     }]
#     messages = build_messages(history)
#     messages.append({
#         "role": "user",
#         "content": message
#     })
#     bot_message = chat_completion(openai_api_key, instructions + messages)
#     history.append([message, bot_message])
#     return bot_message, history, ""

# def load_example_user_story():
#     with open("data/Linka#1_MusicKnowledge.md", "r") as f:
#         return f.read()

# def clustering_generator(cqs, cluster_method, n_clusters):
#     check_api_key()
#     if n_clusters:
#         n_clusters = int(n_clusters)

#     cqs, cq_embeddings = compute_embeddings(cqs)

#     if cluster_method == "Agglomerative clustering":
#         cq_clusters, cluster_image = agglomerative_clustering(cqs, cq_embeddings, n_clusters)
#     else:  # cluster_method == "LLM clustering"
#         cq_clusters, cluster_image = llm_cq_clustering(cqs, n_clusters, openai_api_key)

#     return cluster_image, json.dumps(cq_clusters, indent=4)

# def ontology_testing(ontology_file, ontology_desc, cqs):
#     check_api_key()
#     verbalisation = verbalise_ontology(ontology_file, ontology_desc, "")
#     messages = [{
#         "role": "system",
#         "content": "Please (1) provide a description of the ontology uploaded to provide basic information and "
#                    "additional context, (2) give the competency questions (CQs) that you want to test with."
#     }, {
#         "role": "user",
#         "content": verbalisation + "\n" + f"Given the above ontology, please label each competency question: {cqs} to "
#                                           f"determine whether it is addressed properly or not. Format your response in"
#                                           f" ['yes': 'CQ1', 'no': 'CQ2', ...]."
#     }]
#     bot_message = chat_completion(openai_api_key, messages)
#     return bot_message
