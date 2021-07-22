import json
from pprint import pprint
import os


def reformating_json(json_file):
    with open(json_file, "r") as read_file:
        information = json.load(read_file)
    information["Пятницкое шоссе"] = "МО, ГО Красногорск, пос. Отрадное"
    information["Красногорск"] = "МО, ГО Красногорск, пос. Отрадное"
    information["Залинейный переулок"] = "Г. Москва, Залинейный переулок, д.10А, стр.1"
    information["шереметьево антис 17 ( зеленый зона )   КПП 12"] = "МО, аэропорт Шереметьево"
    information["дер. Хлыново"] = "МО, ГО Раменский, дер. Хлыново"
    with open(json_file, "w") as write_file:
        json.dump(information, write_file, indent=4)


def main():
    reformating_json('address.json')


if __name__ == '__main__':
    main()