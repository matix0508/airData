import json
from datetime import datetime
from os import listdir

from measurement import Day, Hour, Measurement, Index

def extract_index(data: dict) -> Index:
    output = Index()
    output.name = data['name']
    output.value = data['value']
    output.level = data['level']
    output.description = data['description']
    output.advice = data['advice']
    output.color = data['color']
    return output

def extract_hour(hour: dict) -> Hour:
    output = Hour()
    output.starting_hour = datetime.strptime(hour['fromDateTime'][:-5], '%Y-%m-%dT%H:%M:%S')
    for value in hour['values']:
        m = Measurement(value['name'], value['value'])
        output.values.append(m)
    output.index = extract_index(hour['indexes'][0])
    return output
    

def extract_day(hours: list) -> Day:
    day = Day()
    for item in hours:
        hour = extract_hour(item)
        day.history.append(hour)
    return day

def get_data(filename: str) -> dict:
    with open(filename) as f:
        return json.loads(f.read())



class App:
    def __init__(self) -> None:
        self.dir = '/home/wleklinski/Documents/Study/Semestr5/Przyrka/Projekt/airData'
        self.data = []

    def extract_files_data(self) -> list[Day]:
        output = []
        for filename in listdir(self.dir):
            if '.json' not in filename:
                continue
            raw_data = get_data(filename)
            hist = raw_data['history']
            day = extract_day(hist)
            output.append(day)
        return output

    def run(self):
        self.data = self.extract_files_data()

    def __repr__(self) -> str:
        return f"Set of data from {len(self.data)} days"
        
if __name__ == "__main__":
    app = App()
    app.run()
    print(app)
    # for item in app.data:
    #     for i in item.history:
    #         print(i.values)






    

    
        