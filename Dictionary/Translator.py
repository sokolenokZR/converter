import json
import os
from datetime import datetime


def time(route):
    return int(route["time"].split('-')[0] + route["time"].split('-')[1])


def day(days):
    return int(days['date'].split('.')[0])


def get_past_month(Month, Year):
    if Month == 'jan':
        return [str(int(Year) - 1), 'dec']
    else:
        if Month == 'feb':
            return [Year, 'jan']
        elif Month == 'mar':
            return [Year, 'feb']
        elif Month == 'apr':
            return [Year, 'mar']
        elif Month == 'may':
            return [Year, 'apr']
        elif Month == 'jun':
            return [Year, 'may']
        elif Month == 'jul':
            return [Year, 'jun']
        elif Month == 'oug':
            return [Year, 'jul']
        elif Month == 'sep':
            return [Year, 'oug']
        elif Month == 'oct':
            return [Year, 'sep']
        elif Month == 'nov':
            return [Year, 'oct']
        elif Month == 'dec':
            return [Year, 'nov']


def get_day_of_week_by_date(date):
    date_obj = datetime.strptime(date, '%Y.%m.%d')
    day = date_obj.weekday() + 1
    if day == 7:
        return "Sunday"
    elif day == 1:
        return "Monday"
    elif day == 2:
        return "Tuesday"
    elif day == 3:
        return "Wednesday"
    elif day == 4:
        return "Thursday"
    elif day == 5:
        return "Friday"
    elif day == 6:
        return "Saturday"


def get_ru_month(date):
    date_obj = datetime.strptime(date, '%Y.%m.%d')
    month = date_obj.month
    if month == 1:
        return "Января"
    elif month == 2:
        return "Февраля"
    elif month == 3:
        return "Марта"
    elif month == 4:
        return "Апреля"
    elif month == 5:
        return "Мая"
    elif month == 6:
        return "Июня"
    elif month == 7:
        return "Июля"
    elif month == 8:
        return "Августа"
    elif month == 9:
        return "Сентября"
    elif month == 10:
        return "Октября"
    elif month == 11:
        return "Ноября"
    elif month == 12:
        return "Декабря"


def get_year(date):
    date_obj = datetime.strptime(date, '%Y.%m.%d')
    year = date_obj.year
    return year


def get_day(date):
    date_obj = datetime.strptime(date, '%Y.%m.%d')
    day = date_obj.day
    return day


def reformat(date):
    date_obj = datetime.strptime(date, '%Y.%m.%d')
    reformat_date = date_obj.strftime('%d.%m.%Y')
    return reformat_date


class Translate:
    Property = False
    Input_File = os.getcwd() + '\\Exporter\\exported_input\\{}\\{}.json'
    Start_Calculated_Data_Path = os.getcwd() + '\\calculator\\calculated\\{}\\{}.json'
    Start_Input_Data_Path = os.getcwd() + '\\input\\start\\start.json'
    Translated_Path = os.getcwd() + '\\Dictionary\\translated\\{}\\'
    Translated_File = Translated_Path + '{}.json'
    Address_Dict = os.getcwd() + '\\Dictionary\\address.json'
    Cars_Dict = os.getcwd() + '\\Dictionary\\cars.json'
    Distance_Dict = os.getcwd() + '\\Dictionary\\distance.json'
    Owners_Dict = os.getcwd() + '\\Dictionary\\owners.json'
    Specifications_Dict = os.getcwd() + '\\Dictionary\\specifications.json'
    Customers_Dict = os.getcwd() + '\\Dictionary\\customers.json'
    availability_Start_Data = False
    Month = None
    Year = None
    Distances = []

    def __init__(self, Month, Year):
        self.Month = Month
        self.Year = Year
        self.Input_File = self.Input_File.format(Year, Month)
        self.Translated_Path = self.Translated_Path.format(Year)
        self.Translated_File = self.Translated_File.format(Year, Month)
        self.Property = self.checking_for_availability()
        if self.Property:
            self.tranlation()

    def checking_for_availability(self):
        previous_month = get_past_month(self.Month, self.Year)
        if os.path.isfile(self.Start_Calculated_Data_Path.format(previous_month[0], previous_month[1])):
            self.Start_Calculated_Data_Path = self.Start_Calculated_Data_Path.format(previous_month[0], previous_month[1])
            self.availability_Start_Data = True
        if os.path.isfile(self.Input_File):
            print('File for translate found')
            if os.path.isfile(self.Translated_File):
                print('Translated Input File found')
            else:
                try:
                    os.makedirs(self.Translated_Path)
                    print('Translated Directory, created')
                except FileExistsError:
                    pass
                with open(self.Translated_File, "w") as write_file:
                    json.dump({}, write_file)
                    print('Translated File created')
            return True
        else:
            print("\033[31m {}".format('File not found, load export data'))
            return False

    def get_start_data(self, car):
        if self.availability_Start_Data:
            with open(self.Start_Calculated_Data_Path, 'r') as read_file:
                start_data = json.load(read_file)
                try:
                    st_odometer = int(start_data[car]["schedule"][-1]["end_odometer"])
                    st_fuel = int(start_data[car]["schedule"][-1]["end_fuel"])
                except KeyError:
                    with open(self.Start_Input_Data_Path, 'r') as read_file:
                        start_data = json.load(read_file)
                    try:
                        return start_data[car]
                    except KeyError:
                        print('\033[33m Enter a start data for "{}":'.format(car))
                        print("\033[33m Enter a st_fuel for {}:".format(car))
                        st_fuel = int(input())
                        print("\033[33m Enter a st_odometer for {}:".format(car))
                        st_odometer = int(input())
                        start_data[car] = {"st_fuel": st_fuel, "st_odometer": st_odometer}
                        with open(self.Start_Input_Data_Path, "w") as write_file:
                            json.dump(start_data, write_file, indent=4)
                        return {"st_fuel": st_fuel, "st_odometer": st_odometer}
                return {"st_fuel": st_fuel, "st_odometer": st_odometer}
        else:
            with open(self.Start_Input_Data_Path, 'r') as read_file:
                start_data = json.load(read_file)
            try:
                return start_data[car]
            except KeyError:
                print('\033[33m Enter a start data for "{}":'.format(car))
                print("\033[33m Enter a st_fuel for {}:".format(car))
                st_fuel = int(input())
                print("\033[33m Enter a st_odometer for {}:".format(car))
                st_odometer = int(input())
                start_data[car] = {"st_fuel": st_fuel, "st_odometer": st_odometer}
                with open(self.Start_Input_Data_Path, "w") as write_file:
                    json.dump(start_data, write_file, indent=4)
                return {"st_fuel": st_fuel, "st_odometer": st_odometer}

    def tranlation(self):
        translated_trips = {}
        with open(self.Input_File, "r") as read_file:
            trips = json.load(read_file)
        for car in trips.keys():
            translated_car = self.get_value("cars", car)
            specification = self.get_value("specifications", translated_car["brand"])
            translated_trips[translated_car["license_plate"]] = {"license_plate": translated_car["license_plate"],
                                                                 "brand": translated_car["brand"],
                                                                 "owner": translated_car["owner"],
                                                                 "legal_address": self.get_value("owners", translated_car["owner"]),
                                                                 "fuel_rate": specification["fuel_rate"],
                                                                 "fuel_tank_capacity": specification["fuel_tank_capacity"],
                                                                 "schedule": []
                                                                 }
            for date in trips[car].keys():
                new_day = {"date": reformat(date),
                           "week_day": get_day_of_week_by_date(date),
                           "day": get_day(date),
                           "month": get_ru_month(date),
                           "year": get_year(date),
                           "st_odometer": self.get_start_data(translated_car["license_plate"])["st_odometer"],
                           "end_odometer": None,
                           "st_fuel": self.get_start_data(translated_car["license_plate"])["st_fuel"],
                           "refueling": None,
                           "end_fuel": None,
                           "route": []
                           }
                for place in trips[car][date]:
                    route = {"address_from": self.get_value("address", place["customers_address"]),
                             "address_to": self.get_value("address", place["upload_address"]),
                             "customer": self.get_value("customers", place["customer"]),
                             "time_from": None,
                             "time_to": None,
                             "km": None,
                             "time": place["time"]
                             }
                    new_day["route"].append(route)
                translated_trips[translated_car["license_plate"]]["schedule"].append(new_day)
        with open(self.Translated_File, "w") as write_file:
            json.dump(translated_trips, write_file, indent=4)
        print("Translation is over")

    def get_value(self, Dictionary, key):
        dictionary = None
        if Dictionary == 'address':
            with open(self.Address_Dict, "r") as read_file:
                dictionary = json.load(read_file)
        elif Dictionary == 'cars':
            with open(self.Cars_Dict, "r") as read_file:
                dictionary = json.load(read_file)
        elif Dictionary == 'owners':
            with open(self.Owners_Dict, "r") as read_file:
                dictionary = json.load(read_file)
        elif Dictionary == 'specifications':
            with open(self.Specifications_Dict, "r") as read_file:
                dictionary = json.load(read_file)
        elif Dictionary == 'customers':
            with open(self.Customers_Dict, "r") as read_file:
                dictionary = json.load(read_file)
        else:
            print('\033[31m dictionary {} is not default'.format(Dictionary))
            return None
        try:
            return dictionary[key]
        except KeyError:
            print('\033[33m Input the data for "{}"'.format(Dictionary))
            return self.put_value(Dictionary, dictionary, key)

    def put_value(self, Dictionary, dictionary, key):
        if Dictionary == 'address':
            print('\033[33m Enter a normal address for "{}":'.format(key))
            dictionary[key] = input()
            with open(self.Address_Dict, "w") as write_file:
                json.dump(dictionary, write_file, indent=4)
            return dictionary[key]
        elif Dictionary == 'cars':
            print('\033[33m Enter a normal license_plate for "{}":'.format(key))
            license_plate = input()
            print("\033[33m Enter a brand for {}:".format(key))
            brand = input()
            print("\033[33m Enter a owner for {}:".format(key))
            owner = input()
            dictionary[key] = {"license_plate": license_plate,
                               "brand": brand,
                               "owner": owner}
            with open(self.Cars_Dict, "w") as write_file:
                json.dump(dictionary, write_file, indent=4)
            return dictionary[key]
        elif Dictionary == 'customers':
            print('\033[33m Enter a normal customer_name for "{}":'.format(key))
            dictionary[key] = input()
            with open(self.Customers_Dict, "w") as write_file:
                json.dump(dictionary, write_file, indent=4)
            return dictionary[key]
        elif Dictionary == 'owners':
            print('\033[33m Enter a legal address for "{}":'.format(key))
            legal_address = input()
            dictionary[key] = legal_address
            with open(self.Owners_Dict, "w") as write_file:
                json.dump(dictionary, write_file, indent=4)
            return dictionary[key]
        elif Dictionary == 'specifications':
            print('\033[33m Enter a fuel_rate for "{}":'.format(key))
            fuel_rate = int(input())
            print('\033[33m Enter a fuel_tank_capacity for "{}":'.format(key))
            fuel_tank_capacity = int(input())
            dictionary[key] = {}
            dictionary[key]["fuel_rate"] = fuel_rate
            dictionary[key]["fuel_tank_capacity"] = fuel_tank_capacity
            with open(self.Specifications_Dict, "w") as write_file:
                json.dump(dictionary, write_file, indent=4)
            return dictionary[key]

    def __str__(self):
        return self.Address_Dict


def main():
    print(get_day("2021.02.03"))
    print(get_ru_month("2021.02.03"))
    print(get_year("2021.02.03"))


if __name__ == '__main__':
    main()