from django.contrib import admin

from .models import pokemon
from .models import moveset, stats_set, battle_stats_set
from .models import move

# Register your models here.
class pokemonAdmin(admin.ModelAdmin):
    pass

admin.site.register(pokemon, pokemonAdmin)


class stats_setAdmin(admin.ModelAdmin):
    pass

admin.site.register(stats_set, stats_setAdmin)


class battle_stats_setAdmin(admin.ModelAdmin):
    pass

admin.site.register(battle_stats_set, battle_stats_setAdmin)


class movesetAdmin(admin.ModelAdmin):
    pass

admin.site.register(moveset, movesetAdmin)


class moveAdmin(admin.ModelAdmin):
    pass

admin.site.register(move, moveAdmin)