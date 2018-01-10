# coding: utf-8

from wtforms import Form, TextField
from wtforms.validators import Required, Length

class TextForm(Form):
  start_word = TextField(u'start_with', validators=[
    Required(u'Required'),
    Length(min=1, max=10, message=u'up to 10')
  ])

  word_num = SelectField(u'word_num', choices=[
    (i, i) for i in range(5, 21, 5)
  ])

