from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('home.html', guilds=get_guilds())


def get_guilds():
    file = open('guilds.txt', 'r')
    data = file.readlines()
    file.close()
    data = [i.replace('\n','') for i in data]
    data = [i.split(":") for i in data]
    guilds = data
    return guilds

def run_flask():
    app.run(host='0.0.0.0', port=5001, debug=False)