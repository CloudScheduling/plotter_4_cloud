import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb
import pandas as pd

def energy_plots(df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, ex_name):
    """
    plt.plot(arr1, c="b", label="Maxmin")
    plt.plot(arr2, c="g", label="Minmin")
    plt.title("Energy usage")
    plt.legend(loc="lower right")
    plt.savefig("img/energy.png")

    plt.figure()
    """
    f, ax =plt.subplots()


    df1_2 = pd.DataFrame()
    df1_2["Half scale"] = df3["energyUsage(Power usage of the host in W)"]
    df1_2["Double scale"] = df1["energyUsage(Power usage of the host in W)"]
    df1_2["Base scale"] = df2["energyUsage(Power usage of the host in W)"]

    df3_4 = pd.DataFrame()
    df3_4["Half scale"] = df6["energyUsage(Power usage of the host in W)"]
    df3_4["Double scale"] = df4["energyUsage(Power usage of the host in W)"]
    df3_4["Base scale"] = df5["energyUsage(Power usage of the host in W)"]
    

    df5_6 = pd.DataFrame()
    df5_6["Half scale"] = df9["energyUsage(Power usage of the host in W)"]
    df5_6["Double scale"] = df7["energyUsage(Power usage of the host in W)"]
    df5_6["Base scale"] = df8["energyUsage(Power usage of the host in W)"]


    df7_8 = pd.DataFrame()
    df7_8["Half scale"] = df12["energyUsage(Power usage of the host in W)"]
    df7_8["Double scale"] = df10["energyUsage(Power usage of the host in W)"]
    df7_8["Base scale"] = df11["energyUsage(Power usage of the host in W)"]

    df1_2["Policy"] = "Max-Min"
    df3_4["Policy"] = "Min-Min"
    df5_6["Policy"] = "ELOP"
    df7_8["Policy"] = "Random"

    df = pd.concat([df1_2, df3_4, df5_6, df7_8], ignore_index=True)
    
    df.to_csv("bruh.csv")

    dd=pd.melt(df,id_vars=['Policy'],value_vars=['Half scale', 'Base scale', "Double scale"],var_name='Scale')
    plot = sb.boxplot(x='value',y='Policy',data=dd,hue='Scale', width=0.3)

    ax.set_xlabel("Energy consumption(KW)")
    ax.set_title("Energy consumption per 20 minutes")

    plt.savefig("img/"+ex_name+".png")

def usage_plots(arr1,arr2):
    plt.plot(arr1, c="b", label="Maxmin")
    plt.plot(arr2, c="g", label="Minmin")
    plt.title("CPU usage")
    plt.legend(loc="lower right")
    plt.savefig("img/cpu.png")

def arrival_plots():
    
    pass

def cdf_plots(df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, name):
    list = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12]
    ax, fig = plt.subplots()

    it_number = 0
    for it in list:
        lab = ""
        if(it_number % 3 == 0):
            lab = "Double scale -"
        elif(it_number % 3 == 1):
            lab = "Normal scale -"
        elif(it_number % 3 == 2):
            lab = "Half scale -"
        
        if(it_number//3 == 0):
            lab += " Max-Min"
            mark = "x"
        elif(it_number//3 == 1):
            lab += " Min-Min"
            mark = "*"
        elif(it_number//3 == 2):
            lab += " ELOP"
            mark = "o"
        elif(it_number//3 == 3):
            lab += " Random"
            mark = "v"
        it = convert_to_cdf(it)
        arr = [100, 200, 300, 400, 500, 600, 700, 800]
        plt.plot(it["Time (s)"], it["Percentage of completion"], label=lab, marker=mark, markevery=arr)

        it_number += 1
    plt.legend(loc="lower right")
    plt.xlabel("Time (s)")
    plt.ylabel("Percentage of tasks completed")
    
    plt.savefig("img/"+name+".png")

def convert_to_cdf(df):
    num_tasks = df["Tasks #"].sum()
    sorted_df = df.sort_values(by="Time (s)")

    task_array = sorted_df["Tasks #"].to_numpy()

    percentage_of_completion = []
    perc_task_comp = 0
    for task in task_array:
        perc_task_comp += (task/num_tasks)*100
        percentage_of_completion.append(perc_task_comp)
    
    sorted_df["Percentage of completion"] = percentage_of_completion
    return sorted_df

def makespan_plot(df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, name):
    f, ax =plt.subplots()
    df1_2 = pd.DataFrame()
    
    df1_2["Half scale"] = df3["Makespan (s)"]
    df1_2["Double scale"] = df1["Makespan (s)"]
    df1_2["Base scale"] = df2["Makespan (s)"]
    

    df3_4 = pd.DataFrame()
    df3_4["Half scale"] = df6["Makespan (s)"]
    df3_4["Double scale"] = df4["Makespan (s)"]
    df3_4["Base scale"] = df5["Makespan (s)"]

    df5_6 = pd.DataFrame()
    df5_6["Half scale"] = df9["Makespan (s)"]
    df5_6["Double scale"] = df8["Makespan (s)"]
    df5_6["Base scale"] = df7["Makespan (s)"]

    df7_8 = pd.DataFrame()
    df7_8["Half scale"] = df12["Makespan (s)"]
    df7_8["Double scale"] = df10["Makespan (s)"]
    df7_8["Base scale"] = df11["Makespan (s)"]

    df1_2["Policy"] = "Max-Min"
    df3_4["Policy"] = "Min-Min"
    df5_6["Policy"] = "ELOP"
    df7_8["Policy"] = "Random"

    df = pd.concat([df1_2, df3_4, df5_6, df7_8], ignore_index=True)

    
    dd=pd.melt(df,id_vars=['Policy'],value_vars=['Half scale', 'Base scale', "Double scale"],var_name='Scale')
    plot = sb.boxplot(x='value',y='Policy',data=dd,hue='Scale', width=0.3)


    ax.set_xlabel("Makespan (s)")
    ax.set_title("Makespan for workflows")
    plt.savefig("img/"+name+".png")

