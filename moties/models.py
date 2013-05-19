from django.db.models import *
from django.template import defaultfilters
from django.core.urlresolvers import reverse
import datetime

class Congres(Model):
    naam = CharField(max_length=250, unique=True, verbose_name='Naam')
    datum = DateField()
    #plaats = CharField(max_length=250)
    inleiding = CharField(max_length=250, verbose_name='Inleiding van motie')
    notulen = CharField(max_length=250, blank=True, verbose_name='Link naar notulen')
    kort = CharField(max_length=250, verbose_name='Afkorting in motielijsten', unique=True)

    class Meta:
        ordering = ('datum',)

    def __unicode__(self):
        return "Congres %s" % self.naam
    
class Hoofdstuk(Model):
    naam = CharField(max_length=250, unique=True)
    nummer = IntegerField(unique=True)    
    
    def __unicode__(self):
        return "Hoofdstuk %d: %s" % (self.nummer, self.naam)
    
class Tag(Model):
    kort = CharField(db_index=True, max_length=40, primary_key=True, verbose_name='Tag')
    lang = CharField(max_length=250, verbose_name='Beschrijving', blank=True)

    def __unicode__(self):
        return self.kort
    
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
    constateringen = TextField(blank=True)
    overwegingen = TextField(blank=True)
    uitspraken = TextField(blank=True)
    toelichting = TextField(blank=True)
    content = TextField(blank=True, verbose_name="Custom content (override, kan HTML aan)")
    status = CharField(max_length=2, db_index=True, choices=STATUS_CHOICES, default=INGEDIEND)
    indiener = CharField(max_length=250, blank=True, verbose_name="Indiener(s)")
    woordvoerder = CharField(max_length=40, blank=True, verbose_name="Woordvoerder")
    congres = ForeignKey(Congres, null=True, blank=True, verbose_name="Congres")
    indiendatum = DateField(verbose_name="Datum waarop de motie is ingediend")
    hoofdstuk = ForeignKey(Hoofdstuk, null=True, blank=True, verbose_name="Hoofdstuk uit het politieke programma")
    tags = ManyToManyField(Tag, blank=True)
    datum = DateField(verbose_name="Datum", db_index=True)

    class Meta:
        ordering = ('datum',)

    def update_datum(self):
        self.datum = self.congres != None and self.congres.datum or self.indiendatum 

    def __unicode__(self):
        return self.titel

    def save(self, *args, **kwargs):
        if not self.id:
            self.indiendatum = datetime.date.today()
        if self.congres != None:
            self.datum = self.congres.datum
        else:
            self.datum = self.indiendatum
        super(Motie, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('moties:motie', kwargs={'slug': defaultfilters.slugify(self.titel), 'pk': self.pk})
