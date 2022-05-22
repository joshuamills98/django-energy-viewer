from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly


class GenerationMix:
    startDate: datetime
    endDate: datetime
    generationMix: pd.DataFrame

    def __init__(self, startDate: datetime, endDate: datetime, generationMix: pd.DataFrame) -> None:
        super().__init__()
        assert startDate < endDate, "Time sequence is not valid"
        self.startDate = startDate
        self.endDate = endDate
        assert generationMix.columns[0] == "fuel" and generationMix.columns[1] == "percentage", \
            "Columns not valid (should be fuel and percentage)"
        self.generationMix = generationMix

    def get_pie_chart_mix(self):
        fig = px.pie(self.generationMix, values="percentage", names="fuel",
                     title="Average energy mix for " + self.startDate.__str__() + " to " + self.endDate.__str__())
        graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")
        return fig, graph_div

    def __str__(self) -> str:
        return "From : " + self.startDate.__str__() + " to " + self.endDate.__str__() + "with the following energy " \
                                                                                        "breakdown " + "\n" + \
               self.generationMix.to_string()
