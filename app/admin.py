from django.contrib import admin

# blog
from .models import BlogsPost

# objects
from .models import (
    Mouse,
)

# property
from .models import (
    Phenotype,
    Genotype,
    Health,
    Weight,
    Breed,
    Feed,
    InjectVirus,
)


# blog
admin.site.register(BlogsPost)

# objects
admin.site.register([
    Mouse,
])


# property
admin.site.register([
    Phenotype,
    Genotype,
    Health,
    Weight,
    Breed,
    Feed,
    InjectVirus,
])
