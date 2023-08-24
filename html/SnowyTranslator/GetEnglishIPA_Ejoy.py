import requests
from bs4 import BeautifulSoup

# The URL of the target website
url = "https://glotdojo.com/phonetic"

# Send an HTTP GET request to the URL
response = requests.get(url)
content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, "html.parser")

# Find the input area and button
text_area = soup.find("textarea", class_="text-input")
button = soup.find("button", class_="show-ts")

# Set the text in the input area
text_area.string = "i can't go fast"

# Simulate clicking the button by sending a POST request with the updated text
response = requests.post(url, data={"text": text_area.string})
print(response.content)

# Parse the updated HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the elements containing phonetic symbols
phonetic_divs = soup.find_all("div", class_="phonetic-text")

# Extract and print the phonetic symbols
for phonetic_div in phonetic_divs:
    print(phonetic_div.div.text)
