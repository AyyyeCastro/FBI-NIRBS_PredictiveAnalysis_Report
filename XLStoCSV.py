import pandas as pd
from pathlib import Path
import sys

def convert_all_xls_to_csv(base_dir_path):

    base_dir = Path(base_dir_path)
    if not base_dir.is_dir():
        print(f"SYSTEM ERROR: Base directory could be not found: {base_dir}")
        sys.exit(1)


    xls_files = list(base_dir.rglob("*.xls"))
    if not xls_files:
        print("No .XLS files could be found. Please ensure proper base directory was specified.")
        return    
        
    print(f"\n The following: {len(xls_files)} file(s) were found to convert.")
    print(f"\nConverting all .XLS files to .CSV found in: {base_dir}")
    total_files_converted = 0
    total_files_failed = 0

    for xls_path in xls_files:
        csv_path = xls_path.with_suffix(".csv")
        
        try:
            relative_path = xls_path.relative_to(base_dir)
            print(f"\nConverting: {relative_path}")
            
            # Read the Excel file (first sheet by default)
            df = pd.read_excel(xls_path)
            
            # Save as CSV
            df.to_csv(csv_path, index=False)
            
            print(f"  Success: {csv_path.relative_to(base_dir)}")
            total_files_converted += 1
            
        except Exception as e:
            print(f"  [ERROR] Failed to convert {relative_path}: {e}")
            total_files_failed += 1
                
    print("\n -- PROCESS COMPLETED -- ")
    print(f"Total files converted: {total_files_converted}")
    print(f"Total files failed:    {total_files_failed}")


if __name__ == "__main__":
    

    setBase = "C:/Users/acast/OneDrive/Documents/Repos/FBI-NIRBS_PredictiveAnalysis_Report/nibrs"
    ROOT_DIRECTORY_TO_SEARCH = setBase
    convert_all_xls_to_csv(ROOT_DIRECTORY_TO_SEARCH)