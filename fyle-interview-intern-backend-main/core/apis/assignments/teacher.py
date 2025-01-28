from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

from .schema import AssignmentSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)
@teacher_assignments_resources.route('/assignments/grade', methods=['POST'])
@accept_payload
@authenticate_principal
def grade_assignment(p, incoming_payload):
    assignment_id = incoming_payload['id']
    grade = incoming_payload['grade']
    assignment = Assignment.get_by_id(assignment_id)
    assertions.assert_found(assignment, 'No assignment with this id was found')
    assertions.assert_valid(assignment.teacher_id == p.teacher_id, 'This assignment does not belong to this teacher')
    assertions.assert_valid(assignment.state == AssignmentStateEnum.SUBMITTED, 'only a submitted assignment can be graded')
    assignment.grade = grade
    assignment.state = AssignmentStateEnum.GRADED
    db.session.commit()
    return APIResponse.respond(data=AssignmentSchema().dump(assignment))

