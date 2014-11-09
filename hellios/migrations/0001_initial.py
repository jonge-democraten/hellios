# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tekst', models.TextField()),
                ('auteur', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Congres',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('naam', models.CharField(help_text=b'Wordt o.a. gebruikt bij titel van de motie, bijvoorbeeld "Zomercongres 2013"', unique=True, max_length=250, verbose_name=b'Naam')),
                ('datum', models.DateField()),
                ('inleiding', models.CharField(help_text=b'Bijvoorbeeld: De ALV van de JD, bijeen te <plaats> op <datum>,', max_length=250, verbose_name=b'Inleiding van motie')),
                ('notulen', models.CharField(help_text=b'Gebruik een volledig adres, inclusief http://', max_length=250, verbose_name=b'Link naar notulen', blank=True)),
                ('kort', models.CharField(help_text=b'Bijvoorbeeld: ALV 99', unique=True, max_length=250, verbose_name=b'Afkorting in motielijsten')),
            ],
            options={
                'ordering': ('datum',),
                'verbose_name_plural': 'congressen',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Motie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titel', models.CharField(max_length=250, db_index=True)),
                ('constateringen', models.TextField(help_text=b'Gebruik een dubbele enter voor de volgende bullet', blank=True)),
                ('overwegingen', models.TextField(help_text=b'Gebruik een dubbele enter voor de volgende bullet', blank=True)),
                ('uitspraken', models.TextField(help_text=b'Gebruik een dubbele enter voor de volgende bullet', blank=True)),
                ('toelichting', models.TextField(help_text=b'Gebruik een dubbele enter voor de volgende paragraaf', blank=True)),
                ('content', models.TextField(help_text=b'Als dit veld gevuld is, worden de andere tekstvelden genegeerd. Let op dat dit veld unsafe gebruikt wordt: HTML wordt doorgegeven!', verbose_name=b'Custom content (override, kan HTML aan)', blank=True)),
                ('status', models.CharField(default=b'IN', max_length=2, db_index=True, choices=[(b'IN', b'Ingediend'), (b'GO', b'Goedgekeurd'), (b'CO', b'In congresboek'), (b'NO', b'Verworpen'), (b'JA', b'Aangenomen'), (b'YO', b'Uitgesteld')])),
                ('indiener', models.CharField(max_length=250, verbose_name=b'Indiener(s)', blank=True)),
                ('woordvoerder', models.CharField(max_length=40, verbose_name=b'Woordvoerder', blank=True)),
                ('indiendatum', models.DateField(help_text=b'Als deze motie niet gekoppeld is aan een congres, wordt deze datum gebruikt als datum van de motie', verbose_name=b'Datum waarop de motie is ingediend')),
                ('datum', models.DateField(verbose_name=b'Datum', db_index=True)),
                ('actueel', models.BooleanField(default=False, help_text=b'Actuele PM')),
                ('congres', models.ForeignKey(related_name=b'moties', verbose_name=b'Congres', blank=True, to='hellios.Congres', null=True)),
                ('related', models.ManyToManyField(related_name='related_rel_+', to='hellios.Motie', blank=True)),
            ],
            options={
                'ordering': ('datum',),
                'verbose_name_plural': 'politieke moties',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Programma',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datum', models.DateField()),
                ('text', models.TextField(help_text=b'Beschikbare tags:<br/>[b]vet[/b]<br/>[i]cursief[/i]<br/>[url="link"]linktekst[/url]<br/>[label="linkhier"] om een anchor te maken die met [url="#linkhier"]...[/url] bereikbaar is<br/>[img="link.jpg"] voor plaatjes<br/>[ul]...[/ul] om een bulletlist te maken<br/>[ol]...[/ol] om een genummerde lijst te maken<br/>[li]blablabla[/li] voor elke item in een lijst<br/><br/>Gebruik een dubbele enter voor een nieuwe paragraaf, een enkele enter voor een line-break.<br/><br/>Een * aan het begin van een regel opent een nieuwe hoofdstuk, gebruik meerdere **** voor subsecties')),
                ('zichtbaar', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': "programma's",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultatenboek',
            fields=[
                ('title', models.CharField(max_length=250, serialize=False, verbose_name=b'Naam', primary_key=True)),
                ('file', models.FileField(null=True, upload_to=b'resultatenboeken/%Y/%m/%d')),
            ],
            options={
                'verbose_name_plural': 'resultatenboeken',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Standpunt',
            fields=[
                ('naam', models.CharField(max_length=250, serialize=False, verbose_name=b'Begrip', primary_key=True)),
                ('beschrijving', models.TextField(help_text=b'Gebruik dubbele enter voor nieuwe paragraaf')),
                ('letter', models.CharField(help_text=b'Wordt automatisch gegenereerd indien niet ingevuld', max_length=1, verbose_name=b'Letter voor indexering', blank=True)),
            ],
            options={
                'verbose_name_plural': 'standpunten',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('kort', models.CharField(max_length=40, serialize=False, verbose_name=b'Tag', primary_key=True, db_index=True)),
                ('lang', models.CharField(help_text=b'Optionele beschrijving voor de admin', max_length=250, verbose_name=b'Beschrijving', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='motie',
            name='tags',
            field=models.ManyToManyField(to='hellios.Tag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='congres',
            name='tag',
            field=models.ForeignKey(verbose_name=b'Congrestag', to='hellios.Tag', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='motie',
            field=models.ForeignKey(related_name=b'comments', to='hellios.Motie'),
            preserve_default=True,
        ),
    ]
