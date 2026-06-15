import pandas as pd
import sqlite3

# load breaks_data

df_trades = pd.read_csv("trade_data.csv")
df_breaks = pd.read_csv("breaks_identified.csv")

# standardise column names
df_trades.columns = df_trades.columns.str.strip().str.lower().str.replace(" ","_")
df_breaks.columns = df_breaks.columns.str.strip().str.lower().str.replace(" ","_")

# create a data base memory
# ".memory:" means database lives in RAM, not saved to disk
# fast clean perfect for analysis 

conn = sqlite3.connect(":memory:")

# loading dataframe into database as tables
# to_sql() converts your pandas dataframe into a sql table
# index = false means don't add extra index columns
df_trades.to_sql("trades",conn,index=False,if_exists="replace")
df_breaks.to_sql("breaks",conn,index=False,if_exists="replace")

print("="*50)
print("database loaded")
print("="*50)
print("tables created:trades,breaks")

# QUERY 1 - total breaks and cash at risk by counterparty
# business question : which counterparty is most problematic 

query1="""
SELECT 
counterparty,COUNT(*)AS total_breaks,ROUND(SUM(abs_break_amount),2) AS total_cash_at_risk,
ROUND(AVG(abs_break_amount),2) AS avg_break_amount
FROM breaks
GROUP BY counterparty
ORDER BY total_cash_at_risk DESC
"""

result1=pd.read_sql_query(query1,conn)
print("\n" + "="*50)
print("QUERY 1 - breaks by counterparty")
print(result1.to_string())


# QUERY 2 - High risk breaks only
# business question : what needs immediate attention ?

query2 = """
SELECT
trade_id,counterparty,asset,expected_amounts,settled_amount,abs_break_amount,break_direction
FROM breaks
WHERE risk_level ="high"
ORDER BY abs_break_amount DESC
LIMIT 10
"""

result2=pd.read_sql_query(query2,conn)
print("\n"+"="*50)
print("QUERY 2 - top 10 high breaks")
print("="*50)
print(result2.to_string())

# QUERY 3 break rate by asset 
# business question : which assets cause most breaks?

query3="""
SELECT
asset,
COUNT(*)AS total_breaks,
ROUND(SUM(abs_break_amount),2) AS total_cash_at_risk,
ROUND(AVG(abs_break_amount),2) AS avg_break
FROM breaks
GROUP BY asset
ORDER BY total_breaks DESC
"""

result3 = pd.read_sql_query(query3,conn)
print("\n"+"="*50)
print("QUERY 3 - BREAKS BY ASSET")
print("="*50)
print(result3.to_string())

# QUERY 4 - UNDERPAYMENT VS OVERPAYMENT summary
# business question : which direction is more common

query4="""
SELECT
break_direction,
COUNT(*)AS total_amount,
ROUND(SUM(abs_break_amount),2) AS total_cash,
ROUND(AVG(abs_break_amount),2) AS avg_cash
FROM breaks
GROUP BY break_direction
ORDER BY total_cash DESC
"""

result4= pd.read_sql_query(query4,conn)
print("\n"+"="*50)
print("query 4 underpayment vs overpayment")
print("="*50)
print(result4.to_string())


# QUERY 5 CURRENCY RISK ANALYSIS 
# BUSINESS QUESTION : WHICH CURRENCY HAS MOST EXPOSURE?

query5="""
SELECT
currency,COUNT(*) AS total_breaks,ROUND(SUM(abs_break_amount),2) AS total_cash_at_risk
FROM breaks
GROUP BY currency
ORDER BY total_cash_at_risk DESC
"""

result5=pd.read_sql_query(query5,conn)
print("\n" + "=" *50)
print("query 5 - breaks by currency")
print(result5.to_string())

# query 6 risk level distribution with cash impact
# business question : how is risk spread across portfolio

query6="""
SELECT
risk_level,
COUNT(*) AS total_breaks,
ROUND(SUM(abs_break_amount),2) AS total_cash,
ROUND((COUNT(*)*100.0/(SELECT COUNT(*)FROM breaks)),2)
AS percentage_of_breaks
FROM breaks
GROUP BY risk_level
ORDER BY total_cash DESC
"""

result6 = pd.read_sql_query(query6,conn)
print("\n" + "="*50)
print("QUERY 6 RISK LEVEL DISTRIBUTION")
print("="*50)
print(result6.to_string())

# save all results to csv
result1.to_csv("sql_counterparty_analysis.csv",index=False)
result2.to_csv("sql_high_risk_break.csv",index=False)
result3.to_csv("sql_asset_analysis.csv",index=False)

print("\n" + "="*50)
print("sql analysis complete")
print("sql results saved to csv files")
print("="*50)

# close database connection
conn.close()
