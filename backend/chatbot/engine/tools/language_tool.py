import os
from dotenv import load_dotenv
import deepl

load_dotenv()
translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))

# Detects user language and translates input to English for llm
def translate_input(text):
    result = translator.translate_text(text, target_lang="EN-US")
    native_lang = result.detected_source_lang
    print(result.text, native_lang)
    return result.text, native_lang    

# Translates llm response from English back to user language
def translate_output(text, native_lang):
    result = translator.translate_text(text, target_lang=native_lang)
    print(result.text)
    return result.text
