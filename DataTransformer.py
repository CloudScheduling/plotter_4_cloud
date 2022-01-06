import re

import pandas as pd


def get_trailing_int(string):
    a = [int(s) for s in re.findall(r"\d+", string)]
    if len(a) > 1:
        raise RuntimeError("More than one integer found")
    elif len(a) == 0:
        return None
    return a[0]


class DataTransformer:
    """
    makespan
    taksOvertime
    metrics
    hostInfo
    """
    makespan_file_key = "makespan"
    taskOvertime_file_key = "taksOvertime"
    metrics_file_key = "metrics"
    hostInfo_file_key = "hostInfo"
    variableStore_file_key = "variableStore"

    def __init__(self, data) -> None:
        super().__init__()
        self.data = data

    def to_energy_plot(self, trace_key, environment_key, file_name):
        """
        Structure: policy -> scale -> dataframe
        :param trace_key:
        :param environment_key:
        :return:
        """
        meta = {
            "trace": trace_key,
            "environment": environment_key,
            "file_type": self.metrics_file_key,
            "file_name": file_name,
            "units": {
                "timestamp": "s",
                "energyUsage": "W",
            },
            "scales": -1,  # filled later
            "scale_plot_mapping": {},  # index = position of key
        }

        # filtering
        filtered_data = {}
        for policy_name, policy in self.data[trace_key].items():
            filtered_data[policy_name] = {}
            environment = policy[environment_key]
            # will be written multiple times, but should be of equal size every time due to test setup
            meta["scales"] = len(environment)
            scale_keys = list(environment.keys())
            scale_keys.sort(key=lambda x: get_trailing_int(x))  # make sure to have ascending order of scales
            meta["scale_plot_mapping"] = {scale_keys[i]: i for i in range(len(scale_keys))}
            for scale_name, scale in environment.items():
                metrics_df = scale[self.metrics_file_key]
                # transformation of the actual dataframe
                df_needed_columns = metrics_df[["Timestamp(s)", "energyUsage(Power usage of the host in W)"]]
                df_needed_columns = df_needed_columns.rename(
                    columns={"Timestamp(s)": "timestamp", "energyUsage(Power usage of the host in W)": "energyUsage"})
                filtered_data[policy_name][scale_name] = df_needed_columns.groupby(
                    ["timestamp"]).sum()  # file provides information per host, we need over all hosts

        return filtered_data, meta

    def to_energy_bar(self):
        pass

    def to_usage_plot(self):
        pass

    def to_makespan_plot(self):
        pass

    def to_cdf_plot(self):
        pass

    def to_performance_plot(self):
        pass

    def to_makespan_cdf_per_scale(self, trace_key, environment_key, file_name):
        meta = {
            "file_name": file_name,
        }
        filtered_data = {}

        for policy_name, policy in self.data[trace_key].items():
            for scale_name, scale in policy[environment_key].items():
                if scale_name not in filtered_data:
                    filtered_data[scale_name] = {}
                filtered_data[scale_name][policy_name] = \
                scale[self.makespan_file_key].rename(columns={"Makespan (s)": "makespan"})["makespan"]

        # make sure to have ascending order of scales
        meta["order_plots"] = self.__create_sorted_scale_list(filtered_data.keys())

        return filtered_data, meta

    def to_makespan_cdf_per_policy(self, trace_key, environment_key, file_name):
        meta = {
            "file_name": file_name,
        }
        filtered_data = {}

        for policy_name, policy in self.data[trace_key].items():
            if policy_name not in filtered_data:
                filtered_data[policy_name] = {}
            for scale_name, scale in policy[environment_key].items():
                filtered_data[policy_name][scale_name] = \
                scale[self.makespan_file_key].rename(columns={"Makespan (s)": "makespan"})["makespan"]

        return filtered_data, meta

    def to_utilization_table(self, trace_key, environment_key, file_name):
        """

        :param trace_key:
        :param environment_key:
        :param file_name:
        :return:
        """
        meta = {
            "file_name": file_name
        }

        # filtering
        filtered_data = pd.DataFrame(columns=["policy"])
        for policy_name, policy in self.data[trace_key].items():
            filtered_data = filtered_data.append({"policy": policy_name}, ignore_index=True)
            for scale_name, scale in policy[environment_key].items():
                df = scale[self.metrics_file_key][
                    ["Timestamp(s)", "cpuUsage(CPU usage of all CPUs of the host in MHz)"]]
                df = df.rename(columns={
                    "Timestamp(s)": "timestamp",
                    "cpuUsage(CPU usage of all CPUs of the host in MHz)": "cpuUsage",
                })
                host_df = scale[self.hostInfo_file_key]
                maxCapacity = host_df[["maxCapacity(MHz)"]].sum().values[0]
                df = df.groupby("timestamp").sum()
                df["cpuUsage"] = df["cpuUsage"].apply(lambda absoluteUsage: absoluteUsage / maxCapacity)
                mean = df["cpuUsage"].mean()

                scale_num = get_trailing_int(scale_name)
                if scale_num not in filtered_data.columns:
                    filtered_data[scale_num] = -1
                filtered_data.loc[filtered_data["policy"] == policy_name, scale_num] = mean
        filtered_data = filtered_data.set_index("policy")
        filtered_data = filtered_data.reindex(sorted(filtered_data.columns), axis=1)
        return filtered_data, meta

    def to_electricity_scale(self, trace_key, environment_key, file_name):
        meta = {
            "file_name": file_name,
        }
        filtered_data = {}

        for policy_name, policy in self.data[trace_key].items():
            if policy_name not in filtered_data:
                filtered_data[policy_name] = {}
            df_energy = pd.DataFrame(columns=["scale", "energyUsage"])

            for scale_name, scale in policy[environment_key].items():
                variableStore = scale[self.variableStore_file_key]
                readOutInterval = variableStore[variableStore["variable"] == "readOutInterval"]["value"].array[0]
                readOutInterval /= 60  # convert to minutes

                # we capture for every machine it's current energy consumption EC.
                # if we EC * readOutInterval, we will get the EC over a period of EC.
                # summing all these values up gives roughly the total energy consumption
                energyUsageDf = scale[self.metrics_file_key].rename(
                    columns={"energyUsage(Power usage of the host in W)": "energyUsage (kWh)"})[
                    ["Timestamp(s)", "energyUsage (kWh)"]]
                energyUsageDf = energyUsageDf.groupby("Timestamp(s)").sum()
                totalEnergyUsage = (energyUsageDf["energyUsage (kWh)"] * readOutInterval).sum()  # unit: Ws
                totalEnergyUsage /= (1000 * 3600)  # convert to kWh (1000 for k, 3600 for h)

                df_energy = df_energy.append(
                    {"scale": get_trailing_int(scale_name), "energyUsage (kWh)": totalEnergyUsage}, ignore_index=True)
            df_energy = df_energy.sort_values(by=["scale"])
            filtered_data[policy_name] = df_energy

        return filtered_data, meta

    def to_utilization_table_environment(self, trace_key, scale_key, file_name):
        meta = {}
        filtered_data = pd.DataFrame(columns=[])

        #for policy_name, policy in self.data[trace_key].items():


        return filtered_data, meta

    def __create_sorted_scale_list(self, keys):
        # make sure to have ascending order of scales
        order_plots = list(keys)
        order_plots.sort(key=lambda x: get_trailing_int(x))
        return order_plots
