# -*- coding: utf-8 -*-

from marshmallow import Schema, fields

from app import manager
from app.models import User


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    blog_slug = fields.String()
    blog_image = fields.String()
    blog_title = fields.String()
    blog_description = fields.String()
    blog_bg = fields.String()
    blog_public = fields.String()

    def make_object(self, data):
        return User(api_purpose=True, **data)


def user_serializer(instance):
    return UserSchema().dump(instance).data


def user_deserializer(data):
    return UserSchema().load(data).data

manager.create_api(
    User,
    methods=['GET', ],
    url_prefix="/api/v1",
    serializer=user_serializer,
    deserializer=user_deserializer
)
