from marshmallow import Schema, fields, validate
from .models import StatusEnum, PriorityEnum

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str()
    created_at = fields.DateTime(dump_only=True)

class TaskSchema(Schema):
    task_id = fields.Int(dump_only=True)
    task_name = fields.Str(required=True, validate=validate.Length(min=1))
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)

    status = fields.Method(
        serialize='get_status',
        deserialize='load_status',
        validate=validate.OneOf([e.value for e in StatusEnum])
    )
    due_date = fields.Date()

    priority = fields.Method(
        serialize='get_priority',
        deserialize='load_priority',
        validate=validate.OneOf([e.value for e in PriorityEnum])
    )

    def get_status(self, obj):
        val = getattr(obj, 'status', None)
        return val.value if val is not None else None

    def load_status(self, value):
        return value

    def get_priority(self, obj):
        val = getattr(obj, 'priority', None)
        return val.value if val is not None else None

    def load_priority(self, value):
        return value
