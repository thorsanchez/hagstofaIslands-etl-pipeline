import pandas as pd

def parse_data(data):
    rows = []
    for item in data['data']:
        #dict með col nöfn
        row = dict(zip([col['code'] for col in data['columns'][:3]], item['key']))
        #hagnaður
        row['value'] = item['values'][0]
        rows.append(row)
    #csv
    df = pd.DataFrame(rows)
    #df.to_csv('hagstofaIslands_23og24.csv', index=False)
    #print(df)
    df['value'] = pd.to_numeric(df['value'])
    df['Ár'] = pd.to_numeric(df['Ár'])
    
    # Icelandic labels from your attachment
    labels = {
        "1": "Fjöldi fyrirtækja", "2": "Rekstrartekjur (mkr)", 
        "3": "Framleiðsluverðmæti", "5": "Vergur rekstrarafgangur", 
        "11": "Fjöldi starfsmanna"
    }
    df['Breyta_text'] = df['Breyta'].map(labels)
    return df