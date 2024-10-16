# Generated by Django 4.1.4 on 2024-10-12 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_montapote_options_alter_pedido_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sacolaitens',
            options={'verbose_name': 'C - Itens da Sacola', 'verbose_name_plural': 'C - Itens da Sacola'},
        ),
        migrations.AlterField(
            model_name='pedido',
            name='pago',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SelCobertura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_cobertura', models.PositiveIntegerField()),
                ('cobertura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cobertura', to='myapp.cobertura')),
                ('pote', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pote_cobertura', to='myapp.montapote')),
            ],
            options={
                'verbose_name': 'B - SelCobertura',
                'verbose_name_plural': 'B - SelCobertura',
            },
        ),
    ]
