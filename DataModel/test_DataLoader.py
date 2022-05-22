from unittest import TestCase
from DataModel.Generation import Generation


class Test(TestCase):
    def test_generation(self):
        dl = Generation()
        start_time = "2018-01-20T12:00Z"
        end_time = "2018-01-20T12:30Z"
        gen_mix = dl.get_generation_mix(start_time, end_time)
        self.assertEqual(gen_mix.startDate.strftime("%Y-%m-%d"), "2018-01-20")

    def test_intensity(self):
        intensity = Intensity()
        result = intensity.get_intensity()
        self.assertEqual(type(result), float)