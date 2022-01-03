import pandas as pd
import numpy as np
import os


def read_makespan_csv(path_to_folder):
    het16 = pd.read_csv(path_to_folder + "hetro_scale16_makespan.csv")
    het8 = pd.read_csv(path_to_folder + "hetro_scale8_makespan.csv")
    het4 = pd.read_csv(path_to_folder + "hetro_scale4_makespan.csv")
    hom4 = pd.read_csv(path_to_folder + "homo_scale4_makespan.csv")
    hom8 = pd.read_csv(path_to_folder + "homo_scale8_makespan.csv")
    hom16 = pd.read_csv(path_to_folder + "homo_scale16_makespan.csv")

    return het16, het8, het4, hom16, hom8, hom4


def read_metrics_csv(path_to_folder):
    het16 = pd.read_csv(path_to_folder + "hetro_scale16_metrics.csv")
    het8 = pd.read_csv(path_to_folder + "hetro_scale8_metrics.csv")
    het4 = pd.read_csv(path_to_folder + "hetro_scale4_metrics.csv")
    hom16 = pd.read_csv(path_to_folder + "homo_scale16_metrics.csv")
    hom8 = pd.read_csv(path_to_folder + "homo_scale8_metrics.csv")
    hom4 = pd.read_csv(path_to_folder + "homo_scale4_metrics.csv")

    return het16, het8, het4, hom16, hom8, hom4


def read_time_csv(path_to_folder):
    het16 = pd.read_csv(path_to_folder + "hetro_scale16_taksOvertime.csv")
    het8 = pd.read_csv(path_to_folder + "hetro_scale8_taksOvertime.csv")
    het4 = pd.read_csv(path_to_folder + "hetro_scale4_taksOvertime.csv")
    hom16 = pd.read_csv(path_to_folder + "homo_scale16_taksOvertime.csv")
    hom8 = pd.read_csv(path_to_folder + "homo_scale8_taksOvertime.csv")
    hom4 = pd.read_csv(path_to_folder + "homo_scale4_taksOvertime.csv")

    return het16, het8, het4, hom16, hom8, hom4


def sort_dfs():  # calls the readers and sorts dataframes into correct arrays

    maxmin_path = "Max-Min/specTrace2_maxMin_"
    minmin_path = "Min-Min/specTrace2_minMin_"
    elop_path = "ELOP/specTrace2_elop_"
    random_path = "Random/specTrace2_random_"  # add paths for all data, should be this format

    # just add the path here if you want to include it in the mapping
    path_arr = [maxmin_path, minmin_path, elop_path, random_path]

    performance_het = []
    performance_homog = []
    makespan_het = []
    makespan_homog = []
    taskTime_het = []
    taskTime_homog = []

    # loops through and reads the csvs in the paths and appends them to correct dfs
    for path in path_arr:
        makespan_het16, makespan_het8, makespan_het4, makespan_homog16, makespan_homog8, makespan_homog4 = read_makespan_csv(
            path)
        metrics_het16, metrics_het8, metrics_het4, metrics_homog16, metrics_homog8, metrics_homog4 = read_metrics_csv(
            path)
        time_het16, time_het8, time_het4, time_homog16, time_homog8, time_homog4 = read_time_csv(
            path)

        multi_append(performance_het, metrics_het16, metrics_het8, metrics_het4)

        multi_append(performance_homog, metrics_homog16, metrics_homog8, metrics_homog4)

        multi_append(makespan_het, makespan_het16, makespan_het8, makespan_het4)

        multi_append(makespan_homog, makespan_homog16, makespan_homog8, makespan_homog4)

        multi_append(taskTime_het, time_het16, time_het8, time_het4)

        multi_append(taskTime_homog, time_homog16, time_homog8, time_homog4)

    return performance_het, performance_homog, makespan_het, makespan_homog, taskTime_het, taskTime_homog


def multi_append(array, element1, element2, element3):
    array.append(element1)
    array.append(element2)
    array.append(element3)

    return
