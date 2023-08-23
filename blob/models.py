from django.db import models
import uuid
# Create your models here.

class Session(models.Model):
    def generator():
        return str(uuid.uuid4())

    id = models.CharField(primary_key=True, unique=True, max_length=40,
                          default=generator, editable=False)



class Sector(models.Model):
    related = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Form(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
