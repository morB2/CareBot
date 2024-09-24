import pandas as pd
from collections import Counter
from sklearn.preprocessing import LabelEncoder
import joblib

# Reading the test data
test_data = pd.read_csv("dataset/Testing.csv", encoding='ISO-8859-8').dropna(axis=1)

# Loading the feature names
feature_names = joblib.load("feature_names.pkl")
test_X = test_data.reindex(columns=feature_names, fill_value=0)

# Encoding the target value into numerical value using LabelEncoder
encoder = LabelEncoder()
encoder.fit(test_data["prognosis"])

# Loading the models
svm_model = joblib.load("svm_model.pkl")
nb_model = joblib.load("nb_model.pkl")
rf_model = joblib.load("rf_model.pkl")

symptoms = feature_names.values

# Creating a symptom index dictionary to encode the input symptoms into numerical form
symptom_index = {symptom: index for index, symptom in enumerate(symptoms)}

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}


def predict_disease(symptoms):
    # Creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in symptoms:
        if symptom in data_dict["symptom_index"]:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1

    # Converting the input data into DataFrame with correct feature names
    input_data_df = pd.DataFrame([input_data], columns=feature_names)

    # Generating individual outputs
    rf_prediction = data_dict["predictions_classes"][rf_model.predict(input_data_df)[0]]
    nb_prediction = data_dict["predictions_classes"][nb_model.predict(input_data_df)[0]]
    svm_prediction = data_dict["predictions_classes"][svm_model.predict(input_data_df)[0]]

    # Making final prediction by taking mode of all predictions
    final_predictions = [rf_prediction, nb_prediction, svm_prediction]
    predictions_count = Counter(final_predictions)

    # Find the most common prediction
    final_prediction = predictions_count.most_common(1)[0][0]

    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": svm_prediction,
        "final_prediction": final_prediction
    }

    # Check if all models gave different predictions
    values = list(predictions.values())
    if len(set(values)) == len(values) or final_prediction == 'איידס':
        return -1

    return final_prediction
