from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask_uploads import IMAGES, UploadSet


photos = UploadSet("photos", IMAGES)


class AddItem(FlaskForm):
    item_name = StringField('Имя предмета', validators=[DataRequired()])
    price = StringField("Цена", validators=[DataRequired()])
    # type = StringField("Тип", validators=[DataRequired()])
    about = StringField("Расскажите о предмете")
    photo = FileField(
        validators=[
            FileAllowed(UploadSet("photos", IMAGES), "Only images are allowed"),
            FileRequired("File field should not be empty")
        ]
    )
    # info = None
    submit = SubmitField('Create Item')

