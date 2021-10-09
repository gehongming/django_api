#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/9/23 22:48
# @Author : ASUS
# @File : XIAOMING.py
# @Software: PyCharm

def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }
