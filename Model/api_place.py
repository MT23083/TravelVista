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
CORS(app, resources={r"/place_rank": {"origins": "http://localhost:3000"}})




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

@app.route('/place_rank', methods=['GET','POST'])
def rank_places():
    input = request.json.get('city')
    # Get JSON data from the request
    df = pd.read_csv('places_final_preprocess.csv')
    # Search for "Agra" in the "City" column
    result = df[df['City'] == input]

    # Check if there's any result
    if not result.empty:
        # Get the filename from the "hotel/final" column
        filename = result.iloc[0]['places_final']

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

    all_words = good_words + bad_words
    # Merge good_words and bad_words lists after converting them into sets to remove duplicates
    all_words = list(set(good_words + bad_words))

    # Determine the maximum length among good_words and bad_words
    max_length = max(len(good_words), len(bad_words))

    # Pad the shorter list with a placeholder word to match the maximum length
    padding_word = "padding_word"

    if len(good_words) < max_length:
        good_words += [padding_word] * (max_length - len(good_words))

    if len(bad_words) < max_length:
        bad_words += [padding_word] * (max_length - len(bad_words))

    # Initialize CountVectorizer
    vectorizer = CountVectorizer(vocabulary=all_words, tokenizer=lambda text: text.split())

    # Lists to store overall scores and place names
    overall_scores = []
    place_names = []
    # List to store ranked places with original JSON objects
    ranked_places_with_original = []
    # Loop through each place with reviews
    for place in places_with_reviews:
        place_name = place['name']
        print("Place:", place_name)

        # Extract reviews and preprocess them
        reviews = place['preprocessed_reviews']
        preprocessed_reviews = []
        problematic_reviews = []  # List to store problematic reviews
        for review in reviews:
            try:
                preprocessed_review = remove_special_characters(review.lower())  # Fix here
                preprocessed_review = " ".join(preprocessed_review.split())
                preprocessed_reviews.append(preprocessed_review)
            except Exception as e:
                problematic_reviews.append(review)
                print("Error processing review:", review)
                print("Error message:", str(e))

        # Transform reviews into vectors
        #print(preprocessed_reviews)
        #print("Vocabulary:", vectorizer.get_feature_names())
        review_vectors = vectorizer.fit_transform(preprocessed_reviews)

        # Calculate cosine similarity between reviews and good/bad words
        good_similarity = cosine_similarity(review_vectors, vectorizer.transform(good_words).toarray())
        bad_similarity = cosine_similarity(review_vectors, vectorizer.transform(bad_words).toarray())

        # Calculate average rating
        avg_rating = np.mean(place['rating'])

        # Calculate overall score
        overall_score = np.mean(good_similarity - bad_similarity) + avg_rating

        place_copy = place.copy()  # Make a copy to avoid modifying the original object
        place_copy['overall_score'] = overall_score
        ranked_places_with_original.append(place_copy)

    # Sort the places based on overall score in descending order
    ranked_places_with_original = sorted(ranked_places_with_original, key=lambda x: x['overall_score'], reverse=True)

    # Create a JSON object containing the ranked places
    ranked_json_object = {"places_with_reviews": ranked_places_with_original}

    # Return the ranked JSON object
    return jsonify(ranked_json_object), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=9003, host='0.0.0.0', debug=True)
