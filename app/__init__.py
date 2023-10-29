from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]

# Fetch the GPT-4 password from an environment variable
if "GPT4_PASSWORD" not in os.environ:
    raise EnvironmentError("GPT4_PASSWORD environment variable not set")
GPT4_PASSWORD = os.environ["GPT4_PASSWORD"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct_text():
    text = request.json.get('text')
    refinementType = request.json.get('refinementType')
    model = request.json.get('model')
    password = request.json.get('password', '')

    # Check if GPT-4 is selected and validate password
    if model == "gpt-4" and password != GPT4_PASSWORD:
        return jsonify({"error": "Invalid password entered. Please contact Mr Lin for assistance with accessing the GPT-4 model."}), 403

    base_message = f" 'Text': \"{text}\""

    if refinementType == "grammar":
        instruction = "Do not change the language, refine the Text', based on the 'requirement'. requirement: refine only the grammar while maintaining its original language. return only the corrected text, no quotation and explanations" + base_message
    elif refinementType == "translation":
        instruction = "if the 'Text' is Chinese Language, translate the text to fluent and natural British English. if the text is English, translate the text to fluent and natural Chinese Language. return only the translated text, no quotation and explanations" + base_message
    else: # Ask Mr Lin Anything
        instruction = "Answer the question only the question is approriate, which is not evil question. Answer the question in the same language of the question. meaning if the text is chinese reply in chinese, if the text is in english, reply in enlglish. return only your response, no quotation." + base_message


    messages = [
        {"role": "system", "content": "You are Mr Lin who is good at languages, especially Chinese and English."},
        {"role": "user", "content": instruction}
    ]

    response = openai.ChatCompletion.create(
        model=model,  # Use the selected model
        messages=messages
    )
    return jsonify({"corrected_text": response.choices[0].message['content'].strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
