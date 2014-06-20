from wtforms import Form, BooleanField, TextField, PasswordField, validators, SelectMultipleField, widgets, SelectField
from wtforms.validators import StopValidation, ValidationError

class MultiCheckboxField(SelectMultipleField):
	"""
	A multiple-select, except displays a list of checkboxes.

	Iterating the field will produce subfields, allowing custom rendering of
	the enclosed checkbox fields.
	"""
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()

class BookForm(Form):
	title = TextField('Title', [validators.Length(min=2, max=50)])

class AuthorForm(Form):
	name = TextField('Name', [validators.Length(min=2, max=50)])
	books = MultiCheckboxField('Book', choices=[], default=[])