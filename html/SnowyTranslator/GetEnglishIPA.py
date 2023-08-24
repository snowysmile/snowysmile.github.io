import requests
from bs4 import BeautifulSoup

DoesScrape = False
if (DoesScrape):
    url = ""
    response = requests.get(url)
    with open("scraped_page.html", "w", encoding="utf-8") as html_file:
        html_file.write(response.text)

"""
soup = BeautifulSoup(response.content, "html.parser")
post_response = requests.post(url + form_action, data=form_data)
american_radio = soup.find("input", {"name": "output_dialect", "value": "am"})
if american_radio:
    american_radio.parent["class"] = "btn btn-outline-secondary btn-sm active"
    print("american_radio.parent:", american_radio.parent)

line_by_line_radio = soup.find("input", {"name": "output_style", "value": "inline"})
if line_by_line_radio:
    line_by_line_radio.parent["class"] = "btn btn-outline-secondary btn-sm active"
    print("line_by_line_radio.parent:", line_by_line_radio.parent)
"""

def get_IPA(text):
    url = "https://tophonetics.com/"
    form_data = {
        "text_to_transcribe": text,
        "submit": "Show transcription",
        "output_style": "inline",
        "output_dialect": "am",
    }
    post_response = requests.post(url, data=form_data)

    post_soup = BeautifulSoup(post_response.content, "html.parser")
    transcr_output_element = post_soup.find(id="transcr_output")
    transcribed_word_elements = transcr_output_element.find_all("span", class_="transcribed_word")
    for transcribed in transcribed_word_elements:
        parent_div = transcribed.find_parent("div", class_="inline_ipa")
        if parent_div:
            inline_orig = parent_div.find_previous_sibling("div", class_="inline_orig")
            if inline_orig:
                print(f"{transcribed.text.strip()}: {inline_orig.text.strip()}")

get_IPA("I have a cat, I have 10 books. I have a girl")
