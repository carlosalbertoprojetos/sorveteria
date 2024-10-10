from django.db import models
from django.contrib.auth.models import User


# Tipo de Pote (1L - 1/5L - 2L - 400mL - 800mL )
class Embalagem(models.Model):
    tipo = models.CharField(max_length=50)
    capacidade_maxima_bolas = models.PositiveIntegerField()
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.tipo} | PREÇO: R$ {self.preco:.2f}"

    class Meta:
        verbose_name = "1 - Embalagem"
        verbose_name_plural = "1 - Embalagem"


class TipoSabor(models.Model):
    tipo = models.CharField(max_length=100)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.tipo} | PREÇO: R$ {self.preco:.2f}"

    class Meta:
        verbose_name = "2 - TipoSabor"
        verbose_name_plural = "2 - TipoSabor"


class Sabor(models.Model):
    nome = models.CharField(max_length=50)
    tipo = models.ForeignKey(
        TipoSabor, related_name="tipo_sabor", on_delete=models.CASCADE
    )
    ativo = models.BooleanField()

    def __str__(self):
        return f"{self.nome} | PREÇO: R$ {self.tipo.preco:.2f}"

    class Meta:
        verbose_name = "3 - Sabor"
        verbose_name_plural = "3 - Sabor"


class Cobertura(models.Model):
    nome = models.CharField(max_length=50)
    ativo = models.BooleanField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"

    def __str__(self):
        return f"{self.nome} | PREÇO: R$ {self.preco:.2f}"

    class Meta:
        verbose_name = "4 - Cobertura"
        verbose_name_plural = "4 - Cobertura"


class MontaPote(models.Model):
    embalagem = models.ForeignKey(
        Embalagem, related_name="embalagem", on_delete=models.CASCADE, null=True
    )
    coberturas = models.ManyToManyField(Cobertura)
    quantidade = models.PositiveIntegerField(null=True)

    def preco_total(self):
        preco_embalagem = self.embalagem.preco if self.embalagem else 0
        preco_coberturas = sum(cobertura.preco for cobertura in self.coberturas.all())
        preco_sabores = 0
        for selsabor in self.pote.all():
            preco_sabor = selsabor.sabor.tipo.preco
            quantidade_bolas = selsabor.quantidade_bolas
            preco_sabores += preco_sabor * quantidade_bolas
        total_pote = preco_embalagem + preco_coberturas + preco_sabor
        total = total_pote * self.quantidade
        return total

    def __str__(self):
        return f"ID: {self.id} / POTE: {self.embalagem.tipo} / Qtd: {self.quantidade} / R$ {self.preco_total()}"

    class Meta:
        verbose_name = "A - MontaPote"
        verbose_name_plural = "A - MontaPote"


class SelSabor(models.Model):
    pote = models.ForeignKey(
        MontaPote, related_name="pote", on_delete=models.CASCADE, null=True
    )
    sabor = models.ForeignKey(
        Sabor, related_name="sabor", on_delete=models.CASCADE, null=True
    )
    quantidade_bolas = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Sabor: {self.sabor.nome}, Quantidade de Bolas: {self.quantidade_bolas}"

    class Meta:
        verbose_name = "Selecinar Sabor"
        verbose_name_plural = "Selecinar Sabor"


class SacolaItens(models.Model):
    potes = models.ManyToManyField(MontaPote)
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )  # Armazena o valor como um número decimal

    def preco_formatado(self):
        return f"R$ {self.preco:.2f}"  # Formata o valor com 2 casas decimais

    # calcula a soma dos preços de todos os produtos da sacola
    def preco_total(self):
        sacola_total = 0
        for pote in self.potes.all():
            sacola_total += pote.preco_total()
        self.preco = sacola_total
        self.save()
        return sacola_total

    def __str__(self):
        return f"CARINHO: {self.id} / R$ {self.preco_total()}"

    class Meta:
        verbose_name = "B - Itens da Sacola"
        verbose_name_plural = "B - Itens da Sacola"


class Pedido(models.Model):
    data_pedido = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, related_name="pedido_user", on_delete=models.PROTECT)
    itens_da_sacola = models.OneToOneField(
        SacolaItens, on_delete=models.CASCADE, null=True
    )
    status = models.BooleanField()
    pago = models.BooleanField()
    # Endereço
    # Pagamento com Card / Dinheiro / Pix

    def __str__(self):
        return f"Pedido: {self.id} / {self.user} / (PAGO: {self.pago})"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"
