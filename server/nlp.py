import stanza

# Download and initialize the Stanza Hebrew NLP pipeline
# stanza.download('he')
nlp = stanza.Pipeline('he')


def filter_data(user_sentence):
    """
    Processes the input Hebrew sentence to extract relevant linguistic features.

    Parameters:
    user_sentence (str): The user's input sentence in Hebrew.

    Returns:
    tuple: A tuple containing:
        - dfa_array (list): List of lemmas of NOUN and VERB words.
        - question_word (str): The question word in the sentence, if any.
        - max_gender (str): The most frequent gender in the sentence (Fem or Masc).
        - max_person (str): The most frequent person in the sentence (First, Second, or Third).
    """

    # Process the input sentence
    doc = nlp(user_sentence)

    # Initialize variables
    dfa_array = []
    question_word = ""

    # Iterate over the sentences and words in the document
    for sentence in doc.sentences:
        for word in sentence.words:
            # Find question words (interrogative adverbs)
            if word.upos == "ADV" and word.feats and "PronType=Int" in word.feats:
                question_word = word.text

            # Check if the word is a symptom or disease (NOUN, VERB)
            if word.upos in ["NOUN", "ADJ", "VERB", "PROPN", "ADV"]:
                dfa_array.append(word.lemma)

    return dfa_array, question_word
