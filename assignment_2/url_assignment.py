import os
import requests
from bs4 import BeautifulSoup
import re

dangerous_words = {"bomb", "kill", "murder", "terror", "terrorist", "terrorists", "terrorism"}

def download_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (status code >= 400)
        return response.content, response.headers.get('content-type')
    except requests.RequestException as e:
        print(f"Error occurred while fetching content: {e}")
        return None, None

def check_for_dangerous_words(content):
    if content is None:
        return []

    text_content = content.lower()  # Convert text to lowercase for case-insensitive matching
    found_words = []
    for word in dangerous_words:
        occurrences = len(re.findall(r'\b{}\b'.format(re.escape(word)), text_content))
        if occurrences > 0:
            found_words.append((word, occurrences))
    return found_words

def save_content_to_file(content, path):
    try:
        with open(path, 'wb') as file:
            file.write(content)
        print(f"Saving succeeded to: {path}")
    except IOError as e:
        print(f"Error occurred while saving content: {e}")

def main():
    url = input("Enter the URL you want to download: ")
    content, content_type = download_url_content(url)
    if content:
        if content_type and 'text/html' in content_type:
            text_content = BeautifulSoup(content, 'html.parser').get_text()
            found_words = check_for_dangerous_words(text_content)
            if found_words:
                print("The content contains the following dangerous words and their occurrences:")
                for word, occurrences in found_words:
                    print(f"- {word}: {occurrences} occurrences")
            else:
                print("The content does not contain any dangerous words.")
        else:
            print("Doesn't appear to be an HTML file with utf-8 encoding.")

        save_path = input("Enter a valid path to save the contents: ")
        try:
            save_content_to_file(content, save_path)
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
