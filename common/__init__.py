# -*- coding: utf-8 -*-
from .utils import pretty_result, hash_md5
from flask_mail import Mail
mail = Mail()
__all__ = ['pretty_result', 'hash_md5']
