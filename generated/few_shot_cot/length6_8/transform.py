import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the datetime column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour components
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour  # 0-23
    
    # 3. Group by date and hour, and aggregate (mean)
    # We group by the date object and the hour integer
    grouped = df.groupby(['date_only', 'hour'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot the table to wide format
    # Index: date_only, Columns: hour, Values: cerc_logger_1
    pivoted = grouped.pivot(index='date_only', columns='hour', values='cerc_logger_1')
    
    # 5. Reset index to make date a column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'date_only': 'Date'}, inplace=True)
    
    # 6. Format the Date column as MM/DD/YYYY
    pivoted['Date'] = pd.to_datetime(pivoted['Date']).dt.strftime('%m/%d/%Y')
    
    # 7. Rename hour columns from 0-23 to 'Hr 1'-'Hr 24'
    # The pivot columns are integers 0..23. We need to map them to strings.
    rename_map = {h: f'Hr {h+1}' for h in range(24)}
    pivoted.rename(columns=rename_map, inplace=True)
    
    # 8. Ensure all 24 hour columns exist and are in the correct order
    target_hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure all hours are present (filling NaN if a hour is missing for a day)
    # First, ensure the 'Date' column is first, then the hour columns
    all_target_cols = ['Date'] + target_hour_cols
    
    # Select only the target columns. If some hours are missing in the pivot, they will be NaN.
    # We need to make sure the columns exist in the dataframe before selecting.
    for col in target_hour_cols:
        if col not in pivoted.columns:
            pivoted[col] = float('nan')
            
    # Final selection and ordering
    result = pivoted[all_target_cols]
    
    return result