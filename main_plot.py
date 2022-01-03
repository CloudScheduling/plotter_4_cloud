import pandas as pd
import numpy as np
import plotters
import reader
from DataTransformer import DataTransformer


def plot_data():
    #performance_het, performance_homog, makespan_het, makespan_homog, taskTime_het, tasktime_homog = reader.sort_dfs()
    #data = reader.sort_dfs(["Max-Min", "Min-Min", "ELOP", "Random"])
    data = reader.sort_dfs(["Random"])

    transformer = DataTransformer(data)
    plotters.energy_plots(*transformer.to_energy_plot("specTrace2", "homo", "img2/Homo.png"))
    plotters.energy_plots(*transformer.to_energy_plot("specTrace2", "hetro", "img2/Hetro.png"))

    a, _ = transformer.to_utilization_table("specTrace2", "homo", "asdasd")
    print()
    # plotters.energy_plots(performance_het, "HeterogeneousEnergy")
    # plotters.energy_plots(performance_homog, "HomogeneousEnergy")
    #
    # plotters.energy_bar(performance_het, "HetrogEnergyBar", 1)
    # plotters.energy_bar(performance_homog, "HomogEnergyBar", 1)
    #
    # # plotters.usage_plots(arr1_usage, arr2_usage)
    #
    # plotters.usage_plots(performance_het, "HeterogeneousUsage")
    # plotters.usage_plots(performance_homog, "HomogeneousUsage")
    #
    # plotters.makespan_plot(makespan_het, "heterogeneousMakespan")
    # plotters.makespan_plot(makespan_homog, "homogeneousMakespan")
    #
    # plotters.cdf_plots(taskTime_het, "hetrogeneousFinish")
    # plotters.cdf_plots(tasktime_homog, "homogeneousFinish")
    #
    # plotters.performance_per_KWH(performance_het, makespan_het, 2190, "HetrogFlopsPerkWh")
    # # Homogeneous plots
    # plotters.performance_per_KWH(performance_homog, makespan_homog, 2513, "HomogFlopsPerkWh")


if __name__ == "__main__":
    plot_data()
