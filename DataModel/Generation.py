from datetime import datetime

import pandas as pd
import requests

from DataModel.DataLoader import BaseLoader, DataType
from DataModel.GenerationMix import GenerationMix


class Generation(BaseLoader):

    def __init__(self, start_date = None, end_date = None) -> None:
        super().__init__(start_date=start_date, end_date=end_date)
        self.base_url += "/" + DataType.generation.name

    def __call__(self):
        return self.get_generation_mix()

    def get_generation_mix(self) -> GenerationMix:
        # Extract the information
        if self.start_date is None or self.end_date is None:
            r = requests.get(self.base_url).json()
            generation_mix = self.get_individual_period_energy_mix(r)
        else:
            try:
                new_url = self.base_url + "/" + self.start_date.strftime(self.date_format) + "/" + self.end_date.strftime(self.date_format)
                print(new_url)
                r = requests.get(new_url).json()
            except ValueError:
                print("incorrectly formatted return string it should be YYYY-MM-DDThh:mmZ e.g. 2017-08-25T12:35Z")
            generation_mix = self.get_aggregate_mix(r)
        return generation_mix

    def get_aggregate_mix(self, r) -> GenerationMix:
        """
        Return an average power generation mix over a given time frame
        :param r:
        :return:
        """
        fuel_table = {}
        for period in r["data"]:
            for fuel_percentage_set in period["generationmix"]:
                if fuel_percentage_set["fuel"] in fuel_table:
                    fuel_table[fuel_percentage_set["fuel"]] += fuel_percentage_set["perc"]
                else:
                    fuel_table[fuel_percentage_set["fuel"]] = 0  # create a new value in fuel_table set
        fuel_table = {k: v / sum(fuel_table.values()) * 100 for k, v in fuel_table.items()}  # Get average
        df = pd.DataFrame.from_dict(fuel_table, columns=["fuel"], orient="index").reset_index().rename(
            columns={"fuel": "percentage", "index": "fuel"})
        return GenerationMix(self.start_date, self.end_date, df)

    def get_individual_period_energy_mix(self, r):
        start_date = datetime.strptime(r["data"]["from"], "%Y-%m-%dT%H:%MZ")
        end_date = datetime.strptime(r["data"]["to"], "%Y-%m-%dT%H:%MZ")
        generation_mix = []
        for generationType in r["data"]["generationmix"]:
            fuel = generationType["fuel"]
            percentage = generationType["perc"]
            generation_mix.append([fuel, percentage])
        df = pd.DataFrame(data=generation_mix, columns=["fuel", "percentage"])
        generation_mix = GenerationMix(start_date, end_date, df)
        return generation_mix

if __name__ == "__main__":
    start_time = "2019-01-20T12:00Z"
    end_time = "2019-01-20T12:30Z"
    dl = Generation()

    gen_mix = dl.get_generation_mix()
    img, code = gen_mix.get_pie_chart_mix()
    img.show()