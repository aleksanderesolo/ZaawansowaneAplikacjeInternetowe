from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Part(models.Model):
    nazwa = models.CharField(max_length=64, blank=False, unique=True)
    marka = models.CharField(max_length=64, blank=False)
    opis = models.TextField(default="")
    data_produkcji = models.DateField(null=True, blank=True)
    cena = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    samochody = models.ManyToManyField('Samochod', blank=True)
    zdjecie = models.ImageField(upload_to='parts/', null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nazwa} ({self.marka})"

class PartDetails(models.Model):
    part = models.OneToOneField('Part', on_delete=models.CASCADE)
    kod_producenta = models.CharField(max_length=32)
    kraj_produkcji = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.part.nazwa} – {self.kod_producenta}"

class Ocena(models.Model):
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    ocena = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    komentarz = models.TextField(blank=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE) #usun null!!!!!

    class Meta:
        unique_together = ('part', 'autor')

    def __str__(self):
        return f"{self.part.nazwa}: {self.ocena}/5"

class Samochod(models.Model):
    marka = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    rok = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.marka} {self.model} ({self.rok})"

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imie = models.CharField(max_length=100, blank=True)
    nazwisko = models.CharField(max_length=100, blank=True)
    opis = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatary/', blank=True, null=True)

    def __str__(self):
        return f"Profil: {self.user.username}"

@receiver(post_save, sender=User)
def utworz_profil(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)
