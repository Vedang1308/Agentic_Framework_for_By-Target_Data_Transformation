import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original source DataFrame
    df = source.copy()
    
    # Define the target columns in the exact order required
    target_columns = [
        'cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', 
        '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', 
        '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', 
        '22:00', '23:00', '24:00'
    ]
    
    # Rename columns to match the target schema
    # 1. 'Date' becomes 'cst'
    # 2. '24:00:00' becomes '24:00'
    rename_map = {
        'Date': 'cst',
        '24:00:00': '24:00'
    }
    df.rename(columns=rename_map, inplace=True)
    
    # Drop the 'Segment' column as it is not in the target schema
    if 'Segment' in df.columns:
        df.drop(columns=['Segment'], inplace=True)
    
    # Select and reorder columns to match the target schema exactly
    # This ensures that even if the source had extra columns or different order,
    # the output matches the target verbatim.
    df = df[target_columns]
    
    return df[target_columns]