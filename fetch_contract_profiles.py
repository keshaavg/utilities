# Filename: fetch_contract_profiles.py

import requests
import csv
import os
from dotenv import load_dotenv
from zipfile import ZipFile

def load_token():
    load_dotenv()
    token = os.getenv("BEARER_TOKEN")
    if not token:
        raise EnvironmentError("BEARER_TOKEN not found in .env file")
    return token

def get_contract_data(contract_name, start_date, end_date, headers, api_url):
    payload = {
        "contractName": contract_name,
        "startDate": start_date,
        "endDate": end_date,
        "isMultilegContract": False
    }
    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json().get("contractStorage", [])
    else:
        print(f"Request failed for {contract_name} with status code {response.status_code}")
        return []

def write_csv(data, filename):
    fieldnames = ["gasDay", "nomination", "capacityUnit", "gasInStore", "gasInStoreEod", "hoursInGasDay"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({
                "gasDay": row.get("gasDay"),
                "nomination": row.get("nomination"),
                "capacityUnit": row.get("capacityUnit"),
                "gasInStore": row.get("gasInStore"),
                "gasInStoreEod": row.get("gasInStoreEod"),
                "hoursInGasDay": row.get("hoursInGasDay")
            })

def zip_csv_files(filenames, archive_name="contracts_export.zip"):
    with ZipFile(archive_name, "w") as zipf:
        for file in filenames:
            if os.path.exists(file):
                zipf.write(file)

def main():
    api_url = "https://your-api-url.com/ContractProfile"  # Replace with actual API URL
    token = load_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    default_start = "2025-04-01"
    default_end = "2026-03-31"

    contracts = [
        {"name": "HiAdch"},
        {"name": "ContractB", "startDate": "2025-05-01", "endDate": "2026-04-30"},
        {"name": "ContractC"},
        {"name": "ContractD", "startDate": "2025-06-01", "endDate": "2026-05-31"},
        {"name": "ContractE"},
        {"name": "ContractF", "startDate": "2025-07-01", "endDate": "2026-06-30"}
    ]

    csv_files = []
    for contract in contracts:
        name = contract["name"]
        start = contract.get("startDate", default_start)
        end = contract.get("endDate", default_end)
        data = get_contract_data(name, start, end, headers, api_url)
        if data:
            csv_file = f"{name}_contract.csv"
            write_csv(data, csv_file)
            csv_files.append(csv_file)

    zip_csv_files(csv_files)

if __name__ == "__main__":
    main()
