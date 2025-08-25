import pandas as pd
import glob

csv_files = glob.glob("/Users/angelikiandreadi/Library/CloudStorage/OneDrive-unine.ch/Unine/Semestre_4/Environnement_Python/csv_dates_naissance/*.csv")
print(csv_files)

dfs = [pd.read_csv(f) for f in csv_files]
combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv("/Users/angelikiandreadi/Downloads/combined_singers.csv", index=False)

