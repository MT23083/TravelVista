from flask import Flask, request, jsonify
import json
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/hotel_rank": {"origins": "http://localhost:3000"}})



# Helper function to read a list from a pickle file
def read_list_from_pickle(file_path):
    with open(file_path, 'rb') as file:
        my_list = pickle.load(file)
    return my_list

# Function to preprocess reviews by removing special characters and converting to lowercase
def remove_special_characters(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII characters
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation and symbols
    return text

@app.route('/hotel_rank', methods=['GET','POST'])
def rank_places():
    input = request.json.get('city')
    # Get JSON data from the request
    df = pd.read_csv('hotel_final_preprocess.csv')
    # Search for "Agra" in the "City" column
    result = df[df['City'] == input]

    # Check if there's any result
    if not result.empty:
        # Get the filename from the "hotel/final" column
        filename = result.iloc[0]['hotel_final']

        # Load the JSON file
        with open(filename, 'r') as file:
            json_data = json.load(file)

        #print(json_data)  # Print or use the loaded JSON data
    else:
        print("No entry found")
        json_data = request.get_json()

    # Extract the places with reviews from the JSON data
    places_with_reviews = json_data.get('places_with_reviews', [])

    # Load good_words and bad_words from pickle
    good_words_counter = read_list_from_pickle("good_words.pkl")
    good_words = list(good_words_counter.keys())
    bad_words_counter = read_list_from_pickle("bad_words.pkl")
    bad_words = list(bad_words_counter.keys())

    # Determine the maximum length among good_words and bad_words
    max_length = max(len(good_words), len(bad_words))

    # Pad the shorter list with a placeholder word to match the maximum length
    padding_word = "padding_word"

    if len(good_words) < max_length:
        good_words += [padding_word] * (max_length - len(good_words))

    if len(bad_words) < max_length:
        bad_words += [padding_word] * (max_length - len(bad_words))

    # Initialize CountVectorizer
    vectorizer = CountVectorizer()

    # Preprocess reviews and calculate overall scores
    ranked_places_with_original = []
    for place in places_with_reviews:
        preprocessed_reviews = []
        for review_data in place['reviews']:
            review_text = review_data.get('text', '')
            try:
                preprocessed_review = remove_special_characters(review_text.lower())
                preprocessed_review = " ".join(preprocessed_review.split())
                preprocessed_reviews.append(preprocessed_review)
            except Exception as e:
                print("Error processing review:", review_text)
                print("Error message:", str(e))

        # Transform reviews into vectors
        review_vectors = vectorizer.fit_transform(preprocessed_reviews)

        # Calculate cosine similarity between reviews and good/bad words
        good_similarity = cosine_similarity(review_vectors, vectorizer.transform(good_words))
        bad_similarity = cosine_similarity(review_vectors, vectorizer.transform(bad_words))

        # Calculate average rating
        avg_rating = np.mean([rating_data for review_data in place['reviews'] for rating_data in review_data.get('rating', [])])

        # Calculate overall score
        overall_score = np.mean(good_similarity - bad_similarity) + avg_rating

        # Create a copy of the place with the overall score
        place_copy = place.copy()
        place_copy['overall_score'] = overall_score
        ranked_places_with_original.append(place_copy)

    # Sort the places based on overall score in descending order
    ranked_places_with_original = sorted(ranked_places_with_original, key=lambda x: x['overall_score'], reverse=True)

    # Create a JSON object containing the ranked places
    ranked_json_object = {"places_with_reviews": ranked_places_with_original}

    # Return the ranked JSON object
    return jsonify(ranked_json_object), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=9002, host='0.0.0.0', debug=True)
