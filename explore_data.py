import pandas as pd 

#loading data set we created

df=pd.read_csv("trade_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# strings multiplication & organizing the data_set

print("="*50)
print("dataset overview")
print("="*50)
print(f"total rows : {df.shape[0]}")
print(f"total columns : {df.shape[1]}")
print(f"column names : {list(df.columns)}")

# the data and its types columns & rows

print("\n"+"="*50)
print("column data types")
print("="*50)
print(df.dtypes)

print("\n" + "="*50)
print("first 5 rows")
print("="*50)
print(df.head().to_string())

# missing values

print("\n"+ "="*50)
print("misisng values per column")
print("="*50)
print(df.isnull().sum())

print ("\n"+"="*50)
print("duplicate rows")
print("="*50)
print(f" total duplicates : {df.duplicated().sum()}")

# describe()

print ("\n"+"="*50)
print("statistical summary")
print("="*50)
print(df.describe())

# distribution 

print("\n" + "="*50)
print("trade status distribution")
print("="*50)
status_counts = df["status"].value_counts()
status_pct = df["status"].value_counts(normalize=True)*100
status_summary = pd.DataFrame({
    "count":status_counts,
    "percentage":status_pct.round(2)
})
print(status_summary)

# counter party distribution
print("\n"+"="*50)
print("trades per counterparty")
print("="*50)
print(df["currency"].value_counts())


print("\n"+"="*50)
print("trades per counterparty")
print("="*50)
print(df["counterparty"].value_counts())





