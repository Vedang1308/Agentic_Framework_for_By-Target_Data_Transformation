import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the target column names exactly as specified
    target_columns = [
        'date', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', 
        '10:00 AM', '11:00 AM', '12:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', 
        '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 PM'
    ]
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Map source hour columns to target time labels
    # Based on the target column list order:
    # Hour 1 -> 1:00 AM
    # ...
    # Hour 11 -> 11:00 AM
    # Hour 12 -> 12:00 AM (Note: Target schema puts 12:00 AM here)
    # Hour 13 -> 1:00 PM
    # ...
    # Hour 23 -> 11:00 PM
    # Hour 24 -> 12:00 PM (Note: Target schema puts 12:00 PM here)
    
    rename_map = {}
    for h in range(1, 25):
        src_col = f'Hour {h}'
        if h < 12:
            tgt_col = f'{h}:00 AM'
        elif h == 12:
            tgt_col = '12:00 AM'  # As per target schema position 12
        elif h < 24:
            tgt_col = f'{h-12}:00 PM'
        else: # h == 24
            tgt_col = '12:00 PM'  # As per target schema position 24
        rename_map[src_col] = tgt_col
        
    df.rename(columns=rename_map, inplace=True)
    
    # Parse and format the date column
    # Source format: m/d/Y (e.g., 7/3/2015)
    # Target format: YYYY-MM-DD 00:00:00
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Select and order columns to match target schema exactly
    df = df[target_columns]
    
    return df