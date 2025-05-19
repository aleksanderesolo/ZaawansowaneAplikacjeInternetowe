from .models import Part
from .forms import PartForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .models import PartDetails
from .forms import PartDetailsForm
from .forms import OcenaForm
from django.utils.safestring import mark_safe
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import ProfilForm, UserForm
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404, render
from .models import Part, Ocena
from .forms import SamochodForm
from django.shortcuts import get_object_or_404, redirect
from .models import Samochod
from .serializers import SamochodSerializer, OcenaSerializer
from .serializers import PartSerializer
from django.db.models import Avg, Count
from rest_framework.permissions import IsAuthenticated

def wszystkie(request):
    czesci = Part.objects.annotate(
        srednia_ocena=Avg('ocena__ocena'),
        liczba_ocen=Count('ocena')
    )
    return render(request, 'parts/wszystkie.html', {'czesci': czesci})

@login_required
def nowy(request):
    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES)
        if form.is_valid():
            czesc = form.save(commit=False)
            czesc.autor = request.user
            czesc.save()
            return redirect('wszystkie')
    else:
        form = PartForm()

    return render(request, 'parts/formularz.html', {'form': form})

@login_required
def edytuj(request, id):
    try:
        czesc = Part.objects.get(pk=id)
    except Part.DoesNotExist:
        return HttpResponseNotFound("Nie znaleziono tej części.")

    if czesc.autor and czesc.autor != request.user:
        return HttpResponseForbidden(mark_safe(
            "<h2>To nie Twoja część.</h2>"
            "<a href='/' class='btn btn-primary'>Wróć</a>"
        ))

    if request.method == 'POST':
        form = PartForm(request.POST, request.FILES, instance=czesc)
        if form.is_valid():
            czesc = form.save(commit=False)
            if czesc.autor is None:
                czesc.autor = request.user
            form.save()
            return redirect('wszystkie')
    else:
        form = PartForm(instance=czesc)

    return render(request, 'parts/formularz.html', {'form': form, 'czesc': czesc})

@login_required
def usun(request, id):

    try:
        czesc = Part.objects.get(pk=id)
    except Part.DoesNotExist:
        return HttpResponseNotFound("Nie znaleziono tej części.")

    if czesc.autor and czesc.autor != request.user:
        return HttpResponseForbidden(mark_safe(
            "<h2>To nie Twoja część.</h2>"
            "<a href='/' class='btn btn-primary'>Wróć</a>"
        ))

    if request.method == 'POST':
        czesc.delete()
        return redirect('wszystkie')

    return render(request, 'parts/usun.html', {'czesc': czesc})

def szczegoly(request, id):
    part = get_object_or_404(Part, pk=id)
    try:
        szczegoly = PartDetails.objects.get(part=part)
    except PartDetails.DoesNotExist:
        szczegoly = None

    if request.method == 'POST':
        form = PartDetailsForm(request.POST, instance=szczegoly)
        if form.is_valid():
            dane = form.save(commit=False)
            dane.part = part
            dane.save()
            return redirect('wszystkie')
    else:
        form = PartDetailsForm(instance=szczegoly)

    return render(request, 'parts/szczegoly.html', {'form': form, 'czesc': part})

def szczegoly_z_ocenami(request, id):
    czesc = get_object_or_404(Part, pk=id)
    oceny = Ocena.objects.filter(part=czesc)
    return render(request, 'parts/szczegoly_oceny.html', {
        'czesc': czesc,
        'oceny': oceny
    })

@login_required
def dodaj_ocene(request, id):

    part = get_object_or_404(Part, pk=id)

    try:
        ocena = Ocena.objects.get(part=part, autor=request.user)
    except Ocena.DoesNotExist:
        ocena = None

    if request.method == 'POST':
        form = OcenaForm(request.POST, instance=ocena)
        if form.is_valid():
            nowa_ocena  = form.save(commit=False)
            nowa_ocena.part = part
            nowa_ocena.autor = request.user
            nowa_ocena.save()
            return redirect('szczegoly_oceny', id=part.id)
    else:
        form = OcenaForm(instance=ocena)
    return render(request, 'parts/dodaj_ocene.html', {'form': form, 'czesc': part})

def szczegoly_z_ocenami(request, id):
    czesc = get_object_or_404(Part, pk=id)
    oceny = Ocena.objects.filter(part=czesc)
    return render(request, 'parts/szczegoly_z_ocenami.html', {'czesc': czesc, 'oceny': oceny})

class KontaktForm(forms.Form):
    temat = forms.CharField(max_length=100, label="Temat")
    wiadomosc = forms.CharField(widget=forms.Textarea, label="Wiadomość")
    email = forms.EmailField(label="Twój adres e-mail", required=False)

def kontakt(request):
    if request.method == 'POST':
        form = KontaktForm(request.POST)
        if form.is_valid():
            temat = form.cleaned_data['temat']
            wiadomosc = form.cleaned_data['wiadomosc']

            if not request.user.is_authenticated:
                email = form.cleaned_data.get('email')
                if not email:
                    form.add_error('email', 'Pole email jest wymagane dla niezalogowanych użytkowników.')
                    return render(request, 'parts/kontakt.html', {'form': form})
            else:
                email = request.user.email

            #send_mail(temat, wiadomosc, email, ['aleksanderes@gmail.com'])
            send_mail(
                subject=temat,
                message = f"Wiadomość od: {email}\n\n{wiadomosc}",
                from_email=email,
                recipient_list=['aleksanderesolo@gmail.com', email],
            )
            return redirect('wszystkie')
    else:
        form = KontaktForm()
    return render(request, 'parts/kontakt.html', {'form': form})

def rejestracja(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('wszystkie')
    else:
        form = CustomUserCreationForm()
    return render(request, 'parts/rejestracja.html', {'form': form})

@login_required
def moj_profil(request):
    profil = request.user.profil
    if request.method == 'POST':
        p_form = ProfilForm(request.POST, request.FILES, instance=profil)
        u_form = UserForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            return redirect('moj_profil')
    else:
        p_form = ProfilForm(instance=profil)
        u_form = UserForm(instance=request.user)
    return render(request, 'parts/moj_profil.html', {'p_form': p_form, 'u_form': u_form})

class OcenaViewSet(viewsets.ModelViewSet):
    serializer_class = OcenaSerializer
    queryset = Ocena.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ocena.objects.all()
        part_id = self.request.query_params.get('part')
        if part_id:
            queryset = queryset.filter(part__id=part_id)
        return queryset

@login_required
def dodaj_samochod(request):
    if request.method == 'POST':
        form = SamochodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dodaj_samochod')  # zostajesz na tej samej stronie
    else:
        form = SamochodForm()

    samochody = Samochod.objects.all()  # ✅ dodane
    return render(request, 'parts/dodaj_samochod.html', {
        'form': form,
        'samochody': samochody  # ✅ przekazane do szablonu
    })

@login_required
def edytuj_samochod(request, id):
    samochod = get_object_or_404(Samochod, pk=id)
    if request.method == 'POST':
        form = SamochodForm(request.POST, instance=samochod)
        if form.is_valid():
            form.save()
            return redirect('wszystkie')
    else:
        form = SamochodForm(instance=samochod)
    return render(request, 'parts/dodaj_samochod.html', {'form': form})

@login_required
def usun_samochod(request, id):
    samochod = get_object_or_404(Samochod, pk=id)
    samochod.delete()
    return redirect('wszystkie')

class SamochodViewSet(viewsets.ModelViewSet):
    queryset = Samochod.objects.all()
    serializer_class = SamochodSerializer

class OcenaViewSet(viewsets.ModelViewSet):
    queryset = Ocena.objects.all()
    serializer_class = OcenaSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer