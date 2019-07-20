from django.db.models import *
from django.template import defaultfilters
from django.core.urlresolvers import reverse
import datetime

class Standpunt(Model):
    naam = CharField(max_length=250, verbose_name="Begrip", primary_key=True)
    beschrijving = TextField(help_text="Gebruik dubbele enter voor nieuwe paragraaf")
    letter = CharField(blank=True, max_length=1, verbose_name="Letter voor indexering", help_text="Wordt automatisch gegenereerd indien niet ingevuld")

    class Meta:
        verbose_name_plural = 'standpunten'

    def save(self, *args, **kwargs):
        if self.letter == None:
            self.letter = self.naam[0].upper()
        if len(self.letter) != 1:
            self.letter = self.naam[0].upper()
        super(Standpunt, self).save(*args, **kwargs)

    def __str__(self):
        return self.naam

class Tag(Model):
    kort = CharField(db_index=True, max_length=40, primary_key=True, verbose_name='Tag')
    lang = CharField(max_length=250, verbose_name='Beschrijving', blank=True, help_text="Optionele beschrijving voor de admin")

    def __str__(self):
        return self.kort

class Programma(Model):
    datum = DateField()
    text = TextField(help_text="Beschikbare tags:<br/>[b]vet[/b]<br/>[i]cursief[/i]<br/>[url=\"link\"]linktekst[/url]<br/>"+
                               "[label=\"linkhier\"] om een anchor te maken die met [url=\"#linkhier\"]...[/url] bereikbaar is<br/>"+
                               "[img=\"link.jpg\"] voor plaatjes<br/>[ul]...[/ul] om een bulletlist te maken<br/>"+
                               "[ol]...[/ol] om een genummerde lijst te maken<br/>[li]blablabla[/li] voor elke item in een lijst<br/><br/>"+
                               "Gebruik een dubbele enter voor een nieuwe paragraaf, een enkele enter voor een line-break.<br/><br/>"+
                               "Een * aan het begin van een regel opent een nieuwe hoofdstuk, gebruik meerdere **** voor subsecties")
    zichtbaar = BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'programma\'s'

    def __str__(self):
        return "Programma van " + str(self.datum)

    def parse_programma(self):
        levels = []
        pieces = []

        cur_level = 0
        cur_index = None
        cur_title = None
        cur_text_list = []
        cur_text = None
        sup = False
    
        for line in self.text.strip().split("\n"):
            line = line.strip()
            # strip stars
            stars = 0
            while len(line) > 0:
                if line[0] == '*':
                    stars = stars + 1
                    line = line[1:]
                else:
                    break
            line = line.strip() # strip whitespace after stars
            if len(line) == 0:
                # empty line
                if cur_text != None: cur_text_list += [cur_text]
                cur_text = None
            elif stars == 0:
                # no stars
                if cur_text == None: cur_text = line
                else: cur_text += "\n" + line
            else:
                # update level
                levels = levels[:stars]
                while stars > (len(levels)+1): levels = levels + [1]
                if len(levels) == stars: 
                    levels[stars-1] = levels[stars-1] + 1
                elif stars == 0: levels += [1]
                else: levels += [1]
   
                if cur_text != None: cur_text_list += [cur_text]
                if len(cur_text_list) > 0 or cur_title != None:
                    pieces += ((cur_level, cur_index, sup, cur_title, tuple(cur_text_list)),)
    
                if line[0] == "!":
                    sup = True
                    line = line[1:].strip()
                else:
                    sup = False

                cur_level = len(levels)
                cur_index = ".".join([str(i) for i in levels])
                cur_title = line
                cur_text_list = []
                cur_text = None
    
        if cur_text != None: cur_text_list += [cur_text]
        pieces += ((cur_level, cur_index, sup, cur_title, tuple(cur_text_list)),)
        return pieces

    def hoofdstukken_iter(self):
        count = 1
        for line in self.text.strip().split("\n"):
            line = line.strip()
            if len(line) > 2 and line[0] == "*" and line[1] != "*":
                yield (str(count), line[1:].strip(),)
                count += 1

class Congres(Model):
    naam = CharField(max_length=250, unique=True, verbose_name='Naam', help_text='Wordt o.a. gebruikt bij titel van de motie, bijvoorbeeld "Zomercongres 2013"')
    datum = DateField()
    inleiding = CharField(max_length=250, verbose_name='Inleiding van motie', help_text='Bijvoorbeeld: De ALV van de JD, bijeen te <plaats> op <datum>,')
    notulen = CharField(max_length=250, blank=True, verbose_name='Link naar notulen', help_text='Gebruik een volledig adres, inclusief http://')
    kort = CharField(max_length=250, verbose_name='Afkorting in motielijsten', unique=True, help_text='Bijvoorbeeld: ALV 99')
    tag = ForeignKey(Tag, null=False, verbose_name="Congrestag", on_delete=PROTECT)

    class Meta:
        ordering = ('datum',)
        verbose_name_plural = 'congressen'

    def __str__(self):
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
    actueel = BooleanField(default=False, help_text="Actuele PM")

    class Meta:
        ordering = ('datum',)
        verbose_name_plural = 'politieke moties'

    def __str__(self):
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
        return reverse('hellios:motie', kwargs={'slug': defaultfilters.slugify(self.titel), 'pk': self.pk})

class Comment(Model):
    tekst = TextField()
    auteur = CharField(max_length=250)
    email = CharField(max_length=250, blank=True)
    motie = ForeignKey(Motie, related_name="comments")

    def __str__(self):
        return "Comment van %s" % (self.auteur,)

class Resultatenboek(Model):
    title = CharField(max_length=250, verbose_name="Naam", primary_key=True)
    file = FileField(upload_to='resultatenboeken/%Y/%m/%d', null=True)

    class Meta:
        verbose_name_plural = 'resultatenboeken'

    def __str__(self):
        return "Resultatenboek %s" % (self.title,)
