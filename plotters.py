import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd
import plotters_help


def energy_plots(list, ex_name):
    f, axs = plt.subplots(3, 1)
    counter = 0

    # iterate through every dataframe
    for it in list:
        lab = ""
        host_number = 0
        if (counter % 3 == 0):
            host_number = 16
        elif (counter % 3 == 1):
            host_number = 8
        elif (counter % 3 == 2):
            host_number = 4

        # configure df to KW and to mash together all hosts
        it, temp_length = plotters_help.all_hosts_df(it, host_number)

        length_array = []
        # Get length (so that we can plot x axis with correct times)
        for i in range(0, temp_length):
            length_array.append(temp_length * i)

        # so that we can categorize correctly
        if (counter // 4 == 0):
            mark = "x"
            lab = "Max-Min"
        elif (counter // 4 == 1):
            lab = "Min-Min"
        elif (counter // 4 == 2):
            lab = "ELoP"
        elif (counter // 4 == 3):
            lab = "HEFT"
        elif (counter // 4 == 4):
            lab = "Random"

        # plot per scale
        if (host_number == 16):
            axs[2].plot(length_array, it["Energy"], label=lab)
            axs[2].set_title("Double scale", size=10)
            axs[2].tick_params(labelsize=6)
        elif (host_number == 8):
            axs[1].plot(length_array, it["Energy"], label=lab)
            axs[1].set_title("Base scale", size=10)
            axs[1].tick_params(labelsize=6)
        elif (host_number == 4):
            axs[0].plot(length_array, it["Energy"], label=lab)
            axs[0].set_title("Half scale", size=10)
            axs[0].tick_params(labelsize=6)
        counter += 1
        # plt.plot(it["Time (s)"], it["Energy"], label=lab, marker=mark, markevery=arr)

    # Extra labels
    axs[1].set_ylabel("Energy consumption(KW)")
    axs[2].set_xlabel("Time (minutes)")
    axs[0].legend(loc="upper right")

    # adjust spaces between each plot so that labels fit
    plt.subplots_adjust(left=0.1,
                        bottom=0.1,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)

    plt.savefig("img2/" + ex_name + "perScale2.png")


def energy_bar(list, ex_name, mode):
    energy_list = []
    name = ["Double", "Base", "Half", "Double", "Base", "Half", "Double", "Base",
            "Half", "Double", "Base", "Half", "Double", "Base", "Half"]
    for it in list:
        energy_list.append(((it["energyUsage(Power usage of the host in W)"].sum()) / 1000))

    if (mode == 1):
        fig, axs = plt.subplots(1, 5, sharey="all")
        axs[0].bar(name[0:3], energy_list[0:3])
        axs[0].set_title("MaxMin", size=10)
        axs[1].bar(name[3:6], energy_list[3:6])
        axs[1].set_title("MinMin", size=10)
        axs[2].bar(name[6:9], energy_list[6:9])
        axs[2].set_title("ELoP", size=10)
        axs[3].bar(name[9:12], energy_list[9:12])
        axs[3].set_title("HEFT", size=10)
        axs[4].bar(name[12:15], energy_list[12:15])
        axs[4].set_title("Random", size=10)
        plt.ylabel("Energy consumption (kW)")

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
    df9_10 = pd.DataFrame()
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

        if (counter // 4 == 0):  # i could make this a function... we'll see....
            if (host_number == 16):
                df1_2["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df1_2["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df1_2["Half scale"] = it["cpuUsage"]
        elif (counter // 4 == 1):
            if (host_number == 16):
                df3_4["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df3_4["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df3_4["Half scale"] = it["cpuUsage"]
        elif (counter // 4 == 2):
            if (host_number == 16):
                df5_6["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df5_6["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df5_6["Half scale"] = it["cpuUsage"]
        elif (counter // 4 == 3):
            if (host_number == 16):
                df7_8["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df7_8["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df7_8["Half scale"] = it["cpuUsage"]
        elif (counter // 4 == 4):
            if (host_number == 16):
                df9_10["Double scale"] = it["cpuUsage"]
            elif (host_number == 8):
                df9_10["Base scale"] = it["cpuUsage"]
            elif (host_number == 4):
                df9_10["Half scale"] = it["cpuUsage"]

        counter += 1

    df1_2["Policy"] = "Max-Min"
    df3_4["Policy"] = "Min-Min"
    df5_6["Policy"] = "ELoP"
    df7_8["Policy"] = "HEFT"
    df9_10["Policy"] = "Random"

    df = pd.concat([df1_2, df3_4, df5_6, df7_8, df9_10], ignore_index=True)

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
            lab += " HEFT"
            mark = "p"
        elif (it_number // 3 == 4):
            lab += " Random"
            mark = "v"
        it = plotters_help.convert_to_cdf(it)
        arr = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
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
    policy_names = ["Max-Min", "Min-Min", "ELOP", "HEFT", "Random"]
    counter = 0

    data_req = (
                len(list) // 3)  # DO INTEGER DIV since there are three different scales... has to edited if we scale up... shit code my bad

    for i in range(0, data_req):
        df_combo = pd.DataFrame()
        df1 = list[counter]
        df2 = list[counter + 1]
        df3 = list[counter + 2]
        #df4 = list[counter + 3]

        counter += 3
        df_combo["Double scale"] = df1["Makespan (s)"]
        df_combo["Base scale"] = df2["Makespan (s)"]
        df_combo["Half scale"] = df3["Makespan (s)"]
        df_combo["Policy"] = policy_names[i]
        data.append(df_combo)

    df = pd.concat([data[0], data[1], data[2], data[3], data[4]], ignore_index=True)

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
    dfheft = pd.DataFrame()
    dfrandom = pd.DataFrame()

    # Do the calculations from formula on top
    counter_time = 0
    calculated_list = []
    for it in configured_list:
        it["cpuUsage"] = it["cpuUsage"] / (makespan_list[counter_time])
        it["Energy"] = it["Energy"] / (response_list[counter_time])

        calculated_list.append(it)

        # horrible horrible horrible if nests
        if (counter_time // 4 == 0):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfmax_min["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfmax_min["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfmax_min["Half scale"] = it["cpu/energy"]
        elif (counter_time // 4 == 1):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfmin_min["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfmin_min["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfmin_min["Half scale"] = it["cpu/energy"]
        elif (counter_time // 4 == 2):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfelop["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfelop["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfelop["Half scale"] = it["cpu/energy"]
        elif (counter_time // 4 == 3):
            if (host_number_arr[counter_time] == 16):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 16 * gflop / it['Energy'])
                dfheft["Double scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 8):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 8 * gflop / it['Energy'])
                dfheft["Base scale"] = it["cpu/energy"]
            elif (host_number_arr[counter_time] == 4):
                it['cpu/energy'] = np.where(it['cpuUsage'] < 0.0001, it['cpuUsage'], 4 * gflop / it['Energy'])
                dfheft["Half scale"] = it["cpu/energy"]
        elif (counter_time // 4 == 4):
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
    dfelop["Policy"] = "ELoP"
    dfheft["Policy"] = "HEFT"
    dfrandom["Policy"] = "Random"

    df = pd.concat([dfmax_min, dfmin_min, dfelop, dfheft, dfrandom], ignore_index=True)

    dd = pd.melt(df, id_vars=['Policy'], value_vars=['Half scale', 'Base scale', "Double scale"], var_name='Scale')
    plot = sb.boxplot(x='value', y='Policy', data=dd, hue='Scale', width=0.3)

    ax.set_xlabel("Max GFLOPs per kWh")

    plt.savefig("img2/" + name + ".png")
    pass
