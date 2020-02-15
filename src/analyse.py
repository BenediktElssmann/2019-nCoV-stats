# -*- coding: utf-8 -*-

import json
import math
import matplotlib as mpl
mpl.use('PDF')
import matplotlib.pyplot as plt
import numpy as np


class Analyse(object):
    def __init__(self, orig_list=[], comp_list=[], data=None):
        if data is not None:
            self._infections = list(data.get_infection_numbers())
            self._deaths = list(data.get_death_numbers())
            self._dates = list(data.get_dates())

        elif len(orig_list) == len(comp_list):
            self._infections = orig_list
            self._deaths = comp_list
            self._data = None

        self._infections.sort()
        self._deaths.sort()

        self._infection_derivation = []
        self._death_derivation = []

        self._infection_factors = []
        self._death_factors = []
        self._factor_description = 0

    def calc_factors(self):
        for i in range(len(self._infections)-1):
            self._infection_factors.append(self._infections[i+1]/self._infections[i])
            self._death_factors.append(self._deaths[i+1]/self._deaths[i])

    def derive(self):
        for i in range(1, len(self._infections)-1):
            self._infection_derivation.append((self._infections[i+1] - self._infections[i-1])/2)
            self._death_derivation.append((self._deaths[i+1] - self._deaths[i-1]) / 2)

    def plot_defined(self):
        with open('/home/benedikt/PROJECTS/2019-nCoV-stats/data/diagrams.json',
                  'r', encoding='utf-8') as definition:
            diagrams = json.load(definition)

        for dia in diagrams:
            try:
                x = self._get_data(dia["x_axis"])
                y = self._get_data(dia["y_axis"])

                if len(y) > len(x):
                    print(">>> Somethin' wrong here, I guess. <<<")

                elif len(x) > len(y):
                    x = x[math.floor((len(x) - len(y))/2):-math.ceil((len(x) - len(y))/2)]

                x_label = dia["x_description"]
                y_label = dia["y_description"]
                title = dia["title"]

                if "per_cent" in dia:
                    per_cent = dia["per_cent"]
                else:
                    per_cent = False

                self._plot_values(x, y, x_label, y_label, title, per_cent=per_cent)

            except KeyError as e:
                print(e)

    def _get_data(self, name):
        if name == "date":
            return self._dates
        if name == "infections":
            return self._infections
        if name == "deaths":
            return self._deaths
        if name == "infection-increase":
            return self._infection_factors
        if name == "death-increase":
            return self._death_factors
        if name == "infection-derivation":
            return self._infection_derivation
        if name == "death-derivation":
            return self._death_derivation
        raise KeyError(name + " is not a permitted key.")

    @staticmethod
    def _plot_values(x_values, y_values, x_label, y_label, title, optimum=None, per_cent=False):
        x = x_values
        y = y_values

        if per_cent:
            y = list(map(lambda l: (l-1)*100, y))

        plt.style.use('ggplot')

        fig, ax = plt.subplots(figsize=(6, 4))
        plt.stem(x, y, use_line_collection=True)

        labels = ax.get_xticklabels()
        plt.setp(labels, rotation=60, horizontalalignment='right')
        ax.set(xlabel=x_label, ylabel=y_label,
               title=title)

        if optimum is not None:
            ax.axhline(optimum, ls=':', color='r')
        plt.tight_layout()

        fig.savefig('/home/benedikt/PROJECTS/2019-nCoV-stats/analysis/' + title.replace(' ', '-') + '.pdf')

        del fig, ax

