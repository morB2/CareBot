import json


def get_disease_info(disease_name, question_word, json_file='diseases_data.json'):
    """
    Retrieves the relevant information about a disease from a JSON file based on the disease name and question word.

    Parameters:
    disease_name (str): The name of the disease to search for.
    question_word (str): The specific question word or category to look for.
    json_file (str): The path to the JSON file containing disease information.

    Returns:
    str: The relevant information about the disease based on the question word.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if disease_name in data:
            disease_info = data[disease_name]
            if question_word in disease_info:
                return disease_info[question_word]
            else:
                return disease_info["תיאור כללי"]
        else:
            return f', לצערי אין לי מידע על מחלה זו.'
    except Exception as e:
        return f"אירעה תקלה בעת קריאת קובץ ה-JSON: {e}"
