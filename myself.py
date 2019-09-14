# coding: utf-8

from flask import Flask, render_template, request
from text_generator import TextGenerator
from text_form import TextForm
import sys, os
import re, glob
import requests
from datetime import date


app = Flask(__name__)
title = 'virtual-ogawa'
host = '0.0.0.0'

model_path = '{}/model'.format(
  os.path.dirname(os.path.abspath(__file__))
)
model_file_glob = '{}/model_iter_*'.format(model_path)
model_file_url = 'YOUR MODEL FILE URL'

def download_model_file(url):
  response = requests.get(url)
  downloaded_path =  '{0}/{1}'.format(model_path, os.path.basename(model_file_url))
  with open(downloaded_path, 'wb') as f:
    f.write(response.content)

  print('model downloaded')
  return downloaded_path

def get_latest_model_file():
  model_files = glob.glob(model_file_glob)
  if not len(model_files):
    file_path = download_model_file(model_file_url)
    model_files = [file_path]
    # raise FileNotFoundError('no model file found')

  return model_files[-1]

def get_model_information():
  latest_model_file = get_latest_model_file()
  iteration = re.search(r'model_iter_(\d+)', latest_model_file)

  modified = date.fromtimestamp(os.path.getmtime(latest_model_file)).strftime('%Y-%m-%d')
  size = os.path.getsize(latest_model_file)
  return {
    'name': latest_model_file,
    'iter': iteration.group(1),
    'modified': modified,
    'size': size
  }

# ------------------------------ #

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
      model=model)

if __name__ == "__main__":
  app.run(host=host, debug=True)
