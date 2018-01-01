# coding: utf-8

from flask import Flask, render_template, request
from text_generator import TextGenerator

app = Flask(__name__)
model_file = './myself.model'
title = 'virtual-ogawa'
host = '0.0.0.0'

@app.route('/', methods=['POST', 'GET'])
def describe():
  generated_text = ''
  if request.method == 'POST':
    start_word = request.form['start_word']
    word_num = request.form['word_num']
    generator = TextGenerator(model_file, start_word, word_num)
    generated_text = generator.execute()
    if generated_text is None:
      generated_text = "Sorry! '%s' is unknown word..." % start_word

  return render_template('describe.html', title=title, generated_text=generated_text)

if __name__ == "__main__":
  app.run(host=host, debug=True)
