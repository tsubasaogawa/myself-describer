"""
Text form module.
"""
from wtforms import Form, TextField, SelectField, SubmitField
from wtforms.validators import Required, Length


class TextForm(Form):
    """
    Text form class.
    """
    start_word = TextField(
        u'start_with',
        validators=[
            Required(u'Required'),
            Length(min=1, max=10, message=u'up to 10'),
        ],
        render_kw={"placeholder": u"e.g. 今日"},
    )

    word_num = SelectField(
        u'word_num',
        coerce=str,
        choices=[(str(i), str(i)) for i in range(5, 21, 5)],
    )

    submit = SubmitField(
        u'Make a sentence',
        render_kw={"class": "pure-button pure-button-primary"}
    )
