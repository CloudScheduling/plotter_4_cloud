# Usage
1. Put the CSV files in folders, one per policy.
2. Adapt the following if needed in the notebooks in `Notebooks`:
   1. block 2: `data = reader.sort_dfs(["Random",])`: the list contains the names of the folders of the policies you want to analyze
   2. every other block: if you change the kind of trace/scale/environment and that is fixed in the experiment you want to visualize, you need to change the string accordingly.

Every string found in the transform functions corresponds to keys in the dictionary behind the variable `data`.
If you get errors of keys not being present, check that the key is present (in every dictionary). 
3. Run the notebook.
