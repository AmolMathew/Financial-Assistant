from downloader.bse_downloader import download_annual_reports

if __name__ == "__main__":
    csv_file = "data/Equity.csv"
    target_year = "2023"
    download_folder = "downloads/2023"
    log_file = f"{download_folder}/download_log_{target_year}.txt"
    download_annual_reports(csv_file, target_year, download_folder, log_file)
