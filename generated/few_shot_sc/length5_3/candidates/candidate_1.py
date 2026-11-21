import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    df['date_str'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to 1-24 bucket
    # 0 (midnight) -> 24
    # 1..23 -> 1..23
    df['hour_bucket'] = df['dt'].dt.hour
    df['hour_bucket'] = df['hour_bucket'].replace(0, 24)
    
    # 4. Aggregate by date and hour bucket
    # Using mean as the aggregation function for sensor data
    agg_df = df.groupby(['date_str', 'hour_bucket'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: date_str, Columns: hour_bucket, Values: cerc_logger_1
    pivoted = agg_df.pivot(index='date_str', columns='hour_bucket', values='cerc_logger_1')
    
    # 6. Rename columns to value1...value24
    pivoted.columns = [f'value{col}' for col in pivoted.columns]
    
    # 7. Reset index to make date_str a column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_str': 'date'})
    
    # 8. Define target columns
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (in case some hours are missing, though unlikely in dense data)
    for col in target_columns[1:]:
        if col not in pivoted.columns:
            pivoted[col] = pd.NA
            
    # 10. Return with exact column order
    return pivoted[target_columns]