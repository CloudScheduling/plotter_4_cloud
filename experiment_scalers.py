import pandas as pd
import numpy as np
import plotters

#Read CSVs and create
def read_makespan_csv(path_to_folder):    
    het16 = pd.read_csv(path_to_folder+"hetro_scale16_makespan.csv")
    het8 = pd.read_csv(path_to_folder+"hetro_scale8_makespan.csv")
    het4 = pd.read_csv(path_to_folder+"hetro_scale4_makespan.csv")  
    hom4 = pd.read_csv(path_to_folder+"homo_scale4_makespan.csv")
    hom8 = pd.read_csv(path_to_folder+"homo_scale8_makespan.csv")
    hom16 = pd.read_csv(path_to_folder+"homo_scale16_makespan.csv")
        
    
    return het16, het8, het4, hom16, hom8, hom4

def read_metrics_csv(path_to_folder):
    het16 = pd.read_csv(path_to_folder+"hetro_scale16_metrics.csv")
    het8 = pd.read_csv(path_to_folder+"hetro_scale8_metrics.csv")
    het4 = pd.read_csv(path_to_folder+"hetro_scale4_metrics.csv")
    hom16 = pd.read_csv(path_to_folder+"homo_scale16_metrics.csv")
    hom8 = pd.read_csv(path_to_folder+"homo_scale8_metrics.csv")    
    hom4 = pd.read_csv(path_to_folder+"homo_scale4_metrics.csv") 

    return het16, het8, het4, hom16, hom8, hom4

def read_time_csv(path_to_folder):
    het16 = pd.read_csv(path_to_folder+"hetro_scale16_taksOverTime.csv")
    het8 = pd.read_csv(path_to_folder+"hetro_scale8_taksOverTime.csv")
    het4 = pd.read_csv(path_to_folder+"hetro_scale4_taksOverTime.csv")
    hom16 = pd.read_csv(path_to_folder+"homo_scale16_taksOverTime.csv")
    hom8 = pd.read_csv(path_to_folder+"homo_scale8_taksOverTime.csv")
    hom4 = pd.read_csv(path_to_folder+"homo_scale4_taksOverTime.csv")       

    return het16, het8, het4, hom16, hom8, hom4

def treatDF(df):
    pass

def plot_data(amount_of_csvs):
    max_makespan_het16, max_makespan_het8, max_makespan_het4, max_makespan_homo16, max_makespan_homo8, max_makespan_homo4 = read_makespan_csv(
        "Max-Min/specTrace2_maxMin_")
    max_metrics_het16, max_metrics_het8, max_metrics_het4, max_metrics_homo16, max_metrics_homo8, max_metrics_homo4 = read_metrics_csv(
        "Max-Min/specTrace2_maxMin_")
    max_time_het16, max_time_het8, max_time_het4, max_time_homo16, max_time_homo8, max_time_homo4 = read_time_csv(
        "Max-Min/specTrace2_maxMin_")

    min_makespan_het16, min_makespan_het8, min_makespan_het4, min_makespan_homo16, min_makespan_homo8, min_makespan_homo4 = read_makespan_csv(
        "Min-Min/specTrace2_minMin_")
    min_metrics_het16, min_metrics_het8, min_metrics_het4, min_metrics_homo16, min_metrics_homo8, min_metrics_homo4 = read_metrics_csv(
        "Min-Min/specTrace2_minMin_")
    min_time_het16, min_time_het8, min_time_het4, min_time_homo16, min_time_homo8, min_time_homo4 = read_time_csv(
        "Min-Min/specTrace2_minMin_")

    elop_makespan_het16, elop_makespan_het8, elop_makespan_het4, elop_makespan_homo16, elop_makespan_homo8, elop_makespan_homo4 = read_makespan_csv(
        "ELOP/specTrace2_elop_")
    elop_metrics_het16, elop_metrics_het8, elop_metrics_het4, elop_metrics_homo16, elop_metrics_homo8, elop_metrics_homo4 = read_metrics_csv(
        "ELOP/specTrace2_elop_")
    elop_time_het16, elop_time_het8, elop_time_het4, elop_time_homo16, elop_time_homo8, elop_time_homo4 = read_time_csv(
        "ELOP/specTrace2_elop_")

    random_makespan_het16, random_makespan_het8, random_makespan_het4, random_makespan_homo16, random_makespan_homo8, random_makespan_homo4 = read_makespan_csv(
        "Random/specTrace2_random_")
    random_metrics_het16, random_metrics_het8, random_metrics_het4, random_metrics_homo16, random_metrics_homo8, random_metrics_homo4 = read_metrics_csv(
        "Random/specTrace2_random_")
    random_time_het16, random_time_het8, random_time_het4, random_time_homo16, random_time_homo8, random_time_homo4 = read_time_csv(
        "Random/specTrace2_random_")
    """
    arr1_energy = df[["energyUsage"]].to_numpy()
    arr1_usage = df[["cpuUsage"]].to_numpy()


    arr2_energy = df2[["energyUsage"]].to_numpy()
    arr2_usage = df2[["cpuUsage"]].to_numpy()
    """

    plotters.energy_plots(max_metrics_het16, max_metrics_het8, max_metrics_het4,
    min_metrics_het16, min_metrics_het8, min_metrics_het4,
    elop_metrics_het16, elop_metrics_het8, elop_metrics_het4,
    random_metrics_het16, random_metrics_het8, random_metrics_het4, "HeterogeneousEnergy")

    plotters.energy_plots(max_metrics_homo16, max_metrics_homo8, max_metrics_homo4,
    min_metrics_homo16, min_metrics_homo8, min_metrics_homo4,
    elop_metrics_homo16, elop_metrics_homo8, elop_metrics_homo4, 
    random_metrics_homo16, random_metrics_homo8, random_metrics_homo4, "HomogeneousEnergy")
    
    #plotters.usage_plots(arr1_usage, arr2_usage)

    plotters.arrival_plots()
    plotters.arrival_plots()

    plotters.makespan_plot(max_makespan_het16, max_makespan_het8, max_makespan_het4,
    min_makespan_het16, min_makespan_het8, min_makespan_het4,
    elop_makespan_het16, elop_makespan_het8, elop_makespan_het4, random_makespan_het16, 
    random_makespan_het8, random_makespan_het4,"heterogeneousMakespan")

    plotters.makespan_plot(max_makespan_homo16, max_makespan_homo8, max_makespan_homo4,
    min_makespan_homo16, min_makespan_homo8, min_makespan_het4,
    elop_makespan_homo16, elop_makespan_homo8, elop_makespan_homo4,
    random_makespan_homo16, random_makespan_homo8, random_makespan_homo4, "homogeneousMakespan")


    plotters.cdf_plots(max_time_het16, max_time_het8, max_time_het4, min_time_het16, min_time_het8, min_time_het4, 
    elop_time_het16, elop_time_het8, elop_time_het4, random_time_het16, random_time_het8, random_time_het4, "hetrogeneousFinish")

    plotters.cdf_plots(max_time_homo16, max_time_homo8, max_time_homo4, min_time_homo16, min_time_homo8, min_time_homo4, 
    elop_time_homo16, elop_time_homo8, elop_time_homo4, random_time_homo16, random_time_homo8, random_time_homo4, "homogeneousFinish")
plot_data(2)

    
        




