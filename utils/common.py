import os
import pandas as pd

def clean_name(full_text):
    parts = full_text.split(".")
    name_part = parts[-1].strip()

    if "Üyesi" in name_part:
        name_part = name_part.replace("Üyesi", "").strip()

    return name_part

def add_department_url(university_name, department_name, url, url_data):
    existing_entry = next((item for item in url_data if item["Departman"] == department_name and item["Üniversite"] == university_name), None)
    if existing_entry:
        if url not in existing_entry["URL"]:
            existing_entry["URL"] += f", {url}"
    else:
        url_data.append({
            "Üniversite": university_name,
            "Departman": department_name,
            "URL": url,
        })

def handle_excel_output(data, file_path):
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path)
        df = pd.concat([existing_data, pd.DataFrame(data)], ignore_index=True).drop_duplicates()
    else:
        df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    print(f"Updated data written to {file_path}.")