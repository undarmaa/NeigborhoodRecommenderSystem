from geopy.geocoders import Nominatim
import geopy

def getAddrFromGeocoord(lat, lon):

    geolocator = Nominatim()

    try:
        location = geolocator.reverse(str(lat) + ", " + str(lon))
        addr = location.address
    except geopy.exc.GeocoderTimedOut:
        addr = ""

    # print location.address
    # print (location.latitude, location.longitude)

    return addr #sido.strip(), gungu.strip(), dong[0]


# addr is unicode
def getGeocoordFromAddr(addr):

    geolocator = Nominatim()

    try:
        location = geolocator.geocode(addr)
        lat, lon, err = location.latitude, location.longitude, False
    except:
        lat, lon, err = 0., 0., True

    # print location.address.encode('utf-8')
    # print location.latitude, location.longitude
    # print location.raw

    return lat, lon, err