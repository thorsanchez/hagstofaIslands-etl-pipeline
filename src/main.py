import requests
import json
from clean import parse_data
from export import create_pivot_and_export, plot_revenue_trend
"""
ætla bara sækja upplýsingatækni rekstratekjur
https://px.hagstofa.is/pxis/pxweb/is/Atvinnuvegir/Atvinnuvegir__fyrirtaeki__afkoma__1_afkoma/FYR08000.px/table/tableViewLayout2/
"""

API_URL = "https://px.hagstofa.is:443/pxis/api/v1/is/Atvinnuvegir/fyrirtaeki/afkoma/1_afkoma/FYR08000.px"

QUERY = {
    "query": [
        {"code": "Atvinnugrein", "selection": {"filter": "item", "values": ["48"]}},
        # Hversu mörg fyrirtæki, Velta, Production, Hagnaður, Starfsmenn
        {"code": "Breyta", "selection": {"filter": "item", "values": ["1", "2", "3", "5", "11"]}},
        {"code": "Ár", "selection": {"filter": "item", "values": ["2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"]}}
    ],
    "response": {"format": "json"}
}



def extract_data():
    try:
        response = requests.post(API_URL, json=QUERY, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data
        
    except Exception as e:
        print(f"error: {e}")
        return None


def main():    
    #taka json fra api
    raw_data = extract_data()
    #tekka a data og key
    if raw_data is not None and 'data' in raw_data:
        #clean
        df = parse_data(raw_data)
        print(df[['Breyta_text', 'Ár', 'value']].to_string(index=False))
        #pivot and export
        df_pivot = create_pivot_and_export(df)

        #bua til plot
        plot_revenue_trend(df_pivot)

    else:
        print("error að sækja gögn")

if __name__ == "__main__":
    main()
