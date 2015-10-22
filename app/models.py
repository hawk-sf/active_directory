from app  import db
from json import dumps

# Set up association table for User/Group many-to-many relationship
memberships = db.Table('memberships',
                       db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                      )


class User(db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name  = db.Column(db.String(64))
    userid     = db.Column(db.String(64), unique=True)
    groups     = db.relationship('Group',
                                 secondary = memberships,
                                 backref   = db.backref('users', lazy='dynamic'),
                                 lazy      = 'dynamic')

    def __repr__(self):
        return "User(id=%s, userid=%s)" % (self.id, self.userid)

    def add_group(self, group):
        if not self.is_member_of(group):
            self.groups.append(group)
            return self

    def remove_group(self, group):
        if self.is_member_of(group):
            self.groups.remove(group)
            return self

    def is_member_of(self, group):
        return group in self.get_groups()

    def get_groups(self):
        return self.groups.all()

    def as_dict(self):
        d           = self.__dict__.copy()
        groups      = self.get_groups()
        d['groups'] = [g.name for g in groups]
        # Remove SQLAlchemy meta attribute
        del d['_sa_instance_state']
        return d

    def as_json(self):
        return dumps(self.as_dict(), ensure_ascii=False).encode('utf8')


class Group(db.Model):
    __tablename__ = 'groups'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "Group(id=%s, name=%s)" % (self.id, self.name)

    def add_user(self, user):
        if not self.has_user(user):
            self.users.append(user)
            return self

    def remove_user(self, user):
        if self.has_user(user):
            self.users.remove(user)
            return self

    def has_user(self, user):
        return user in self.get_users()

    def get_users(self):
        return self.users.all()

    def as_dict(self):
        d          = self.__dict__.copy()
        users      = self.get_users()
        d['users'] = [u.userid for u in users]
        # Remove SQLAlchemy meta attribute
        del d['_sa_instance_state']
        return d

    def as_json(self):
        return dumps(self.as_dict(), ensure_ascii=False).encode('utf8')
