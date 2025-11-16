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
## Forecasted [Homicide] Offenses Accuracy VS FBI NIBRS 2019 Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-2.png)
## Forecasted [Total] Offenses VS FBI NIBRS 2019 Data
![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-1.png)
## Linear VS Autoregressive MAE & Accuracy [Total] 
While the accuracy gap between the Linear and Autoregression Models are only 8.02 percentage points off, it's important to look at the scoring like a test. The Autoregression Model had a forecasting accuracy of 91.69% for total offenses, which means it predicted 8.31% of them inaccurately (errors).  Meanwhile, the Linear Regression Model had a forecasting accuracy of 83.67% for total offenses. Again, this means it predicted 16.33% of them inaccurately (errors). 

This means that despite the 8.02 accuracy gap between the two models, the Linear Regression Model also had double the error rate in predictive capability for the 'Total Offenses' dataset (16.33% vs 8.31%). That is the error magnatitude value of 96.58%.

![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-3.png)
## Linear VS Autoregressive MAE & Accuracy [Homicide] 
As previously outlined, despite the 9.18 percentage point difference, the error rate of each model is a layer which must be considered. With the Linear Regression mMdel producing approximately 31.82% more errors in forecasting capability for the 'Homicide Offenses' dataset, than the Autoregression Model. That is the error magnatitude value of 31.82% displayed.

![Dashboard](REPORT-MATERIALS/powerBI_dashboard/PNG/powerBI_dashboard_toPNG-4.png)
