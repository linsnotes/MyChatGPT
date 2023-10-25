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

    base_message = f"do not change the language, Please refine the following text: \"{text}\""

    if refinementType == "grammar":
        instruction = base_message + " only the grammar while maintaining its original language."
    elif refinementType == "original":
        instruction = base_message + " only the grammar while maintaining its original language and tone."
    elif refinementType == "formal":
        instruction = base_message + " into a formal tone maintaining its original language."
    elif refinementType == "casual":
        instruction = base_message + " into a casual tone maintaining its original language."
    elif refinementType == "serious":
        instruction = base_message + " into a serious tone maintaining its original language."
    elif refinementType == "motivational":
        instruction = base_message + " into a motivational tone maintaining its original language."
    else: # humorous
        instruction = base_message + " into a humorous tone maintaining its original language."

    messages = [
        {"role": "system", "content": "You are a helpful assistant who is good at both English and Chinese."},
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
