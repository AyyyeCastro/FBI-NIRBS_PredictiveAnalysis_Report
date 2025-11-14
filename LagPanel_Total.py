import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import os


df = pd.read_csv("nibrs_cleaned_2011_2018.csv")

# very important to sort by state and year for lagging.
df = df.sort_values(by=['State', 'Year'])

# Tototal offenses will be the 'y' variable.
df['Total_Offenses_Lag1'] = df.groupby('State')['Total Offenses'].shift(1)
df['Total_Offenses_Lag2'] = df.groupby('State')['Total Offenses'].shift(2)

# Include the Population sample from the databases.
df['Population_Lag1'] = df.groupby('State')['Population Covered'].shift(1)

# Drop the NaN rows (the first 2 years for each state)
df_model = df.dropna()

print("DataFrame with Lag Features:")
print(df_model.head())

# now we can define (x,y). Using the sampled population size, predict the total offenses.
features = ['Total_Offenses_Lag1', 'Total_Offenses_Lag2', 'Population_Lag1']
target = 'Total Offenses'
X = df_model[features]
y = df_model[target]

# train a model on ALL the data with basic linear patterns.
model = LinearRegression()
model.fit(X, y)

print("\n Linear Model trained successfully.")

# Grab the two most recent years. Since our dataset is limited, 2011 - 2018. We do not want to go further than two lags
# until we view the results first.
df_2018 = df[df['Year'] == 2018].set_index('State')
df_2017 = df[df['Year'] == 2017].set_index('State')

# 7. Create the feature set for our 2019 prediction
X_predict_2019 = pd.DataFrame({
    'Total_Offenses_Lag1': df_2018['Total Offenses'],
    'Total_Offenses_Lag2': df_2017['Total Offenses'],
    'Population_Lag1': df_2018['Population Covered']
}).dropna() # Drop states that might be missing data

# forecast
predictions_2019 = model.predict(X_predict_2019)

# formatting
df_predictions = X_predict_2019.copy()
df_predictions['State'] = df_predictions.index
df_predictions['Predicted_Total_Offenses_2019'] = predictions_2019

print("\nPredictions for 2019:")
print(df_predictions.head())

# Save to CSV for Power BI
output_dir = "predictive_output"
os.makedirs(output_dir, exist_ok=True)
df_predictions.to_csv(os.path.join(output_dir, "2019_predictiveAnalysis_LagPanel_Total.csv"), index=False)

