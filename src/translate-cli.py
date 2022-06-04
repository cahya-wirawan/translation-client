import os
import requests
import json
import sys
import argparse
import fileinput

"""
Author: Cahya Wirawan <cahya.wirawan@gmail.com>

This is a command line interface for the Translation API.
Usage:
First we have to set the environment variable TRANSLATION_API_KEY or pass it as an argument such as:
   $ translate-cli.py -k <key>
or
   $ export TRANSLATION_API_KEY=<key> && translate-cli.py

By default, source language is Indonesian and target language is English.
This can be set by passing the arguments --source "id" and --target "en", or vice versa.

An example with key:
1. Translate a text from Indonesian to English with the auth key "Abc123":
   $ python translate-cli.py -t "Halo, apa kabar? Siapa namamu?" -k Abc123
   
2. Translate a text from English to Indonesian with the key "Abc123":
   $ python translate-cli.py --source "en" --target "id" -t "Hi, how are you? would you like to drink with me?" -k Abc123

Some examples after the environment variable TRANSLATION_API_KEY is set:
3. Translate a text file from English to Indonesian:
   $ python translate-cli.py --source "en" --target "id" -f "file.txt"

4. Translate a text file using the model "finance" from Indonesian to English:
   $ python translate-cli.py --source "id" --target "en" -f "file.txt" -m finance

5. Translation using interactive mode and the model "standard" from Indonesian to English:
   $python translate-cli.py -i -m standard

6. Translate a text file with pipe:
    cat file.txt | python translate-cli.py
"""

REST_API_URL = 'https://translation-api.ai-research.id/translate/v1'
languages = {
    "en": "English",
    "id": "Indonesian"
}

def translate(texts, source="id", target="en", model="standard", rest_api_url=REST_API_URL, key=""):
    """
    Translate a text or a list of texts
    :param texts:
    :param model:
    :param rest_api_url:
    :param key:
    :return:
    """
    texts_type = type(texts)
    if texts_type == str:
        texts = [texts]
    my_request = {
      "q": texts,
      "source": source,
      "target": target,
      "model": model,
      "format": "",
      "key": key
    }
    response = requests.post(rest_api_url, data=json.dumps(my_request))
    if response.status_code == 200:
        response = response.json()
        if response['status'] == 'Success':
            if texts_type == str:
                return response["translations"][0]
            else:
                return response['translations']
        else:
            raise Exception(f"Error: {response['status']}")
    else:
        raise Exception(f"Error: {response.status_code} ({response.reason})")


def main():
    """
    Main function
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text", type=str, required=False, default=None,
                        help="The text to be translated")
    parser.add_argument("-i", "--interactive", required=False, default=False, action="store_true",
                        help="Interactive mode")
    parser.add_argument("--source", type=str, required=False, default="id",
                        help="The source language")
    parser.add_argument("--target", type=str, required=False, default="en",
                        help="The target language")
    parser.add_argument("-m", "--model", type=str, required=False, default="standard",
                        help="The translator model type [standard, finance]")
    parser.add_argument("-f", "--file", type=str, required=False, default=None,
                        help="The file to be translated")
    parser.add_argument("-p", "--paragraph_max", type=int, required=False, default=10,
                        help="The maximal number of paragraph to be translated in one request")
    parser.add_argument("-l", "--translate_per_line", required=False, default=False, action="store_true",
                        help="Translate directly each line of the file (don't concatenate them)")
    parser.add_argument("-r", "--rest_api_url", type=str, required=False, default=REST_API_URL,
                        help="The Rest API URL")
    parser.add_argument("-k", "--key", type=str, required=False, default=None,
                        help="The authorization key")
    args = parser.parse_args()
    model = args.model
    if args.key:
        translation_api_key = args.key
    elif os.getenv("TRANSLATION_API_KEY"):
        translation_api_key = os.getenv("TRANSLATION_API_KEY")
    else:
        translation_api_key = ""
    if args.text:
        print(translate(args.text, source=args.source, target=args.target, model=args.model,
                        rest_api_url=args.rest_api_url, key=translation_api_key))
    elif args.interactive:
        while True:
            try:
                text = input(f"{languages[args.source]}: ")
                translation = translate(text, source=args.source, target=args.target, model=args.model,
                                        rest_api_url=args.rest_api_url, key=translation_api_key)
                print(f"{languages[args.target]}: {translation}")
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit()
    else:
        texts = []
        text = ""
        paragraph_max = args.paragraph_max
        if args.file:
            lines = fileinput.input(args.file)
        else:
            lines = sys.stdin
        try:
            for line in lines:
                if line.strip() == "" or args.translate_per_line:
                    if args.translate_per_line:
                        text = line.strip()
                    texts.append(text)
                    text = ""
                    if len(texts) == paragraph_max:
                        for paragraph in translate(texts, source=args.source, target=args.target, model=args.model,
                                                   rest_api_url=args.rest_api_url, key=translation_api_key):
                            print(f"{paragraph}")
                        texts = []
                else:
                    text += line.strip() + " "
            if text != "":
                texts.append(text)
            for paragraph in translate(texts, source=args.source, target=args.target, model=args.model,
                                       rest_api_url=args.rest_api_url, key=translation_api_key):
                print(f"{paragraph}")
        except KeyboardInterrupt:
            if text != "":
                texts.append(text)
            for paragraph in translate(texts, source=args.source, target=args.target, model=args.model,
                                       rest_api_url=args.rest_api_url, key=translation_api_key):
                print(f"{paragraph}\n")
            sys.exit()


if __name__ == '__main__':
    main()
