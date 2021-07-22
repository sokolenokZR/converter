import configparser
import requests
from random import randint
import json
import os


class Map:
    URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    API_KEY = None
    Trafic_jams = os.getcwd() + '\\Dictionary\\google_map\\traffic_jams.json'

    def __init__(self):
        config = configparser.ConfigParser()
        if __name__ == '__main__':
            config.read_file(open('secret.cfg'))
        else:
            config.read_file(open(os.getcwd() + '\\Dictionary\\google_map\\secret.cfg'))

        self.API_KEY = config.get('GOOGLE', 'API_KEY')
        if __name__ == '__main__':
            self.Trafic_jams = 'traffic_jams.json'

    def request_(self, **params):
        return requests.get(
            self.URL + 'origins=' + params["place_from"] + '&destinations=' + params[
                "place_to"] + '&key=' + self.API_KEY).json()

    def get_distances_and_times(self, **params):
        place_from = self.translate(params["place_from"])
        places_to = self.translate(params["places_to"])
        day = params["day"]
        time = params["time"]
        result = self.request_(place_from=place_from, place_to=places_to)
        return self.reformat_distances_and_times(results=result["rows"][0]["elements"],
                                                 place_from=params["place_from"][0], places_to=params["places_to"], day=day, time=time)

    def reformat_distances_and_times(self, results, **params):
        ans = {params["place_from"]: {}}
        for i in range(len(results)):
            if results[i]["status"] == 'NOT_FOUND':
                print("\033[33m Enter a normal data from address '{}', to address '{}':]".format(params["place_from"], params["places_to"]))
                print('distance in km:')
                distance = int(input())
                print('time in minutes without traffic jams:')
                in_time = int(input())
                ans[params["place_from"]][params["places_to"][i]] = {
                    "distance": distance,
                    "time": in_time}
            else:
                ans[params["place_from"]][params["places_to"][i]] = {
                    "distance": (results[i]["distance"]["value"] // 1000) + (
                        1 if results[i]["distance"]["value"] % 1000 >= 100 else 0),
                    "time": (results[i]["duration"]["value"] // 60) + (1 if results[i]["duration"]["value"] % 60 >= 25 else 0)}
        return ans

    def get_local_time(self, time):
        h = int(time.split('-')[0])
        m = int(time.split('-')[1])
        if m % 15 > 7:
            m = (((m // 15) + 1) * 15)
        else:
            m = ((m // 15) * 15)
        if m == 60:
            h = h + 1
        time = str(h) + ':' + ('00' if m == 0 or m == 60 else str(m))
        return time

    def time_with_traffic_jams_on_time(self, day, time, time_without_traffic_jams):
        time = self.get_local_time(time)
        with open(self.Trafic_jams, "r") as read_file:
            traffic_jams = json.load(read_file)
        try:
            traffic_jam = traffic_jams[day][time]
        except KeyError:
            traffic_jam = 1
        return int(time_without_traffic_jams + (time_without_traffic_jams * 0.2 * traffic_jam))

    def test_api(self, place_from, places_to, day, time):
        return {place_from[0]: {places_to[0]: {"distance": randint(10, 30), "time": randint(85, 90)}}}

    def translate(self, places):
        places_str = ''
        for place in places:
            places_str = places_str + place + '|'
        places_str = places_str[:-1]
        return places_str


def main():
    m = Map()
    r = m.time_with_traffic_jams_on_time('Monday', '18-08', 30)
    print(r)


if __name__ == '__main__':
    main()
