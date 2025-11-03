from django.contrib import admin
from news_app.models import News


# Register your models here.
admin.site.register(News) # was stated here so that the news model can be viewed and managed in the admin panel on 127.0.0.1:8000/admin