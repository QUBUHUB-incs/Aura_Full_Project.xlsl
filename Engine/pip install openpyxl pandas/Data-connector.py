import pandas as pd

def load_aura_data(file_path='Aura_Full_Project.xlsx'):
    try:
        # Reads the spreadsheet into a data frame
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        return f"Error loading data: {e}"

def save_aura_data(df, file_path='Aura_Full_Project.xlsx'):
    # Saves UI changes back to the spreadsheet
    df.to_excel(file_path, index=False)
