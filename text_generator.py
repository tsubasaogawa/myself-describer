# coding: utf-8

# This code is greatly based on chainer/sample/ptb/gentxt.py

"""Example to generate text from a recurrent neural network language model.

This code is ported from following implementation.
https://github.com/longjie/chainer-char-rnn/blob/master/sample.py

"""

import sys

import numpy as np
import six

import chainer
from chainer import cuda
import chainer.functions as F
import chainer.links as L
import chainer_fixed.serializers

import train_ptb

class TextGenerator:
  def __init__(self, model_file, primetext, length):
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', '-m', type=str, required=True,
                        help='model data, saved by train_ptb.py')
    parser.add_argument('--primetext', '-p', type=str, required=True,
                        default='',
                        help='base text data, used for text generation')
    parser.add_argument('--seed', '-s', type=int, default=123,
                        help='random seeds for text generation')
    parser.add_argument('--unit', '-u', type=int, default=650,
                        help='number of units')
    parser.add_argument('--sample', type=int, default=1,
                        help='negative value indicates NOT use random choice')
    parser.add_argument('--length', type=int, default=20,
                        help='length of the generated text')
    parser.add_argument('--gpu', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    args = parser.parse_args()
    """

    self.model_file = model_file
    self.primetext = primetext
    self.length = int(length) if length != '' else 5
    self.seed = 123
    self.unit = 650
    self.sample = 1
    self.gpu = -1

  def execute(self):
    np.random.seed(self.seed)
    chainer.config.train = False

    xp = cuda.cupy if self.gpu >= 0 else np

    # load vocabulary
    vocab = chainer.datasets.get_ptb_words_vocabulary()
    ivocab = {}
    for c, i in vocab.items():
      ivocab[i] = c

    # should be same as n_units , described in train_ptb.py
    n_units = self.unit

    lm = train_ptb.RNNForLM(len(vocab), n_units)
    model = L.Classifier(lm)

    chainer_fixed.serializers.load_npz(self.model_file, model)

    if self.gpu >= 0:
      cuda.get_device_from_id(self.gpu).use()
      model.to_gpu()

    model.predictor.reset_state()

    if isinstance(self.primetext, six.binary_type):
      self.primetext = self.primetext.decode('utf-8')

    if self.primetext in vocab:
      prev_word = chainer.Variable(xp.array([vocab[self.primetext]], xp.int32))
    else:
      print('ERROR: Unfortunately ' + self.primetext + ' is unknown.')
      return None

    prob = F.softmax(model.predictor(prev_word))
    result = self.primetext + ' '

    for i in six.moves.range(self.length):
      prob = F.softmax(model.predictor(prev_word))
      if self.sample > 0:
        probability = cuda.to_cpu(prob.data)[0].astype(np.float64)
        probability /= np.sum(probability)
        index = np.random.choice(range(len(probability)), p=probability)
      else:
        index = np.argmax(cuda.to_cpu(prob.data))

      if ivocab[index] == '<eos>':
        result += '.'
      else:
        result += ivocab[index] + ' '

      prev_word = chainer.Variable(xp.array([index], dtype=xp.int32))

    result += "\n"
    return result

if __name__ == '__main__':
  exit(1)
