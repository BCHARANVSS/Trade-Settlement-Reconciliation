# Trade Settlement Reconciliation Project

## About this project

I'm a first-year BSc Data Science student. I built this project to learn how trade reconciliation works in bank operations, and to practice Python, SQL, R, Excel and Tableau on something real instead of small textbook examples.

I generated a dataset of 50,000 trades (with some built-in errors), then found and analysed the trades where the expected amount and the settled amount don't match. These mismatches are called breaks.

## What I found

- 7,500 out of 50,000 trades had breaks (15% break rate) — this matches the error rate I built into the data
- Total cash at risk from these breaks: $4.74 billion
- Largest single break: $2.49 million (Morgan Stanley, INFY trade)
- High risk breaks were 23.7% of all breaks but made up 55% of the total cash at risk
- Morgan Stanley had the most exposure ($631.7M across 986 breaks)
- GBP trades had the highest currency exposure ($1.01B)

## Tools used

Python — generated the data, calculated break amounts, assigned risk levels (high/medium/low) and break direction (overpayment/underpayment)

SQL — wrote queries on the break data to answer questions like which counterparty has the most breaks, and what percentage of breaks fall into each risk category

R — calculated statistics on the break amounts and made some charts. Mean was higher than median, which means most breaks are smaller but a few large ones pull the average up

Excel — built a script that generates a formatted multi-sheet report (summary, top breaks, counterparty breakdown) so it doesn't have to be done by hand

Tableau — built a dashboard showing breaks by counterparty, risk level, and currency

## Files

- generate_data.py — creates the dataset
- explore_data.py — checks for missing values, duplicates, basic stats
- reconciliation.py — main logic, finds breaks and assigns risk levels
- sql_queries.py — SQL queries on the breaks
- r_analysis.R — statistics and charts
- excel_report.py — generates the Excel report
- GS_break_report.xlsx — the Excel output
- trade_data.csv / breaks_identified.csv — the data
- chart1-3.png — charts from R

## Tableau Dashboard link 

https://tinyurl.com/4baem3cj

## Note

This is a learning project. I'm still building up these skills, and this was a way to use them together on something close to what operations teams actually do.
