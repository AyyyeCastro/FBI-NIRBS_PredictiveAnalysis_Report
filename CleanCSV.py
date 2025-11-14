import pandas as pd
import unicodedata
import os

def clean_column_name(col):
    # Normalize unicode, remove non-breaking spaces, remove newlines, strip
    if pd.isna(col):
        return ''
    col = str(col)
    col = unicodedata.normalize("NFKD", col) 
    col = col.replace('\n', ' ').replace('\r', ' ')
    col = col.replace('\xa0', ' ') 
    col = col.replace('\t', ' ')
    col = col.strip()
    col = ' '.join(col.split())
    return col

range_of_years = range(2011, 2019)
store_all_data = []
BASE_DIR = r'nibrs'
output_dir = r'nibrs\toCSV_CleanedByYear'  
os.makedirs(output_dir, exist_ok=True)

for year in range_of_years:
    file_path = os.path.join(BASE_DIR, str(year), f"{year}.csv")
    print(f"PROCESSING THE FOLLOWING: {file_path}")

    try:
        # Skip first 3 "junk-rows". Each CSV starts in this format, and is not relevant.
        df_raw = pd.read_csv(file_path, skiprows=3, header=None)

        # Grab first two rows, we'll be merging this into a single header later.
        header_row_1 = df_raw.iloc[0].fillna('')
        header_row_2 = df_raw.iloc[1].fillna('')
        headers = []
        
        for a, b in zip(header_row_1, header_row_2):
            # if both are NaN
            if pd.isna(a) and pd.isna(b):
                headers.append('')
            elif a and not b:
                headers.append(str(a).strip())
            elif not a and b:
                headers.append(str(b).strip())
            else:
                headers.append(f"{a.strip()} {b.strip()}")
       
        # copy only the data only from row 2 onwards, and make a fresh column/header.
        df_clean = df_raw.iloc[2:].copy()
        df_clean.columns = headers

        # Standardize, remove any 'Unnamed'/blank columns, or unwanted rows that don't start with an alphabet character
        df_clean = df_clean.loc[:, ~df_clean.columns.str.contains('^Unnamed')]
        df_clean = df_clean.loc[:, df_clean.columns.notna()]
        df_clean = df_clean[df_clean['State'].str.match(r'^[A-Za-z\s]+$', na=False)]
        df_clean.columns = [clean_column_name(c) for c in df_clean.columns]
        df_clean = df_clean[df_clean['State'] != 'Total']

        # Only select the columns you want for forecasting
        desired_columns = [
            'State',
            'Homicide Offenses',
            'Total Offenses',
            'Population Covered',
        ]
        available_cols = [c for c in desired_columns if c in df_clean.columns]
        df_clean = df_clean[available_cols]

        # Add 'Year' column
        df_clean['Year'] = year
        store_all_data.append(df_clean)

        # Save individual cleaned CSV for each year processed.
        cleaned_file_path = os.path.join(output_dir, f"{year}_cleaned.csv")
        df_clean.to_csv(cleaned_file_path, index=False)
        print(f"Saved cleaned file: {cleaned_file_path}")

    except Exception as e:
        print(f" SYSTEM ERROR: {file_path}: {e}\n")

# Combine all cleaned yearly data
combined_df = pd.concat(store_all_data, ignore_index=True)
combined_df.to_csv("nibrs_cleaned_2011_2018.csv", index=False)
print("Saved combined cleaned file: nibrs_cleaned_2011_2018.csv")
