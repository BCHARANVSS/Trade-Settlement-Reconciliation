import pandas as pd # pyright: ignore[reportMissingModuleSource]
import numpy as np
import random
from datetime import datetime,timedelta

# creating data lines

np.random.seed(42)
n=50000

#trade id's generating between with starting are filled up z.fill(6)zeros

trade_ids = [f"TRD{str(i).zfill(6)}" for i in range(1,n+1)]

# the terms and other data points

counter_parties = ["GOLDMAN SACHS","JP MORGAN","MORGAN STANLEY","BARCLAYS","CITI BANK","HSBC","DEUTSCHE BANK","UBS"]
assets = ["AAPL",'MSFT','GOOGL','AMZN','TSLA','NIFTY50','SENSEX','RELIANCE','TCS','INFY']
currencies = ['USD','GBP','EUR','INR','JPY']
trade_type = ['BUY','SELL']
statuses = ['SETTLED','PENDING','FAILED','MISMATCHED']

#creating random trades b/w the year & amount rounding off two decimals

base_date = datetime(2025,1,1)
trade_dates = [base_date+timedelta(days=random.randint(0,365)) for _ in range(n)]
settlement_dates = [d+timedelta(days=random.randint(1,5)) for d in trade_dates]
expected_amounts = np.round(np.random.uniform(1000,5000000,n),2)

# errors at 15% rate 

settled_amounts = expected_amounts.copy()
error_indices = np.random.choice(n, size=int(n*0.15),replace=False)
settled_amounts[error_indices] = np.round(settled_amounts[error_indices]*np.random.uniform(0.5,1.5,len(error_indices)),2)
# creating data frame

df = pd.DataFrame({
    "TRADE_ID": trade_ids,
    "TRADE_DATE": trade_dates,
    "settlement_date": settlement_dates,
    "counterparty": np.random.choice(counter_parties,n),
    "asset":np.random.choice(assets,n),
    "trade_type":np.random.choice(trade_type,n),
    "currency":np.random.choice(currencies,n),
    "expected_amounts": expected_amounts,
    "settled_amount" : settled_amounts,
    "status" : np.random.choice(statuses,n,p=[0.70,0.15,0.08,0.07])
})

# csv files

df.to_csv("trade_data.csv",index=False)
print(f"dataset generated: {len(df)} rows")
print(df.head())


