import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (with timestamped sensor readings) into a 
    daily hourly aggregated DataFrame with columns 'date' and 'Hour 1' to 'Hour 24'.
    """
    # 1. Parse the date column
    # Format: %m/%d/%Y %H:%M
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date part for grouping and formatting
    # Target date format: %m/%d/%Y
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and adjust to 1-based indexing (Hour 1 = 00:00-00:59)
    # Source hour 0 -> Target Hour 1
    # Source hour 23 -> Target Hour 24
    df['target_hour'] = df['datetime'].dt.hour + 1
    
    # 4. Aggregate data
    # Group by date string and target hour, then calculate the mean of cerc_logger_1
    aggregated = df.groupby(['date_str', 'target_hour'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the data
    # Rows: date_str, Columns: target_hour, Values: cerc_logger_1
    pivoted = aggregated.pivot(index='date_str', columns='target_hour', values='cerc_logger_1')
    
    # 6. Rename columns to 'Hour 1', 'Hour 2', etc.
    pivoted.columns = [f'Hour {col}' for col in pivoted.columns]
    
    # 7. Reset index to make date_str a column named 'date'
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 8. Define the exact target column order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Ensure all columns exist (in case some hours are missing in data, pivot won't create them)
    # If hours are missing, they will be NaN. We need to ensure the columns exist for the final selection.
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 10. Select and return only the target columns in the correct order
    return pivoted[target_columns]