# -*- coding: utf-8 -*-

from marshmallow import Schema, fields
from flask import g
from flask_restless import ProcessingException

from app import manager
from app.models import Post

from .user import UserSchema
from .utils import auth_required


class PostSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    user = fields.Nested(UserSchema)

    def make_object(self, data):
        return Post(**data)


def post_serializer(instance):
    return PostSchema().dump(instance).data


def post_deserializer(data):
    return PostSchema().load(data).data


def owner_single(instance_id=None, **kw):
    post = Post.query.filter_by(id=instance_id).first()
    if post:
        if post.user != g.user:
            raise ProcessingException(description="Not Authorized", code=401)
    else:
        raise ProcessingException(description="Not Found", code=404)


def post_preprocessor(data=None, **kwargs):
    post = post_deserializer(data)
    post.user = g.user
    data = post_serializer(post)


manager.create_api(
    Post,
    methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
    preprocessors=dict(
        POST=[auth_required, post_preprocessor],
        PATCH_SINGLE=[auth_required, owner_single],
        PATCH_MANY=[auth_required, owner_single],
        PUT=[auth_required, owner_single],
        DELETE_SINGLE=[auth_required, owner_single],
        DELETE_MANY=[auth_required, owner_single]
    ),
    url_prefix="/api/v1",
    collection_name="article",
    serializer=post_serializer,
    deserializer=post_deserializer
)
