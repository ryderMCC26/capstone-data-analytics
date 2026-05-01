# capstone-data-analytics
Final Capstone Project for Data Analytics Course

This capstone project analyzes transportation inequality in Maricopa County, Arizona by examining how commute time is related to socioeconomic factors such as median household income and vehicle access at the ZIP code level.

The project combines data analysis, statistical modeling, and dashboard visualization to explore whether lower-income areas or areas with limited access to vehicles experience longer commute times. Results are presented through both regression analysis and an interactive Power BI dashboard.



Technologies Used:
Python (pandas) – Data cleaning and transformation

Microsoft Excel – Regression analysis

Power BI – Dashboard visualization

PolicyMap – Data source (ZIP code-level socioeconomic data)

GitHub – Version control and project documentation

How to Reproduce the Analysis

Download Data

Obtain datasets from PolicyMap:

Average Travel Time to Work - Median Household Income - Households with No Vehicle Available - Total Population - Run Data Cleaning Script - Navigate to the scripts/ folder

Run: python clean_policymap_data.py
 This will generate a cleaned dataset: cleaned_transportation_capstone_data.csv


There is a excel file with the Regression Analysis labeled : Data_Regression
Otherwise:
Run Regression Analysis
Open the cleaned dataset in Excel
Use Data Analysis ToolPak → Regression
Dependent variable: avg_commute_minutes
Independent variables:
median_household_income
no_vehicle_percent
Open Power BI Dashboard
Navigate to the visualizations/ folder
Open the .pbix file in Power BI
Refresh data if needed


Author
Ryder Brown

Notes
All data is aggregated at the ZIP code level
ZCTA (Census ZIP approximations) may differ slightly from USPS ZIP codes
Regression results show weak statistical relationships, highlighting the importance of geographic factors in transportation inequality
