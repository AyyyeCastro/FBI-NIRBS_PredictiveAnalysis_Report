import pandas as pd
import numpy as np
import os
import sys


# If using "\" relative paths, just annotate 'r' before the path. ex. r"path\name\here".
# --- Configuration: Set your file paths here ---
PATH_ACTUAL_2019 = "nibrs/toCSV_CleanedByYear/2019_cleaned.csv"
PATH_LINEAR_PRED = "predictive_output/2019_predictiveAnalysis_LinearRegression.csv"
PATH_LAG_TOTAL_PRED = "predictive_output/2019_predictiveAnalysis_LagPanel_Total.csv"
PATH_LAG_HOMICIDE_PRED = "predictive_output/2019_predictiveAnalysis_LagPanel_Homicide.csv"

def load_and_prep_csv(filepath, use_cols, rename_cols):
    try:
        df = pd.read_csv(filepath)
        df = df[use_cols] 
        df.columns = rename_cols
        return df
    except FileNotFoundError:
        # Keep error output
        print(f"ERROR: File not found at: {filepath}", file=sys.stderr)
        return None
    except KeyError:
        # Keep error output
        print(f"ERROR: Columns not found in {filepath}.", file=sys.stderr)
        print(f"       Expected: {use_cols}", file=sys.stderr)
        return None
    except Exception as e:
        # Keep error output
        print(f"ERROR loading {filepath}: {e}", file=sys.stderr)
        return None

def run_accuracy_comparison():
    files_to_load = [
        {
            "name": "actual",
            "path": PATH_ACTUAL_2019,
            "use_cols": ['State', 'Total Offenses', 'Homicide Offenses'],
            "rename_cols": ['State', 'Actual Total', 'Actual Homicide']
        },
        {
            "name": "linear",
            "path": PATH_LINEAR_PRED,
            "use_cols": ['State', 'Total Offenses', 'Homicide Offenses'],
            "rename_cols": ['State', 'LR Total Forecast', 'LR Homicide Forecast']
        },
        {
            "name": "lag_total",
            "path": PATH_LAG_TOTAL_PRED,
            "use_cols": ['State', 'Predicted_Total_Offenses_2019'],
            "rename_cols": ['State', 'AR Total Forecast']
        },
        {
            "name": "lag_homicide",
            "path": PATH_LAG_HOMICIDE_PRED,
            "use_cols": ['State', 'Predicted_Homicide_Offenses_2019'],
            "rename_cols": ['State', 'AR Homicide Forecast']
        }
    ]

    loaded_dfs = {}
    
    for file_info in files_to_load:
        df = load_and_prep_csv(
            file_info["path"], 
            file_info["use_cols"], 
            file_info["rename_cols"]
        )
        
        # stop the script if loading error
        if df is None:
            print("\n SYSTEM ERROR: ", file=sys.stderr)
            return
            
        loaded_dfs[file_info["name"]] = df


    # Start with the original FBI data then merge the modeled data for MAE calc
    df_compare = loaded_dfs['actual']
    df_compare = pd.merge(df_compare, loaded_dfs['linear'], on='State', how='inner')
    df_compare = pd.merge(df_compare, loaded_dfs['lag_total'], on='State', how='inner')
    df_compare = pd.merge(df_compare, loaded_dfs['lag_homicide'], on='State', how='inner')
    df_compare['Error_Linear_Total'] = (df_compare['LR Total Forecast'] - df_compare['Actual Total']).abs()
    df_compare['Error_Lag_Total'] = (df_compare['AR Total Forecast'] - df_compare['Actual Total']).abs()
    df_compare['Error_Linear_Homicide'] = (df_compare['LR Homicide Forecast'] - df_compare['Actual Homicide']).abs()
    df_compare['Error_Lag_Homicide'] = (df_compare['AR Homicide Forecast'] - df_compare['Actual Homicide']).abs()
    mae_linear_total = df_compare['Error_Linear_Total'].mean()
    mae_lag_total = df_compare['Error_Lag_Total'].mean()
    mae_linear_homicide = df_compare['Error_Linear_Homicide'].mean()
    mae_lag_homicide = df_compare['Error_Lag_Homicide'].mean()
    
    # Create these new columns into the Dataframe since we'll be using them for later analysis.
    df_compare['Overall_MAE_Linear_Total'] = mae_linear_total
    df_compare['Overall_MAE_Lag_Total'] = mae_lag_total
    df_compare['Overall_MAE_Linear_Homicide'] = mae_linear_homicide
    df_compare['Overall_MAE_Lag_Homicide'] = mae_lag_homicide
        
    # output into a .csv, since we'll be working it into PowerBI
    output_dir = "predictive_output"
    os.makedirs(output_dir, exist_ok=True)
    comparison_file = os.path.join(output_dir, "Model_MAE_Comparison.csv")
    df_compare.to_csv(comparison_file, index=False)

if __name__ == "__main__":
    run_accuracy_comparison()