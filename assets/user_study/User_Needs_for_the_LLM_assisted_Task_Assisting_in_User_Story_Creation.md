# Ontology Prompt Templates

## **Ontology Domain Specification**
```plaintext
The ontology's domain is **[DOMAIN]**.

Ensure all subsequent responses strictly adhere to the scope of my domain.
```

## **Persona Refinement**
```plaintext
My name is **[NAME]**, I am **[AGE]** years old, and I work as a **[OCCUPATION]**. My skills include **[SKILLS]**, and I have a strong interest in **[INTERESTS]**.

Please refine my response to ensure:

1. The persona is clearly described.
2. The details (name, age, occupation, skills, interests) are logically and professionally aligned.
3. If the skills and interests provided by the user are very similar and hard to differentiate, generate distinct ones. Skills should focus on technical aspects, while interests should be more general.
4. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
5. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **User Goal Refinement**
```plaintext
My user goal description is **[USER GOAL DESCRIPTION]**.

Please refine my response to ensure:

1. The goal is clearly described and practical.
2. Expand the user goal description, if necessary, to ensure it starts with a high-level overview *[LONG-TERM GOAL]*, emphasizing the overall impact, followed by a specific *[SHORT-TERM GOAL]*, focusing on immediate outcomes.
3. Ensure the goal description aligns with my interests and domain expertise.
4. The focus remains solely on the goal, without referencing unrelated elements.
5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **Action Refinement**
```plaintext
The actions I need to take to achieve my goal are **[ACTIONS]**.

Please refine my response to ensure:

1. The actions are clearly described.
2. The actions are actionable and presented as a logical sequence of steps.
3. Each step includes specific *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]*, and is practical.
4. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the actions.
5. Ensure the actions align logically with my skills, occupation, and overall goal.
6. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
7. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **Keyword Refinement**
```plaintext
The keywords for my user goal and actions are **[KEYWORDS]**.

Please refine my response to ensure:

1. The keywords are clearly defined.
2. Each keyword directly supports my goals and actions.
3. Keywords are expanded with the same level of granularity as *[KEYWORD]*.
4. Keywords are broadened to include additional options.
5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **Current Methods Refinement**
```plaintext
The current methods I use to perform my actions are **[CURRENT METHODS]**.

Please refine my response to ensure:

1. The methods are clearly described.
2. The methods must be manually time-intensive.
3. The methods are actionable and presented as a logical sequence of steps.
4. Each step includes specific *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]*, and is practical.
5. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the methods.
6. The methods align logically with my skills, occupation, and overall goal.
7. The methods include only the methods themselves, without any words describing challenges, new methods, or outcomes.
8. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
9. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **Challenges Refinement**
```plaintext
The challenges I face with my current methods are **[CHALLENGES]**.

Please refine my response to ensure:

1. The challenges are clearly described.
2. Each challenge should be derived from the *[TOOLS]*, *[METHODS]*, or *[TECHNIQUES]* used.
3. Where relevant, incorporate *[INTERDISCIPLINARY INSIGHTS]* to describe the challenges.
4. The challenges align logically with my skills, occupation, and overall goal.
5. The challenges include only the challenges themselves, without any words describing current methods, new methods, or outcomes.
6. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
7. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
```

## **New Methods Refinement**
```plaintext
The new methods I will use through this ontology to address my challenges are **[NEW METHODS]**.

Please refine my response to ensure:

1. The new methods are clearly described.
2. The new methods must align with what a knowledge-based system can offer.
3. The new methods align logically with my overall goal.
4. The new methods include only the new methods themselves, without any words describing current methods, challenges, or outcomes.
5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
6. The final answer is structured as *[A SINGLE SENTENCE / A DETAILED PARAGRAPH]*.
```

## **Expected Outcomes Refinement**
```plaintext
The outcomes I expect after implementing the new methods are **[OUTCOMES]**.

Please refine my response to ensure:

1. The outcomes are clearly described.
2. The outcomes must align with the benefits a knowledge-based system can provide.
3. The outcomes align logically with my overall goal.
4. The outcomes include only the outcomes themselves, without any words describing current methods, challenges, or new methods.
5. The language is *[CONCISE & PRECISE / CREATIVE & DETAILED]*, ensuring clarity and professionalism.
6. The final answer is structured as *[BULLET POINTS / A DETAILED PARAGRAPH]*.
