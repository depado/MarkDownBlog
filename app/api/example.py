# -*- coding: utf-8 -*-


def get_single_preprocessor(instance_id=None, **kw):
    """Accepts a single argument, `instance_id`, the primary key of the
    instance of the model to get.

    """
    pass


def get_single_postprocessor(result=None, **kw):
    """Accepts a single argument, `result`, which is the dictionary
    representation of the requested instance of the model.

    """
    pass


def get_many_preprocessor(search_params=None, **kw):
    """Accepts a single argument, `search_params`, which is a dictionary
    containing the search parameters for the request.

    """
    pass


def get_many_postprocessor(result=None, search_params=None, **kw):
    """Accepts two arguments, `result`, which is the dictionary
    representation of the JSON response which will be returned to the
    client, and `search_params`, which is a dictionary containing the
    search parameters for the request (that produced the specified
    `result`).

    """
    pass


def patch_single_preprocessor(instance_id=None, data=None, **kw):
    """Accepts two arguments, `instance_id`, the primary key of the
    instance of the model to patch, and `data`, the dictionary of fields
    to change on the instance.

    """
    pass


def patch_single_postprocessor(result=None, **kw):
    """Accepts a single argument, `result`, which is the dictionary
    representation of the requested instance of the model.

    """
    pass


def patch_many_preprocessor(search_params=None, data=None, **kw):
    """Accepts two arguments: `search_params`, which is a dictionary
    containing the search parameters for the request, and `data`, which
    is a dictionary representing the fields to change on the matching
    instances and the values to which they will be set.

    """
    pass


def patch_many_postprocessor(query=None, data=None, search_params=None,
                             **kw):
    """Accepts three arguments: `query`, which is the SQLAlchemy query
    which was inferred from the search parameters in the query string,
    `data`, which is the dictionary representation of the JSON response
    which will be returned to the client, and `search_params`, which is a
    dictionary containing the search parameters for the request.

    """
    pass


def post_preprocessor(data=None, **kw):
    """Accepts a single argument, `data`, which is the dictionary of
    fields to set on the new instance of the model.

    """
    pass


def post_postprocessor(result=None, **kw):
    """Accepts a single argument, `result`, which is the dictionary
    representation of the created instance of the model.

    """
    pass


def delete_single_preprocessor(instance_id=None, **kw):
    """Accepts a single argument, `instance_id`, which is the primary key
    of the instance which will be deleted.

    """
    pass


def delete_postprocessor(was_deleted=None, **kw):
    """Accepts a single argument, `was_deleted`, which represents whether
    the instance has been deleted.

    """
    pass


def delete_many_preprocessor(search_params=None, **kw):
    """Accepts a single argument, `search_params`, which is a dictionary
    containing the search parameters for the request.

    """
    pass


def delete_many_postprocessor(result=None, search_params=None, **kw):
    """Accepts two arguments: `result`, which is the dictionary
    representation of which is the dictionary representation of the JSON
    response which will be returned to the client, and `search_params`,
    which is a dictionary containing the search parameters for the
    request.

    """
    pass

