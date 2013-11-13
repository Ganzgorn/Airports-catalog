# coding: utf-8
from django.db import DatabaseError
from airports_catalog.airports.models import Country, City, Airport


def load_data():
    file_a = open('apinfo.ru.csv', 'r')
    errors = []
    for line in file_a:
        fields = line.split(';')

        if fields[9]:
            try:
                country = Country.objects.get(iso_code=fields[9])
            except Country.DoesNotExist:
                country = Country()
                country.iso_code = fields[9]
                country.eng_name = fields[8]
                country.rus_name = fields[7].decode('cp1251')
                try:
                    country.save()
                except DatabaseError:
                    errors.append(country.eng_name)
            except DatabaseError:
                errors.append(fields[9])

        if country:
            latit = float(fields[10]) if fields[10] else None
            longit = float(fields[11]) if fields[11] else None
            try:
                city = City.objects.get(eng_name=fields[5], latitude=latit, longitude=longit)
            except City.DoesNotExist:
                city = City()
                city.eng_name = fields[5]
                city.rus_name = fields[4].decode('cp1251')
                city.gmt_offset = fields[6]
                city.latitude = latit
                city.longitude = longit
                city.country = country
                try:
                    city.save()
                except DatabaseError:
                    errors.append(city.eng_name)

            except DatabaseError:
                errors.append(fields[5])

        if city and fields[0]:
            try:
                airport = Airport.objects.get(iata_code=fields[0])
            except Airport.DoesNotExist:
                airport = Airport(fields[0])
            except DatabaseError:
                errors.append()
            airport.iata_code = fields[0]
            airport.icao_code = fields[1]
            airport.eng_name = fields[3]
            airport.rus_name = fields[2].decode('cp1251')
            airport.latitude = latit
            airport.longitude = longit
            airport.runway_length = fields[12] if fields[12] else None
            airport.elevation = fields[13] if fields[13] else None
            airport.city = city
            try:
                airport.save()
            except DatabaseError:
                errors.append(airport.eng_name)

    if not errors:
        print 'All ok'
    else:
        print u'Не загрузились следующие объекты:'
        for i in errors:
            print i