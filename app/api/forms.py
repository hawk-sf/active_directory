from flask.ext.wtf      import Form
from wtforms            import StringField, SelectMultipleField


class UserForm(Form):
    first_name = StringField(u'First Name')
    last_name  = StringField(u'First Name')
    userid     = StringField(u'First Name')
    groups     = SelectMultipleField(u'First Name')


class GroupForm(Form):
    name    = StringField(u'Group Name')
    userids = SelectMultipleField(u'Users')
