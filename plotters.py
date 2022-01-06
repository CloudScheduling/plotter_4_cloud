import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import plotters_help
from DataTransformer import get_trailing_int


def energy_plots(data, meta):
    f, axs = plt.subplots(meta["scales"], 1)
    axis_mapping = meta["scale_plot_mapping"]

    # iterate through every dataframe
    for policy_name, policy in data.items():
        for scale_name, scale in policy.items():
            axs_idx = axis_mapping[scale_name]
            axs[axs_idx].plot(scale.index, scale[["energyUsage"]], label=policy_name)
            axs[axs_idx].set_title(scale_name, size=10)
            axs[axs_idx].tick_params(labelsize=6)

    # Extra labels
    middle_idx = int(len(axis_mapping) / 2)
    axs[middle_idx].set_ylabel("Energy consumption(W)")
    axs[-1].set_xlabel("Time (minutes)")
    axs[0].legend(loc="upper right")

    # adjust spaces between each plot so that labels fit
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)

    plt.savefig(meta["file_name"])


def energy_bar(list, ex_name, mode):
    energy_list = []
    name = ["Double", "Base", "Half", "Double", "Base", "Half", "Double", "Base",
            "Half", "Double", "Base", "Half"]
    for it in list:
        energy_list.append(((it["energyUsage(Power usage of the host in W)"].sum()) / 1000))

    if (mode == 1):
        fig, axs = plt.subplots(2, 2, sharey="all")
        axs[0, 0].bar(name[0:3], energy_list[0:3])
        axs[0, 0].set_title("MaxMin", size=10)
        axs[0, 1].bar(name[3:6], energy_list[3:6])
        axs[0, 1].set_title("MinMin", size=10)
        axs[1, 0].bar(name[6:9], energy_list[6:9])
        axs[1, 0].set_title("ELOP", size=10)
        axs[1, 1].bar(name[9:12], energy_list[9:12])
        axs[1, 1].set_title("Random", size=10)
        axs[1, 0].set_ylabel("Energy consumption (kW)")

    plt.subplots_adjust(left=0.2,
                        bottom=0.1,
                        top=0.9,
                        wspace=0.2,
                        hspace=0.4)

    plt.savefig("img2/" + ex_name + ".png")


def usage_plots(list, ex_name):
    f, ax = plt.subplots()

    counter = 0

    df1_2 = pd.DataFrame()
    df3_4 = pd.DataFrame()
    df5_6 = pd.DataFrame()
    df7_8 = pd.DataFrame()
    for it in list:
        lab = ""
        host_number = 0
        if (counter % 3 == 0):
            host_number = 16
        elif (counter % 3 == 1):
            host_number = 8
        elif (counter % 3 == 2):
            host_number = 4

        it, empty = plotters_help.all_hosts_df(it, host_number)

        if (counter // 3 == 0):  # i could make this a function... we'll see....
            if (host_number == 16):
                df1_2["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df1_2["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df1_2["Half scale"] = it["cpuUsage"]
        elif (counter // 3 == 1):
            if (host_number == 16):
                df3_4["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df3_4["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df3_4["Half scale"] = it["cpuUsage"]
        elif (counter // 3 == 2):
            if (host_number == 16):
                df5_6["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df5_6["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df5_6["Half scale"] = it["cpuUsage"]
        elif (counter // 3 == 3):
            if (host_number == 16):
                df7_8["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df7_8["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df7_8["Half scale"] = it["cpuUsage"]

        counter += 1

    df1_2["Policy"] = "Max-Min"
    df3_4["Policy"] = "Min-Min"
    df5_6["Policy"] = "ELOP"
    df7_8["Policy"] = "Random"

    df = pd.concat([df1_2, df3_4, df5_6, df7_8], ignore_index=True)

    dd = pd.melt(df, id_vars=['Policy'], value_vars=['Half scale', 'Base scale', "Double scale"], var_name='Scale')
    plot = sb.boxplot(x='value', y='Policy', data=dd, hue='Scale', width=0.3)

    ax.set_xlabel("CPU usage (MHz)")
    ax.set_title("CPU usage per 20 minutes")

    plt.savefig("img2/" + ex_name + ".png")


def arrival_plots():
    pass


def cdf_plots(list, name):
    ax, fig = plt.subplots()

    it_number = 0
    for it in list:
        lab = ""
        if (it_number % 3 == 0):
            lab = "Double scale -"
        elif (it_number % 3 == 1):
            lab = "Normal scale -"
        elif (it_number % 3 == 2):
            lab = "Half scale -"

        if (it_number // 3 == 0):
            lab += " Max-Min"
            mark = "x"
        elif (it_number // 3 == 1):
            lab += " Min-Min"
            mark = "*"
        elif (it_number // 3 == 2):
            lab += " ELOP"
            mark = "o"
        elif (it_number // 3 == 3):
            lab += " Random"
            mark = "v"
        it = plotters_help.convert_to_cdf(it)
        arr = [100, 200, 300, 400, 500, 600, 700, 800]
        plt.plot(it["Time (s)"], it["Percentage of completion"], label=lab, marker=mark, markevery=arr)

        it_number += 1
    plt.legend(loc="lower right")
    plt.xlabel("Time (s)")
    plt.ylabel("Percentage of tasks completed")

    plt.savefig("img2/" + name + ".png")


def makespan_plot(list, name):
    f, ax = plt.subplots()

    """df1_3 = pd.DataFrame()
    df4_6 = pd.DataFrame()
    df7_9 = pd.DataFrame()
    df10_12 = pd.DataFrame()"""
    data = []
    policy_names = ["Max-Min", "Min-Min", "ELOP", "Random"]
    counter = 0

    data_req = (
            len(list) // 3)  # DO INTEGER DIV since there are three different scales... has to edited if we scale up... shit code my bad

    for i in range(0, data_req):
        df_combo = pd.DataFrame()
        df1 = list[counter]
        df2 = list[counter + 1]
        df3 = list[counter + 2]

        counter += 3
        df_combo["Double scale"] = df1["Makespan (s)"]
        df_combo["Base scale"] = df2["Makespan (s)"]
        df_combo["Half scale"] = df3["Makespan (s)"]
        df_combo["Policy"] = policy_names[i]
        data.append(df_combo)

    df = pd.concat([data[0], data[1], data[2], data[3]], ignore_index=True)

    dd = pd.melt(df, id_vars=['Policy'], value_vars=['Half scale', 'Base scale', "Double scale"], var_name='Scale')
    plot = sb.boxplot(x='value', y='Policy', data=dd, hue='Scale', width=0.3)

    ax.set_xlabel("Makespan (s)")
    ax.set_title("Makespan for workflows")
    plt.savefig("img2/" + name + ".png")


def performance_per_KWH(list, time_list, gflop, name):
    # homogeneous test = 2513 FLOPs
    # hetrogeneous test = 2190 FLOPs

    # (flo / makespan) / (totalEnergy / response time) = performance per kWh

    f, ax = plt.subplots()
    # iterate through dfs to transform them into approrpriate values
    counter = 0
    configured_list = []

    # needed for proper categorization later
    host_number_arr = []

    for it in list:
        host_number = 0
        if (counter % 3 == 0):
            host_number = 16
        elif (counter % 3 == 1):
            host_number = 8
        elif (counter % 3 == 2):
            host_number = 4

        # configure df to KW and to mash together all hosts
        it, temp_length = plotters_help.all_hosts_df(it, host_number)

        configured_list.append(it)
        host_number_arr.append(host_number)
        counter += 1

    # get sum makespan and response time for all of the different scales
    makespan_list = []
    response_list = []
    for it in time_list:
        makespan_list.append(it["Makespan (s)"].sum())
        response_list.append(it["Workflow Response time (s)"].sum())
    # empty dfs for categorizations
    dfmax_min = pd.DataFrame()
    dfmin_min = pd.DataFrame()
    dfelop = pd.DataFrame()
    dfrandom = pd.DataFrame()

    # Do the calculations from formula on top
    counter_time = 0
    calculated_list = []
    for it in configured_list:
        it["cpuUsage"] = it["cpuUsage"] / (makespan_list[counter_time])
        it["Energy"] = it["Energy"] / (response_list[counter_time])

        calculated_list.append(it)

        # horrible horrible horrible if nests
        if (counter_time // 3 == 0):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfmax_min["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfmax_min["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfmax_min["Half scale"] = it["cpu/energy"]
        elif (counter_time // 3 == 1):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfmin_min["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfmin_min["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfmin_min["Half scale"] = it["cpu/energy"]
        elif (counter_time // 3 == 2):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfelop["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfelop["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfelop["Half scale"] = it["cpu/energy"]
        elif (counter_time // 3 == 3):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfrandom["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfrandom["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfrandom["Half scale"] = it["cpu/energy"]
        counter_time += 1
    dfmax_min["Policy"] = "Max-Min"
    dfmin_min["Policy"] = "Min-Min"
    dfelop["Policy"] = "ELOP"
    dfrandom["Policy"] = "Random"

    df = pd.concat([dfmax_min, dfmin_min, dfelop, dfrandom], ignore_index=True)

    dd = pd.melt(df, id_vars=['Policy'], value_vars=['Half scale', 'Base scale', "Double scale"], var_name='Scale')
    plot = sb.boxplot(x='value', y='Policy', data=dd, hue='Scale', width=0.3)

    ax.set_xlabel("Max GFLOPs per kWh")

    plt.savefig("img2/" + name + ".png")
    pass


def create_makespan_cdf_order_scale(data, meta):
    order_plots = meta["order_plots"]
    fig, axs = plt.subplots(1, len(data), figsize=(5 * len(data), 5))

    # TODO: order needed -> mapping in meta
    for ax, scale_name in zip(axs, order_plots):
        scale = data[scale_name]
        sb.histplot(data=scale, element="step", fill=False, cumulative=True, stat="density", common_norm=False, ax=ax)
        ax.set_xlabel("Workflow makespan [s]")
        ax.set_ylabel("ECDF")
        ax.set_title(f"Scale: {get_trailing_int(scale_name)}")
    plt.savefig(meta["file_name"])


def create_makespan_cdf_order_policy(data, meta):
    fig, axs = plt.subplots(1, len(data), figsize=(5 * len(data), 5))

    # single policy breaks the loop -> do seperately
    if len(data) == 1:
        for policy_name, policy in data.items():
            sb.histplot(data=policy, element="step", fill=False, cumulative=True, stat="density", common_norm=False,
                        ax=axs)
            axs.set_xlabel("Workflow makespan [s]")
            axs.set_ylabel("ECDF")
            axs.set_title(policy_name)
        plt.savefig(meta["file_name"])
        return

    # TODO: order needed -> mapping in meta
    for ax, (policy_name, policy) in zip(axs, data.items()):
        sb.histplot(data=policy, element="step", fill=False, cumulative=True, stat="density", common_norm=False, ax=ax)
        ax.set_xlabel("Workflow makespan [s]")
        ax.set_ylabel("ECDF")
        ax.set_title(policy_name)
    plt.savefig(meta["file_name"])


def create_energy_plot_scale(data, meta):
    for policy in data.values():
        sb.lineplot(x=policy["scale"], y=policy["energyUsage (kWh)"])
    plt.savefig(meta["file_name"])
