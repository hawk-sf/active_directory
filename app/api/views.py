from flask       import request, jsonify, make_response
from .           import api
from ..          import db
from ..models    import User, Group
from .forms      import UserForm, GroupForm


# User Routes ##################################################################

@api.route('/users/<userid>', methods=['GET'])
def get_user(userid):
    """
    Returns the matching user record or 404 if none exist.
    """
    user = User.query.filter_by(userid=userid).first()
    if not user:
        return make_response(jsonify({'error': 'Not Found'}), 404)
    else:
        return jsonify({'result': user.as_dict()})


@api.route('/users', methods=['POST'])
def post_user():
    """
    Creates a new user record. The body of the request should be a valid user
    record. POSTs to an existing user should be treated as errors and flagged
    with the appropriate HTTP status code.
    """
    # NOTE: Assumes userid is the only required field
    if request.json:
        # NOTE: json not sanitized
        userid     = request.json.get('userid', '')
        first_name = request.json.get('first_name', '')
        last_name  = request.json.get('last_name', '')
        groups     = request.json.get('groups', []) if request.json.get('groups', []) else []
    else:
        form       = UserForm(request.form)
        userid     = form.userid.data
        first_name = form.first_name.data
        last_name  = form.last_name.data
        groups     = form.groups.data if form.groups.data else []
    if not userid:
        return make_response(jsonify({'error': 'Missing userid'}), 400)

    # Check if user exists
    user = User.query.filter_by(userid=userid).first()
    if user:
        return make_response(jsonify({'error': 'User Exists'}), 400)

    # Create user
    try:
        user = User(userid=userid, first_name=first_name, last_name=last_name)
        for name in groups:
            # NOTE: creates group, if doesn't already exist
            group = Group.query.filter_by(name=name).first()
            if not group:
                group = Group(name=name)
            db.session.add(group)
            user.add_group(group)
        db.session.add(user)
        db.session.commit()
    except Exception, e:
        print e
        db.session.rollback()
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return jsonify({'result': True})


@api.route('/users/<userid>', methods=['PUT'])
def update_user(userid):
    """
    Updates an existing user record. The body of the request should be a valid
    user record. PUTs to a non-existant user should return a 404.
    """
    # NOTE: Assumes userid is the only required field
    user = User.query.filter_by(userid=userid).first()
    if not user:
        return make_response(jsonify({'error': 'User Not Found'}), 404)

    if request.json:
        # NOTE: json not sanitized
        first_name = request.json.get('first_name', '')
        last_name  = request.json.get('last_name', '')
        groups     = request.json.get('groups', []) if request.json.get('groups', []) else []
    else:
        form       = UserForm(request.form)
        first_name = form.first_name.data
        last_name  = form.last_name.data
        groups     = form.groups.data if form.groups.data else []

    # Update user
    try:
        user.first_name = first_name
        user.last_name  = last_name
        new_groups      = []
        # NOTE: Replaces old groups with new list
        for name in groups:
            # NOTE: creates group, if doesn't already exist
            group = Group.query.filter_by(name=name).first()
            if not group:
                group = Group(name=name)
            db.session.add(group)
            new_groups.append(group)
        user.groups = new_groups
        db.session.add(user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return jsonify({'result': True})


@api.route('/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    """
    Deletes a user record. Returns 404 if the user doesn't exist.
    """
    user = User.query.filter_by(userid=userid).first()
    if not user:
        return make_response(jsonify({'error': 'User Not Found'}), 404)
    else:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
        else:
            return jsonify({'result': True})


# Group Routes #################################################################

@api.route('/groups/<name>', methods=['GET'])
def get_group(name):
    """
    Returns a JSON list of userids containing the members of that group. Should
    return a 404 if the group doesn't exist.
    """
    group = Group.query.filter_by(name=name).first()
    if not group:
        return make_response(jsonify({'error': 'Group Not Found'}), 404)
    else:
        user_list = group.get_users()
        user_list = [user.userid for user in user_list]
        return jsonify({'result': user_list})


@api.route('/groups', methods=['POST'])
def post_group():
    """
    Creates a empty group. POSTs to an existing group should be treated as
    errors and flagged with the appropriate HTTP status code. The body should contain
    a `name` parameter
    """
    if request.json:
        # NOTE: json not sanitized
        name = request.json.get('name', '')
    else:
        form = GroupForm(request.form)
        name = form.name.data
    if not name:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    # Check if group exists
    group = Group.query.filter_by(name=name).first()
    if group:
        return make_response(jsonify({'error': 'Group Exists'}), 400)

    # Create group
    try:
        group = Group(name=name)
        db.session.add(group)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return jsonify({'result': True})


@api.route('/groups/<name>', methods=['PUT'])
def update_group(name):
    """
    Updates the membership list for the group. The body of the request should
    be a JSON list describing the group's members.
    """
    group = Group.query.filter_by(name=name).first()
    if not group:
        return make_response(jsonify({'error': 'Group Not Found'}), 404)

    if request.json:
        # Note: json not sanitized
        userids = request.json.get('userids', [])
    else:
        form    = GroupForm(request.form)
        userids = form.userids.data

    # Replace group members with new userid list
    try:
        new_users = []
        for userid in userids:
            user = User.query.filter_by(userid=userid).first()
            if not user:
                return make_response(jsonify({'error': 'Not All userids Exist'}), 400)
            new_users.append(user)
        group.users = new_users
        db.session.add(group)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Internal Server Error'}), 500)
    else:
        return jsonify({'result': True})


@api.route('/groups/<name>', methods=['DELETE'])
def delete_group(name):
    """
    Deletes a group.
    """
    group = Group.query.filter_by(name=name).first()
    if not group:
        return make_response(jsonify({'error': 'Group Not Found'}), 404)
    else:
        try:
            db.session.delete(group)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return make_response(jsonify({'error': 'Internal Server Error'}), 500)
        else:
            return jsonify({'result': True})
