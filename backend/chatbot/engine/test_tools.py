from language_tool import translate_input, translate_output

def main():
    trans_prompt, native_lang = translate_input("¿Qué pasa si me detiene ICE?")
    output = translate_output("I am a chatbot", native_lang)

if __name__ == "__main__":
    main()