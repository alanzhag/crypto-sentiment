from typing import List

from marshmallow import fields

from app.ext import ma


class UserSchema(ma.Schema):
    id = fields.String(dump_only=True)
    name = fields.String()
    email = fields.String()
    profile_pic = fields.String()
    roles = fields.Method("get_roles")

    def get_roles(self, obj) -> List[str]:
        return [role.role_name.name for role in obj.roles]


class TokenSchema(ma.Schema):
    access_token = fields.String(attribute="token")
