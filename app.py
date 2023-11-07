import os
import nltk
import urllib.request
import json
import ssl
nltk.download("punkt")
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for ,session
# from azure.identity import DefaultAzureCredential
# from azure.core.exceptions import ResourceNotFoundError
# from azure.core.credentials import AzureKeyCredential
# from nltk import download as nltk_download
# from weasyprint import HTML
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.chains import RetrievalQA
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import AzureChatOpenAI
# from langchain.document_loaders import PyPDFLoader
# from langchain.vectorstores import FAISS
# from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'genai1234'


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/main', methods=['POST'])
# Assuming you've imported necessary libraries and defined your Flask app and routes
def main():
    def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context
    allowSelfSignedHttps(True)  

    # Import pdb; pdb.set_trace()
    email = request.form.get('email')
    additional_context = request.form.get('additional_context')

    # Process checkbox state
    mask_toggle = request.form.get('maskToggle') == 'on' if request.form.get('maskToggle') else False

    # Store the checkbox value in session
    session['mask_toggle'] = mask_toggle
    print("Checkbox value stored in session:", mask_toggle)

    print(f"The email is {email}")   
    if not email:
        flash('Please insert email.')
        return redirect(url_for('index'))
    data = {"email": f"{email}",  "additional_context": f"{additional_context}"}

    body = str.encode(json.dumps(data))
    
    url = 'https://email-endpoint.southeastasia.inference.ml.azure.com/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = 'wWgs4sjQ4DbkvKP4uj3sPs2UDnCymeaG'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'email-endpoint-2' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        decode_result = json.loads(result.decode('utf-8'))
        summary = decode_result['sum']
        email_response = decode_result['reply']
        
        # Store the values in session
        session['email'] = email
        session['summary'] = summary
        session['email-response'] = email_response
        # Retrieve the checkbox value from session
        mask_toggle = session.get('mask_toggle')

        # Pass the output as a variable to the template
        return render_template('index.html', summary=summary , email = email , mask_toggle = mask_toggle, additional_context = additional_context, email_response= email_response)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))        

if __name__ == "__main__":
    app.run()
            
