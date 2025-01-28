from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources, \
    principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from core.apis.teachers import principal_teachers_resources
app.register_blueprint(principal_teachers_resources, url_prefix='/principal')
from core import db, migrate


from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err


from flask import request
import json

@principal_teachers_resources.route('/teachers', methods=['GET'])
def get_teachers():
    principal_header = request.headers.get('X-Principal')
    if not principal_header:
        return jsonify({'error': 'Principal not authenticated'}), 401
    
    principal_data = json.loads(principal_header)
    principal_id = principal_data.get('principal_id')
    if not principal_id:
        return jsonify({'error': 'Invalid principal ID'}), 400

    teachers = Teacher.query.filter_by(principal_id=principal_id).all()
    response = [
        {
            'id': teacher.id,
            'user_id': teacher.user_id,
            'created_at': teacher.created_at,
            'updated_at': teacher.updated_at
        }
        for teacher in teachers
    ]
    return jsonify(data=response)
from core.apis.teachers import principal_blueprint
app.register_blueprint(principal_blueprint, url_prefix='/principal')


