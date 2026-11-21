import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with columns 'date' and 'cerc_logger_1'
    into a target DataFrame with daily hourly averages.
    """
    # 1. Parse the date column
    # The format is '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Define the target column names for hours 1-24
    # Source hour 0 -> 'Hour 1', Source hour 23 -> 'Hour 24'
    hour_map = {h: f'Hour {h+1}' for h in range(24)}
    
    # 4. Group by date and hour, and calculate the mean
    # We group by 'date_only' and 'hour'
    grouped = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean()
    
    # 5. Pivot the data
    # We want 'date_only' as index, hours as columns, and mean values as data
    # unstack the 'hour' level
    pivoted = grouped.unstack(level='hour')
    
    # 6. Rename columns to match target schema ('Hour 1', 'Hour 2', ...)
    pivoted = pivoted.rename(columns=hour_map)
    
    # 7. Reset index to bring 'date_only' back as a column
    pivoted = pivoted.reset_index()
    
    # 8. Format the date column as string '%m/%d/%Y'
    pivoted['date'] = pivoted['date_only'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # 9. Select and order the columns as required
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Ensure all hour columns exist (fill missing with NaN if necessary)
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    df_result = pivoted[target_columns]
    
    return df_result