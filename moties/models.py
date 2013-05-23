from django.db.models import *
from django.template import defaultfilters
from django.core.urlresolvers import reverse
import datetime

class Standpunt(Model):
    naam = CharField(max_length=250, verbose_name="Begrip", primary_key=True)
    beschrijving = TextField(help_text="Gebruik dubbele enter voor nieuwe paragraaf")
    letter = CharField(blank=True, max_length=1, verbose_name="Letter voor indexering", help_text="Wordt automatisch gegenereerd indien niet ingevuld")

    def save(self, *args, **kwargs):
        if self.letter == None:
            self.letter = self.naam[0].upper()
        if len(self.letter) != 1:
            self.letter = self.naam[0].upper()
        super(Standpunt, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.naam

class Tag(Model):
    kort = CharField(db_index=True, max_length=40, primary_key=True, verbose_name='Tag')
    lang = CharField(max_length=250, verbose_name='Beschrijving', blank=True, help_text="Optionele beschrijving voor de admin")

    def __unicode__(self):
        return self.kort

class Congres(Model):
    naam = CharField(max_length=250, unique=True, verbose_name='Naam', help_text='Wordt o.a. gebruikt bij titel van de motie, bijvoorbeeld "Zomercongres 2013"')
    datum = DateField()
    inleiding = CharField(max_length=250, verbose_name='Inleiding van motie', help_text='Bijvoorbeeld: De ALV van de JD, bijeen te <plaats> op <datum>,')
    notulen = CharField(max_length=250, blank=True, verbose_name='Link naar notulen', help_text='Gebruik een volledig adres, inclusief http://')
    kort = CharField(max_length=250, verbose_name='Afkorting in motielijsten', unique=True, help_text='Bijvoorbeeld: ALV 99')
    tag = ForeignKey(Tag, null=True, verbose_name="Congrestag")

    class Meta:
        ordering = ('datum',)

    def __unicode__(self):
        return "Congres %s" % self.naam

    def save(self, *args, **kwargs):
        # add tags
        if self.tag != None:
            for motie in self.moties.all():
                motie.tags.add(self.tag)
                motie.save()
        super(Congres, self).save(*args, **kwargs)
    
class Motie(Model):
    INGEDIEND = "IN"
    GOEDGEKEURD = "GO"
    CONGRES = "CO"
    VERWORPEN = "NO"
    AANGENOMEN = "JA"
    UITGESTELD = "YO"
    
    STATUS_CHOICES = (
        (INGEDIEND, 'Ingediend'),
        (GOEDGEKEURD, 'Goedgekeurd'),
        (CONGRES, 'In congresboek'),
        (VERWORPEN, 'Verworpen'),
        (AANGENOMEN, 'Aangenomen'),
        (UITGESTELD, 'Uitgesteld'))
    
    titel = CharField(max_length=250, db_index=True)
    constateringen = TextField(blank=True, help_text='Gebruik een dubbele enter voor de volgende bullet')
    overwegingen = TextField(blank=True, help_text='Gebruik een dubbele enter voor de volgende bullet')
    uitspraken = TextField(blank=True, help_text='Gebruik een dubbele enter voor de volgende bullet')
    toelichting = TextField(blank=True, help_text='Gebruik een dubbele enter voor de volgende paragraaf')
    content = TextField(blank=True, verbose_name="Custom content (override, kan HTML aan)", help_text="Als dit veld gevuld is, worden de andere tekstvelden genegeerd. Let op dat dit veld unsafe gebruikt wordt: HTML wordt doorgegeven!")
    status = CharField(max_length=2, db_index=True, choices=STATUS_CHOICES, default=INGEDIEND)
    indiener = CharField(max_length=250, blank=True, verbose_name="Indiener(s)")
    woordvoerder = CharField(max_length=40, blank=True, verbose_name="Woordvoerder")
    congres = ForeignKey(Congres, null=True, blank=True, verbose_name="Congres", related_name='moties')
    indiendatum = DateField(verbose_name="Datum waarop de motie is ingediend", help_text="Als deze motie niet gekoppeld is aan een congres, wordt deze datum gebruikt als datum van de motie")
    tags = ManyToManyField(Tag, blank=True)
    datum = DateField(verbose_name="Datum", db_index=True)
    related = ManyToManyField('self', blank=True, symmetrical=True)

    class Meta:
        ordering = ('datum',)

    def __unicode__(self):
        return self.titel

    def save(self, *args, **kwargs):
        if self.congres != None:
            self.datum = self.congres.datum
        else:
            self.datum = self.indiendatum
        super(Motie, self).save(*args, **kwargs)

        # note: when editing in admin tag is removed (!)
        if self.congres != None:
            if self.congres.tag != None:
                if self.tags.filter(pk=self.congres.tag.pk).count() == 0:
                    self.tags.add(self.congres.tag)
                    super(Motie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('moties:motie', kwargs={'slug': defaultfilters.slugify(self.titel), 'pk': self.pk})

class Comment(Model):
    tekst = TextField()
    auteur = CharField(max_length=250)
    email = CharField(max_length=250, blank=True)
    motie = ForeignKey(Motie, related_name="comments")

    def __unicode__(self):
        return "Comment van %s" % (self.auteur,)
