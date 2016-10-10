from django.contrib import admin

# Register your models here.

from .models import Question
from .models import Choice

from .models import BlogsPost

from .models import Mouse
from .models import Country
from .models import Person


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(BlogsPost)

admin.site.register(Mouse)

admin.site.register(Country)
admin.site.register(Person)
