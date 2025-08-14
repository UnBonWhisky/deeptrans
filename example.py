# Example usage
from deeptrans import AsyncDeepLClient, Formality, ModelType, SOURCE_LANGUAGES
import asyncio

async def main():
    api_key = "<YOUR_API_KEY>" # Your API key here

    async with AsyncDeepLClient(api_key) as client:
        # Simple translation
        result = await client.translate_text(
            "I am trying something with multiple mentions at once\n<@341257685901246466><@815328232537718794><#815328232537718794>",
            target_lang="french",
            show_billed_characters=True
        )
        print(f"Translation: {result.text}")
        print(f"Input text: {result.input}")
        print(f"Detected language: {SOURCE_LANGUAGES[result.src.lower()]}")
        print(f"To language: {SOURCE_LANGUAGES[result.dest.lower()]}")
        print(f"Billed characters: {result.billed_characters}")
        
        # Multiple texts
        results = await client.translate_text(
            ["Hello", "How are you?"],
            target_lang="FR",
            formality=Formality.MORE
        )
        for i, result in enumerate(results):
            print(f"Text {i+1}: {result.text}")
        
        # Advanced options
        result = await client.translate_text(
            "Hello <b>world</b>!",
            target_lang="ES",
            tag_handling="html",
            model_type=ModelType.QUALITY_OPTIMIZED
        )
        print(f"HTML translation: {result.text}")
        
        # Get usage
        usage = await client.get_usage()
        print(f"Used: {usage.character_count}/{usage.character_limit}")
        
        # Get supported source languages
        source_langs = await client.get_source_languages()
        print(f"Supported source languages: {len(source_langs)}")
        
        # Get supported target languages
        target_langs = await client.get_target_languages()
        print(f"Supported target languages: {len(target_langs)}")

# Run example
asyncio.run(main())