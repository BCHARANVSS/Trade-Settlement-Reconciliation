import pandas as pd 
import numpy as np 

#loading the data 

df = pd.read_csv("trade_data.csv")

#columns standardise
df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")

print("="*50)
print("RECONCILIATION PIPELINE STARTING")
print("="*50)
print(f"total trades loaded : {df.shape[0]}")

# calculate break amount for every single trade 

df["break_amount"] = df["expected_amounts"] - df["settled_amount"]

#break amount = 0 clean
# break amount +ve we recieved/paid less than expected
# break amount -ve we recieved/paid more than expected 

print("\n" + "="*50)
print("="*50)
print(f"sample break amounts (first 5 rows):")
print(df[["trade_id","expected_amounts","settled_amount","break_amount"]].head())

# identifying actual breaks  # a break exists only when break amount is not zero 

break_df = df[df["break_amount"]!=0]

clean_df = df[df["break_amount"]==0]

print("\n"+"="*50)
print("BREAK IDENTIFICATION")
print("="*50)
print(f"total clean trades : {len(clean_df)}")
print(f"total breaks found : {len(break_df)}")
print(f"break rate : {round(len(break_df)/len(df)*100,2)}%")



# absolute break
# break can be negative over paid 
# for risk we have to look for the size not the direction so we use the abs() to conv -ve into +ve

break_df = break_df.copy()
break_df["abs_break_amount"] = break_df["break_amount"].abs()

# risk categorisation

# every break gets a risk level based on the cash impact
# high risk break get prioritised

def assign_risk(amount):
    if amount>=1000000:
        return "high"
    elif amount>=100000:
        return "medium"
    else:
        return "low"
    
# running this function on every single row

break_df["risk_level"] = break_df["abs_break_amount"].apply(assign_risk)

print("\n"+ "="*50)
print("risk categorisation")
print("="*50)
risk_summary = break_df["risk_level"].value_counts()
print(risk_summary)

# break direction
# +ve or -ve was the break under(received less) or over payments (received more)

break_df["break_direction"] = break_df["break_amount"].apply(
    lambda x : "underpayment" if x > 0 else "over payment"
)
print("\n"+"="*50)
print("break direction")
print("="*50)
print(break_df["break_direction"].value_counts())

# summary statistics on breaks

print("\n"+"="*50)
print("break summary statistics")
print("="*50)
print(f"total cash at risk :",f"{break_df['abs_break_amount'].sum():,.2f}")
print (f"average break amount:",f"{break_df['abs_break_amount'].mean():,.2f}")
print(f"largest single break :", f"{break_df['abs_break_amount'].max():,.2f}")
print(f"smallest break :"f"{break_df['abs_break_amount'].min():,.2f}")

# top 10 highest risk breaks 

print("\n" + "="*50)
print("top 10 highest risk breaks")
print("="*50)
top_breaks = break_df.nlargest(10,"abs_break_amount")[
    ["trade_id","counterparty","asset","expected_amounts","settled_amount","abs_break_amount","risk_level","break_direction"]
]
print(top_breaks.to_string())

# counter party break analysis

print("\n" + "="*50)
print("BREAKS BY COUNTERPARTY")
print("="*50)
counterparty_breaks = break_df.groupby("counterparty").agg(
    total_breaks = ("trade_id","count"),
    total_cash_at_risk = ("abs_break_amount","sum"),
    average_break = ("abs_break_amount","mean")
).round(2).sort_values("total_cash_at_risk",ascending = False)

print(counterparty_breaks.to_string())

# save breaks to csv for next steps

break_df.to_csv("breaks_identified.csv",index = False)
print(f"breaks saved to breaks_identified.csv")
print(f"total breaks exported : {len(break_df)}")
print("="*50)




