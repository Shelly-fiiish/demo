# ================
# Imports
# ================

import os
import pdb
import math
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import dates
from matplotlib.ticker import MaxNLocator
from matplotlib import rc
import datetime
import statistics
import scipy.signal as sig


# Temperature & Doser plot in whole range for overview
def DIVA_Plot(df, Export_Path):
    x = df["Zeit"]
    y1 = df["T204RI"]
    y2 = df["Dosierer"]

    fig, ax = plt.subplots(1, figsize=(7, 5))

    ax.plot(x, y1, color="red", label=r"Temperature")
    ax2 = ax.twinx()
    ax2.plot(x, y2, color="blue", label=r"Doser Speed")

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=400, top=750)
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperatur in degree C")
    ax.set_title("Temp & Doser in DIVA")
    ax.legend(bbox_to_anchor=(0.03, 0.85), loc="lower left")
    ax2.legend(bbox_to_anchor=(0.03, 0.78), loc="lower left")

    ax2.set_ylabel("Doser speed in %")

    # Plot anzeigen
    # plt.show()


# Average temperature & Doser plot in sliced range
def DIVA_Plot2(df_Temp, df_Doser, Export_Path):
    x = df_Temp["Zeit"]

    y1 = df_Temp.mean(1)
    y2 = df_Doser["Dosierer"]

    fig, ax = plt.subplots(1, figsize=(7, 5))

    ax.plot(x, y1, color="red", label=r"Temperature")
    ax2 = ax.twinx()
    ax2.plot(x, y2, color="blue", label=r"Doser Speed")

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=400, top=750)
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperatur in degree C")
    ax.set_title("Temp & Doser in DIVA")
    ax.legend(bbox_to_anchor=(0.03, 0.85), loc="lower left")
    ax2.legend(bbox_to_anchor=(0.03, 0.78), loc="lower left")

    ax2.set_ylabel("Doser speed in %")

    Filename = "Temp_Doser_DIVA"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    # plt.show()


def Temperaturen_Plotten(df, Export_Path):
    x = df["Zeit"]

    # Name der Temperatursensoren
    Temp_ids = df.drop(columns="Zeit").columns

    fig, ax = plt.subplots(1, figsize=(7, 5))
    plt.subplots_adjust(right=0.8)

    for I in Temp_ids:
        # Entsprechende Spalte auswählen
        y = df[I]
        # Anschließend in das Fenster plotten
        plt.plot_date(x, y, ls="-", lw=1, ms=1.5, label=I)

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Temperatur in Grad Celsius")
    ax.set_title("Temperaturmessungen DIVA")
    ax.set_ylim(bottom=400, top=750)
    ax.legend(bbox_to_anchor=(1, 0.0), loc="lower left")

    Filename = "Temperaturen_DIVA"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


# Temperature plot by height
def T_H_Plot(df, Export_Path):
    Mean_Temp = df.mean().tolist()

    Height = (0.195, 0.705, 1.210, 2.300, 4.089, 5.453, 6.405, 8.200, 9.965, 10.990)
    df_T_H = pd.DataFrame({'Height': Height, 'Mean_Temp': Mean_Temp})

    fig, ax = plt.subplots(1, figsize=(5, 7))
    ax.plot(df_T_H['Mean_Temp'], df_T_H['Height'])

    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Temperature in Grad Celsius")
    ax.set_ylabel("Height")
    ax.set_title("Temperature through the carbonator")
    ax.set_xlim([100, 700])

    Filename = "Temp_Height_Plot"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


# Temperature and pressure plot by height
def TP_H_Plot(df_Temp, df_Pressure, Export_Path):
    Mean_Temp = df_Temp.mean().tolist()
    Mean_Pressure = df_Pressure.mean().tolist()

    Height_T = (0.195, 0.705, 1.210, 2.300, 4.089, 5.453, 6.405, 8.200, 9.965, 10.990)
    Height_P = (0.195, 1.210, 1.900, 3.389, 4.790, 6.405, 8.200, 9.965, 10.990)

    x1 = Mean_Temp
    x2 = Mean_Pressure

    x1_median = statistics.median(map(float, x1))
    x2_median = statistics.median(map(float, x2))
    x1_lim = [round((x1_median - (x1_median * 0.6)) / 50) * 50, round((x1_median + (x1_median * 0.2)) / 50) * 50]
    x2_lim = [0, round((x2_median + (x2_median * 3)) / 5) * 5]

    y1 = Height_T
    y2 = Height_P

    fig, ax1 = plt.subplots(1, figsize=(5, 7))
    # plt.subplots_adjust(right=0.8)

    ax1.plot(x1, y1, color="red", ls="-", lw=1, marker='o', ms=4, label=r"Temperature")
    ax1.set_xlim(x1_lim)
    ax2 = ax1.twiny()
    ax2.plot(x2, y2, color="blue", ls="-", lw=1, marker='^', ms=4, label=r"Pressure")
    ax2.set_xlim(x2_lim)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel("Temperature in degree Celcius")
    ax2.set_xlabel("Relative Pressure in mbar")
    ax1.set_ylabel("Height in meter")
    ax1.set_title("Temperature & Pressure profile")
    ax1.legend(bbox_to_anchor=(0.35, 0.88), loc="lower left")
    ax2.legend(bbox_to_anchor=(0.35, 0.82), loc="lower left")

    # fig.tight_layout()

    Filename = "Temp_Pressure_Height_Plot"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


def Input_Gas_Plot(df, Export_Path):
    x = df["Zeit"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    plt.subplots_adjust(right=0.8)

    Gasinput_ids = df.columns.tolist()

    # pdb.set_trace()
    del Gasinput_ids[-2:]

    for I in Gasinput_ids:
        # Entsprechende Spalte auswählen
        y = df[I]
        # Anschließend in das Fenster plotten
        plt.plot_date(x, y, ls="-", lw=1, ms=1.5, label=I)

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Flow rate")
    ax.set_title("Gasinput into DIVA")
    ax.legend(bbox_to_anchor=(1, 0.0), loc="lower left")

    Filename = "Gasinput_DIVA"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


def Output_Gas_Plot(df, Export_Path, Messgerät):
    x = df["Zeit"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    plt.subplots_adjust(right=0.8)

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Zeit")
    ax.set_ylabel("Concentration in Volumn % ")
    ax.set_title("Gasoutpit into DIVA")
    ax.legend(bbox_to_anchor=(1, 0.0), loc="lower left")

    Filename = "Gasoutput_DIVA"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


def CO2_breakthrough(df, Export_Path):
    df_GC = df.dropna(subset=['CO2'])
    x = df["Zeit"]
    x_GC = df_GC["Zeit"]

    y1 = df["CO2_MGSB"]
    y2 = df["Volumenanteil_H2O"]
    y3 = df_GC["CO2"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    # plt.subplots_adjust(right=0.8)

    ax.plot_date(x, y1, color="red", ls="-", lw=1, ms=0, label=r"$CO_2$")
    ax.plot_date(x, y2, color="blue", ls="--", lw=1, ms=0, label=r"$H_2O$")
    ax.plot_date(x_GC, y3, color="grey", ls="-.", lw=1, ms=0, label=r"$CO_2$ (GC)")

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Time")
    ax.set_ylabel("Concentration in Volumn percent")
    ax.set_title("CO2 breakthrough curve")
    # ax.set_ylim([0, 15])
    ax.legend(bbox_to_anchor=(0.02, 0.4), loc="upper left")

    Filename = "CO2_breakthrough"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    # plt.show()



def CO2_soll_MFC(df, Export_Path):
    x = df["Zeit"]

    y1 = df["F203_MFC_CO2_1"]
    y2 = df["CO2_1"]

    df["CO2_rollavg"] = df["CO2_1"].rolling(window=10, min_periods=1).mean()
    y3 = df["CO2_rollavg"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    plt.subplots_adjust(right=0.8)

    ax.plot(x, y1, color="red", label=r"CO2 set")
    ax.plot(x, y2, color="blue", label=r"CO2 actual")
    ax.plot(x, y3, color="black", label=r"CO2 actual Avg.")

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Time")
    ax.set_ylabel("CO2 conc. in %")
    ax.set_title("MFC reliability")
    ax.set_ylim(1, 1.5)
    ax.legend(bbox_to_anchor=(0.03, 0.13), loc="lower left")

    Filename = "MFC_reliability"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    plt.show()


def Sorbent_supply(df, Export_Path):
    # unit conversion to kg
    df["Waage_abs_kg"] = df["Waage_abs"] / 1000
    # smoothing
    df["Waage_abs_kg_movingAVG"] = df["Waage_abs_kg"].rolling(window=60).mean()

    # Applying sav-gol filter
    df["Waage_abs_fil"] = sig.savgol_filter(df["Waage_abs_kg"], 200, 2)

    # weight change per second, NaN filled as zero
    df["Waage_massflow_cal"] = (3600) * (-1) * df["Waage_abs_kg"].diff()
    df["Waage_massflow_cal"] = df["Waage_massflow_cal"].fillna(0)
    # Applying sav-gol filter to weight change
    df["Waage_massflow_cal_fil"] = sig.savgol_filter(df["Waage_massflow_cal"], 200, 2)  # kg

    # Assume 100% Ca(OH)2, convert to kmol
    df["Waage_massflow_cal_fil_mol"] = df["Waage_massflow_cal_fil"] / 74.1

    # weight change itself has too much fluctuation, use moving average
    df["Waage_massflow_movingAVG"] = df["Waage_massflow_cal"].rolling(window=10, min_periods=5).mean()
    # NaN filled as zero
    df["Waage_massflow_movingAVG"] = df["Waage_massflow_movingAVG"].fillna(0)
    # Smoothing once again.
    df["Waage_massflow_movingAVG_fil"] = sig.savgol_filter(df["Waage_massflow_movingAVG"], 100, 2)  # kg/h
    df["Waage_massflow_movingAVG_fil_mol"] = df["Waage_massflow_movingAVG_fil"] * (1 / 3600) * (
                1 / 74.1) * 1000  # mol/s

    x = df["Zeit"]

    # y1 = df["Waage_massflow_movingAVG"]
    y2 = df["Waage_massflow_movingAVG_fil"]
    y3 = df["Waage_abs_kg"]
    y4 = df["Waage_abs_fil"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    plt.subplots_adjust(right=0.9)

    ax2 = ax.twinx()

    # ax.plot_date(x, y1, color = "gray", ls="-", lw=1, ms=0, label=r"Mass_flow")
    ax.plot_date(x, y2, color="red", ls="-", lw=1, ms=0, label=r"Mass_flow_filter")
    ax2.plot_date(x, y3, color="gray", ls="-", lw=1, ms=0, label=r"Weight")
    ax2.plot_date(x, y4, color="black", ls="--", lw=1, ms=0, label=r"Weight_filter")

    # Aussehen anpassen
    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Time")
    ax.set_ylabel("Sorbent_massflow in kg/h")
    ax2.set_ylabel("Weight in kg")
    ax.set_title("Sorbent supply")
    min_ylim = round(1.3 * df["Waage_massflow_movingAVG_fil"].min(), 0)
    max_ylim = round(1.3 * df["Waage_massflow_movingAVG_fil"].max(), 0)
    ax.set_ylim(min_ylim, max_ylim)
    ax.legend(bbox_to_anchor=(0.69, 0.875), loc="lower left")
    ax2.legend(bbox_to_anchor=(0.69, 0.91), loc="upper left")

    Filename = "Sorbent supply"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    # plt.show()


# Dosing & CO2 capture graph plot 
def graph_test(df, Export_Path):
    x = df["Zeit"]

    y1 = df["CO2_removal_mol"]  # mol/s
    y2 = df["Waage_massflow_movingAVG_fil_mol"]  # mol/s
    # y3 = df["Sorbent_conversion"]

    fig, ax = plt.subplots(1, figsize=(7, 5))
    # plt.subplots_adjust(right=0.8)

    # par1 = ax.twinx()
    # par2 = ax.twinx()

    ax.plot_date(x, y1, color="gray", ls="-", lw=1, ms=0, label=r"Captured_CO2")
    ax.plot_date(x, y2, color="red", ls="-", lw=1, ms=0, label=r"Sorbent_input")
    # par2.plot_date(x, y3, color = "black", ls = "--", lw = 1, ms = 0, label = r"Conversion")

    ax.xaxis.set_major_formatter(dates.DateFormatter("%H:%M"))
    ax.xaxis.set_minor_formatter(dates.DateFormatter("%H:%M"))
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Time")
    ax.set_ylabel("Flow in mol/s")
    # par1.set_ylabel("Sorbent in mol/s")
    # par2.set_ylabel("Conversion")
    ax.set_title("Sorbent-CO2 flow")
    ax.set_ylim(-0.001, 1.05 * df["Waage_massflow_movingAVG_fil_mol"].max())
    # par1.set_ylim(-0.001, 1.05*df["Waage_massflow_movingAVG_fil_mol"].max())
    ax.legend(bbox_to_anchor=(1, 0.95), loc="upper right")

    Filename = "Conversion"
    fig.savefig("{}.png".format(os.path.join(Export_Path, Filename)), dpi=400)

    # Plot anzeigen
    # plt.show()
