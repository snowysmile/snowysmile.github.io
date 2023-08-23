import requests
from bs4 import BeautifulSoup
import unicodedata

DoesScrape = False
if (DoesScrape):
    url = "https://www.purpleculture.net/chinese-pinyin-converter/?session=f55c0c0c86315671cf71762d4c49a087"
    response = requests.get(url)
    with open("scraped_page.html", "w", encoding="utf-8") as html_file:
        html_file.write(response.text)

def is_chinese_kanji(char):
    return 'CJK' in unicodedata.name(char, '')

def get_pinyin(text):
    url = "https://www.purpleculture.net/chinese-pinyin-converter"
    form_data = {
        "wdqchs": text,
        "convert": "y"
    }

    response = requests.post(url, data=form_data)
    with open("scraped_page.html", "w", encoding="utf-8") as html_file:
        html_file.write(response.text)

    soup = BeautifulSoup(response.content, "html.parser")
    annoatedtext_element = soup.find(id="annoatedtext")
    pinyin_elements = annoatedtext_element.find_all("a", class_="pinyin")
    pinyins = []
    for pinyin in pinyin_elements:
        pinyins.append(pinyin.text.strip())
    print("pinyins:", pinyins)

    inner_html = ""
    textPos = 0
    pinyinId = 0
    while textPos < len(text):
        if pinyinId < len(pinyins) and is_chinese_kanji(text[textPos]):
            inner_html += f"<ruby>&nbsp;{text[textPos]}<rt>&ensp;{pinyins[pinyinId]}</rt></ruby>"
            pinyinId += 1
            textPos += 1
        else:
            inner_html += text[textPos]
            textPos += 1
    print("inner_html:", inner_html)
    return inner_html

get_pinyin("一閃一閃亮晶晶，滿天都是小星星。")