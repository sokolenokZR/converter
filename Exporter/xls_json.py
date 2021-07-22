import json
import os
import pandas


class Export:
    Propriety = False
    Year = None
    Month = None
    Project_Path = os.getcwd().split('\\')
    Input_Dir = None
    Input_File = None
    Exported_Input_Dir = None
    Exported_Input_File = None

    def __init__(self, Month, Year):
        self.Year = str(Year)
        self.Month = str(Month).lower()
        self.Input_Dir = '\\'.join(self.Project_Path) + '\\' + 'input' + '\\' + self.Year + '\\'
        self.Input_File = self.Input_Dir + self.Month + '.xlsx'
        self.Exported_Input_Dir = '\\'.join(
            self.Project_Path) + '\\' + 'Exporter\\exported_input' + '\\' + self.Year + '\\'
        self.Exported_Input_File = self.Exported_Input_Dir + self.Month + '.json'
        self.Propriety = self.checking_for_availability()
        if self.Propriety:
            self.Export_to_json()

    def __str__(self):
        return self.Exported_Input_File

    def checking_for_availability(self):
        if os.path.isfile(self.Input_File):
            print('Input File found')
            if os.path.isfile(self.Exported_Input_File):
                print('Exported File found')
            else:
                try:
                    os.makedirs(self.Exported_Input_Dir)
                    print('Directory, created')
                except FileExistsError:
                    pass
                with open(self.Exported_Input_File, "w") as write_file:
                    json.dump({}, write_file)
                    print('Exported File created')
            return True
        else:
            print("\033[31m {}".format('File not found, load input data'))
            return False

    def Export_to_json(self):
        excel_data_df = pandas.read_excel(self.Input_File, sheet_name='Лист1')
        customers = excel_data_df['ЗАКАЗЧИК'].tolist()
        customers_addresses = excel_data_df['АДРЕС'].tolist()
        cars = excel_data_df['МАШИНА'].tolist()
        dates = excel_data_df['Дат+L2а выполнения'].tolist()
        times = excel_data_df['время'].tolist()
        upload_addresses = excel_data_df['ВЫГРУЗКА'].tolist()
        exported_json = {}
        for i in range(len(cars)):
            car_name = str(cars[i]).replace(' прицеп', '')
            date = str(dates[i])[:-9].replace("-", ".")
            time = str(times[i])[:-3].replace(":", "-")
            customer = str(customers[i])
            if "ИП " in customer:
                continue
            customers_address = str(customers_addresses[i])
            upload_address = str(upload_addresses[i])
            if car_name not in exported_json.keys():
                exported_json[car_name] = {}
                exported_json[car_name][date] = []
                exported_json[car_name][date].append({})
                exported_json[car_name][date][-1]["time"] = time
                exported_json[car_name][date][-1]["customer"] = customer
                exported_json[car_name][date][-1]["customers_address"] = customers_address
                exported_json[car_name][date][-1]["upload_address"] = upload_address
            else:
                if date not in exported_json[car_name]:
                    exported_json[car_name][date] = []
                    exported_json[car_name][date].append({})
                    exported_json[car_name][date][-1]["time"] = time
                    exported_json[car_name][date][-1]["customer"] = customer
                    exported_json[car_name][date][-1]["customers_address"] = customers_address
                    exported_json[car_name][date][-1]["upload_address"] = upload_address
                else:
                    if time in [event["time"] for event in exported_json[car_name][date]]:
                        continue
                    else:
                        exported_json[car_name][date].append({})
                        exported_json[car_name][date][-1]["time"] = time
                        exported_json[car_name][date][-1]["customer"] = customer
                        exported_json[car_name][date][-1]["customers_address"] = customers_address
                        exported_json[car_name][date][-1]["upload_address"] = upload_address
        with open(self.Exported_Input_File, "w") as write_file:
            json.dump(exported_json, write_file, indent=4)
        print('Exported Input File filled')
