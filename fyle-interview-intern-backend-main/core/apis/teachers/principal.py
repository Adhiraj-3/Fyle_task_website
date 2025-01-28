


from flask import Blueprint
from core.apis.responses import APIResponse
from core.apis.decorators import authenticate_principal
from core.models.teachers import Teacher  # Assuming Teacher model is defined in core/models.py
from core.libs.assertions import assertions


from tests import app
# Create a blueprint for principal-related APIs
principal_blueprint = Blueprint('principal', __name__)

@principal_blueprint.route('/principal/teachers', methods=['GET'])
@authenticate_principal
def get_principal_teachers(auth_principal):
    """
    Fetch all teachers associated with a principal.
    """
    try:
        principal_id = auth_principal.principal_id
        # Query the database for teachers associated with this principal
        teachers = Teacher.query.filter_by(principal_id=principal_id).all()

        # Format the response
        data = [
            {
                "id": teacher.id,
                "user_id": teacher.user_id,
                "created_at": teacher.created_at.isoformat(),
                "updated_at": teacher.updated_at.isoformat()
            }
            for teacher in teachers
        ]

        return APIResponse.respond(data)

    except Exception as e:
        return APIResponse.respond({"error": str(e)}, 500)
@principal_blueprint.route('/principal/teachers', methods=['GET'])
@authenticate_principal
def get_principal_teachers(auth_principal):
    principal_id = auth_principal.principal_id
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
    return APIResponse.respond(data=response)    
