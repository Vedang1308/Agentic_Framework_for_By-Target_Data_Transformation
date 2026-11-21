import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source time columns to target time columns
    # Source columns are in a specific order in the schema, but we map by name.
    col_mapping = {
        '1:00 AM': '1:00',
        '2:00 AM': '2:00',
        '3:00 AM': '3:00',
        '4:00 AM': '4:00',
        '5:00 AM': '5:00',
        '6:00 AM': '6:00',
        '7:00 AM': '7:00',
        '8:00 AM': '8:00',
        '9:00 AM': '9:00',
        '10:00 AM': '10:00',
        '11:00 AM': '11:00',
        '12:00 PM': '12:00',  # Noon
        '1:00 PM': '13:00',
        '2:00 PM': '14:00',
        '3:00 PM': '15:00',
        '4:00 PM': '16:00',
        '5:00 PM': '17:00',
        '6:00 PM': '18:00',
        '7:00 PM': '19:00',
        '8:00 PM': '20:00',
        '9:00 PM': '21:00',
        '10:00 PM': '22:00',
        '11:00 PM': '23:00',
        '12:00 AM': '24:00'   # Midnight
    }
    
    # Make a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['date_parsed'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # Sort by date to ensure chronological order (target sample is sorted)
    df = df.sort_values(by='date_parsed').reset_index(drop=True)
    
    # Format the date column to target format '%a %m/%d/%Y'
    # %a is abbreviated weekday name (e.g., Wed)
    df['cst'] = df['date_parsed'].dt.strftime('%a %m/%d/%Y')
    
    # Rename the time columns
    df = df.rename(columns=col_mapping)
    
    # Define the target column order
    # Start with 'cst', then the time columns 1:00 to 24:00
    time_cols = [f'{h}:00' for h in range(1, 25)]
    target_columns = ['cst'] + time_cols
    
    # Select only the target columns
    # Note: We drop 'date', 'date_parsed', and 'DSL' implicitly by selection
    df = df[target_columns]
    
    return df