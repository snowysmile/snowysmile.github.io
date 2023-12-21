from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from openai import OpenAI
import emoji
import ssl
import os
import re
import asyncio
emojis = emoji.UNICODE_EMOJI["en"].keys()

app = Flask(__name__)
CORS(app)

def dprint(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

def lprint(*args, **kwargs):
    if DEBUG_MODE or LOCAL_TEST:
        print(*args, **kwargs)

@app.route('/chatgpt-emoji', methods=['POST'])
async def chatgpt_emoji():
    try:
        client = OpenAI(
            api_key=request.json['apikey'],
        )
        input_text = request.json['text']
        lprint("input_text:", input_text)
        messages = [{
            "role": "system",
            "content": "Please translate my input to many many many emojis as many as you can. Do your best with only emojis only."
        }, {"role": "user", "content": input_text}]

        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=80,
                )
            )
        except asyncio.TimeoutError:
            print("chatGPT(): The request timed out!")

        response_text = response.choices[0].message.content

        emoji_list = []
        demoji_text = emoji.demojize(response_text)
        matches = re.findall(r':[^:]*:', demoji_text)
        for word in matches:
            the_emoji = emoji.emojize(word)
            if the_emoji not in emoji_list:
                emoji_list.append(the_emoji)
        emoji_text = ' '.join(emoji_list)

        # return response_text + " \n " + emoji_text
        return emoji_text

    except Exception as e:
        print('error:', str(e))
        return jsonify({'error': str(e)})

@app.route('/chatgpt', methods=['POST'])
async def chatgpt():
    try:
        client = OpenAI(
            api_key=request.json['apikey'],
        )
        input_text = request.json['text']
        query_type = request.json['query']
        max_token = 360
        temperature = 0.75 # not used here yet
        model = "gpt-3.5-turbo"

        lprint("input_text:", input_text)
        lprint("query_type:", query_type)

        messages = []
        if query_type == "easy-gpt":
            messages.append({
                "role": "system",
                "content": "Answer decently. Don't reply long unless I ask."
            })
        elif query_type == "cute-japanese":
            messages.append({
                "role": "system",
                "content": "Please translate my input sentence to happy, friendly, and gramatically correct Japanese. ONLY translate, DON'T change my meaning."
            })
        elif query_type == "cute-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to cute and natural Japanese."
            })
        elif query_type == "lovely-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to considerate, lovely and friendly Japanese with cute and fun 顔文字. (Don't make the texts much longer than before)"
            })
        elif query_type == "casual-ja":
            messages.append({
                "role": "system",
                "content": "Please translate my input text to casual, relaxing and natural Japanese."
            })
        elif query_type == "no-katanana-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard Japanese. Meantime, minimize the use of katakana vocabulary (カタカナ語を似た意味の漢字語に置き換えてみましょう！例えば：アルゴリズム->算法; クラブ->倶楽部)."
            })
        elif query_type == "translate-ja":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard Japanese."
            })
        elif query_type == "translate-en":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard English."
            })
        elif query_type == "translate-cn":
            messages.append({
                "role": "system",
                "content": "You will be provided with statements, and your task is to translate them to decent, natural, and standard Traditional Chinese."
            })
        elif query_type == "sentence-emojis":
            messages.append({
                "role": "system",
                "content": "Please add many 顔文字 to my input sentence to make it cute and interesting. Don't do other things."
            })
        elif query_type == "related-emojis":
            messages.append({
                "role": "system",
                "content": "Please convert input to related emojis, answer me with as many different emojis as you can."
            })
            max_token = max_token // 2
        elif query_type == "grammar-fix":
            messages.append({
                "role": "system",
                "content": f"Please be my decent language teacher. You will be provided with statements, please check the grammar mistakes seriously and and fix it. Make your reply succinct."
            })
        elif query_type == "grammar-check":
            messages.append({
                "role": "system",
                "content": f"Please be my decent language teacher. You will be provided with statements, please check the grammar mistakes seriously and list them clearly with bullet points. If it has any mistakes, also tell me a best decent way to express it in its same language(En or Jp). Make your reply succinct." + "Please explain it nicely."
            })
        elif query_type == "grammar-fix-gpt4":
            messages.append({
                "role": "system",
                "content": f"Please be my decent language teacher. You will be provided with statements, please check the grammar mistakes seriously and and fix it. Make your reply succinct."
            })
            model = "gpt-4"; max_token = max_token // 2
        elif query_type == "grammar-check-gpt4":
            messages.append({
                "role": "system",
                "content": f"Please be my decent language teacher. You will be provided with statements, please check the grammar mistakes seriously and list them clearly with bullet points. If it has any mistakes, also tell me a best decent way to express it in its same language(En or Jp). Make your reply succinct." + "Please explain it nicely."
            })
            model = "gpt-4"; max_token = max_token // 2
        else:
            print("wrong query type")
            return "wrong query type"

        messages.append({"role": "user", "content": input_text})

        try:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None,
                lambda: client.chat.completions.create(
                    messages=messages,
                    max_tokens=max_token,
                    model=model,
                )
            )
        except asyncio.TimeoutError:
            print("chatGPT(): The request timed out!")

        response_text = response.choices[0].message.content
        response_token = response.usage.total_tokens

        lprint("response_text:", response_text)
        lprint("response:", response.usage)

        if query_type == "related-emojis":
            emoji_list = []
            demoji_text = emoji.demojize(response_text)
            matches = re.findall(r':[^:]*:', demoji_text)
            for word in matches:
                the_emoji = emoji.emojize(word)
                if the_emoji not in emoji_list:
                    emoji_list.append(the_emoji)
            emoji_text = ' '.join(emoji_list)
            return emoji_text
        else:
            return response_text

    except Exception as e:
        print('error:', str(e))
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    LOCAL_TEST = True if 0 else False
    DEBUG_MODE = True if 0 else False

    if LOCAL_TEST:
        print("LOCAL_TEST")
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='localhost', use_reloader=False)
    else:
        print("SERVER_RUN")
        current_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_path)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(current_dir + '/fullchain.pem', current_dir + '/privkey.pem')
        app.run(debug=DEBUG_MODE, threaded=True, port=3002, host='0.0.0.0', use_reloader=False, ssl_context=context)
