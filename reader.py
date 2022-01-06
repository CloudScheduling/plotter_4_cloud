import pandas as pd
import numpy as np
import os


def sort_dfs(paths):
    """
    Creates a multi-dimensional dictionary based on all policies provided.
    The function takes the filename of a csv file, takes the attributes contained in it
    and places the file as a dataframe under the attributes contained in the filename.

    Every file follows the pattern "traceId_policy_environmentType_scale_fileType.csv".
    The corresponding dataframe is then found in dict[traceId][policy][environmentType][scale][fileType].

    An error is thrown if the number of attributes is wrong.
    :param paths: names of the folders (relative to current working directory) where the csv files are contained in. Nested folders are not considered and need to be added manually.
    :return: dictionary with keys as described above. The last elements are the dataframes with the metrics captured from OpenDC.
    """

    final_data = {}

    for path in paths:
        for _, _, files in os.walk(path):
            for file in files:
                file_name_with_extension = os.path.basename(file)
                file_name = file_name_with_extension.split(".")[0]

                # extract tokens from the file found
                tokens = file_name.split("_")
                exptected_number_tokens = 5  # [policy, trace, kind, scale, file_kind]
                if len(tokens) != exptected_number_tokens:
                    raise RuntimeError(
                        f"Error splitting name of {file}: found {len(tokens)} tokens, expected {exptected_number_tokens}")

                # create missing keys recursively
                temp_data_ref = final_data
                for token in tokens[0:-1]:  # -1: last key is special, this will be the dataframe
                    if token not in temp_data_ref:
                        temp_data_ref[token] = {}
                    temp_data_ref = temp_data_ref[token]

                path_relative_to_root = os.path.join(path, file_name_with_extension)
                temp_data_ref[tokens[-1]] = pd.read_csv(path_relative_to_root)

    return final_data
