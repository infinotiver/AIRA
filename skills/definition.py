import requests


def get_word_definition(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


# Function to format and speak the definition


def speak_definition(word, definition_data):
    response = ""
    if not definition_data:
        response += f"Sorry, I couldn't find the definition for {word}."
        return
    word_info = definition_data[0]

    # Word and phonetic pronunciation

    response += f"\nThe word {word} is pronounced as {word_info['phonetic']}."

    # Meanings and definitions

    for meaning in word_info["meanings"]:
        part_of_speech = meaning["partOfSpeech"]
        response = +f"\nAs a {part_of_speech}, it can mean:"

        for idx, definition in enumerate(meaning["definitions"], start=1):
            response += f"\n{idx}. {definition['definition']}"
    # Synonyms and antonyms

    synonyms = word_info.get("synonyms", [])
    antonyms = word_info.get("antonyms", [])

    if synonyms:
        response += f"\nSynonyms for {word} include: {', '.join(synonyms)}."
    if antonyms:
        response += f"\nAntonyms for {word} include: {', '.join(antonyms)}."
    return response
