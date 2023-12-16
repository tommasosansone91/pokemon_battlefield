from django.contrib import admin

from .models import pokemon
from .models import moveset, battle_stats
from .models import move

# Register your models here.
class pokemonAdmin(admin.ModelAdmin):
    pass

    # search_fields = ["Glossary_file"]
    # list_filter = ['Admin_approval_switch']

admin.site.register(pokemon, pokemonAdmin)