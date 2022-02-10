import pandas as pd
import json

with open("result.json", "r", encoding="utf8") as f:
    res_data = json.load(f)

res_df = pd.DataFrame(res_data)
res_df.to_csv("north_interface_result.csv", encoding="utf8")

