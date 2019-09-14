"""
Describe myself module.
"""
import os
import re
import glob
from datetime import date
import requests
from flask import Flask, render_template, request

from text_generator import TextGenerator
from text_form import TextForm


APP = Flask(__name__)
TITLE = 'virtual-ogawa'
HOST = '0.0.0.0'

MODEL_PATH = '{0}/model'.format(
    os.path.dirname(os.path.abspath(__file__))
)
MODEL_PATH_GLOB = '{0}/model_iter_*'.format(MODEL_PATH)
MODEL_FILE_REGEX = r'model_iter_(\d+)'

# ------------------------------ #

def download_model_file(url):
    """
    Download model file from internet.
    Environment variable `MODEL_FILE_URL` is must be set.
    """
    response = requests.get(url)
    downloaded_path = '{0}/{1}'.format(
        MODEL_PATH,
        os.path.basename(url),
    )
    with open(downloaded_path, 'wb') as handler:
        handler.write(response.content)

    print('model downloaded')
    return downloaded_path

def get_latest_model_file_name():
    """
    Get model file name in local storage.
    """
    local_model_files = glob.glob(MODEL_PATH_GLOB)
    if not local_model_files:
        model_url = os.environ.get('MODEL_FILE_URL')
        file_path = download_model_file(model_url)
        local_model_files = [file_path]

    return local_model_files[-1]

def get_model_information():
    """
    Get information of the model file.
    """
    model_filename = get_latest_model_file_name()
    iteration = re.search(MODEL_FILE_REGEX, model_filename)

    modified = date.fromtimestamp(
        os.path.getmtime(model_filename)
    ).strftime('%Y-%m-%d')
    size = os.path.getsize(model_filename)

    return {
        'name': model_filename,
        'iter': iteration.group(1),
        'modified': modified,
        'size': size,
    }

# ------------------------------ #

@APP.route('/', methods=['POST', 'GET'])
def describe():
    """
    Describe myself.
    """
    generated_text = ''
    model = None
    try:
        model = get_model_information()
    except FileNotFoundError as err:
        generated_text = err

    form = TextForm(request.form)
    if model and request.method == 'POST' and form.validate():
        start_word = form.start_word.data
        word_num = form.word_num.data
        generator = TextGenerator(model['name'], start_word, word_num)
        generated_text = generator.execute()
        if generated_text is None:
            generated_text = "Sorry! '{0}' is unknown word...".format(start_word)

    return render_template(
        'describe.html',
        title=TITLE,
        generated_text=generated_text,
        form=form,
        model=model,
    )

if __name__ == "__main__":
    APP.run(host=HOST, debug=True)
