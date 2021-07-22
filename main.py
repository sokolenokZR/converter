from Exporter.xls_json import Export
from Dictionary.Translator import Translate
from Calculator.calculator import Calculate
from Output.docks_creator import Create


def main():
    Year = 2021
    Month = "jun"
    work_time_start = '09-00'
    work_time_end = '19-00'
    Export(Month, Year)
    Translate(Month, Year)
    Calculate(Month, Year, work_time_start, work_time_end)
    Create(Month, Year)


if __name__ == '__main__':
    main()
