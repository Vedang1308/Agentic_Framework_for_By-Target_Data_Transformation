import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the datetime column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract date string for grouping and final output
    # Format: MM/DD/YYYY
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23) and map to 1-24 for target column names
    df['hour_bin'] = df['dt'].dt.hour + 1
    
    # 4. Aggregate data by Date and Hour Bin
    # We use mean to aggregate minute-level data to hourly level.
    # If multiple minutes exist in an hour, we average them.
    agg_df = df.groupby(['Date', 'hour_bin'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data to have Hours as columns
    pivot_df = agg_df.pivot(index='Date', columns='hour_bin', values='zone_016')
    
    # 6. Rename columns to match target schema ('Hr 1', 'Hr 2', ...)
    # The column names from pivot are integers 1..24 (or subset if missing)
    pivot_df.columns = [f'Hr {col}' for col in pivot_df.columns]
    
    # 7. Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Define the exact target columns in order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 9. Reindex columns to ensure all Hr 1..24 are present (filling NaN if missing)
    # and in the correct order.
    df_result = pivot_df.reindex(columns=target_columns)
    
    return df_result[target_columns]