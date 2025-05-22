import csv
from zipfile import ZipFile

def refresh_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id
    }
    r = requests.post(token_url, data=data)
    new_tokens = r.json()
    return new_tokens.get('access_token'), new_tokens.get('refresh_token')

def get_contract_data(contract_name, start_date, end_date, headers):
    url = "https://your-api-url.com/ContractProfile"
    payload = {
        "contractName": contract_name,
        "startDate": start_date,
        "endDate": end_date,
        "isMultilegContract": False
    }
    r = requests.post(url, json=payload, headers=headers)
    if r.status_code == 401:  # token expired
        global access_token, refresh_token
        access_token, refresh_token = refresh_access_token(refresh_token)
        headers["Authorization"] = f"Bearer {access_token}"
        r = requests.post(url, json=payload, headers=headers)
    return r.json().get("contractStorage", [])

def write_csv(data, filename):
    fields = ["gasDay", "nomination", "capacityUnit", "gasInStore", "gasInStoreEod", "hoursInGasDay"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in data:
            writer.writerow({key: row.get(key) for key in fields})

def zip_csv_files(files, zip_name="contracts_export.zip"):
    with ZipFile(zip_name, "w") as zipf:
        for f in files:
            if os.path.exists(f):
                zipf.write(f)

headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
csv_files = []

for contract in contracts:
    name = contract["name"]
    start = contract.get("startDate", default_start)
    end = contract.get("endDate", default_end)
    data = get_contract_data(name, start, end, headers)
    file = f"{name}_contract.csv"
    write_csv(data, file)
    csv_files.append(file)

zip_csv_files(csv_files)
print("All CSV files zipped into contracts_export.zip")
