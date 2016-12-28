# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hellios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congres',
            name='inleiding',
            field=models.CharField(help_text='Bijvoorbeeld: De ALV van de JD, bijeen te <plaats> op <datum>,', verbose_name='Inleiding van motie', max_length=250),
        ),
        migrations.AlterField(
            model_name='congres',
            name='kort',
            field=models.CharField(unique=True, help_text='Bijvoorbeeld: ALV 99', verbose_name='Afkorting in motielijsten', max_length=250),
        ),
        migrations.AlterField(
            model_name='congres',
            name='naam',
            field=models.CharField(unique=True, help_text='Wordt o.a. gebruikt bij titel van de motie, bijvoorbeeld "Zomercongres 2013"', verbose_name='Naam', max_length=250),
        ),
        migrations.AlterField(
            model_name='congres',
            name='notulen',
            field=models.CharField(help_text='Gebruik een volledig adres, inclusief http://', blank=True, verbose_name='Link naar notulen', max_length=250),
        ),
        migrations.AlterField(
            model_name='congres',
            name='tag',
            field=models.ForeignKey(verbose_name='Congrestag', null=True, to='hellios.Tag'),
        ),
        migrations.AlterField(
            model_name='motie',
            name='actueel',
            field=models.BooleanField(help_text='Actuele PM', default=False),
        ),
        migrations.AlterField(
            model_name='motie',
            name='congres',
            field=models.ForeignKey(verbose_name='Congres', null=True, to='hellios.Congres', blank=True, related_name='moties'),
        ),
        migrations.AlterField(
            model_name='motie',
            name='constateringen',
            field=models.TextField(help_text='Gebruik een dubbele enter voor de volgende bullet', blank=True),
        ),
        migrations.AlterField(
            model_name='motie',
            name='content',
            field=models.TextField(help_text='Als dit veld gevuld is, worden de andere tekstvelden genegeerd. Let op dat dit veld unsafe gebruikt wordt: HTML wordt doorgegeven!', blank=True, verbose_name='Custom content (override, kan HTML aan)'),
        ),
        migrations.AlterField(
            model_name='motie',
            name='datum',
            field=models.DateField(verbose_name='Datum', db_index=True),
        ),
        migrations.AlterField(
            model_name='motie',
            name='indiendatum',
            field=models.DateField(help_text='Als deze motie niet gekoppeld is aan een congres, wordt deze datum gebruikt als datum van de motie', verbose_name='Datum waarop de motie is ingediend'),
        ),
        migrations.AlterField(
            model_name='motie',
            name='indiener',
            field=models.CharField(blank=True, verbose_name='Indiener(s)', max_length=250),
        ),
        migrations.AlterField(
            model_name='motie',
            name='overwegingen',
            field=models.TextField(help_text='Gebruik een dubbele enter voor de volgende bullet', blank=True),
        ),
        migrations.AlterField(
            model_name='motie',
            name='status',
            field=models.CharField(choices=[('IN', 'Ingediend'), ('GO', 'Goedgekeurd'), ('CO', 'In congresboek'), ('NO', 'Verworpen'), ('JA', 'Aangenomen'), ('YO', 'Uitgesteld')], default='IN', db_index=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='motie',
            name='toelichting',
            field=models.TextField(help_text='Gebruik een dubbele enter voor de volgende paragraaf', blank=True),
        ),
        migrations.AlterField(
            model_name='motie',
            name='uitspraken',
            field=models.TextField(help_text='Gebruik een dubbele enter voor de volgende bullet', blank=True),
        ),
        migrations.AlterField(
            model_name='motie',
            name='woordvoerder',
            field=models.CharField(blank=True, verbose_name='Woordvoerder', max_length=40),
        ),
        migrations.AlterField(
            model_name='programma',
            name='text',
            field=models.TextField(help_text='Beschikbare tags:<br/>[b]vet[/b]<br/>[i]cursief[/i]<br/>[url="link"]linktekst[/url]<br/>[label="linkhier"] om een anchor te maken die met [url="#linkhier"]...[/url] bereikbaar is<br/>[img="link.jpg"] voor plaatjes<br/>[ul]...[/ul] om een bulletlist te maken<br/>[ol]...[/ol] om een genummerde lijst te maken<br/>[li]blablabla[/li] voor elke item in een lijst<br/><br/>Gebruik een dubbele enter voor een nieuwe paragraaf, een enkele enter voor een line-break.<br/><br/>Een * aan het begin van een regel opent een nieuwe hoofdstuk, gebruik meerdere **** voor subsecties'),
        ),
        migrations.AlterField(
            model_name='resultatenboek',
            name='file',
            field=models.FileField(upload_to='resultatenboeken/%Y/%m/%d', null=True),
        ),
        migrations.AlterField(
            model_name='resultatenboek',
            name='title',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Naam', max_length=250),
        ),
        migrations.AlterField(
            model_name='standpunt',
            name='beschrijving',
            field=models.TextField(help_text='Gebruik dubbele enter voor nieuwe paragraaf'),
        ),
        migrations.AlterField(
            model_name='standpunt',
            name='letter',
            field=models.CharField(help_text='Wordt automatisch gegenereerd indien niet ingevuld', blank=True, verbose_name='Letter voor indexering', max_length=1),
        ),
        migrations.AlterField(
            model_name='standpunt',
            name='naam',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Begrip', max_length=250),
        ),
        migrations.AlterField(
            model_name='tag',
            name='kort',
            field=models.CharField(serialize=False, primary_key=True, verbose_name='Tag', db_index=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='tag',
            name='lang',
            field=models.CharField(help_text='Optionele beschrijving voor de admin', blank=True, verbose_name='Beschrijving', max_length=250),
        ),
    ]
