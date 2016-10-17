from django.contrib import admin

# blog
from .models import BlogsPost

# objects
from .models import (
    Mouse,
    Genotype,
)

# events
from .models import (
    Get_Phenotype,
    Get_Genotype,
    Get_Phenotype_Weight,
    Mate,
    Wean,
    Do_Sack,
    Do_AddChow,
    Do_AddDrink,
    Do_AddBedding,
    Do_InjectVirus,
)


# blog
admin.site.register(BlogsPost)

# objects
admin.site.register([
    Mouse,
    Genotype,
])


# events
admin.site.register([
    Get_Phenotype,
    Get_Genotype,
    Get_Phenotype_Weight,
    Mate,
    Wean,
    Do_Sack,
    Do_AddChow,
    Do_AddDrink,
    Do_AddBedding,
    Do_InjectVirus,
])
