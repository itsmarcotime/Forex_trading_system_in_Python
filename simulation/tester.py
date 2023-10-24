import pandas as pd

from timeit import default_timer as timer

df = pd.read_pickle("./data/GBP_JPY_M5.pkl")

print(f"Total Rows:{df.shape[0]}")

start = timer()
for index, row in df.iterrows():
    val1 = row.mid_c * 12
    val2 = row.mid_h - 14
print(f"df.iterrows() -> {(timer()-start):.4f}s")

start = timer()
for index in range(df.shape[0]):
    val1 = df.mid_c.iloc[index] * 12
    val2 = df.mid_h.iloc[index] - 14
print(f"iloc[index]   -> {(timer()-start):.4f}s")

start = timer()
ar1 = df.mid_c.array
ar2 = df.mid_h.array
for index in range(ar1.shape[0]):
    val1 = ar1[index] * 12
    val2 = ar2[index] - 14
print(f"ar1[index]    -> {(timer()-start):.4f}s")

start = timer()
items = [df.mid_c.array,df.mid_h.array]
for index in range(ar1.shape[0]):
    val1 = items[0][index] * 12
    val2 = items[1][index] - 14
print(f"items[index]    -> {(timer()-start):.4f}s")
