from flask import Flask, render_template, request, jsonify
import openai
import os

# Define the path to the directory containing the HTML files
HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'webpages')

app2 = Flask(__name__, template_folder=HTML_DIR)
print(app2.root_path)
print(HTML_DIR)
# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app2.route('/')
def home():
    
    return render_template('chatbot.html')

@app2.route('/chat', methods=['POST'])
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

if __name__ == '__main__':
    app2.run(debug=True)