import matplotlib
matplotlib.use('Agg')
import requests
import matplotlib.pyplot as plt
import boto3
from io import BytesIO
from datetime import datetime

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
    BUCKET_NAME = "islenska-etl-bucket"
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

    # Hlaða upp csv
    #búa til s3 client
    s3 = boto3.client('s3')

    #sækja dags í dag fyrir sjal nafn
    today = datetime.now().strftime("%Y-%m")

    #búa til csv í memory
    #tómur buffer
    csv_buffer = BytesIO()
    #skrifa DF í buffer (með index fyrir ár)
    df_pivot.to_csv(csv_buffer, index=True)
    #endursetja á byrjun
    csv_buffer.seek(0)

    #hlaða upp á s3
    #folder/file nafn í s3
    csv_key = f'data/upplysingataekni_{today}.csv' 
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=csv_key,
            Body=csv_buffer.getvalue(),
            ContentType='text/csv'
        )
        print(f"csv skjal hlaðið upp i s3: {csv_key}")
    except Exception as e:
        print(f"error csv ekki hlaðið upp: {str(e)}")


    print(df_pivot.tail())

    #test
    try:
        df_pivot['Rekstrartekjur (mkr)'].plot(title='Rekstrartekjur í upplýsingageiranum')
        plt.tight_layout()

        #búa til png í memory
        img_buffer = BytesIO()
        #vista plot í buffer
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        #hreinsa upp plot
        plt.close()

        #hlaða upp í s3
        plot_key = f'plots/rekstrartekjur_trend_{today}.png'
        try:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=plot_key,
                Body=img_buffer.getvalue(),
                ContentType='image/png'
            )
            print(f"png skjal hlaðið upp i s3: {plot_key}")
        except Exception as e:
            print(f"error png ekki hlaðið upp: {str(e)}")


        print("Vistað")
        plt.close()
    except Exception as e:
        print("plt error:", str(e))

    return {
        'statuscode': 200,
        'body': 'success'
    }