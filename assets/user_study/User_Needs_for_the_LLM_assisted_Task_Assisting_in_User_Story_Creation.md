# Ontology Prompt Templates

## **Ontology Domain Specification**
```plaintext
The domain of the ontology-based system is **[DOMAIN]**.

Please ensure that all responses are strictly relevant to this system's domain. Use terminology and structures that are specific to ontology-based systems, including appropriate relationships and reasoning principles. Do not introduce information outside the defined scope.
```

## **Persona Refinement**
```plaintext
My persona is **[NAME]**, I am **[AGE]** years old, and I work as a **[OCCUPATION]** in the domain of **[DOMAIN]**. My expertise includes **[SKILLS]**, and I have a strong interest in **[INTERESTS]**.

Please refine my response to ensure:

1. The persona is described clearly, emphasizing expertise or experience relevant to ontology-based systems in the specified domain.
2. Details (name, age, occupation, skills, interests) are logically aligned with domain knowledge, typical users, and the use of ontology-based systems.
3. If skills and interests overlap, make them distinct by separating conceptual knowledge (e.g., data modeling, requirements analysis) from applied skills (e.g., ontology development, knowledge graph implementation).
4. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language for clarity and suitability in a knowledge-intensive context.
5. Present the output as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **User Goal Refinement**
```plaintext
My ontology user goal is **[USER GOAL DESCRIPTION]**.

Please refine my response to ensure:

1. The goal is clearly described and directly related to using an ontology-based system to support a real task in the specified domain.
2. Expand the goal if needed: start with a high-level *[KNOWLEDGE REPRESENTATION OBJECTIVE]* (such as representing key domain knowledge, integrating data, or enabling reasoning), then describe a specific *[DOMAIN TASK]* or *[USER NEED]* that the ontology-based system should support.
3. Make sure the goal aligns with my domain expertise and addresses a practical scenario where ontology-based systems add value.
4. Focus on the ontology-supported aspects of the task, not unrelated system functions or technology details.
5. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language as needed for clarity.
6. Present the output as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **Action Refinement**
```plaintext
The actions I need to take to build the ontology-based system for my goal are **[ACTIONS]**.

Please refine my response to ensure:

1. The actions are clearly described and directly relate to the step-by-step process of developing or configuring the ontology-based system.
2. List the actions as simple, practical steps required to design, construct, and deploy the ontology-based system for the target domain or goal.
3. For each step, specify any *[ONTOLOGY ENGINEERING METHODS]*, *[KNOWLEDGE REPRESENTATION TOOLS]*, *[DATA SOURCES]*, or *[REASONING TECHNIQUES]* used in the process.   
4. If relevant, include *[COLLABORATION WITH DOMAIN EXPERTS]* or integration of *[EXTERNAL DATASETS]* to enhance system quality.   
5. Ensure the actions logically align with my background and the requirements of the domain and user goal.   
6. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language, as appropriate.
7. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **Keyword Refinement**
```plaintext
The key ontology concepts and terms related to my goal are **[KEYWORDS]**.

Please refine my response to ensure:

1. The keywords are clearly defined and directly relevant to the ontology-based system and the target domain.
2. Each keyword should support knowledge structuring and reasoning within the ontology.
3. Where possible, align the keywords with *[EXISTING ONTOLOGY VOCABULARIES]* or recognized *[STANDARDS]*.
4. Expand each keyword by adding related ontological terms, such as subclasses, parent classes, or linked data mappings.
5. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language as required.
6. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **Current Methods Refinement**
```plaintext
The current methods I use to achieve my goal, without using any ontology-based system, are **[CURRENT METHODS]**.

Please refine my response to ensure:

1. The methods are clearly described and involve only manual or ad-hoc approaches for structuring and applying domain knowledge, with no use of ontology-based systems or automated reasoning tools.
2. Present the methods as a logical, step-by-step sequence of actions or procedures currently used to achieve my goal.
3. For each step, specify any *[MANUAL TOOLS, DOCUMENTATION PRACTICES, or INFORMAL REPRESENTATION TECHNIQUES]* (such as spreadsheets, text documents, or diagrams).
4. The methods should reflect established practices within my domain and align logically with my expertise and goals.
5. Do not mention challenges, ontology-based systems, new methods, or expected outcomes.
6. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language, as needed.
7. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **Challenges Refinement**
```plaintext
The challenges I face in my current manual or ad-hoc methods (without ontology-based systems) are **[CHALLENGES]**.

Please refine my response to ensure:

1. The challenges are clearly described and arise directly from my current tools, workflows, or informal practices for structuring and reasoning about domain knowledge.
2. Each challenge should be specific and derived from limitations of *[CURRENT TOOLS]*, *[METHODOLOGIES]*, or *[LOGICAL CONSTRAINTS]* used in my existing (non-ontology) approaches.
3. Where relevant, include issues related to data consistency, integration across sources, or knowledge reuse.
4. The challenges should logically relate to my domain and my knowledge structuring goals.
5. Focus only on core difficulties with current methods—do not discuss possible solutions or expected improvements.
6. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language, as needed.
7. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **New Methods Refinement**
```plaintext
The new methods I will use to address my challenges with the support of an ontology-based system are **[NEW METHODS]**.

Please refine my response to ensure:

1. The methods are clearly described and directly enabled by features of the ontology-based system.
2. Each method should show how the ontology-based system supports automated reasoning, semantic search, ontology alignment, or other advanced knowledge management functions.
3. All methods should logically align with my stated goals and expected improvements in managing or utilizing domain knowledge.
4. Only describe new approaches and capabilities that are possible with the ontology-based system—do not discuss previous challenges or prior manual methods.
5. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language, as best fits the context.
6. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```

## **Expected Outcomes Refinement**
```plaintext
The expected outcomes of implementing ontology-based system methods are **[OUTCOMES]**.

Please refine my response to ensure:

1. The outcomes are clearly described and directly result from using the ontology-based system.
2. The outcomes reflect benefits such as improved knowledge structuring, reasoning, semantic interoperability, or automation enabled by the ontology-based system.
3. The outcomes align logically with my overall goal for the ontology-based application.
4. Only include ontology-driven improvements—do not discuss prior methods or challenges.
5. Use *[CONCISE & PRECISE / CREATIVE & DETAILED]* language as best fits the context.
6. Structure the answer as *[BULLET POINTS / A DETAILED PARAGRAPH / TAXONOMY-LIKE HIERARCHY]*.
```
