import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid SettingWithCopyWarning or modifying original
    df = source.copy()
    
    # Define the mapping for column renames
    # 1. 'Date' becomes 'cst'
    # 2. '24:00:00' becomes '24:00'
    rename_map = {
        'Date': 'cst',
        '24:00:00': '24:00'
    }
    
    # Apply renames
    df.rename(columns=rename_map, inplace=True)
    
    # Define the exact target column order
    target_columns = [
        'cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', 
        '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', 
        '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', 
        '22:00', '23:00', '24:00'
    ]
    
    # Select only the required columns in the correct order
    # This implicitly drops 'Segment' and any other unwanted columns
    df = df[target_columns]
    
    return df[target_columns]