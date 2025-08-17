import os
from dotenv import load_dotenv
from openai import OpenAI
from .step1prompts import step1_category_prompt, step1_example_response
from .step3prompts import step3_start_prompt, step3_end_prompt, step3_category_prompt, step3_example_response
from .step4prompts import step4_complete_prompt, step4_example_response
import google.generativeai as genai
import openai
import pdfplumber
import json
import time
from groq import Groq

load_dotenv()

def send_to_llm(file, api, model, step, mitigations):
    print("Sending request to "+api+" "+model)
    with pdfplumber.open(file) as pdf:
        pdf_text = ''
        for page in pdf.pages:
            pdf_text += page.extract_text()
    if step == 1:
        category_prompt = step1_category_prompt
        simulate = step1_example_response
    elif step==3:
        category_prompt = []                           
        for prompt in step3_category_prompt:           
            parts = [step3_start_prompt]   
            for mitigation in mitigations:    
                if mitigation in prompt:
                    parts.append(f"{mitigation}: {prompt[mitigation]}")
            if len(parts) > 1:                    
                parts.append(step3_end_prompt)
                category_prompt.append("".join(parts)) 
        simulate = step3_example_response
    else: 
        category_prompt = [step4_complete_prompt]
        simulate = step4_example_response

    if model=="simulate" or api=="simulate":
        time.sleep(2)
        return simulate
 
    return category_get_response(pdf_text, api, model, category_prompt)


def get_response(pdf_text, api, model, prompt):
    if api=="openai":
        return openai_api(pdf_text, model, prompt)
    elif api=="deepseek":
        return deepseek_api(pdf_text, model, prompt)
    elif api=="gemini":
        return gemini_api(pdf_text, model, prompt)
    elif api=="groq":
        return groq_api(pdf_text, model, prompt)
    else:
        return {}

    
def category_get_response(pdf_text, api, model, category_prompt):
    complete_response = {}
    for prompt in category_prompt:
        response = get_response(pdf_text, api, model, prompt)
        print(response)
        complete_response.update(response)
    return complete_response

def check_response(response):
    start = response.find("{")
    end = response.rfind("}")
    if start != -1 and end != -1 and start < end:
        response = response[start:end+1]
    try:
        response = json.loads(response)
        return response
    except json.JSONDecodeError:
        return {}

def openai_api(pdf_text, model, prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI()
    if model=="o3-mini":
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system", 
                    "content": (prompt)},
                {
                    "role": "user",
                    "content": f"<doc>{pdf_text}</doc>"
                }
            ]
        )
    else: 
        completion = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[
                {
                    "role": "system", 
                    "content": (prompt)},
                {
                    "role": "user",
                    "content": f"<doc>{pdf_text}</doc>"
                }
            ]
        )
    response = completion.choices[0].message.content.replace('\n', '')
    return check_response(response)

def deepseek_api(pdf_text, model, prompt):  
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1" 
    )
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"<doc>{pdf_text}</doc>"}
        ],
        response_format={
        'type': 'json_object'
    }
    )

    response = completion.choices[0].message.content.replace('\n', '')
    return check_response(response)

def gemini_api(pdf_text, model, prompt):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    full_prompt = f"{prompt} <doc>{pdf_text}</doc>"
    
    generation_config = genai.types.GenerationConfig(
        temperature=0,
        top_p=1.0,
        top_k=1
    )
    model_obj = genai.GenerativeModel(model, generation_config=generation_config)
    response = model_obj.generate_content(full_prompt)

    return check_response(response.text)

def groq_api(pdf_text,model,prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"<doc>{pdf_text}</doc>"}
        ],
        temperature=0,
        max_completion_tokens=5000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    response = completion.choices[0].message.content.replace('\n', '')
    return check_response(response)