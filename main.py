from flask import Flask, jsonify, request, render_template
import random
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

def read_poems_from_file(filename):
    poems = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_poem = ''
        for line in lines:
            line = line.strip()
            if line:
                current_poem += line + '\n'
            elif current_poem:
                poems.append(current_poem.strip())
                current_poem = ''
    return poems


poems_filename = 'poem_7.txt'
poems = read_poems_from_file(poems_filename)

def build_markov_chain(poems):
    matrix = {}
    rhyme_scheme = {}

    for poem in poems:
        poem = poem.replace('，', '').replace('。', '')
        poem = poem.strip()
        if len(poem) < 2:
            continue

        for i in range(len(poem) - 1):
            current_char = poem[i]
            next_char = poem[i + 1]


            if current_char in matrix:
                if next_char in matrix[current_char]:
                    matrix[current_char][next_char] += 1
                else:
                    matrix[current_char][next_char] = 1
            else:
                matrix[current_char] = {next_char: 1}


            if i == len(poem) - 2:
                if current_char in rhyme_scheme:
                    rhyme_scheme[current_char].append(next_char)
                else:
                    rhyme_scheme[current_char] = [next_char]


    for current_char in matrix:
        total = sum(matrix[current_char].values())
        for next_char in matrix[current_char]:
            matrix[current_char][next_char] /= total

    return matrix, rhyme_scheme


matrix, rhyme_scheme = build_markov_chain(poems)

def generate_poem_with_markov_chain(matrix, start_keyword, rhyme_scheme, length=28):
    poem = start_keyword
    current_char = poem[-1]
    word_count = len(start_keyword)
    last_word = None

    while word_count < length:
        next_chars = matrix.get(current_char, None)
        if not next_chars:
            break

        if word_count % 7 == 5:

            rhyme_chars = rhyme_scheme.get(current_char, list(next_chars.keys()))
            next_char = random.choice(rhyme_chars)
        elif word_count % 7 == 6:

            if last_word:
                related_chars = rhyme_scheme.get(last_word, list(next_chars.keys()))
                next_char = random.choice(related_chars)
            else:
                next_char = random.choice(list(next_chars.keys()))
            last_word = next_char
            poem += next_char + '。'
        else:
            next_char = random.choices(list(next_chars.keys()), weights=next_chars.values())[0]
            poem += next_char

        if word_count % 7 == 6:
            poem += '\n'
        current_char = next_char
        word_count += 1

    return poem



def format_poem(poem):
    formatted_poem = []
    line = ""
    word_count = 0

    for char in poem:
        if char != '\n':
            line += char
            word_count += 1

            if word_count == 7:
                formatted_poem.append(line)
                line = ""
                word_count = 0


    while word_count < 7:
        line += ' '
        word_count += 1

    formatted_poem.append(line)


    while len(formatted_poem) < 4:
        formatted_poem.append('       ')

    return formatted_poem


@app.route('/generate-poem', methods=['GET'])
def generate_poem_route():
    keyword = request.args.get('keyword', '')

    generated_poem = generate_poem_with_markov_chain(matrix, keyword, rhyme_scheme)
    formatted_poem = format_poem(generated_poem)

    return jsonify({'poem': formatted_poem})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
