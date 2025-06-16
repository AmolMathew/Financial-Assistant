import requests
FMP_API_KEY = "your_fmp_api_key"
def fetch_integrated_annual_report(symbol: str):
    endpoints = {
        "balance_sheet": f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={symbol}&apikey={FMP_API_KEY}",
        "cashflow": f"https://financialmodelingprep.com/stable/cash-flow-statement?symbol={symbol}&apikey={FMP_API_KEY}",
        "income_statement": f"https://financialmodelingprep.com/stable/income-statement?symbol={symbol}&apikey={FMP_API_KEY}"
    }
    report_data = {}
    for key, url in endpoints.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                report_data[key] = response.json()
            else:
                report_data[key] = {"error": f"Status code {response.status_code}"}
        except Exception as e:
            report_data[key] = {"error": str(e)}
    return report_data
