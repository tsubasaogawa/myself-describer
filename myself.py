# coding: utf-8

from flask import Flask, render_template, request
from text_generator import TextGenerator
from text_form import TextForm
import sys

app = Flask(__name__)
model_file = './myself.model'
title = 'virtual-ogawa'
host = '0.0.0.0'

@app.route('/', methods=['POST', 'GET'])
def describe():
  generated_text = ''
  form = TextForm(request.form)
  if request.method == 'POST' and form.validate():
    start_word = form.start_word.data
    word_num = form.word_num.data
    generator = TextGenerator(model_file, start_word, word_num)
    generated_text = generator.execute()
    if generated_text is None:
      generated_text = "Sorry! '%s' is unknown word..." % start_word

  return render_template('describe.html', title=title, generated_text=generated_text, form=form)

if __name__ == "__main__":
  app.run(host=host, debug=True)
