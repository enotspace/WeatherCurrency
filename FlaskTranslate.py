from translate import Translator
text=input("Text for translate (autodetect)")
translator= Translator(to_lang="uk")
translation = translator.translate(text)
print(translation)