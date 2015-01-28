# -*- coding: utf-8 -*-

from flask_wtf import Form


class CustomForm(Form):

    def has_been_submitted(self, request):
        """
        Returns whether it was this form or not that was submitted.

        :param request: The flask request of the route
        :return: True if form has been submitted, False otherwise
        """
        return request.method == "POST" and request.form['btn'] == "{}btn".format(getattr(self, "_prefix"))
