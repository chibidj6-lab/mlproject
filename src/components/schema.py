import io
import os
import pandas as pd

# Define the folder path where CSV files are stored
DATA_DIR = r"C:\Users\Acer\Downloads\Data Science\ML\practiceProjectHealth\healthcare_insurance_project\healthcare_insurance_project\data\raw"  # Change to r"C:\path\to\your\folder" if stored elsewhere

# File mapping dictionary
files = {
    "claims": os.path.join(DATA_DIR, "claims.csv"),
    "members": os.path.join(DATA_DIR, "members.csv"),
    "policies": os.path.join(DATA_DIR, "policies.csv"),
    "providers": os.path.join(DATA_DIR, "providers.csv"),
    "diagnosis": os.path.join(DATA_DIR, "claim_diagnosis.csv"),
    "procedures": os.path.join(DATA_DIR, "claim_procedures.csv"),
    "history": os.path.join(DATA_DIR, "medical_history.csv"),
    "payments": os.path.join(DATA_DIR, "payments.csv"),
}


def get_safe_schema_summary(
    file_dict, output_filename="schema_metadata_summary.txt"
):
    metadata_str = ""
    for name, path in file_dict.items():
        if os.path.exists(path):
            # Read first 500 rows to infer schema safely
            df = pd.read_csv(path, nrows=500)
            buffer = io.StringIO()
            df.info(buf=buffer)
            metadata_str += f"=== Table: {name} (Path: {path}, Sample Shape: {df.shape}) ===\n"
            metadata_str += buffer.getvalue() + "\n\n"
        else:
            metadata_str += f"=== Table: {name} (File NOT found at {path}) ===\n\n"

    # Save summary report locally to disk
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(metadata_str)

    print(f"Schema metadata successfully saved to: {output_filename}")
    return metadata_str


# Execute script
schema_metadata = get_safe_schema_summary(files)