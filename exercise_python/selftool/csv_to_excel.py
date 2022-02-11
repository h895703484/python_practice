import pandas as pd

def csv_to_xlsx(c,e):
    csv=pd.read_csv(c,encoding='utf-8',index_col=False)
    csv.to_excel(e,sheet_name='case')

if __name__=="__main__":
    csv_to_xlsx("1.csv","1.xlsx")