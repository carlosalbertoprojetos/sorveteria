import json
from django.shortcuts import get_object_or_404, render
from .models import (
    Embalagem,
    MontaPote,
    Pedido,
    SacolaItens,
    SelCobertura,
    SelSabor,
    TipoSabor,
    Cobertura,
)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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


# Adicionar itens na sacola
@login_required(login_url="/admin/login/")
def adicionar_sacola(request):
    if request.method == "POST":
        try:
            dados_str = request.POST.get("dados", None)
            dados = json.loads(dados_str)

            embalagem_id = dados.get("embalagem_id", None)
            quantidade_pote = int(dados.get("quantidade_pote", None))

            # Tente obter a sacola existente do usuário
            pedido = Pedido.objects.filter(user=request.user, status=True).first()

            # Se não existir uma sacola, crie uma nova
            if not pedido:
                # Crie um novo pedido e associe a sacola criada
                pedido = Pedido.objects.create(
                    user=request.user,
                    status=True,
                    itens_da_sacola=SacolaItens.objects.create(),
                )
            monta_pote = MontaPote.objects.create(
                embalagem_id=embalagem_id, quantidade=quantidade_pote
            )

            for sabor in dados["sabores_selecionados"]:
                # Adicione os sabore ao pote durante a criação
                SelSabor.objects.create(
                    pote=monta_pote,
                    sabor_id=sabor["sabor_id"],
                    quantidade_bolas=sabor["quantidade"],
                )

            for cobertura in dados["cobertura_selecionadas"]:
                # Adicione as coberturas ao pote durante a criação
                SelCobertura.objects.create(
                    pote=monta_pote,
                    cobertura_id=cobertura["cobertura_id"],
                    quantidade_cobertura=cobertura["quantidade"],
                )
            pedido.itens_da_sacola.potes.add(monta_pote)
            pedido.itens_da_sacola.preco_total()

            return JsonResponse(
                {
                    "status": "success",
                    "message": "Item adicionado na sacola com sucesso!!!",
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Requisição inválida."})


@login_required(login_url="/admin/login/")
def atualiza_quantidade_sacola(request):
    if request.method == "POST":
        pedido = Pedido.objects.filter(user=request.user, status=True).first()

        pote_id = request.POST.get("poteId", None)
        novaQuantidade = request.POST.get("novaQuantidade", None)

        pote = get_object_or_404(MontaPote, id=pote_id)
        pote.quantidade = int(novaQuantidade)
        pote.save()

        response = {
            "status": "success",
            "message": "Atualizado",
            "novo_valor": f"R$ {pedido.itens_da_sacola.preco_total()}",
        }
        return JsonResponse(response)
    else:
        # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
        return JsonResponse(
            {"status": "error", "message": "Método não permitido"}, status=405
        )


@login_required(login_url="/admin/login/")
def remove_item_sacola(request):
    if request.method == "POST":
        pedido = Pedido.objects.filter(user=request.user, status=True).first()

        pote_id = request.POST.get("poteId", None)

        # Verifique se o pote_id é fornecido
        if not pote_id:
            return JsonResponse(
                {"status": "error", "message": "ID do pote não fornecido"}, status=400
            )

        # Encontre o MontaPote específico
        pote = get_object_or_404(MontaPote, id=pote_id)

        # Exclua o pote
        pote.delete()

        response = {
            "status": "success",
            "message": "Item removido com sucesso",
            "novo_valor": f"R$ {pedido.itens_da_sacola.preco_total()}",
        }

        return JsonResponse(response)
    else:
        # Se a requisição não for do tipo POST, você pode retornar um erro ou outra resposta apropriada
        return JsonResponse(
            {"status": "error", "message": "Método não permitido"}, status=405
        )
