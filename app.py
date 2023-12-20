from flask import Flask, request, jsonify
from difflib import get_close_matches
import os

app = Flask(__name__)

# Read Kannada words from the file
def read_kannada_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        kannada_words_list = file.read().splitlines()
    return kannada_words_list

# Replace 'kannada_words.txt' with the actual file path
kannada_words_file_path = 'kannada_words.txt'
kannada_words_list = read_kannada_words(kannada_words_file_path)

def autocorrect(sentence, word_list):
    corrected_sentence = []

    for word in sentence.split():
        # Check if the word is in the Kannada words list
        if word not in word_list:
            # If not, find the closest match using difflib
            closest_match = get_close_matches(word, word_list, n=1, cutoff=0.8)

            # If a close match is found, replace the word
            if closest_match:
                corrected_sentence.append(closest_match[0])
            else:
                # If no close match is found, keep the original word
                corrected_sentence.append(word)
        else:
            # If the word is in the Kannada words list, keep it as it is
            corrected_sentence.append(word)

    return ' '.join(corrected_sentence)

@app.route('/autocorrect', methods=['POST'])
def autocorrect_api():
    data = request.get_json()

    if 'sentence' not in data:
        return jsonify({'error': 'Missing sentence parameter'}), 400

    sentence = data['sentence']
    corrected_sentence = autocorrect(sentence, kannada_words_list)

    return jsonify({'original_sentence': sentence, 'corrected_sentence': corrected_sentence})

if __name__ == '__main__':
    # Use the PORT environment variable if available, otherwise default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
