import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # Define the mapping from source hour columns to target hour columns
    # Source uses 12-hour format AM/PM, Target uses 1-24 index
    source_hour_cols = [
        '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', 
        '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
        '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', 
        '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM', '12:00 AM'
    ]
    
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    hour_col_mapping = dict(zip(source_hour_cols, target_hour_cols))
    
    # Create a copy to avoid modifying the original source
    df = source.copy()
    
    # Rename the hour columns
    df.rename(columns=hour_col_mapping, inplace=True)
    
    # Drop the DSL column as it's not in the target
    if 'DSL' in df.columns:
        df.drop(columns=['DSL'], inplace=True)
        
    # Process the date column
    # 1. Parse to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # 2. Format to string 'YYYY-MM-DD HH:MM:SS'
    # The source only has dates, so time will be 00:00:00, which matches the target
    df['Date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Drop the original date column
    df.drop(columns=['date'], inplace=True)
    
    # Define the exact target columns in order
    target_columns = ['Date'] + target_hour_cols
    
    # Sort by Date to match the chronological order typically expected in time series
    # and observed in the target sample
    df.sort_values(by='Date', inplace=True)
    
    # Reset index to have a clean 0-based integer index
    df.reset_index(drop=True, inplace=True)
    
    # Return the DataFrame with columns in the exact order specified
    return df[target_columns]