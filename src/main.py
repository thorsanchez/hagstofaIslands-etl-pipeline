import requests
import json
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
        {"code": "Ár", "selection": {"filter": "item", "values": ["2024"]}}
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
    data = extract_data()
    
    if data:
        # fyrstu lykla
        #print(list(data.keys()))
        #allt json 
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("error að sækja gögn")


if __name__ == "__main__":
    main()