from datetime import timedelta, date, datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.xkcd()

HEADERS = [
    "TIME",
    "PM1",
    "PM25",
    "PM10",
    "PRESSURE",
    "HUMIDITY",
    "TEMPERATURE",
    "NO2",
    "O3"
]


def merge_dict(dict1: dict, dict2: dict) -> dict:
    output = dict1
    for key in dict2.keys():
        output[key] += dict2[key]
    return output



class Info:
    def __init__(self, data: dict = None) -> None:
        self.data = data
        self.time: datetime = None
        self.pm1: float = None
        self.pm25: float = None
        self.pm10: float = None
        self.pressure: float = None
        self.humidity: float = None
        self.temperature: float = None
        self.no2: float = None
        self.o3: float = None

    def set_data(self) -> None:
        self.time = self.data.get('TIME')
        self.pm1 = self.data.get('PM1')
        self.pm25 = self.data.get('PM25')
        self.pm10 = self.data.get('PM10')
        self.pressure = self.data.get('PRESSURE')
        self.humidity = self.data.get('HUMIDITY')
        self.temperature = self.data.get('TEMPERATURE')
        self.no2 = self.data.get('NO2')
        self.o3 = self.data.get("O3")

    def get_data(self) -> None:
        for i, item in enumerate([self.time, self.pm1, self.pm25, self.pm10, self.pressure, self.humidity, self.temperature, self.no2, self.o3]):
            self.data[HEADERS[i]] = item

    # def __add__(self, other) -> dict:
    #     if not self.data:
    #             self.get_data()
    #     if isinstance(other, Info):

    #         if not other.data:
    #             other.get_data()
    #         return merge_dict(self.data, other.data)
    #     if isinstance(other, dict):
    #         return merge_dict(self.data, other)
        

        
class Infos:
    def __init__(self, data: list[Info]) -> None:
        self.data = data
    
    def get_table(self) -> pd.DataFrame:
        output = {}
        for h in HEADERS:
            output[h] = []
        for info in self.data:
            for i, item in enumerate([info.time, info.pm1, info.pm25, info.pm10, info.pressure, info.humidity, info.temperature, info.no2, info.o3]):
                output[HEADERS[i]] += [item]
        output = pd.DataFrame(output)
        output.set_index("TIME", inplace=True)
        return output
    
    def __add__(self, other):
        return Infos(self.data + other.data)





class Index:
    def __init__(self) -> None:
        self.name = None
        self.value = None
        self.level = None
        self.description = None
        self.advice = None
        self.color = None


class Measurement:
    def __init__(self, name: str, value: float) -> None:
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"


class Hour:
    def __init__(self) -> None:
        self.starting_hour: datetime = None
        self.values: list[Measurement] = []
        self.index: Index = None

    def make_info(self) -> Info:
        output = {}
        for m in self.values:
            output[m.name] = m.value
        return Info(output)

    def make_dict(self) -> dict:
        output = {}
        for value in self.values:
            output[value.name] = value.value
        return output

    def __repr__(self) -> str:
        return f"{self.starting_hour} -> {self.starting_hour+timedelta(minutes=60)}"


class Day:
    def __init__(self) -> None:
        self.date = date.today()
        self.history: list[Hour] = []

    def make_dict(self) -> dict:
        output = {}
        for key in self.history[0].make_dict().keys():
            output[key] = []
            for h in self.history:
                add = h.make_dict().get(key)

                if add:
                    output[key].append(h.make_dict()[key])
                else:
                    output[key].append(None)
            output[key] = np.array(output[key])
        return output

    def make_infos(self):
        output = [h.make_info() for h in self.history]
        return Infos(output)
        


    def mean(self):
        return self.np_values().mean()

    def __repr__(self) -> str:
        return f"Data of day: {self.date}"


class Days:
    def __init__(self) -> None:
        self.days: list[Day] = []
        self.table: pd.DataFrame = None

    def get_times(self) -> list[datetime]:
        output: list[datetime] = []
        for day in self.days:
            output += [h.starting_hour for h in day.history]
        return output

    def get_infos(self) -> Infos:
        output: Infos = None
        for d in self.days:
            if not output:
                output = d.make_infos()
                continue
            output = output + d.make_infos()
        return output

    def make_table(self) -> pd.DataFrame:
        output = self.get_infos()
        return output.get_table()
        # d = self.make_dict()
        # for _, item in d.items():
        #     print(len(item))
        # output = pd.DataFrame(self.make_dict())
        # # output.index = self.get_times()
        # return output

    def get_csv(self, filename: str) -> None:
        self.make_table().to_csv(filename)

    def info(self):
        if self.table is None:
            self.table = self.make_table()
        print(self.table.info())

    def plot(self, x, y):
        plt.scatter(self.table[x], self.table[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.tight_layout()
        plt.show()

    def make_dict(self) -> dict:
        output = {}
        for key in self.days[0].make_dict().keys():
            output[key] = []
            for d in self.days:
                if key in d.make_dict().keys():
                    output[key] += list(d.make_dict()[key])
            output[key] = np.array(output[key])
        return output

    def make_plot(self, key: str) -> None:
        my_dict = self.make_dict()
        print(my_dict)
        plt.bar(range(len(my_dict[key])), my_dict[key])
        plt.title(key)
        plt.xlabel("Time [days]")
        plt.ylabel("")
        plt.show()

    def make_plots(self):
        for key in self.make_dict().keys():
            self.make_plot(key)

    def __repr__(self) -> str:
        return f"Set of data from {len(self.days)} days"
