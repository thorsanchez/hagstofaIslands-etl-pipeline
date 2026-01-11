import matplotlib
matplotlib.use('Agg')
import requests
import matplotlib.pyplot as plt

from clean import parse_data, labels

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

def lambda_handler(event, context):
    #extract
    try:
        response = requests.post(API_URL, json=QUERY, timeout=15)
        response.raise_for_status()
        raw_data = response.json()
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statuscode': 500, 'body': str(e)}

    # clean
    df = parse_data(raw_data)

    df['Breyta_text'] = df['Breyta'].map(labels)
    df_pivot = df.pivot(index='Ár', columns='Breyta_text', values='value')

    print(df_pivot.tail())

    #test
    try:
        df_pivot['Rekstrartekjur (mkr)'].plot(title='Rekstrartekjur í upplýsingageiranum')
        plt.tight_layout()
        plt.savefig("test_plot.png")
        print("Vistað")
        plt.close()
    except Exception as e:
        print("plt error:", str(e))

    return {
        'statuscode': 200,
        'body': 'success'
    }