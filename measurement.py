from datetime import timedelta, date
import numpy as np
import matplotlib.pyplot as plt

plt.xkcd()

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
        self.starting_hour: timedelta = None
        self.values: list[Measurement] = []
        self.index: Index = None

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
            output[key] = np.array(output[key])
        return output
        
                

    
    def mean(self):
        return self.np_values().mean()

    def __repr__(self) -> str:
        return f"Data of day: {self.date}"

class Days:
    def __init__(self) -> None:
        self.days: list[Day] = []

    def make_dict(self) -> dict:
        output = {}
        for key in self.days[0].make_dict().keys():
            output[key] = []
            for d in self.days:
                output[key].append(d.make_dict()[key].mean())
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

    