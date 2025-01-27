from flask import Flask, render_template_string, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chuck Norris Quotes</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
            background-color: #f5f5f5;
        }
        .quote-container {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .quote {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        .button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>Chuck Norris Quote Generator</h1>
    <div class="quote-container">
        <p class="quote">{{ quote }}</p>
    </div>
    <a href="/" class="button">Get New Quote</a>
    <br><br>
    <a href="https://j25.AppFarms.org/cdn-cgi/access/logout" class="button" style="background-color: #f44336;">Logout</a>
</body>
</html>
'''

def log_request(ip, email):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - IP: {ip} - Email: {email}\n"
    
    with open('request_log.txt', 'a') as f:
        f.write(log_entry)

def get_chuck_norris_quote():
    try:
        response = requests.get('https://api.chucknorris.io/jokes/random')
        if response.status_code == 200:
            return response.json()['value']
        return "Chuck Norris is currently roundhouse kicking our servers. Please try again."
    except:
        return "Chuck Norris has temporarily disabled the internet. Please try again later."

@app.route('/auth/logout')
def logout():
    return '', 401  # This will trigger CloudFlare to show the login page again

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    email = request.headers.get('Cf-Access-Authenticated-User-Email', 'unknown')
    log_request(ip, email)
    quote = get_chuck_norris_quote()
    return render_template_string(HTML_TEMPLATE, quote=quote)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

