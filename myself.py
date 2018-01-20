# coding: utf-8

from flask import Flask, render_template, request
from text_generator import TextGenerator
from text_form import TextForm
import sys, os
import re, glob

def get_model_information():
  base = os.path.dirname(os.path.abspath(__file__))
  model_files = glob.glob('{}/model/model_iter_*'.format(base))
  if not len(model_files):
    raise FileNotFoundError('no model file found')

  latest_model_file = model_files[-1]
  iteration = re.search(r'model_iter_(\d+)', latest_model_file)

  return { 'name': latest_model_file, 'iter': iteration.group(1) }

app = Flask(__name__)
title = 'virtual-ogawa'
host = '0.0.0.0'

@app.route('/', methods=['POST', 'GET'])
def describe():
  generated_text = ''
  model = None
  try:
    model = get_model_information()
  except FileNotFoundError as e:
    generated_text = e

  form = TextForm(request.form)
  if model and request.method == 'POST' and form.validate():
    start_word = form.start_word.data
    word_num = form.word_num.data
    generator = TextGenerator(model['name'], start_word, word_num)
    generated_text = generator.execute()
    if generated_text is None:
      generated_text = "Sorry! '%s' is unknown word..." % start_word

  return render_template('describe.html',
      title=title,
      generated_text=generated_text,
      form=form,
      model_iter=model['iter'])

if __name__ == "__main__":
  app.run(host=host, debug=True)
