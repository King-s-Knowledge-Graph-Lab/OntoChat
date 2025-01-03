# [PID7](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat/blob/main/assets/user_study/Demographic_Information_of_Participants.md) User Goal Description Generation Illustrative Example

## Step 1 - Query Initiation

Participants were first instructed on how to write an ontology user story, with the instructions available online.

[Instructions on How to Write Ontology User Stories](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat/blob/main/assets/user_study/Instructions_on_How_to_Write_Ontology_User_Stories.md)

The task involved using GPT-4 to generate an ontology user story leveraging their domain-specific knowledge. We will now provide an example to demonstrate how each step works.

### Example

When participants were prompted to write the **USER GOAL DESCRIPTION** section of their user story, the instruction provided was:

> *"What the persona aims to achieve in the story."*

#### Example User Query
PID7, a software engineer specializing in multisensory interaction and involved in the MuseIT project, aimed to create an ontology to connect cultural artifacts with visual, auditory, and tactile elements for a museum exhibit. PID7 initially asked:

> *"Can you help me define the goal for integrating sensory elements in a museum exhibit using an ontology?"*

## Step 2 - Prompt Refinement

Following the prompting strategy, the researcher augmented PID7’s initial query by adding a persona and explicit constraints to scope the LLM’s response.

[Pre-identified Prompts for Ontology User Story Elicitation](https://github.com/King-s-Knowledge-Graph-Lab/OntoChat/blob/main/assets/user_study/Pre_identified_Prompts_for_Ontology_User_Story_Elicitation.md)

### Refined Query Example

> *"Alex, a software engineer specializing in multisensory interaction, aims to create a cohesive and engaging multisensory museum exhibit by integrating tactile, auditory, and visual elements using an ontology. Provide a goal statement based on Alex’s expertise and project needs, ensuring the language is free from unnecessary details."*

#### LLM Response
> *"Alex’s goal is to use the ontology to link tactile, auditory, and visual elements in a museum exhibit, ensuring a seamless and engaging visitor experience."*

PID7 found the response insufficient, stating:

> *"It’s too general and doesn’t specify how to perform the linking."*

#### Further Refinement
The researcher refined the query to include constraints requiring **ACTIONS** to be presented step-by-step, ensuring practicality by specifying tools or methods. The refined query became:

> *"Provide a detailed sequence of actions Alex needs to take to achieve the goal of linking tactile, auditory, and visual elements in the museum exhibit using an ontology. Ensure the response includes specific tools or methods for data collection, processing, and mapping. The steps should be logical, actionable, and aligned with Alex’s expertise in multisensory interaction."*

#### Updated LLM Response

> *"1. Use tactile sensors to collect texture and material data from artifacts.
2. Process the tactile data using a classification tool to organize it into categories like texture, material, and surface properties.
3. Record auditory elements, such as soundscapes or narration, using high-quality audio equipment and tag them with metadata.
4. Map the tactile and auditory data to the ontology using an ontology editing tool like Protégé.
5. Integrate visual elements, such as images or 3D models, by linking them to tactile and auditory data within the ontology.
6. Validate the connections between the sensory data to ensure alignment and consistency with the exhibit’s design goals."*

PID7 found this response logical, clear, and actionable, stating:

> *"Good!"*

After obtaining user satisfaction for the current task, it demonstrates that LLMs have two key potentials for supporting story creation:

1. Generating clear **USER GOAL DESCRIPTIONS**.
2. Providing a sequence of practical **ACTIONS** to achieve the goal.

### Final Prompt Templates

#### USER GOAL DESCRIPTION Template

> *"My user goal description is **[USER GOAL DESCRIPTION]**. Please refine my response to ensure:
1. The goal is clearly described and practical.
2. Expand the user goal description, if necessary, to ensure it starts with a high-level overview [LONG-TERM GOAL], emphasizing the overall impact, followed by a specific [SHORT-TERM GOAL], focusing on immediate outcomes.
3. Ensure the goal description aligns with my interests, domain expertise.
4. The focus remains solely on the goal, without referencing unrelated elements.
5. The language is concise, precise, and written in a professional tone.
6. The final refined answer is presented as bullet points, with the first bullet for the long-term goal and the second bullet for the short-term goal."*

#### ACTIONS Template

> *"The actions I need to take to achieve my goal are **[ACTIONS]**. Please refine my response to ensure:
1. The actions are clearly described.
2. The actions are actionable and presented as a logical sequence of steps.
3. Each step includes specific [TOOLS], [METHODS], or [TECHNIQUES], and is practical.
4. Where relevant, incorporate [INTERDISCIPLINARY INSIGHTS] to describe the actions.
5. Ensure the actions align logically with my skills, expertise, and overall goal, showcasing their relevance.
6. The language is concise, precise, and written in a professional tone.
7. The final refined answer is structured as bullet points, with each step represented as a separate bullet."*
