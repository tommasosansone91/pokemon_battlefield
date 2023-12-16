from django.db import models

# Create your models here.

# nota che i modelli sono tutti in minuscolo

# ogni modello django possiede per default
# id = models.AutoField(primary_key=True)

class pokemon(models.Model):

    # id = models.AutoField(primary_key=True)

    Name = models.CharField(max_length=256, blank=False, null=False)

    Pokedex_entry = models.CharField(max_length=256, blank=False, null=False)

    Pokedex_id = models.IntegerField(blank=False, null=False)


    def __str__(self):       
        return  self.id, self.Name, self.Pokedex_id

    class Meta:
        ordering = ['id']


class battle_stats(models.Model):

    # nota che il nome dell'attributo è maiuscolo
    # il nome del modello è minuscolo
    Pokemon = models.OneToOneField(
        'pokemon',
        on_delete=models.CASCADE,        
    )

    HP = models.IntegerField(blank=False, null=False)

    ATK = models.IntegerField(blank=False, null=False)
    DEF = models.IntegerField(blank=False, null=False)
    SPD = models.IntegerField(blank=False, null=False)

    # SPCATK = models.IntegerField(blank=False, null=False)
    # SPCDEF = models.IntegerField(blank=False, null=False)

    # PRECISION = models.IntegerField(blank=False, null=False)

    def __str__(self):       
        return self.id, self.Pokemon

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

    Description = models.CharField(max_length=256, blank=False, null=False)

    Damage = models.IntegerField(blank=False, null=False)

    # Accuracy = models.IntegerField(blank=False, null=False)

    # Type = models.CharField(max_length=256, blank=False, null=False)


    def __str__(self):       
        return  self.Name, self.Moveset 

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
        return  self.id, self.Pokemon  

    class Meta:
        ordering = ['id']

