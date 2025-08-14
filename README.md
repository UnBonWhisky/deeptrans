# Deeptrans

This is an asynchronous and a bit edited version of the Deepl translator API dependency.

> **Note**: I have no intention to add features or to maintain this project except for a personal use. This is a temporary solution to a temporary a problem. If you have ideas to maintain this project, your help is welcome

### Changes about the original one :

- This version is running asynchronously, so the translate functions are all using await
- This version shows the languages like google, so I can use it with my [googletrans fork](https://github.com/UnBonWhisky/googletrans) without changing much informations in my projects.

## Installation

### PyPI

Actually I have not posted this project on pypi. The better way is to use the git install from pip

### Repository

You can install the project directly from this repository.

```shell
pip install git+https://github.com/UnBonWhisky/deeptrans.git
```

## How to use

This version is actually an asynchronous version of deepl package.

#### Make a translation :
```py
from deeptrans import AsyncDeepLClient, SOURCE_LANGUAGES
import asyncio

async def main():
    api_key = "<YOUR_API_KEY>" # Your API key here

    async with AsyncDeepLClient(api_key) as client:
        # Simple translation
        result = await client.translate_text(
            "I am doing a test",
            target_lang="french",
            show_billed_characters=True
        )
        print(f"Translation: {result.text}") # Je fais un test
        print(f"Input text: {result.input}") # I am doing a test
        print(f"Detected language: {SOURCE_LANGUAGES[result.src.lower()]}") # english
        print(f"To language: {SOURCE_LANGUAGES[result.dest.lower()]}") # french
        print(f"Billed characters: {result.billed_characters}") # 17
```

#### Translate multiple texts at once :
```py
from deeptrans import AsyncDeepLClient
import asyncio

async def main():
    api_key = "<YOUR_API_KEY>" # Your API key here

    async with AsyncDeepLClient(api_key) as client:
        results = await client.translate_text(
            ["Hello", "How are you?"],
            target_lang="french"
        )
        for i, result in enumerate(results):
            print(f"Text {i+1}: {result.text}")
```

#### Other examples are availables in the [example file](/example.py)

## CLI

This package installs a CLI version which is lighter to make translations directly from the terminal.

### Example 1
```shell
$ dtrans -a "<YOUR_API_KEY>" -s fr "Bonjour tout le monde"
```
Returns :
```
Hello everyone
-----
Target Language: english
```
---
### Example 2
```shell
$ dtrans -a "<YOUR_API_KEY>" "Bonjour tout le monde"
```
Returns :
```
Hello everyone
-----
Detected language: french
Target Language: english
```
---
### Example 3
```shell
export DEEPTRANS="<YOUR_API_KEY>"
dtrans -d fr "I am doing a test" -bc
```
Returns :
```
Je fais un test
-----
Detected language: english
Target Language: french
Billed Characters: 17
```