import json
from datetime import datetime
from os import listdir, path

from measurement import Day, Hour, Measurement, Index, Days

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
        self.dir = '/home/feynman/Documents/University/Przyrka/airData/data'
        self.data: Days = None

    def extract_files_data(self) -> list[Day]:
        output : list[Day]= []
        for filename in listdir(self.dir):
            if '.json' not in filename:
                continue
            raw_data = get_data(path.join(self.dir, filename))
            hist = raw_data['history']
            day = extract_day(hist)
            output.append(day)
        return output

    def run(self):
        self.data = Days()
        self.data.days = self.extract_files_data()

    
        
if __name__ == "__main__":
    app = App()
    app.run()
    print(app.data)
    # for item in app.data:
    #     for i in item.history:
    #         print(i.values)






    

    
        