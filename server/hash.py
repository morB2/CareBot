def questions_words_hash(questions_word, filtered_data):
    """
    Categorizes the given question word based on predefined categories.

    Parameters:
    questions_word (str): The question word to be categorized.
    filtered_data (str): The filtered data string which might contain specific keywords.

    Returns:
    str: The category corresponding to the question word.
    """
    # Dictionary mapping question words to categories
    question_categories = {
        'מה': '',
        'למה': 'סיבות וגורמי סיכון',
        'איך': 'טיפולים ותרופות',
        'כיצד': 'טיפולים ותרופות',
    }

    # Check if 'מנע' or 'מניעה' is in the filtered data
    if 'מנע' in filtered_data or 'מניעה' in filtered_data:
        return 'מניעה'

    if 'סיבוך' in filtered_data or 'הסתבך' in filtered_data:
        return 'סיבוכים אפשריים'

    # Return the category if the question word is in the dictionary, otherwise return ''
    return question_categories.get(questions_word, '')
