import numpy as np
import pandas as pd


def convert_to_cdf(df):
    num_tasks = df["Tasks #"].sum()
    sorted_df = df.sort_values(by="Time (s)")

    task_array = sorted_df["Tasks #"].to_numpy()

    percentage_of_completion = []
    perc_task_comp = 0
    for task in task_array:
        perc_task_comp += (task / num_tasks) * 100
        percentage_of_completion.append(perc_task_comp)

    sorted_df["Percentage of completion"] = percentage_of_completion
    return sorted_df


# method to reconfig the metrics
def all_hosts_df(df, hosts):
    new_df = pd.DataFrame()
    df_en_arr = []
    df_us_arr = []

    for i in range(1, (len(df["energyUsage(Power usage of the host in W)"]))):
        it = i
        it_2 = i + hosts

        df_en_arr.append((df["energyUsage(Power usage of the host in W)"].iloc[it:it_2].sum()) / 1000)
        df_us_arr.append((df["cpuUsage(CPU usage of all CPUs of the host in MHz)"].iloc[it:it_2].sum()))

        i = it_2 + 1
    new_df["cpuUsage"] = df_us_arr
    new_df["Energy"] = df_en_arr
    """
    new_df = pd.DataFrame()
    df_en_arr = []
    df_us_arr = []
    
    for i in range(1, (len(df["energyUsage(Power usage of the host in W)"]) // hosts)):
        it = i
        it_2 = i+2
        
        df_en_arr.append((df["energyUsage(Power usage of the host in W)"].iloc[it:it_2].sum())/1000)
        df_us_arr.append((df["cpuUsage(CPU usage of all CPUs of the host in MHz)"].iloc[it:it_2].sum()))
    
    new_df["cpuUsage"] = df_us_arr
    new_df["Energy"] = df_en_arr
    """
    length = len(df_us_arr)
    return new_df, length
