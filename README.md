# OntoChat

We introduce **OntoChat**, a framework for conversational ontology engineering that supports requirement elicitation, 
analysis, and testing. By interacting with a conversational agent, users can steer the creation of use cases and the 
extraction of competency questions, while receiving computational support to analyse the overall requirements and test 
early versions of the resulting ontologies.

## Deploy
If you would like to deploy this demo locally,
1. Create a python environment and install the requirements using `pip install -r requirements.txt`.
2. Run `app.py`.

## Hosting in Hugging Face Spaces
OntoChat has been hosted in HF Spaces at: [https://huggingface.co/spaces/b289zhan/OntoChat](https://huggingface.co/spaces/b289zhan/OntoChat).

## Note
- The ontology testing part has been tested with the [Music Meta Ontology](https://github.com/polifonia-project/music-meta-ontology) and works well.

## TODO
- Improve the verbaliser (classes, named entities, and relations might be messy in some cases)
- Optimize clustering visualization (maybe only keep LLM lcustering)
- Add [flagging](https://www.gradio.app/docs/flagging), e.g., [`HuggingFaceDatasetSaver`](https://www.gradio.app/docs/flagging#hugging-face-dataset-saver-header)
