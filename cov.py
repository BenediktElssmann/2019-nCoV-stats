#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import datetime
from src.analyse import Analyse
from src.data import Vir


parser = argparse.ArgumentParser()

parser.add_argument("--date",
                    help="date in format YYYY-MM-DD (not needed if it's today)")

parser.add_argument("--infections",
                    help="number of infections with 2019-nCoV today")

parser.add_argument("--deaths",
                    help="number of deaths from 2019-nCoV today")

parser.add_argument("--plot",
                    help="ploting values (results in analysis)",
                    action="store_true")

args = parser.parse_args()


if __name__ == '__main__':
    data = Vir()
    analyse = Analyse(data=data)
    analyse.calc_factors()
    analyse.derive()

    if args.infections is not None and args.deaths is not None:
        if args.date is None:
            date = datetime.date.today()
        else:
            try:
                date = datetime.date.fromisoformat(args.date)
            except ValueError as e:
                print("A wild error appeared while parsing the date.\n\n")
                print(e)

        try:
            infections = int(args.infections)
            deaths = int(args.deaths)

            data.add_day(date, infections, deaths)

        except ValueError as e:
            print("A wild error appeared while parsing the infections or deaths value.\n\n")
            print(e)

    if args.plot is True:
        analyse.plot_defined()

    del analyse, data
