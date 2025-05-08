<div align="center">
    <img src="assets/title_logo.png" width="96%" height="auto" />
</div>

# OntoChat: a Framework for Conversational Ontology Engineering using Language Models

OntoChat is a LLM-based conversational agent designed to facilitate collaborative ontology engineering. It currently supports ontology requirement elicitation, analysis, and testing. Its CQs generation is evaluated with [Bench4KE](https://github.com/fossr-project/ontogenia-cini), a benchmarking framework that compares generated CQs against gold standards using lexical and semantic metrics. OntoChat is publicly available on **[Hugging Face Spaces](https://huggingface.co/spaces/1hangzhao/OntoChat)**. For the best experience, we recommend using **Google Chrome**.

---

## Deployment Instructions

1. **Set Up Your Environment**  
   - Ensure you have **Python 3.11** or higher installed.  

2. **Install Dependencies**  
   - Download the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application**  
   - Start the OntoChat framework using Gradio:
     ```bash
     Gradio app.py
     ```

## Authors and attribution
```
@inproceedings{zhang-et-al-2024-ontochat,
  author = {Zhang, Bohui and Carriero, Valentina Anita and Schreiberhuber, Katrin and Tsaneva, Stefani and Gonz\'{a}lez, Luc\'{\i}a S\'{a}nchez and Kim, Jongmo and de Berardinis, Jacopo},
  title = {OntoChat: A&nbsp;Framework for&nbsp;Conversational Ontology Engineering Using Language Models},
  year = {2025},
  isbn = {978-3-031-78951-9},
  publisher = {Springer-Verlag},
  address = {Berlin, Heidelberg},
  url = {https://doi.org/10.1007/978-3-031-78952-6_10},
  doi = {10.1007/978-3-031-78952-6_10},
  booktitle = {The Semantic Web: ESWC 2024 Satellite Events: Hersonissos, Crete, Greece, May 26–30, 2024, Proceedings, Part I},
  pages = {102–121},
  numpages = {20},
  keywords = {Ontology Engineering, Large Language Models, Competency Questions, Computational Creativity},
  location = {Hersonissos, Greece}
}

@inproceedings{zhao2024improving,
  title={Improving Ontology Requirements Engineering with OntoChat and Participatory Prompting},
  author={Zhao, Yihang and Zhang, Bohui and Hu, Xi and Ouyang, Shuyin and Kim, Jongmo and Jain, Nitisha and de Berardinis, Jacopo and Mero{\~n}o-Pe{\~n}uela, Albert and Simperl, Elena},
  url = {https://ojs.aaai.org/index.php/AAAI-SS/article/view/31799},
  doi = {10.1609/aaaiss.v4i1.31799},
  booktitle={Proceedings of the AAAI Symposium Series},
  volume={4},
  number={1},
  pages={253--257},
  year={2024}
}
```

## Acknowledgement

This project has received multiple sources of funding, including co-funding from [MuseIT](https://www.muse-it.eu/) under grant agreement No. 101061441 as part of the European Union’s Horizon 2021-2027 research and innovation programme, as well as support from [SIEMENS AG](https://www.siemens.com/global/en.html) and the [Technical University of Munich](https://www.tum.de/), Institute for Advanced Study, Germany. We also extend our gratitude to all the evaluators for their valuable feedback on the tool’s effectiveness and for sharing their user experiences.

## License

Copyright 2025 OntoChat maintainers

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
