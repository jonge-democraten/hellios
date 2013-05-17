from django.db import models
import datetime

class Congres(models.Model):
    naam = models.CharField(max_length=250)
    datum = models.DateField()
    plaats = models.CharField(max_length=250)

    def __unicode__(self):
        return "Congres %s" % self.naam
    
class Hoofdstuk(models.Model):
    naam = models.CharField(max_length=250)
    nummer = models.IntegerField()    
    
    def __unicode__(self):
        return "Hoofdstuk %d: %s" % (self.nummer, self.naam)
    
class Tag(models.Model):
    kort = models.CharField(max_length=40)
    lang = models.CharField(max_length=140)

    def __unicode__(self):
        return self.kort
    
class Motie(models.Model):
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
    
    titel = models.CharField(max_length=250)
    content = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=INGEDIEND)
    indiener = models.CharField(max_length=140)
    woordvoerder = models.CharField(max_length=40, verbose_name="Woordvoerder")
    congres = models.ForeignKey(Congres, null=True, blank=True, verbose_name="Congres")
    indiendatum = models.DateField(verbose_name="Datum waarop de motie is ingediend")
    hoofdstuk = models.ForeignKey(Hoofdstuk, null=True, blank=True, verbose_name="Hoofdstuk uit het politieke programma")
    tags = models.ManyToManyField(Tag, blank=True)
    datum = models.DateField(verbose_name="Datum")

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
