from flask import Blueprint, render_template, request
from .llmapi import send_to_llm
import json

main = Blueprint('main', __name__)

@main.route('/')
def form():
    return render_template('index.html')

@main.route('/step1')
def step1():
    return render_template('step1form.html')

@main.route('/step3')
def step3():
    return render_template('step3form.html')

@main.route('/step4')
def step4():
    return render_template('step4form.html')


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400

    api, model = request.form["llmAPI"].split(":", 1)

    response = send_to_llm(file,api,model, 1, [])
    print(response)
    return response

@main.route('/mitigations', methods=['POST'])
def estimate():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400

    api, model = request.form["llmAPI"].split(":", 1)

    mitigations_json = request.form.get("mitigations_list", "['m1036']")
    try:
        mitigations_list = json.loads(mitigations_json) 
    except json.JSONDecodeError:
        return "Invalid mitigations_list JSON", 400
    print(mitigations_list)
    response = send_to_llm(file,api,model,3,mitigations_list)
    print(response)
    return response

@main.route('/estimate', methods=['POST'])
def find_mitigations():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400

    api, model = request.form["llmAPI"].split(":", 1)

    response = send_to_llm(file,api,model,4,[])
    print(response)
    return response

@main.route('/getThreats', methods=['POST'])
def get_threats():
    return "<h1>Threats!</h1>"
