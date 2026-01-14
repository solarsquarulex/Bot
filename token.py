from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# HTML Template with modern UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DEVILXGOD Token Checker</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(0,0,0,0.7);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,255,255,0.3);
        }
        h1 {
            color: cyan;
            text-align: center;
            text-shadow: 0 0 10px rgba(0,255,255,0.5);
        }
        textarea {
            width: 100%;
            padding: 10px;
            background: #111;
            color: lime;
            border: 1px solid #444;
            border-radius: 5px;
            font-family: monospace;
        }
        button {
            background: linear-gradient(45deg, #ff00cc, #3333ff);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            margin-top: 15px;
            width: 100%;
            transition: all 0.3s;
        }
        button:hover {
            transform: scale(1.02);
            box-shadow: 0 0 15px rgba(255,0,255,0.5);
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background: rgba(0,0,0,0.5);
            border-radius: 10px;
            border-left: 4px solid cyan;
        }
        .checkbox {
            margin: 15px 0;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TOKEN CHECKER</h1>
        
        <form method="POST">
            <textarea name="token" rows="5" placeholder="PASTE FACEBOOK TOKEN HERE..."></textarea>
            <button type="submit">CHECK TOKEN</button>
        </form>
        
        {% if result %}
        <div class="result">
            <div class="checkbox" style="color: {% if result.status == 'valid' %}lime{% else %}red{% endif %}">
                • Status: {{ result.status|upper }}
            </div>
            {% if result.status == 'valid' %}
                <div class="checkbox">• Name: {{ result.data.name }}</div>
                <div class="checkbox">• Email: {{ result.data.email }}</div>
                <div class="checkbox">• Birthday: {{ result.data.birthday }}</div>
                <div class="checkbox">• ID: {{ result.data.id }}</div>
                <div class="checkbox">• Profile: <a href="https://{{ result.data.link }}" target="_blank">{{ result.data.link }}</a></div>
            {% else %}
                <div class="checkbox">• Error: {{ result.error }}</div>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="footer">
            MADE BY DEVILXGOD | USE RESPONSIBLY
        </div>
    </div>
</body>
</html>
"""

def check_token(token):
    try:
        url = "https://graph.facebook.com/me"
        params = {
            'access_token': token,
            'fields': 'id,name,email,birthday'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            return {
                'status': 'invalid',
                'error': data['error']['message']
            }
        return {
            'status': 'valid',
            'data': {
                'name': data.get('name', 'N/A'),
                'email': data.get('email', 'N/A'),
                'birthday': data.get('birthday', 'N/A'),
                'id': data.get('id', 'N/A'),
                'link': f"facebook.com/{data.get('id', '')}"
            }
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        token = request.form.get('token', '').strip()
        if token:
            result = check_token(token)
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
