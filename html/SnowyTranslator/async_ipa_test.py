async def fetch_IPA(session, text):
    url = "https://tophonetics.com/"
    form_data = {
        "text_to_transcribe": text,
        "submit": "Show transcription",
        "output_style": "inline",
        "output_dialect": "am",
    }

    async with session.post(url, data=form_data) as response:
        post_content = await response.text()
        post_soup = BeautifulSoup(post_content, "html.parser")
        transcr_output_element = post_soup.find(id="transcr_output")
        transcribed_word_elements = transcr_output_element.find_all("span", class_="transcribed_word")
        results = []
        for transcribed in transcribed_word_elements:
            parent_div = transcribed.find_parent("div", class_="inline_ipa")
            if parent_div:
                inline_orig = parent_div.find_previous_sibling("div", class_="inline_orig")
                if inline_orig:
                    results.append((transcribed.text.strip(), inline_orig.text.strip()))
        return results