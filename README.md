<div align="center">
  
  <h1 align="center">CareBot</h1>

  <p align="center">
    A medical chatbot for diagnosing potential health conditions based on user symptoms!
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

**CareBot** is a web application designed to help users diagnose potential medical conditions by inputting their symptoms. The system uses a combination of natural language processing (NLP), deterministic finite automaton (DFA) filtering, and machine learning models to analyze user input and provide accurate results based on pre-scraped medical data.

Key Features:
* Users can describe their symptoms, which are processed through NLP using the Stanza library.
* Symptoms are filtered using a DFA to ensure valid inputs.
* Predictions are made using three machine learning models: Random Forest, Naive Bayes, and Support Vector Machine (SVM).
* The system retrieves results from a pre-scraped JSON file containing a list of conditions to ensure fast response times.
* Information about detected conditions is stored, enabling faster responses if users ask follow-up questions.

### Built With

* [![React][React.js]][React-url]
* [![Python][Python]][Python-url]
* [![C++][CPP]][CPP-url]
* [![CSS][CSS]][CSS-url]
* [![NLP][NLP]][NLP-url]

---

<!-- MARKDOWN LINKS & IMAGES -->
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[CPP]: https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white
[CPP-url]: https://en.wikipedia.org/wiki/C%2B%2B
[CSS]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[NLP]: https://img.shields.io/badge/NLP-006600?style=for-the-badge&logo=nlp&logoColor=white
[NLP-url]: https://stanfordnlp.github.io/stanza/
