import os
import requests
from flask import Flask, redirect, render_template, request, send_from_directory, url_for

app = Flask(__name__)

# Umgebungsvariablen für Azure OpenAI
api_key = os.environ.get('API_KEY')
azure_endpoint = os.environ.get('AZURE_ENDPOINT')

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
    req = request.form.get('req')

    try:
        # Manuelle HTTP-POST-Anfrage mit der requests-Bibliothek
        response = requests.post(
            azure_endpoint,
            headers={
                "Content-Type": "application/json",
                "api-key": api_key
            },
            json={
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": req}
                ],
                "max_tokens": 150
            }
        )

        # Überprüfung, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
        else:
            return f"An error occurred: {response.status_code} - {response.text}", 500

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return f"An error occurred: {str(e)}", 500

    if req:
        print('Request for hello page received with req=%s' % req)
        return render_template('hello.html', req=answer)
    else:
        print('Request for hello page received with no req or blank req -- redirecting')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
