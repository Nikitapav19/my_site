from flask_uploads import IMAGES, UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import PasswordField, StringField, BooleanField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired

photos = UploadSet("photo", IMAGES)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, "Only images are allowed"),
            FileRequired("File field should not be empty")
        ]
    )
    submit = SubmitField("Upload")
