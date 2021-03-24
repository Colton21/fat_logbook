from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, SelectField, TimeField
from wtforms.validators import ValidationError, DataRequired, Length, AnyOf, NumberRange
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    module_id = TextAreaField('Module ID')
    #room_temp = FloatField('Room Temperature [C]', validators=[DataRequired(), NumberRange(min=10.0, max=30.0, message='Please make sure the entry is in C')])
    #freezer_temp = FloatField('Freezer Temperature [C]', validators=[DataRequired(), NumberRange(min=-57.0, max=30.0, message='Please make sure the entry is in C')])
    #filter_setting = FloatField('Filter Setting', validators=[DataRequired(), AnyOf(values=[0.5, 0.1, 0.05, 0.01, 0.001, 0.0001], message='Please enter a value in %(values)s')])
    #pulser_on = SelectField('Pulser On/Off', choices=[('pulser_on','On'), ('pulser_off', 'Off')], validators=[DataRequired()])
    sw_hw = SelectField('Software or Hardware Observation', 
                        choices=[('sw','Software'), ('hw', 'Hardware'), ('na', 'N/A')],
                        validators=[DataRequired()])
    #led_on = SelectField('LED On/Off', choices=[('led_on', 'On'), ('led_off', 'Off')], validators=[DataRequired()])
    #ref_current = FloatField('Reference PMT Current [mA]', validators=[DataRequired(), NumberRange(min=0.0, max=40.0, message='Please make sure the entry is in mA')])
    post = TextAreaField(_l('Logbook Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class StartShiftForm(FlaskForm):
    run_id = FloatField('Current Run ID (Number only)', validators=[DataRequired(),
                        NumberRange(min=0, message='Please give the number only!')])
    post = TextAreaField(_l('Logbook Comment'))
    submit = SubmitField(_l('Submit'))

class EndShiftForm(FlaskForm):
    post = TextAreaField(_l('Shift Summary'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class StartRunForm(FlaskForm):
    run_id = FloatField('Current Run ID (Number only)', validators=[DataRequired(),
                        NumberRange(min=0, message='Please give the number only!')])
    module_ids = TextAreaField('List D-Egg IDs to test', validators=[DataRequired()])
    function_gen = SelectField('Function Generator On?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    laser = SelectField('Laser Power Supply On?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    thermos = SelectField('Thermometers On?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    humidity = SelectField('Humidity Sensors On?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    fw_wheel = SelectField('Filter Wheel On?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    setup = SelectField('Did You Run setup_deggs.py?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    flash = SelectField('Did You Flash All FPGAs?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    configs = SelectField('Did You Run create_configs.py?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    post = TextAreaField(_l('Logbook Comment'))
    submit = SubmitField(_l('Submit'))

class FreezerForm(FlaskForm):
    hv = SelectField('Is the HV Disabled?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    laser = SelectField('Is the Laser Off?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    freezer_temp_s = FloatField('Start Freezer Temperature [C]', validators=[DataRequired(), 
                                NumberRange(min=-57.0, max=30.0, 
                                message='Please make sure the entry is in C')])
    freezer_temp_e = FloatField('End Freezer Temperature [C]', validators=[DataRequired(), 
                                NumberRange(min=-57.0, max=30.0, 
                                message='Please make sure the entry is in C')])
    freezer_hum_s = FloatField('Start Freezer Humidity [%]', validators=[DataRequired(), 
                                NumberRange(min=-0.0, max=100.0, 
                                message='Please make sure the entry is in %')])
    freezer_hum_e = FloatField('End Freezer Humidity [%]', validators=[DataRequired(), 
                                NumberRange(min=-0.0, max=100.0, 
                                message='Please make sure the entry is in %')])
    post = TextAreaField(_l('Reason For Access'), validators=[DataRequired()])
    start = TextAreaField('Access Start Time (HH:MM)')
    end = TextAreaField('Access End Time (HH:MM)')
    submit = SubmitField(_l('Submit'))


class ChecklistForm(FlaskForm):
    running = SelectField('Is the DAQ (Master Script) Running?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    slack = SelectField('Is the SlackBot Posting?', choices=[('Yes', 'Yes'), ('No', 'No')], 
                    validators=[DataRequired()])
    temp = SelectField('Does the Freezer Temperature Match Our Expectation?', 
                        choices=[('Yes', 'Yes'), ('No', 'No')],
                        validators=[DataRequired()])
    post = TextAreaField(_l('Logbook Comment'))
    submit = SubmitField(_l('Submit'))

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))
