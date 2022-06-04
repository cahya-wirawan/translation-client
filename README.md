# Translation Client

## Client for machine translation service

### Translate.cli 
It is a command line interface for the Translation API using the REST API from 
https://translation-api.ai-research.id/translate/v1

#### Usage:
First we have to set the environment variable TRANSLATION_API_KEY or pass it as an argument such as:
   $ translate-cli.py -k <key>
or
   $ export TRANSLATION_API_KEY=<key> && translate-cli.py

By default, source language is Indonesian and target language is English.
This can be set by passing the arguments --source "id" and --target "en", or vice versa.

An example with key:
- Translate a text from Indonesian to English with the auth key "Abc123":
  ```
  $ python translate-cli.py -t "Halo, apa kabar? Siapa namamu?" -k Abc123
  ```
   
- Translate a text from English to Indonesian with the key "Abc123":
  ```
  $ python translate-cli.py --source "en" --target "id" -t "Hi, how are you? would you like to drink with me?" -k Abc123
  ```

Some examples after the environment variable TRANSLATION_API_KEY is set:
- Translate a text file from English to Indonesian:
  ```
  $ python translate-cli.py --source "en" --target "id" -f "file.txt"
  ```

- Translate a text file using the model "finance" from Indonesian to English:
  ```
  $ python translate-cli.py --source "id" --target "en" -f "file.txt" -m finance
  ```

- Translation using interactive mode and the model "standard" from Indonesian to English:
  ```
  $ python translate-cli.py -i -m standard
  ```

- Translate a text file with pipe:
  ```
  $ cat file.txt | python translate-cli.py
  ```
