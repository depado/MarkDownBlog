# -*- coding: utf-8 -*-

from marshmallow import Schema, fields
from flask import g
from flask_restless import ProcessingException

from app import manager
from app.models import Post

from .user import UserSchema, user_serializer, user_deserializer
from .utils import auth_required


class PostSchema(Schema):
    """
    The Schema representing a Post.
    """
    id = fields.Integer()
    title = fields.String()
    content = fields.String()
    title_slug = fields.String()
    pub_date = fields.Date()
    user = fields.Nested(UserSchema)

    def make_object(self, data):
        return Post(**data)


def post_serializer(instance):
    return PostSchema().dump(instance).data


def post_deserializer(data):
    return PostSchema().load(data).data


def owner_single(instance_id=None, **kw):
    """
    Checks if the current user is the owner of the post.
    Raises an exception if not found or the current user isn't the user.
    Note that this fucntion should always be associated with the auth_required preprocessor.

    :param instance_id: The instance id of the post
    """
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


def get_many_postprocessor(result=None, search_params=None, **kw):
    if result:
        for post in result['objects']:
            post['user'] = user_serializer(user_deserializer(post['user']))


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
    postprocessors=dict(
        GET_MANY=[get_many_postprocessor],
    ),
    url_prefix="/api/v1",
    collection_name="article",
    serializer=post_serializer,
    deserializer=post_deserializer
)
