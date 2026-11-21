import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source data with minute-level granularity into hourly aggregated data.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract the calendar date and the hour of the day.
    3. Map source hours (0-23) to target hours (1-24).
    4. Group by date and target hour, calculating the mean of 'cerc_logger_1'.
    5. Pivot the data to have one row per date and one column per hour.
    6. Rename columns to match the target schema.
    """
    df = source.copy()
    
    # 1. Parse datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string and hour
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    df['hour_src'] = df['dt'].dt.hour
    
    # 3. Map source hour (0-23) to target hour (1-24)
    # Hour 0 -> Hour 1, Hour 23 -> Hour 24
    df['hour_target'] = df['hour_src'] + 1
    
    # 4. Aggregate by date and hour (mean)
    aggregated = df.groupby(['date_str', 'hour_target'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: date_str, Columns: hour_target, Values: cerc_logger_1
    pivoted = aggregated.pivot(index='date_str', columns='hour_target', values='cerc_logger_1')
    
    # 6. Rename columns from integers to 'Hour X'
    pivoted.columns = [f'Hour {int(col)}' for col in pivoted.columns]
    
    # Reset index to make 'date_str' a column
    pivoted = pivoted.reset_index()
    
    # Rename 'date_str' to 'date'
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 7. Define target columns and select them
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Ensure all target columns exist (in case some hours are missing for some dates, pivot handles NaNs)
    # If a column is missing entirely (unlikely if data covers all hours), we might need to add it, 
    # but pivot usually creates all columns present in the data. 
    # To be robust against missing hours in the entire dataset (unlikely given source volume), 
    # we can reindex columns.
    
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    return pivoted[target_columns]