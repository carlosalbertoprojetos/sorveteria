from django.shortcuts import render
from .models import Embalagem, TipoSabor, Cobertura


# Create your views here.
def index(request):
    return render(request, "index.html")


def menu(request):
    embalagens = Embalagem.objects.filter(ativo=True)
    tipo_sabor = TipoSabor.objects.filter(ativo=True)
    coberturas = Cobertura.objects.filter(ativo=True)
    context = {
        "embalagens": embalagens,
        "tipo_sabor": tipo_sabor,
        "coberturas": coberturas,
    }
    return render(request, "menu.html", context)
