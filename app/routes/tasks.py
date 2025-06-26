from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Task, User
from app.schema import TaskSchema
from flask_sqlalchemy import pagination

tasks_ns = Namespace('tasks', description='Task operations')

@tasks_ns.route('/test')
class TasksTest(Resource):
    def get(self):
        return {'message': 'Task service is running'}, 200

task_schema = TaskSchema()
task_list_schema = TaskSchema(many=True)

task_model = tasks_ns.model('Task', {
    'title': fields.String(required=True, description='Task title'),
    'description': fields.String(description='Task description'),
    'completed': fields.Boolean
})

@tasks_ns.route('/')
class TaskList(Resource):
    @jwt_required()
    @tasks_ns.doc(params={
        'page': 'Page number (default: 1)',
        'per_page': 'Number of tasks per page (default: 10)',
        'completed': 'Filter by completion status (true/false)',
        'sort': 'Sort by created_at: asc/desc (default: desc)'
    })
    def get(self):
        """Get all tasks for the authenticated user."""
        user_id = get_jwt_identity()['id']
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        completed = request.args.get('completed', None)
        sort = request.args.get('sort', 'desc')

        query = Task.query.filter_by(user_id=user_id)

        if completed is not None:
            if completed.lower() == 'true':
                query = query.filter_by(completed=True)
            elif completed.lower() == 'false':
                query = query.filter_by(completed=False)

        if sort == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())

        paginated = db.paginate(query, page=page, per_page=per_page, error_out=False)   

        return {
            'tasks': task_list_schema.dump(paginated.items),
            'total': paginated.total,
            'page': paginated.page,
            'pages': paginated.pages
        }, 200
    
    @jwt_required()
    @tasks_ns.expect(task_model)
    def post(self):
        """Create a new task for the authenticated user."""
        user = get_jwt_identity()
        task = task_schema.load(request.get_json(), session=db.session)
        task.user_id = user['id']
        db.session.add(task)
        db.session.commit()
        return task_schema.dump(task), 201
    
@tasks_ns.route('/<int:task_id>')
class TaskDetail(Resource):
    @jwt_required()
    def get(self, task_id):
        """Get a specific task by ID for the authenticated user."""
        user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user['id']).first()
        if not task:
            return {'message': 'Task not found'}, 404
        return task_schema.dump(task), 200

    @jwt_required()
    @tasks_ns.expect(task_model)
    def put(self, task_id):
        """Update a specific task by ID for the authenticated user."""
        user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user['id']).first()
        if not task:
            return {'message': 'Task not found'}, 404
        data = request.json
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        return task_schema.dump(task), 200

    @jwt_required()
    def delete(self, task_id):
        """Delete a specific task by ID for the authenticated user."""
        user = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user['id']).first()
        if not task:
            return {'message': 'Task not found'}, 404
        db.session.delete(task)
        db.session.commit()
        return {'message': 'Task deleted successfully'}, 204
    
