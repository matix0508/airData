from datetime import timedelta, date

class Index:
    def __init__(self) -> None:
        self.name = None
        self.value = None
        self.level = None
        self.description = None
        self.advice = None
        self.color = None

class Measurement:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"{self.name}: {self.value}"

class Hour:
    def __init__(self) -> None:
        self.starting_hour = None
        self.values = []
        self.index = None


    def __repr__(self) -> str:
        return f"{self.starting_hour} -> {self.starting_hour+timedelta(minutes=60)}"

class Day:
    def __init__(self) -> None:
        self.date = date.today()
        self.history = []

    def __repr__(self) -> str:
        return f"Data of day: {self.date}"

    