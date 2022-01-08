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
        meta = {
            "file_name": file_name
        }

        # filtering
        filtered_data = pd.DataFrame(columns=["policy"])
        for policy_name, policy in self.data[trace_key].items():
            filtered_data = filtered_data.append({"policy": policy_name}, ignore_index=True)
            for scale_name, scale in policy[environment_key].items():
                mean = self.__calculateMeanUtilization(scale[self.metrics_file_key], scale[self.hostInfo_file_key])

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
        filtered_data = pd.DataFrame(columns=["policy", "scale", "energyUsage"])

        for policy_name, policy in self.data[trace_key].items():
            for scale_name, scale in policy[environment_key].items():
                metrics_df = scale[self.metrics_file_key]
                variable_df = scale[self.variableStore_file_key]
                total_energy_usage = self.__calculateTotalEnergyUsage(variable_df, metrics_df)

                filtered_data = filtered_data.append(
                    {
                        "policy": policy_name,
                        "scale": get_trailing_int(scale_name),
                        "energyUsage": total_energy_usage,
                    }, ignore_index=True)
            filtered_data = filtered_data.sort_values(by=["scale"])

        return filtered_data, meta

    def to_makespan_cdf_per_environment(self, trace_key, scale_key, file_name):
        meta = {
            "file_name": file_name,
        }
        filtered_data = {}

        for policy_name, policy in self.data[trace_key].items():
            for env_name, env in policy.items():
                if env_name not in filtered_data:
                    filtered_data[env_name] = {}

                makespan_df = env[scale_key][self.makespan_file_key]
                filtered_data[env_name][policy_name] = makespan_df.rename(columns={"Makespan (s)": "makespan"})[
                    "makespan"]

        return filtered_data, meta

    def to_energy_exp_environment(self, trace_key, scale_key, file_name):
        meta = {
            "file_name": file_name
        }
        filtered_data = pd.DataFrame(columns=["policy", "environment", "energyUsage"])

        for policy_name, policy in self.data[trace_key].items():
            for env_name, env in policy.items():
                variable_df = env[scale_key][self.variableStore_file_key]
                metrics_df = env[scale_key][self.metrics_file_key]
                total_energy = self.__calculateTotalEnergyUsage(variable_df, metrics_df)

                filtered_data = filtered_data.append({
                    "policy": policy_name,
                    "environment": env_name,
                    "energyUsage": total_energy,
                }, ignore_index=True)

        return filtered_data, meta

    def to_utilization_table_environment(self, trace_key, scale_key, file_name):
        filtered_data = pd.DataFrame(columns=["policy"])

        meta = {
            "file_name": file_name,
        }

        for policy_name, policy in self.data[trace_key].items():
            filtered_data = filtered_data.append({"policy": policy_name}, ignore_index=True)
            for env_name, env in policy.items():
                if env_name not in filtered_data.columns:
                    filtered_data[env_name] = -1
                metrics_df = env[scale_key][self.metrics_file_key]
                host_df = env[scale_key][self.hostInfo_file_key]
                filtered_data.loc[filtered_data["policy"] == policy_name, env_name] = self.__calculateMeanUtilization(
                    metrics_df, host_df)
        filtered_data = filtered_data.set_index("policy")

        return filtered_data, meta

    def to_utilization_table_workload(self, environment_key, scale_key, file_name):
        filtered_data = pd.DataFrame(columns=["policy"])

        meta = {
            "file_name": file_name,
        }

        for trace_name, trace in self.data.items():
            filtered_data[trace_name] = -1
            for policy_name, policy in trace.items():
                if policy_name not in filtered_data["policy"].values:
                    filtered_data = filtered_data.append({"policy": policy_name}, ignore_index=True)

                metrics_df = policy[environment_key][scale_key][self.metrics_file_key]
                host_df = policy[environment_key][scale_key][self.hostInfo_file_key]
                filtered_data.loc[filtered_data["policy"] == policy_name, trace_name] = self.__calculateMeanUtilization(
                    metrics_df, host_df)
        filtered_data = filtered_data.set_index("policy")

        return filtered_data, meta

    def to_makespan_cdf_per_workflow(self, environment_key, scale_key, file_name):
        meta = {
            "file_name": file_name,
        }
        filtered_data = {}

        for trace_name, trace in self.data.items():
            filtered_data[trace_name] = {}
            for policy_name, policy in trace.items():
                makespan_df = policy[environment_key][scale_key][self.makespan_file_key]
                filtered_data[trace_name][policy_name] = makespan_df.rename(columns={"Makespan (s)": "makespan"})[
                    "makespan"]

        return filtered_data, meta

    def to_energy_exp_workload(self, environment_key, scale_key, file_name):
        meta = {
            "file_name": file_name
        }
        filtered_data = pd.DataFrame(columns=["policy", "trace", "energyUsage"])

        for trace_name, trace in self.data.items():
            for policy_name, policy in trace.items():
                file_dict = policy[environment_key][scale_key]
                variable_df = file_dict[self.variableStore_file_key]
                metrics_df = file_dict[self.metrics_file_key]
                total_energy = self.__calculateTotalEnergyUsage(variable_df, metrics_df)

                filtered_data = filtered_data.append({
                    "policy": policy_name,
                    "trace": trace_name,
                    "energyUsage": total_energy,
                }, ignore_index=True)

        return filtered_data, meta

    def __create_sorted_scale_list(self, keys):
        # make sure to have ascending order of scales
        order_plots = list(keys)
        order_plots.sort(key=lambda x: get_trailing_int(x))
        return order_plots

    def __calculateTotalEnergyUsage(self, variable_df, metrics_df):
        readOutInterval = variable_df[variable_df["variable"] == "readOutInterval"]["value"].array[0]
        readOutInterval /= 60  # convert to minutes

        # we capture for every machine it's current energy consumption EC.
        # if we EC * readOutInterval, we will get the EC over a period of EC.
        # summing all these values up gives roughly the total energy consumption
        energyUsageDf = metrics_df.rename(
            columns={"energyUsage(Power usage of the host in W)": "energyUsage (kWh)"})[
            ["Timestamp(s)", "energyUsage (kWh)"]]
        energyUsageDf = energyUsageDf.groupby("Timestamp(s)").sum()
        totalEnergyUsage = (energyUsageDf["energyUsage (kWh)"] * readOutInterval).sum()  # unit: Ws
        totalEnergyUsage /= (1000 * 3600)  # convert to kWh (1000 for k, 3600 for h)

        return totalEnergyUsage

    def __calculateMeanUtilization(self, metrics_df, host_df):
        """
        Utilization is the mean utilization over all points in time where there was something captured (relative)
        :param metrics_df:
        :param host_df:
        :return:
        """
        df = metrics_df[
            ["Timestamp(s)", "cpuUsage(CPU usage of all CPUs of the host in MHz)"]]
        df = df.rename(columns={
            "Timestamp(s)": "timestamp",
            "cpuUsage(CPU usage of all CPUs of the host in MHz)": "cpuUsage",
        })
        max_capacity = host_df[["maxCapacity(MHz)"]].sum().values[0]
        df = df.groupby("timestamp").sum()
        df["cpuUsage"] = df["cpuUsage"].apply(lambda absoluteUsage: absoluteUsage / max_capacity)
        return df["cpuUsage"].mean()
