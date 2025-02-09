<div align="center">
    <img src="assets/title_logo.png" width="96%" height="auto" />
</div>

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
OntoChat has been hosted in HF Spaces at: [[https://huggingface.co/spaces/1hangzhao/OntoChat](https://huggingface.co/spaces/1hangzhao/OntoChat)]

## Note
- A first evaluation of the framework was performed to reproduce the engineering efforts behind the [Music Meta Ontology](https://github.com/polifonia-project/music-meta-ontology).

## TODO
- Improve the verbaliser (classes, named entities, and relations might be messy in some cases)
- Optimize clustering visualization (maybe only keep LLM lcustering)
- Add [flagging](https://www.gradio.app/docs/flagging), e.g., [`HuggingFaceDatasetSaver`](https://www.gradio.app/docs/flagging#hugging-face-dataset-saver-header)

## Authors and attribution
```
@inproceedings{zhang2024ontochat,
  title={OntoChat: A Framework for Conversational Ontology Engineering Using Language Models},
  author={Zhang, Bohui and Carriero, Valentina Anita and Schreiberhuber, Katrin and Tsaneva, Stefani and Gonz{\'a}lez, Luc{\'i}a S{\'a}nchez and Kim, Jongmo and de Berardinis, Jacopo},
  booktitle={The Semantic Web: ESWC 2024 Satellite Events},
  volume={15344},
  pages={102--121},
  year={2024},
  publisher={Springer Nature Switzerland},
}

@inproceedings{zhao2024improving,
  title={Improving Ontology Requirements Engineering with OntoChat and Participatory Prompting},
  author={Zhao, Yihang and Zhang, Bohui and Hu, Xi and Ouyang, Shuyin and Kim, Jongmo and Jain, Nitisha and de Berardinis, Jacopo and Mero{\~n}o-Pe{\~n}uela, Albert and Simperl, Elena},
  booktitle={Proceedings of the AAAI Symposium Series},
  volume={4},
  number={1},
  pages={253--257},
  year={2024}
}
```

## Acknowledgement

We acknowledge the following support:

- This project is co-funded by [Polifonia](https://polifonia-project.eu) under grant agreement No. 101004746 as part of the European Union’s Horizon 2014-2020 research and innovation programme.
- This project is co-funded by [MuseIT](https://www.muse-it.eu/) under grant agreement No. 101061441 as part of the European Union’s Horizon 2021-2027 research and innovation programme.
- This project is co-funded by [SIEMENS AG](https://www.siemens.com/global/en.html) and the [Technical University of Munich](https://www.tum.de/), Institute for Advanced Study, Germany.

We also thank all the evaluators that contributed feedback on the effectiveness of the tool and provided their experience of use.

## License

Copyright 2024 OntoChat maintainers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
