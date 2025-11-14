import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import os

# Load the cleaned CSV
df = pd.read_csv("nibrs_cleaned_2011_2018.csv")

# Melt the df so each row is state-category-year
categories = ['Homicide Offenses', 'Total Offenses', 'Population Covered']
df_long = df.melt(id_vars=['State', 'Year'], value_vars=categories,
                  var_name='Category', value_name='Count')

# Convert Count to numeric and drop missing values
df_long['Count'] = pd.to_numeric(df_long['Count'], errors='coerce')
df_long.dropna(subset=['Count'], inplace=True)

# Forecast 2019 for each state and category
predictNextYear = []
for (state, category), group in df_long.groupby(['State', 'Category']):
    X = group['Year'].values.reshape(-1, 1)
    y = group['Count'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    modeledValue = model.predict(np.array([[2019]]))[0]
    predictNextYear.append({
        'State': state,
        'Category': category, 
        'Prediction': modeledValue
    })

dict_to_DF = pd.DataFrame(predictNextYear)

# Pivot so each category becomes a column, to follow the standarized format.
standarizeDF = dict_to_DF.pivot(index='State', columns='Category', values='Prediction').reset_index()
cols = ['State'] + [c for c in categories]
standarizeDF = standarizeDF[cols]

# Ensure output folder exists
output_dir = "predictive_output"
os.makedirs(output_dir, exist_ok=True)

# Save filee
standarizeDF.to_csv(os.path.join(output_dir, "2019_predictiveAnalysis_LinearRegression.csv"), index=False)
print(standarizeDF.head())
