from flask import Flask, request, jsonify, render_template
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/get-country-info', methods=['POST'])
def get_country_info():
    country_name = request.json['country']
    prompt = f"Give an interesting, unknown historical story or fact about the country {country_name} that deals with peace or anti-violence."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful historian."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    if response.choices:
        story = response.choices[0].message.content
    else:
        story = "No response received from the API."

    return jsonify({'story': story})


if __name__ == '__main__':
    app.run(debug=True)
