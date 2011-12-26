def save(self):
    print self.descr_choices[self.street_type]

    if not self.geocode_flag:
#            location = "%s, %s, %s, %s" % (self.descr_choices[self.street_type], self.street_name, self.house, self.city)
        location = "%s+%s,+%s" % (self.street_name, self.house, self.city)
        print location

        latlng = self.geocode(location)
        latlng = latlng.split(',')
        self.location_manual_latitude = latlng[0]
        self.location_manual_longitude = latlng[1]

    else:
        self.geocode_flag = None

    super(Address, self).save()


def geocode(self, location):
    output = "csv"
#        location = urllib.quote_plus(location)
    print location
#    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, settings.GOOGLE_API_KEY)
    request = u'http://maps.google.com/maps/geo?q=%s&output=%s&key=%s&sensor=false&oe=utf8' % (location, output, 'ABQIAAAABdHuQzfLcNwgKwRN3Q2l8BRZ5fEhGU1EjcrDWf4PIqpxqvkbTBRRwngWkRz7hd8a4uuGjToYGn2OZg')
    print request
    data = urllib.urlopen(request).read()
    print data
#        dlist = data.split(',')
#        if dlist[0] == '200':
#            return "%s,%s" % (dlist[2], dlist[3])
#        else:
    return ','
