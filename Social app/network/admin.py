from django.contrib import admin
from .models import User,Content,Follow,Like



# Register your models here.
admin.site.register(User)
admin.site.register(Content)
admin.site.register(Follow)
admin.site.register(Like)