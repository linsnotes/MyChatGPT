from flask import Flask, request, jsonify, render_template
import openai
# from azure.keyvault.secrets import SecretClient
# from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv, find_dotenv
import os

app = Flask(__name__)

# Connect to Key Vault and get the OPENAI_API_KEY secret
load_dotenv(find_dotenv())

# KVUri = "https://KeyOpenAI.vault.azure.net"
# credential = DefaultAzureCredential()
# client = SecretClient(vault_url=KVUri, credential=credential)
# retrieved_secret = client.get_secret("OPENAI-API-KEY")

# Initialize OpenAI API
# openai.api_key = retrieved_secret.value
openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct_text():
    text = request.json.get('text')
    refinementType = request.json.get('refinementType')

    base_message = f" 'Text': \"{text}\""

    if refinementType == "grammar":
        instruction = "Do not change the language, refine the Text', based on the 'requirement'. requirement: refine only the grammar while maintaining its original language. return only the corrected text, no quotation and explanations" + base_message
    elif refinementType == "translation":
        instruction = "if the 'Text' is Chinese Language, translate the text to fluent and natural British English. if the text is English, translate the text to fluent and natural Chinese Language. return only the translated text, no quotation and explanations" + base_message
    else: # Ask Mr Lin Anything
        instruction = "Answer the question only the question is approriate, which is not evil question. Answer the question in the same language of the question. meaning if the text is chinese reply in chinese, if the text is in english, reply in enlglish" + base_message

    messages = [
        {"role": "system", "content": "You are Mr Lin who is good at languages, especially Chinese and English."},
        {"role": "user", "content": instruction}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return jsonify({"corrected_text": response.choices[0].message['content'].strip()})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8000)
