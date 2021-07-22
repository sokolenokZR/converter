import os
import json
import datetime as dt
from datetime import datetime
from Dictionary.google_map.googlemap_API import Map
from random import randint
from pprint import pprint

if __name__ != '__main__':
    google_map = Map()

# google_map.get_distances_and_times(place_from=[], places_to=[], day="Tuesday",
#         time="8-00")
# {'Москва, Енисейская улица, 17к1': {
#   'Москва, Милютинский переулок, 19/4с1': {
#       'distance': 14,
#       'time': 24},
#   'Москва, Профсоюзная улица, 22/10к1': {
#       'distance': 29,
#       'time': 44},
#   'Москва, Поварская улица, 35': {
#       'distance': 17,
#       'time': 28},
#   'Москва, Луганская улица, вл5с5': {
#       'distance': 35,
#       'time': 51},
#   'Москва, посёлок Коммунарка, Бачуринская улица, 7к1': {
#       'distance': 48,
#       'time': 60}
#   }
# }


def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def google_api(place_from, places_to, day, time):
    distance_dict = os.getcwd() + '\\Dictionary\\distance.json'
    with open(distance_dict, "r") as read_file:
        addresses = json.load(read_file)
    if place_from[0] in addresses.keys():
        try:
            distance_time = {place_from[0]: {places_to[0]: {"distance": addresses[place_from[0]][places_to[0]]["distance"],
                                                            "time": google_map.time_with_traffic_jams_on_time(day, time, addresses[place_from[0]][places_to[0]]["time"])}}}
            return distance_time
        except KeyError:
            distance_time = google_map.get_distances_and_times(place_from=place_from,
                                                               places_to=places_to,
                                                               day=day,
                                                               time=time)
            addresses[place_from[0]].update(distance_time[place_from[0]])
            with open(distance_dict, "w") as write_file:
                json.dump(addresses, write_file, indent=4)
            distance_time[place_from[0]][places_to[0]]["time"] = google_map.time_with_traffic_jams_on_time(day, time, distance_time[place_from[0]][places_to[0]]["time"])
            return distance_time
    elif places_to[0] in addresses.keys():
        try:
            distance_time = {place_from[0]: {places_to[0]: {"distance": addresses[places_to[0]][place_from[0]]["distance"],
                                                            "time": google_map.time_with_traffic_jams_on_time(day, time, addresses[places_to[0]][place_from[0]]["time"])}}}
            return distance_time
        except KeyError:
            distance_time = google_map.get_distances_and_times(place_from=places_to,
                                                               places_to=place_from,
                                                               day=day,
                                                               time=time)
            addresses[places_to[0]].update(distance_time[places_to[0]])
            with open(distance_dict, "w") as write_file:
                json.dump(addresses, write_file, indent=4)
            distance_time = {place_from[0]: {places_to[0]: addresses[places_to[0]][place_from[0]]}}
            distance_time[place_from[0]][places_to[0]]["time"] = google_map.time_with_traffic_jams_on_time(day, time, distance_time[place_from[0]][places_to[0]]["time"])
            return distance_time
    else:
        distance_time = google_map.get_distances_and_times(place_from=place_from,
                                                           places_to=places_to,
                                                           day=day,
                                                           time=time)
        addresses.update(distance_time)
        with open(distance_dict, "w") as write_file:
            json.dump(addresses, write_file, indent=4)
        distance_time[place_from[0]][places_to[0]]["time"] = google_map.time_with_traffic_jams_on_time(day, time, distance_time[place_from[0]][places_to[0]]["time"])
        return distance_time


def get_end_time(time_st, delta_minute):
    if delta_minute < 0:
        dt1 = datetime.strptime(time_st, '%H-%M')
        end_time = dt1 - dt.timedelta(minutes=-delta_minute)
    else:
        dt1 = datetime.strptime(time_st, '%H-%M')
        end_time = dt1 + dt.timedelta(minutes=delta_minute)
    return end_time.strftime('%H-%M')


def randomize_time_from(time_f):
    delta = randint(10, 31)
    dt1 = datetime.strptime(time_f, '%H-%M')
    time_from = dt1 + dt.timedelta(minutes=delta)
    return time_from.strftime('%H-%M')


def from_base_custom(trip_2, week_day, work_start):
    address_from = 'Г. Москва, 1-я Магистральная улица, д.2'
    address_to = trip_2["address_from"]
    time_from = randomize_time_from(work_start)
    kilometr_time = google_api(place_from=[address_from], places_to=[address_to], day=week_day, time=time_from)
    kilometr = kilometr_time[address_from][address_to]["distance"]
    time_delta = kilometr_time[address_from][address_to]["time"]
    return {
        'address_from': address_from,
        'address_to': address_to,
        'customer': 'ООО "ЭКОПЛЮС"',
        'km': kilometr,
        'time': time_delta,
        'time_from': time_from,
        'time_to': get_end_time(time_from, time_delta)
    }


def calculate_kilometr_time(trip, week_day, time_st):
    address_from = trip["address_from"]
    address_to = trip["address_to"]
    time_from = randomize_time_from(time_st)
    kilometr_time = google_api(place_from=[address_from],
                               places_to=[address_to],
                               day=week_day,
                               time=time_from)
    kilometr = kilometr_time[address_from][address_to]["distance"]
    time_delta = kilometr_time[address_from][address_to]["time"]
    return {
        'address_from': address_from,
        'address_to': address_to,
        'customer': trip['customer'],
        'km': kilometr,
        'time': time_delta,
        'time_from': time_from,
        'time_to': get_end_time(time_from, time_delta)
    }


def b_a_custom(trip_1, trip_2, week_day):
    address_from = trip_1["address_to"]
    address_to = trip_2["address_from"]
    time_from = randomize_time_from(trip_1["time_to"])
    kilometr_time = google_api(place_from=[address_from], places_to=[address_to], day=week_day, time=time_from)
    kilometr = kilometr_time[address_from][address_to]["distance"]
    time_delta = kilometr_time[address_from][address_to]["time"]
    return {
        'address_from': address_from,
        'address_to': address_to,
        'customer': 'ООО "ЭКОПЛЮС"',
        'km': kilometr,
        'time': time_delta,
        'time_from': time_from,
        'time_to': get_end_time(time_from, time_delta)
    }


def to_base_custom(trip_2, week_day):
    address_from = trip_2["address_to"]
    address_to = 'Г. Москва, 1-я Магистральная улица, д.2'
    time_from = randomize_time_from(trip_2["time_to"])
    kilometr_time = google_api(place_from=[address_from], places_to=[address_to], day=week_day, time=time_from)
    kilometr = kilometr_time[address_from][address_to]["distance"]
    time_delta = kilometr_time[address_from][address_to]["time"]
    return {
        'address_from': address_from,
        'address_to': address_to,
        'customer': 'ООО "ЭКОПЛЮС"',
        'km': kilometr,
        'time': time_delta,
        'time_from': time_from,
        'time_to': get_end_time(time_from, time_delta)
    }


def get_normalize_schedule(schedules, work_start, week_day):
    def b_time(trip):
        return int(trip[0]["time"].replace('-', ''))

    def o_time(trip):
        return int(trip["time"].replace('-', ''))

    customer_list = []
    for owner in schedules:
        schedules[owner].sort(key=o_time)
        customer_list.append(schedules[owner])
    customer_list.sort(key=b_time)
    schedules = []
    for i in range(len(customer_list)):
        if len(customer_list[i]) == 1:
            schedules.append(customer_list[i][0])
        else:
            for j in range(len(customer_list[i])):
                schedules.append(customer_list[i][j])
    new_schedules = []
    past_trip = {
        'address_from': None,
        'address_to': None,
        'customer': None,
        'km': None,
        'time': None,
        'time_from': None,
        'time_to': None
    }
    for i in range(len(schedules)):
        if i == 0:
            past_trip = from_base_custom(schedules[i], week_day, work_start)
            new_schedules.append(past_trip)
            past_trip = calculate_kilometr_time(schedules[i], week_day, past_trip["time_to"])
            new_schedules.append(past_trip)
            if len(schedules) == 1:
                past_trip = to_base_custom(past_trip, week_day)
                new_schedules.append(past_trip)
        elif i != len(schedules) - 1:
            if len(new_schedules) < 4:
                past_trip = b_a_custom(past_trip, schedules[i], week_day)
                new_schedules.append(past_trip)
                past_trip = calculate_kilometr_time(schedules[i], week_day, past_trip["time_to"])
                new_schedules.append(past_trip)
            else:
                pass
        else:
            past_trip = b_a_custom(past_trip, schedules[i], week_day)
            new_schedules.append(past_trip)
            past_trip = calculate_kilometr_time(schedules[i], week_day, past_trip["time_to"])
            new_schedules.append(past_trip)
            past_trip = to_base_custom(past_trip, week_day)
            new_schedules.append(past_trip)
    return new_schedules


def get_previous_day(date):
    dt1 = datetime.strptime(date, '%d.%m.%Y')
    dt1 = dt1 - dt.timedelta(days=1)
    previous_date = datetime.strftime(dt1, '%d.%m.%Y')
    return previous_date


def end_work(schedule, work_end, week_day):
    ok = None
    for i in range(len(schedule)):
        if int(schedule[i]['time_to'].replace('-', '')) < int(work_end.replace('-', '')):
            pass
        else:
            ok = i - 1
            if schedule[ok]["customer"] == 'ООО "ЭКОПЛЮС"':
                ok = ok - 1
                break
    if ok is not None:
        end_work_schedule = schedule[:ok+1]
        if len(end_work_schedule) == 0:
            return end_work_schedule
        fast_trip = to_base_custom(end_work_schedule[-1], week_day)
        if int(fast_trip["time_to"].replace('-', '')) > int(get_end_time(work_end, 60).replace('-', '')):
            if len(end_work_schedule) == 2:
                pass
            else:
                end_work_schedule = end_work_schedule[:-2]
                fast_trip = to_base_custom(end_work_schedule[-1], week_day)
        end_work_schedule.append(fast_trip)
    else:
        return schedule
    return end_work_schedule


def get_end_fuel_odometer(st_fuel, st_odometer, route, fuel_tank_capacity, fuel_rate):
    odometer_delta = 0
    for trip in route:
        odometer_delta += trip["km"]
    end_odometer = odometer_delta + st_odometer
    fuel_delta = int_r(odometer_delta / 100 * fuel_rate)
    end_fuel = st_fuel - fuel_delta
    this_refueling = 0
    if end_fuel < 0:
        this_refueling = fuel_tank_capacity - st_fuel
        end_fuel = fuel_tank_capacity - fuel_delta
    return {"end_fuel": end_fuel, "end_odometer": end_odometer, "refueling": this_refueling}


class Calculate:
    Property = False
    Input_File = os.getcwd() + '\\Dictionary\\translated\\{}\\{}.json'
    Calculated_Path = os.getcwd() + '\\calculator\\calculated\\{}\\'
    Calculated_File = Calculated_Path + '{}.json'
    Distance_Dict = os.getcwd() + '\\Dictionary\\distance.json'
    Start_Dict = os.getcwd() + '\\input\\start\\start.json'
    Distances = []
    Calculated_dict = {}
    work_start = None
    work_end = None

    def __init__(self, Month, Year, work_start, work_end):
        self.Input_File = self.Input_File.format(Year, Month)
        self.Calculated_Path = self.Calculated_Path.format(Year)
        self.Calculated_File = self.Calculated_File.format(Year, Month)
        self.Property = self.checking_for_availability()
        self.work_start = work_start
        self.work_end = work_end
        with open(self.Input_File, "r") as read_file:
            self.Calculated_dict = json.load(read_file)
        if self.Property:
            self.calculate()
            with open(self.Calculated_File, "w") as write_file:
                json.dump(self.Calculated_dict, write_file, indent=4)
            print("Calculated")

    def checking_for_availability(self):
        if os.path.isfile(self.Input_File):
            print('File for translate found')
            if os.path.isfile(self.Calculated_File):
                print('Calculated Input File found')
            else:
                try:
                    os.makedirs(self.Calculated_Path)
                    print('Translated Directory, created')
                except FileExistsError:
                    pass
                with open(self.Calculated_File, "w") as write_file:
                    json.dump({}, write_file)
                    print('Calculated File created')
            return True
        else:
            print("\033[31m {}".format('File not found, load translate data'))
            return False

    def calculate(self):
        for car in self.Calculated_dict:
            for i in range(len(self.Calculated_dict[car]["schedule"])):
                previous_customer = 'ООО "ЭКОПЛЮС"'
                individual_customers_trips = {}
                for j in range(len(self.Calculated_dict[car]["schedule"][i]["route"])):
                    if previous_customer == self.Calculated_dict[car]["schedule"][i]["route"][j]["customer"]:
                        try:
                            individual_customers_trips[
                                self.Calculated_dict[car]["schedule"][i]["route"][j]["customer"]].append(
                                self.Calculated_dict[car]["schedule"][i]["route"][j])
                        except KeyError:
                            individual_customers_trips[
                                self.Calculated_dict[car]["schedule"][i]["route"][j]["customer"]] = [
                                self.Calculated_dict[car]["schedule"][i]["route"][j]]
                    else:
                        previous_customer = self.Calculated_dict[car]["schedule"][i]["route"][j]["customer"]
                        individual_customers_trips[self.Calculated_dict[car]["schedule"][i]["route"][j]["customer"]] = [
                            self.Calculated_dict[car]["schedule"][i]["route"][j]]

                week_day = self.Calculated_dict[car]["schedule"][i]["week_day"]
                norm_schedule = end_work(get_normalize_schedule(individual_customers_trips, self.work_start, week_day), get_end_time(self.work_end, -1), week_day)
                self.Calculated_dict[car]["schedule"][i]["route"] = norm_schedule
                if i == 0:
                    end_fuel_odometer = get_end_fuel_odometer(self.Calculated_dict[car]["schedule"][i]["st_fuel"],
                                                              self.Calculated_dict[car]["schedule"][i]["st_odometer"],
                                                              self.Calculated_dict[car]["schedule"][i]["route"],
                                                              self.Calculated_dict[car]["fuel_tank_capacity"],
                                                              self.Calculated_dict[car]["fuel_rate"])
                    self.Calculated_dict[car]["schedule"][i]["end_fuel"] = end_fuel_odometer["end_fuel"]
                    self.Calculated_dict[car]["schedule"][i]["end_odometer"] = end_fuel_odometer["end_odometer"]
                    self.Calculated_dict[car]["schedule"][i]["refueling"] = end_fuel_odometer["refueling"]
                else:
                    self.Calculated_dict[car]["schedule"][i]["st_fuel"] = self.Calculated_dict[car]["schedule"][i-1]["end_fuel"]
                    self.Calculated_dict[car]["schedule"][i]["st_odometer"] = self.Calculated_dict[car]["schedule"][i-1]["end_odometer"]
                    end_fuel_odometer = get_end_fuel_odometer(self.Calculated_dict[car]["schedule"][i]["st_fuel"],
                                                              self.Calculated_dict[car]["schedule"][i]["st_odometer"],
                                                              self.Calculated_dict[car]["schedule"][i]["route"],
                                                              self.Calculated_dict[car]["fuel_tank_capacity"],
                                                              self.Calculated_dict[car]["fuel_rate"])
                    self.Calculated_dict[car]["schedule"][i]["end_fuel"] = end_fuel_odometer["end_fuel"]
                    self.Calculated_dict[car]["schedule"][i]["end_odometer"] = end_fuel_odometer["end_odometer"]
                    self.Calculated_dict[car]["schedule"][i]["refueling"] = end_fuel_odometer["refueling"]
        for car in self.Calculated_dict:
            for car_info in self.Calculated_dict[car]:
                if type(self.Calculated_dict[car][car_info]) is list:
                    for i in range(len(self.Calculated_dict[car][car_info])):
                        for day_info in self.Calculated_dict[car][car_info][i]:
                            if type(self.Calculated_dict[car][car_info][i][day_info]) is int:
                                self.Calculated_dict[car][car_info][i][day_info] = str(self.Calculated_dict[car][car_info][i][day_info])
                            elif type(self.Calculated_dict[car][car_info][i][day_info]) is list:
                                for j in range(len(self.Calculated_dict[car][car_info][i][day_info])):
                                    for trip in self.Calculated_dict[car][car_info][i][day_info][j]:
                                        if type(self.Calculated_dict[car][car_info][i][day_info][j][trip]) is int:
                                            self.Calculated_dict[car][car_info][i][day_info][j][trip] = str(self.Calculated_dict[car][car_info][i][day_info][j][trip])
                elif type(self.Calculated_dict[car][car_info]) is int:
                    self.Calculated_dict[car][car_info] = str(self.Calculated_dict[car][car_info])


def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print(a[:-2])


if __name__ == '__main__':
    main()