from django.db import models

# Create your models here.

class Gas(models.Model):
    name = models.TextField()
    item_id = models.TextField()
    last_price = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    volume = models.IntegerField()
    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.TextField()
    region_id = models.TextField()
    def __str__(self):
        return self.name

class Station(models.Model):
    name = models.TextField()
    station_id = models.TextField()
    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.TextField()
    p_gas = models.ForeignKey(Gas, related_name='p_gas_re')
    s_gas = models.ForeignKey(Gas, related_name='s_gas_re')
    p_qty = models.IntegerField()
    s_qty = models.IntegerField()
    def __str__(self):
        return self.name

class Ship(models.Model):
    name = models.TextField()
    cargo = models.IntegerField()
    yld_bonus = models.DecimalField(max_digits=3,decimal_places=2)
    def __str__(self):
        return self.name

class Harvester(models.Model):
    name = models.TextField()
    harv_id = models.TextField()
    cycle = models.IntegerField()
    yld = models.IntegerField()
    def __str__(self):
        return self.name

class Setup(models.Model):
    setup = models.IntegerField(default=0)
