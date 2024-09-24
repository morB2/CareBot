from flask import Flask, request, jsonify
from flask_cors import CORS
from nlp import filter_data
from cpp import cpp_function
from hash import questions_words_hash
from predict_disease import predict_disease
from db import const_reactions_array, endings, openings
from get_info import get_disease_info
import random
import secrets

app = Flask(__name__)
SECRET_KEY = secrets.token_urlsafe(50)
app.config.from_object(__name__)
CORS(app)


def process_user_input(user_paragraph):
    # Processing user input to filter and identify question word
    filtered_data, question_word = filter_data(user_paragraph)
    question_word_category = questions_words_hash(question_word, filtered_data)
    return filtered_data, question_word_category


def generate_response(name_of_disease, question_word_category):
    # Generate response based on the identified disease and question word category
    if name_of_disease != "":
        return get_disease_info(name_of_disease, question_word_category)
    else:
        return random.choice(const_reactions_array['not_understood'])


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        # Validate input
        if not data or 'text' not in data or 'diseaseName' not in data:
            return jsonify({'error': 'Invalid input'}), 400

        user_paragraph = data['text']
        response_message = ""
        name_of_disease = data['diseaseName']

        # Check for opening or ending phrases
        if user_paragraph in openings:
            return jsonify(
                {'response': random.choice(const_reactions_array['opening']), 'diseaseName': name_of_disease})
        if user_paragraph in endings:
            return jsonify({'response': random.choice(const_reactions_array['finish']), 'diseaseName': name_of_disease})

        # Process user input to get filtered data and question word category
        filtered_data, question_word_category = process_user_input(user_paragraph)

        # Use DFA to identify diseases or symptoms
        dfa_array, is_disease = cpp_function(filtered_data)
        if is_disease:
            name_of_disease = dfa_array
        else:
            if len(dfa_array) > 0:
                disease_name = predict_disease(dfa_array)
                if disease_name == -1 and (name_of_disease == '' or question_word_category == ''):
                    return jsonify(
                        {'response': random.choice(const_reactions_array['other']), 'diseaseName': name_of_disease})
                else:
                    name_of_disease = disease_name
                    response_message = f'נראה שיש לך {name_of_disease}'
            elif name_of_disease == '' or question_word_category == '':
                return jsonify(
                    {'response': random.choice(const_reactions_array['other']), 'diseaseName': name_of_disease})

        # Generate final response
        response_message += generate_response(name_of_disease, question_word_category)
        return jsonify({'response': response_message, 'diseaseName': name_of_disease})
    except Exception as e:
        return jsonify({'response': 'שגיאה'}), 500


if __name__ == '__main__':
    app.run(port=5001)
