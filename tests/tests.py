import unittest
import os
import json
from   app import create_app, db, models

localhost = '/'


class PlanetTestCase(unittest.TestCase):
    def setUp(self):
        self.app         = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a user and a group
        james = models.User(
                            first_name = 'james',
                            last_name  = 'hawkins',
                            userid     = 'jhawkins'
                           )
        admin = models.Group(name='admin')
        james.add_group(admin)
        db.session.add(james)
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class UserTests(PlanetTestCase):
    def test_get_user_200(self):
        james   = models.User.query.filter_by(userid='jhawkins').first()
        db_dict = james.as_dict()
        res     = self.client.get(os.path.join(localhost, 'users', 'jhawkins'))
        data    = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == db_dict)

    def test_get_user_404(self):
        res = self.client.get(os.path.join(localhost, 'users', 'nobody'))
        self.assertTrue(res.status_code == 404)

    def test_post_user_200(self):
        donna = {
                 'first_name': 'donna',
                 'last_name':  'hawkins',
                 'userid':     'dhawkins',
                 'groups':     [],
                }
        res   = self.client.post(os.path.join(localhost, 'users'), data=donna)
        data  = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == True)

    def test_post_user_400(self):
        james = {
                 'first_name': 'james',
                 'last_name':  'hawkins',
                 'userid':     'jhawkins',
                 'groups':     [],
                }
        res   = self.client.post(os.path.join(localhost, 'users'), data=james)
        data  = json.loads(res.data)
        self.assertTrue(res.status_code == 400 and data['error'] == 'User Exists')

    def test_put_user_200(self):
        new_james = {
                     'first_name': 'james',
                     'last_name':  'hawkins',
                     'userid':     'jhawkins',
                     'groups':     ['new_group'],
                    }
        res       = self.client.put(os.path.join(localhost, 'users', 'jhawkins'), data=new_james)
        james     = models.User.query.filter_by(userid='jhawkins').first()
        db_james  = james.as_dict()
        # Remove extra 'id' attribute, for dictionary comparison
        del db_james['id']
        self.assertTrue(res.status_code == 200 and new_james == db_james)

    def test_put_user_404(self):
        donna = {
                 'first_name': 'donna',
                 'last_name':  'hawkins',
                 'userid':     'dhawkins',
                 'groups':     [],
                }
        res   = self.client.put(os.path.join(localhost, 'users', 'dhawkins'), data=donna)
        self.assertTrue(res.status_code == 404)

    def test_delete_user_200(self):
        res  = self.client.delete(os.path.join(localhost, 'users', 'jhawkins'))
        data = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == True)

    def test_delete_user_404(self):
        res = self.client.delete(os.path.join(localhost, 'users', 'not_here'))
        self.assertTrue(res.status_code == 404)


class GroupTests(PlanetTestCase):
    def test_get_group_200(self):
        admin   = models.Group.query.filter_by(name='admin').first()
        userids = [u.userid for u in admin.get_users()]
        res     = self.client.get(os.path.join(localhost, 'groups', 'admin'))
        data    = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == userids)

    def test_get_group_404(self):
        res = self.client.get(os.path.join(localhost, 'groups', 'not_here'))
        self.assertTrue(res.status_code == 404)

    def test_post_group_200(self):
        group = {'name': 'new_group'}
        res   = self.client.post(os.path.join(localhost, 'groups'), data=group)
        data  = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == True)

    def test_post_group_400(self):
        group = {'name': 'admin'}
        res   = self.client.post(os.path.join(localhost, 'groups'), data=group)
        data  = json.loads(res.data)
        self.assertTrue(res.status_code == 400 and data['error'] == 'Group Exists')

    def test_put_group_200(self):
        donna     = {
                     'first_name': 'donna',
                     'last_name':  'hawkins',
                     'userid':     'dhawkins',
                     'groups':     [],
                    }
        res       = self.client.post(os.path.join(localhost, 'users'), data=donna)
        new_users = {'userids': ['dhawkins']}
        res       = self.client.put(os.path.join(localhost, 'groups', 'admin'), data=new_users)
        admin     = models.Group.query.filter_by(name='admin').first()
        userids   = [u.userid for u in admin.get_users()]
        self.assertTrue(res.status_code == 200 and new_users['userids'] == userids)

    def test_put_group_404(self):
        new_users = {'userids': ['dhawkins']}
        res       = self.client.put(os.path.join(localhost, 'groups', 'not_here'), data=new_users)
        self.assertTrue(res.status_code == 404)

    def test_delete_group_200(self):
        res  = self.client.delete(os.path.join(localhost, 'groups', 'admin'))
        data = json.loads(res.data)
        self.assertTrue(res.status_code == 200 and data['result'] == True)

    def test_delete_group_404(self):
        res = self.client.delete(os.path.join(localhost, 'groups', 'not_here'))
        self.assertTrue(res.status_code == 404)
