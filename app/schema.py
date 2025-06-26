from app .models import User, Task
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from app import db
from marshmallow import fields, validate

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True 
        include_relationships = True # Automatically create an instance of the model

    id = auto_field(dump_only=True)  # Exclude from input, only for output
    username = auto_field(required=True)
    email = auto_field(required=True)
#
class TaskSchema(SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = True
        include_relationships = True,
        sqla_session = db.session  # Ensure the schema uses the correct session

    id = auto_field(dump_only=True)  # Exclude from input, only for output
    title = auto_field(required=True)
    description = auto_field()
    completed = auto_field()
    created_at = fields.DateTime(dump_only=True)
    due_date = fields.DateTime(allow_none=True)
    priority = fields.String(validate=validate.OneOf(["Low", "Medium", "High"]))
    user_id = auto_field(dump_only=True) 
    
     