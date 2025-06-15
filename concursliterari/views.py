from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Conte, Vot
from django.db.models import Count


def llistatcontes(request):
    cursos = dict(Conte._meta.get_field('autor').related_model.CURS_ESCOLAR)
    curs_seleccionat = request.GET.get('curs') 

    if request.method == 'POST':
        conte_id = request.POST.get('conte_id')
        conte = get_object_or_404(Conte, id=conte_id)
        Vot.objects.create(conte=conte)
        return redirect('llistatcontes')

    contes = Conte.objects.select_related('autor')

    if curs_seleccionat in cursos:
        llistatcontes = {
            cursos[curs_seleccionat]: contes.filter(autor__curs=curs_seleccionat)
        }
    else:
        llistatcontes = {
            cursos[codi]: contes.filter(autor__curs=codi)
            for codi in cursos
        }

    return render(request, 'llistat.html', {
        'llistatcontes': llistatcontes,
        'cursos': cursos,
        'curs_seleccionat': curs_seleccionat,
    })

def conte(request, conte_id):
    conte = get_object_or_404(Conte, id=conte_id)
    return render(request, 'conte.html', {'conte': conte})   

def resultats(request):
    cursos = dict(Conte._meta.get_field('autor').related_model.CURS_ESCOLAR)

    resultats = {}

    for codi, nom in cursos.items():
        contes_amb_vots = (
            Conte.objects
            .filter(autor__curs=codi)
            .annotate(num_vots=Count('vots'))
            .order_by('-num_vots', 'titol')
        )
        resultats[nom] = contes_amb_vots

    return render(request, 'resultatsactuals.html', {
        'resultats': resultats
    })

def votar_conte(request, conte_id):
    if request.method == 'POST':
        conte = get_object_or_404(Conte, id=conte_id)
        Vot.objects.create(conte=conte)
    return redirect('contes_per_curs')