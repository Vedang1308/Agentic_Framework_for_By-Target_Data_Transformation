import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from high-frequency time series data 
    into a daily hourly aggregated wide-format table.
    """
    df = source.copy()
    
    # 1. Parse the date column
    # Source format: 'M/D/YYYY H:MM'
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date as string 'MM/DD/YYYY' for grouping
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour (0-23)
    df['hour'] = df['datetime'].dt.hour
    
    # 4. Aggregate data
    # Group by date and hour, calculate the mean of zone_016
    # Using mean to handle the multiple minute-level records per hour
    agg_df = df.groupby(['date_str', 'hour'])['zone_016'].mean().reset_index()
    
    # 5. Pivot the data to wide format
    # Index: date_str, Columns: hour, Values: zone_016
    pivot_df = agg_df.pivot(index='date_str', columns='hour', values='zone_016')
    
    # 6. Rename columns to match target schema 'Hour 1' ... 'Hour 24'
    # Mapping logic inferred from sample:
    # Source Hour 0 (midnight) -> Target 'Hour 24'
    # Source Hour 1 -> Target 'Hour 1'
    # ...
    # Source Hour 23 -> Target 'Hour 23'
    rename_map = {i: f'Hour {i}' for i in range(1, 24)}
    rename_map[0] = 'Hour 24'
    
    pivot_df = pivot_df.rename(columns=rename_map)
    
    # 7. Reset index to make 'date_str' a column named 'date'
    pivot_df = pivot_df.reset_index().rename(columns={'date_str': 'date'})
    
    # 8. Define target column order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 9. Ensure all target columns exist (fill missing hours with NaN if necessary)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    # 10. Select and return columns in the exact target order
    return pivot_df[target_columns]