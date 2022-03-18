import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt


def crossings_in_year(year): 
    df = pd.read_csv("Border_Crossing_Entry_Data.csv", parse_dates=["Date"], infer_datetime_format=True)
    people_condition = df["Measure"].isin(["Personal Vehicle Passengers", "Bus Passengers", "Pedestrians"])
    date_condition = df["Date"].dt.year == year 
    totals = df[date_condition] 
    totals = totals[people_condition]

    return totals["Value"].sum()


def plot_date_vs_people(fname): 
    df = pd.read_csv("Border_Crossing_Entry_Data.csv", parse_dates=["Date"], infer_datetime_format=True)
    people = df.loc[df["Measure"].isin(["Personal Vehicle Passengers", "Bus Passengers", "Pedestrians"])]
    dates = df["Date"][people.index]
    people = people.join(dates, rsuffix="_")

    totals = people.groupby("Date_")["Value"].sum()

    totals.plot()
    plt.xlabel("Date")
    plt.ylabel("People")
    plt.title("Total Crossing By Month")
    plt.grid()
    plt.savefig(fname)


def main(): 
    plot_date_vs_people("date_vs_people.png")
    print(crossings_in_year(2021))


if __name__ == '__main__': 
    main()