# Generated by Django 4.1.4 on 2024-10-14 14:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '1 - Base',
                'verbose_name_plural': '1 - Base',
            },
        ),
        migrations.CreateModel(
            name='Cobertura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('ativo', models.BooleanField(default=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Adm - Cobertura',
                'verbose_name_plural': 'Adm - Cobertura',
            },
        ),
        migrations.CreateModel(
            name='Embalagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Adm - Embalagem',
                'verbose_name_plural': 'Adm - Embalagem',
            },
        ),
        migrations.CreateModel(
            name='FormaPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Adm - Formas de Pagamento',
                'verbose_name_plural': 'Adm - Formas de Pagamento',
            },
        ),
        migrations.CreateModel(
            name='Sabor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Adm - Sabor',
                'verbose_name_plural': 'Adm - Sabor',
            },
        ),
        migrations.CreateModel(
            name='TipoMercadoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Adm - Tipo de Mercadoria',
                'verbose_name_plural': 'Adm - Tipo de Mercadoria',
            },
        ),
        migrations.CreateModel(
            name='UnidadeMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('um', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Adm - Unidade de Medida',
                'verbose_name_plural': 'Adm - Unidade de Medida',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ativo', models.BooleanField(default=True)),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='myapp.base')),
                ('sabor', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='myapp.sabor')),
            ],
            options={
                'verbose_name': '2 - Produto',
                'verbose_name_plural': '2 - Produto',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now_add=True, null=True)),
                ('pago', models.BooleanField(default=False)),
                ('entrega', models.BooleanField(default=False)),
                ('pagamento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='myapp.formapagamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pedido_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedido',
            },
        ),
        migrations.AddField(
            model_name='base',
            name='embalagem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='myapp.embalagem'),
        ),
        migrations.AddField(
            model_name='base',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tipomercadoria'),
        ),
        migrations.AddField(
            model_name='base',
            name='um',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='myapp.unidademedida'),
        ),
    ]
