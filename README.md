**Author: Andrew Castro**  

# FBI NIBRS Crime Forecasting 
## Utilizing 2011 - 2018 crime archives to forecast and compare against 2019 data.
This project builds an end-to-end analytics pipeline to clean, process, and forecast FBI NIBRS crime statistics across 9 years of multi-state data. It includes full data engineering, predictive modeling, MAE evaluation, and a multi-page Power BI dashboard that compares forecasted vs actual 2019 crime counts from the FBI NIBRS archives.

**Project Summary**

* Processed 9 years of archived FBI NIBRS state-level crime data from 2011-2019.
* Developed an automatic data-cleaning pipeline to convert messy XLS files into usable and standarized CSVs. 
* Utilized predictive models through Python libraries to forecast 2019 Homicide + Total Offense counts.
* Evaluated model performance using Mean Absolute Error (MAE) as a base factor.
* Engineered a 4-page interactive Power BI dashboard visualizing trends, forecasts, and predictive model accuracy.

**Data Engineering**
* Programmed a Python script to efficiently convert all XLS archives to CSV.
* Reconstructed multi-row, irregular headers into column-normalization
* Removed malformed rows, merged multi-year datasets into unified analytical model, and standardized column name schema.

  -> Using real-world 2019 FBI NIBRS data as ground truth:
* Calculated per-state forecasting absolute error
* Calculated overall MAE for each model (linear/autoregression) and each metric.
* Identified which model performed best for each crime category.

**Power BI Dashboards**
* Model forecasting accuracy and analysis
* Forecast vs real-world metrics
* Total vs homicide trends
* US-wide state coverage variations

PNG copies and a downloadable PDF are included in this repo.
## Forecasted [Homicide] Offenses VS FBI NIBRS Reported Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-2.png)
## Forecasted [Total] Offenses VS FBI NIBRS Reported Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-1.png)
## Linear VS Autoregressive MAE [Total] & FBI NIBRS Reported Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-3.png)
## Linear VS Autoregressive MAE [Homicide] & FBI NIBRS Reported Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-4.png)
