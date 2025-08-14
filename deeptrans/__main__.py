import argparse, sys, asyncio, os
from deeptrans import AsyncDeepLClient, SOURCE_LANGUAGES, LANGUAGES

async def main():
    parser = argparse.ArgumentParser(description="Python DeepL as a command-line tool")
    parser.add_argument('text',
        help='The text you want to translate.')
    parser.add_argument('-a', '--auth', default=None,
        help='Your DeepL API key. If not provided, will use the DEEPTRANS environment variable.')
    parser.add_argument('-d', '--dest', default='en-us',
        help='The destination language you want to translate. (Default: en-us)')
    parser.add_argument('-s', '--src', default=None,
        help='The source language you want to translate. (Default: Will be detected automatically)')
    parser.add_argument('-bc', '--billed_characters', action='store_true',
        help='Show the number of billed characters for this translation request.')
    args = parser.parse_args()

    # Get API key from argument or environment variable
    api_key = args.auth or os.getenv('DEEPTRANS')
    
    if not api_key:
        print("Error: DeepL API key not provided. Please use -a/--auth argument or set DEEPTRANS environment variable.", file=sys.stderr)
        sys.exit(1)

    async with AsyncDeepLClient(api_key) as client:
        result = await client.translate_text(
            args.text,
            target_lang=args.dest,
            source_lang=args.src,
            show_billed_characters=True if args.billed_characters else False
        )
        print(f"{result.text}")
        print("-----")
        print(f"Detected language: {SOURCE_LANGUAGES[result.src.lower()]}\n" if args.src is None else "", end="")
        print(f"Target Language: {LANGUAGES[result.dest.lower()]}")
        if args.billed_characters:
            print(f"Billed Characters: {result.billed_characters}")

def cli_main():
    """Entry point for the CLI script."""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
