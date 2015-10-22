# Description #
A simple Flask REST API to store, fetch, and update user/group records. Based off of specifications in [code_test](https://gist.github.com/jakedahn/3d90c277576f71d805ed). Uses SQLite as its datastore.

# Installation #
After cloning the repository into a virtualenv, change into the project's root directory and install the requirements with:

    pip install -r requirements.txt

The database can be initialized in the project's root, and an initial migration run, using:

    python manage.py deploy

You're all set.

# Testing and Running the Dev Server #
To verify your installation, the unit tests can be run using:

    python manage.py test

The local web server can be run, on `http://localhost:5000`, using:

    python manage.py runserver

# API Overview #
Note: in this implemenation, a user only requires the `userid` field, and a group the `name` field.

## `GET /users/<userid>` ##
Returns `JSON` object. Succesful responses will return user representation inside the `result` attribute. Non `200` responses will contain an `error` attribute.

## `POST /users` ##
Expects user information, with the following fields:

    {
        "first_name": "Joe",
        "last_name": "Smith",
        "userid": "jsmith",
        "groups": ["admins", "users"]
    }

Accepts either a `JSON` payload, in the format above, or a standard paramater payload. `userid` is required. Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute.

## `PUT /users/<userid>` ##
Expects user information, with the following fields:

    {
        "first_name": "Joe",
        "last_name": "Smith",
        "groups": ["admins", "users"]
    }

Accepts either a `JSON` payload, in the format above, or a standard paramater payload. Replaces current user info with new data. Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute. Will return `404` if user doesn't already exist.

## `DELETE /users/<userid>` ##
Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute. Will return `404` if user doesn't already exist.

## `GET /groups/<group name>` ##
Returns `JSON` object. Succesful responses will return a list of userid's inside the `result` attribute. Non `200` responses will contain an `error` attribute.

## `POST /groups` ##
Expects group information, with the following fields:

    {
        "name": "admins"
    }

Accepts either a `JSON` payload, in the format above, or a standard paramater payload. `name` is required. Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute.

## `PUT /groups/<group name>` ##
Expects a list of userids:

    {
        "userids": ["jsmith"]
    }

Accepts either a `JSON` payload, in the format above, or a standard paramater payload. `userids` is required. Replaces current users with the new list. Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute. Will return `404` if group doesn't already exist.

## `DELETE /groups/<group name>` ##
Succesful responses will return `{"result": true}`. Non `200` responses will contain an `error` attribute. Will return `404` if group doesn't already exist.
