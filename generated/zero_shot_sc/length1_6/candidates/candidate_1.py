import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame by:
    1. Formatting the 'Date' column into 'cst' (DayOfWeek MM/DD/YYYY).
    2. Renaming 'Hr N' columns to 'N:00'.
    3. Dropping irrelevant columns (Company, Rate, Rate Code).
    4. Reordering columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Parse Date and format to 'cst'
    # Source format: %m/%d/%Y (e.g., 1/1/2014)
    # Target format: %a %m/%d/%Y (e.g., Wed 01/01/2014)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['cst'] = df['Date'].dt.strftime('%a %m/%d/%Y')
    
    # 2. Rename Hour columns
    # Create a mapping for Hr 1 -> 1:00, ..., Hr 24 -> 24:00
    rename_dict = {}
    for i in range(1, 25):
        rename_dict[f'Hr {i}'] = f'{i}:00'
    
    df.rename(columns=rename_dict, inplace=True)
    
    # 3. Define target columns
    target_columns = [
        'cst', 
        '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', 
        '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', 
        '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00'
    ]
    
    # 4. Select only the target columns
    # This implicitly drops Company, Rate, Rate Code, and the original Date column
    df = df[target_columns]
    
    return df[target_columns]