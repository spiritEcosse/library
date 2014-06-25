from wtforms import Form, BooleanField, TextField, PasswordField, validators, SelectMultipleField, widgets, SelectField
from wtforms.validators import StopValidation, ValidationError, InputRequired

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()

class BookForm(Form):
	title = TextField('Title', [validators.Length(min=2, max=50)])
	authors = MultiCheckboxField('Authors', choices=[], default=[], coerce=int, validators=[InputRequired()])

class AuthorForm(Form):
	name = TextField('Name', [validators.Length(min=2, max=50)])
	books = MultiCheckboxField('Books', choices=[], default=[], coerce=int, validators=[InputRequired()])
