# coding: utf-8
from django.contrib import admin
from django.db.models import Model, ForeignKey, CharField, IntegerField, SlugField, FloatField


TYPE_CHOICES = (
    (1, u'Country'),
    (2, u'City'),
    (3, u'Airport')
)


class Location(Model):
    """
    Поля обязательные по ТЗ у всех локаций
    """
    type_location = IntegerField(choices=TYPE_CHOICES)
    rus_name = CharField(max_length=100, default=u'')
    eng_name = CharField(max_length=100)
    latitude = FloatField(blank=True, null=True)
    longitude = FloatField(blank=True, null=True)
    slug = SlugField(max_length=50, unique=True)

    class Meta:
        abstract = True

    def display(self):
        self.type_location = self.get_type_location_display()
        return self


class Airport(Location):
    """
    """
    iata_code = CharField(max_length=3, primary_key=True)
    icao_code = CharField(max_length=4, default=u'')
    city = ForeignKey('City')
    elevation = IntegerField(blank=True, null=True)
    runway_length = IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.type_location = 3
        self.slug = '-'.join([str(self.type_location), self.iata_code, self.eng_name.replace(' ', '-')])
        super(Airport, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/airport/{0}/'.format(self.slug)


class City(Location):
    """
    """
    gmt_offset = CharField(max_length=8, default='0')
    country = ForeignKey('Country')

    def save(self, *args, **kwargs):
        self.type_location = 2
        self.slug = '-'.join([
            str(self.type_location),
            str(self.latitude),
            str(self.longitude),
            self.eng_name.replace(' ', '-')
        ])
        super(City, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/city/{0}/'.format(self.slug)


class Country(Location):
    """
    """
    iso_code = CharField(max_length=2, primary_key=True)

    def save(self, *args, **kwargs):
        self.type_location = 1
        self.slug = '-'.join([str(self.type_location), self.iso_code, self.eng_name.replace(' ', '-')])
        super(Country, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/country/{0}/'.format(self.slug)


class Change(admin.ModelAdmin):
    list_display = ('rus_name', 'eng_name', 'slug', 'type_location')

admin.site.register(Country, Change)
admin.site.register(City, Change)
admin.site.register(Airport, Change)