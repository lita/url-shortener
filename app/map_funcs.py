
import pygeoip

def getLongLat(ips):
    locations = []
    geoData = pygeoip.GeoIP('./app/static/GeoLiteCity.dat')
    for ip in ips:
        record = geoData.record_by_addr(ip)
        locations.append((record['longitude'], record['latitude']))
    return locations

