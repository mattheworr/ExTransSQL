# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Table

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Table)