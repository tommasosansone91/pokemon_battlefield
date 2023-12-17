from django.db import models

# Create your models here.

# nota che i modelli sono tutti in minuscolo

# ogni modello django possiede per default
# id = models.AutoField(primary_key=True)

class pokemon(models.Model):

    # id = models.AutoField(primary_key=True)

    Name = models.CharField(max_length=256, blank=False, null=False)
    Pokedex_id = models.PositiveIntegerField(blank=False, null=False)

    front_sprite_url = models.URLField(max_length=256, blank=False, null=False)
    back_sprite_url = models.URLField(max_length=256, blank=False, null=False)


    def __str__(self):       
        return  "[{}] N°{} - {}".format(self.id, self.Pokedex_id, self.Name) 

    class Meta:
        ordering = ['id']


class stats_set(models.Model):

    # nota che il nome dell'attributo è maiuscolo
    # il nome del modello è minuscolo
    Pokemon = models.OneToOneField(
        'pokemon',
        on_delete=models.CASCADE,        
    )

    HP = models.PositiveIntegerField(blank=False, null=False)

    ATK = models.PositiveIntegerField(blank=False, null=False)
    DEF = models.PositiveIntegerField(blank=False, null=False)
    SPD = models.PositiveIntegerField(blank=False, null=False)

    # SPCATK = models.PositivePositiveIntegerField(blank=False, null=False)
    # SPCDEF = models.PositivePositiveIntegerField(blank=False, null=False)

    # PRECISION = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):       
            return  "[{}] (pokemon: {})".format(self.id, self.Pokemon)   

    class Meta:
        ordering = ['id']


class battle_stats_set(models.Model):

    # nota che il nome dell'attributo è maiuscolo
    # il nome del modello è minuscolo
    Pokemon = models.OneToOneField(
        'pokemon',
        on_delete=models.CASCADE,        
    )

    HP = models.PositiveIntegerField(blank=False, null=False)

    ATK = models.PositiveIntegerField(blank=False, null=False)
    DEF = models.PositiveIntegerField(blank=False, null=False)
    SPD = models.PositiveIntegerField(blank=False, null=False)

    # SPCATK = models.PositiveIntegerField(blank=False, null=False)
    # SPCDEF = models.PositiveIntegerField(blank=False, null=False)

    # PRECISION = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):       
        return  "[{}] (pokemon: {})".format(self.id, self.Pokemon) 

    class Meta:
        ordering = ['id']


class move(models.Model):

    # nota che il nome dell'attributo è maiuscolo
    # il nome del modello è minuscolo
    Moveset = models.ForeignKey(
        'moveset',
        on_delete=models.CASCADE,        
    )

    Name = models.CharField(max_length=256, blank=False, null=False)

    Description = models.TextField(max_length=256, blank=False, null=False)

    Power = models.PositiveIntegerField(blank=False, null=False)

    # Accuracy = models.PositiveIntegerField(blank=False, null=False)

    # Type = models.CharField(max_length=256, blank=False, null=False)


    def __str__(self):       
        return  "{} (Moveset: {})".format(self.Name, self.Moveset)  

    class Meta:
        ordering = ['Moveset', 'Name']


class moveset(models.Model):

    # nota che il nome dell'attributo è maiuscolo
    # il nome del modello è minuscolo
    Pokemon = models.OneToOneField(
        'pokemon',
        on_delete=models.CASCADE,        
    )


    def __str__(self):       
        return  "[{}] (pokemon: {})".format(self.id, self.Pokemon) 

    class Meta:
        ordering = ['id']

