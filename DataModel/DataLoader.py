from datetime import datetime
from enum import Enum

import requests


class DataType(Enum):
    generation = "generation",
    statistics = "statistics",
    intensity = "intensity"


class BaseLoader:
    base_url: str
    start_date: datetime = None
    end_date: datetime = None
    date_format: str = "%Y-%m-%dT%H:%MZ"

    def __init__(self, start_date: str = None, end_date: str = None) -> None:
        self.base_url = "https://api.carbonintensity.org.uk"
        if start_date is not None and end_date is not None:
            self.start_date = self.get_date_format(start_date)
            self.end_date = self.get_date_format(end_date)

    def __str__(self) -> str:
        return self.base_url

    def get_date_format(self, date: str):
        try:
            return datetime.strptime(date, self.date_format)
        except ValueError:
            print("Please use the correct date format = " + format)


class Intensity(BaseLoader):

    def __init__(self) -> None:
        super().__init__()
        self.base_url += "/" + DataType.intensity.name

    def get_intensity(self) -> float:
        if self.start_date is not None and self.end_date is not None:
            new_url = self.base_url + "/" + self.start_date.strftime(self.date_format) + "/" + self.end_date.strftime(
                self.date_format)
            r = requests.get(new_url).json()
        else:
            r = requests.get(self.base_url).json()
        return float(r["data"][0]["intensity"]["actual"])


class Statistics(BaseLoader):

    def __init__(self) -> None:
        super().__init__()
        self.base_url += "/" + DataType.statistics.name
