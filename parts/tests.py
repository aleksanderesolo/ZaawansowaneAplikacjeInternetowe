from django.shortcuts import render, redirect, get_object_or_404
from .models import Part
from .forms import PartForm
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


def wszystkie(request):
    czesci = Part.objects.all()
    return render(request, 'parts/wszystkie.html', {'czesci': czesci})

def nowy(request):
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wszystkie')
    else:
        form = PartForm()
    return render(request, 'parts/nowy.html', {'form': form})

def edytuj(request, id):
    czesc = get_object_or_404(Part, pk=id)
    if request.method == 'POST':
        form = PartForm(request.POST, instance=czesc)
        if form.is_valid():
            form.save()
            return redirect('wszystkie')
    else:
        form = PartForm(instance=czesc)
    return render(request, 'parts/edytuj.html', {'form': form})

def usun(request, id):
    czesc = get_object_or_404(Part, pk=id)
    if request.method == 'POST':
        czesc.delete()
        return redirect('wszystkie')
    return render(request, 'parts/usun.html', {'czesc': czesc})

class PartModelTest(TestCase):
    def test_create_part(self):
        part = Part.objects.create(nazwa="Filtr oleju", marka="Bosch", cena=99)
        self.assertEqual(part.nazwa, "Filtr oleju")
        self.assertEqual(str(part), "Filtr oleju (Bosch)")

class PartApiTest(APITestCase):
    def test_get_parts(self):
        Part.objects.create(nazwa="Klocki hamulcowe", marka="ATE", cena=150)
        response = self.client.get('/czesci/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)