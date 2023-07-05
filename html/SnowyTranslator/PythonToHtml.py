from flask import Flask, render_template, request, jsonify
import aiohttp
from bs4 import BeautifulSoup
import asyncio

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('SnowySpeechTranslator.html')

@app.route('/process', methods=['POST'])
def process():
    text = request.form['jpExpInputName']
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(ichimoe_japanese_split(text))
    loop.close()
    return jsonify(result=result)

@app.route('/tts', methods=['GET'])
def tts():
    text = request.args.get('text', '')
    source_language = request.args.get('source_language', 'ja')
    url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={source_language}&client=tw-ob&q={text}"
    response = requests.get(url)
    return response.content, response.status_code, {'Content-Type': response.headers['Content-Type']}

async def ichimoe_japanese_split(text):
    print("text:", text)
    inner_html = ""
    try:
        url = f"https://ichi.moe/cl/qr/?q={text}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.read(), 'html.parser')
        row_gloss_rows = soup.find_all('div', class_='row gloss-row')
        for row_gloss_row in row_gloss_rows:
            glosses = row_gloss_row.find_all('div', class_='gloss')
            romaji_str = ""
            inner_html += " 【"
            for i in range(len(glosses)):
                gloss = glosses[i]
                hiragana = gloss.find('dt')
                if i > 0:
                    inner_html += " - "
                    romaji_str += " "

                word = hiragana.get_text()
                word = word.replace("1. ", "")
                word = word.replace("【", "<rt>")
                word = word.replace("】", "</rt>")
                word = "<ruby> " + word + "</ruby>"
                romaji = gloss.find('em').get_text()
                romaji_str += romaji
                inner_html += f"{word}"
            inner_html += f" | {romaji_str}】<br> "
        return inner_html
    except Exception as e:
        return f"japanese_split: an error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5000, host='localhost', use_reloader=False)
