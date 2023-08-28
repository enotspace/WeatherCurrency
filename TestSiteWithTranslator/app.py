from flask import Flask, render_template, url_for, request, redirect
from translate import Translator


def translate(text, from_lang, to_lang):
    Language={'English':"en", 'Ukrainian':"uk"}
    print(from_lang)
    translator= Translator(from_lang=Language[from_lang], to_lang=Language[to_lang])
    return translator.translate(text)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/translator', methods=['GET', 'POST'])
def translator():
    if request.method == "POST":
        output= request.form['text']
        from_lang=request.form['from_language']
        to_lang=request.form['to_language']
        return render_template("translator.html", input=output, output=translate(output, from_lang, to_lang))
    return render_template("translator.html")

if __name__ == '__main__':
    app.run()