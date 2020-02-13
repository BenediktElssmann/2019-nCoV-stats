# -*- coding: utf-8 -*-

import json
import datetime


class Vir(object):
    def __init__(self):
        self._infections = {}
        self._deaths = {}

        self.read_infections()
        self.read_deaths()

    def add_day(self, new_day, infections, deaths):
        if new_day in self._infections:
            return False

        for date in self._infections:
            if date > new_day:
                if self._infections[date] < infections or self._deaths[date] < deaths:
                    return False
            if date < new_day:
                if self._infections[date] > infections or self._deaths[date] > deaths:
                    return False

        self._infections[new_day] = infections
        self._deaths[new_day] = deaths

        return True

    def read_infections(self):
        with open('/home/benedikt/PROJECTS/2019-nCoV-stats/data/infections.json', 'r', encoding='utf-8') as raw_data:
            data = json.load(raw_data)
            print(data)

        for date in data:
            self._infections[datetime.date.fromisoformat(date)] = data[date]

    def read_deaths(self):
        with open('/home/benedikt/PROJECTS/2019-nCoV-stats/data/deaths.json', 'r', encoding='utf-8') as raw_data:
            data = json.load(raw_data)

        for date in data:
            self._deaths[datetime.date.fromisoformat(date)] = data[date]

    def write_infections(self):
        with open('/home/benedikt/PROJECTS/2019-nCoV-stats/data/infections.json', 'w', encoding='utf-8') as raw_data:
            json.dump(self.format_date(self._infections), raw_data, indent=2)

    def write_deaths(self):
        with open('/home/benedikt/PROJECTS/2019-nCoV-stats/data/deaths.json', 'w', encoding='utf-8') as raw_data:
            json.dump(self.format_date(self._deaths), raw_data, indent=2)

    @staticmethod
    def format_date(unformated):
        result = {}
        for date in unformated:
            result[date.isoformat()] = unformated[date]
        return result

    def get_infection_numbers(self):
        return self._infections.values()

    def get_death_numbers(self):
        return self._deaths.values()

    def get_dates(self):
        return self._infections.keys()

    def __str__(self):
        infections = self.format_date(self._infections)
        deaths = self.format_date(self._deaths)

        result = 'Date: Infections |\t Deaths:\n'

        for date in infections:
            result += date + ': ' + str(infections[date]) + ' |\t' + str(deaths[date]) + '\n'

        return result

    def __del__(self):
        self.write_infections()
        self.write_deaths()
