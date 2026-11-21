import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    # The source format is 'M/D/YYYY H:MM' or similar
    df['parsed_dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    df['date_key'] = df['parsed_dt'].dt.date  # Use date object for grouping
    df['hour'] = df['parsed_dt'].dt.hour
    
    # 3. Map hour (0-23) to target column names ('Hour 1' - 'Hour 24')
    # Hour 0 -> Hour 1, Hour 1 -> Hour 2, ..., Hour 23 -> Hour 24
    df['target_hour_col'] = df['hour'].apply(lambda h: f"Hour {h + 1}")
    
    # 4. Aggregate by date and hour
    # We calculate the mean of cerc_logger_1 for each date and hour combination
    grouped = df.groupby(['date_key', 'target_hour_col'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the data
    # Index: date_key, Columns: target_hour_col, Values: cerc_logger_1
    pivoted = grouped.pivot(index='date_key', columns='target_hour_col', values='cerc_logger_1')
    
    # 6. Reset index and rename columns
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'date_key': 'date'})
    
    # 7. Format the date column to '%m/%d/%Y'
    pivoted['date'] = pivoted['date'].apply(lambda d: d.strftime('%m/%d/%Y'))
    
    # 8. Ensure all Hour columns exist (1-24) and reorder
    target_hour_cols = [f"Hour {i}" for i in range(1, 25)]
    
    # Fill any missing hours with NaN (or 0 if preferred, but NaN is standard for missing data)
    for col in target_hour_cols:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # 9. Select and order columns verbatim
    target_columns = ['date'] + target_hour_cols
    return pivoted[target_columns]