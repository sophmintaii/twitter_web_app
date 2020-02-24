import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl
import folium
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent='specify_your_app_name_here', timeout=100)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.01)

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'


def get_dict_of_loc(acct):
    '''
    str -> dict
    returns dictionary where every friend of
    given twitter account is a key
    and their location is a value
    '''
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    while True:
        print('')
        if (len(acct) < 1):
            break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '5'})
        print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)

        headers = dict(connection.getheaders())
        print('Remaining', headers['x-rate-limit-remaining'])
        data = dict()
        for user in js['users']:
            try:
                geolocator = Nominatim(user_agent='specify_your_app_name_here')
                try:
                    location = geolocator.geocode(user['location'])
                    coord = (location.latitude, location.longitude)
                    data[user['screen_name']] = coord
                except:
                    pass
            except:
                pass
        return data


def create_map_layer(data):
    '''
    dict -> folium object
    returns new layer of the map where markers are locations of some twitter account's friends
    '''
    friends = folium.FeatureGroup(name='Friends')

    for user in data:

        folium.Marker(
            location=data[user],
            popup=user,
            icon=folium.Icon(icon='user')
        ).add_to(friends)
    return friends


def main(acct):
    '''
    None -> folium object
    returns new map with layer of friends' locations
    '''
    map = folium.Map(location=[0, 0],
                     zoom_start=1.5)
    data = get_dict_of_loc(acct)
    map.add_child(create_map_layer(data))
    map.save('/templates/friends.html')


if __name__ == '__main__':
    acct = input('Enter Twitter username: ')
    main(acct)
