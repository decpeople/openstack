from django.db import models

# Create your models here.


class ChurmHub(models.Model):
    id = models.IntegerField(verbose_name="ID", primary_key=True)
    entity_url=models.CharField(max_length=400,verbose_name="Entity_url")
    application_name=models.CharField(max_length=400, verbose_name="Application name")
    series = models.CharField(max_length=400,verbose_name="Series")
    channel = models.CharField(max_length=400,verbose_name="Version ChurmHub package")
    constraints = models.CharField(max_length=400,verbose_name="Machine named")
    num_units = models.IntegerField(verbose_name='Count Machine')

    def __str__(self):
        return self.entity_url