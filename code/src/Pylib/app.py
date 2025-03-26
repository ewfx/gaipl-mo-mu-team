from flask import Flask, send_from_directory, render_template, request, jsonify,redirect, url_for
import os
import openai

app = Flask(__name__)

# Define the path to the directory containing the HTML files
HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webpages')

# Define the path to the flat file
FLAT_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contexts.txt')

@app.route('/')
def home():
    return send_from_directory(HTML_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_html(filename):
    return send_from_directory(HTML_DIR, filename)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        chatbot_message = response.choices[0].message.content
        return jsonify({'message': chatbot_message})
    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)})
## API to load contexts to a flat file contexts.txt
@app.route('/save_contexts', methods=['POST'])
def save_contexts():
    contexts = request.form.getlist('contexts')
    with open(FLAT_FILE_PATH, 'w') as file:
        for context in contexts:
            file.write(f"{context}\n")
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)