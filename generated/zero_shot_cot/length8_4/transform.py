import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly percentages
    into a target DataFrame with average percentages per hour per month.
    """
    # 1. Parse the date column to extract the month
    source = source.copy()
    source['DT_STRATA'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month_num'] = source['DT_STRATA'].dt.month
    
    # Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_map)
    
    # 2. Identify hourly columns and melt the dataframe
    # Columns are PCT_HOURLY_0100 to PCT_HOURLY_2500
    # We only care about 0100 to 2400 for hours 1-24
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_')]
    
    # Filter to only include hours 1-24 (0100-2400)
    # 2500 is typically 0 or end-of-day and not in target
    valid_hourly_cols = [col for col in hourly_cols if col.endswith('00') and int(col.split('_')[-1]) <= 2400]
    
    # Melt the dataframe
    df_melted = source.melt(
        id_vars=['month_name'],
        value_vars=valid_hourly_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # 3. Extract hour number from column name
    # e.g., 'PCT_HOURLY_0100' -> 1
    df_melted['hour'] = df_melted['hour_col'].apply(lambda x: int(x.split('_')[-1]) // 100)
    
    # 4. Aggregate: Mean value for each hour and month
    # Group by hour and month_name, then calculate the mean
    df_agg = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 6. Clean up and format
    # Reset index to make 'hour' a column
    df_pivot = df_pivot.reset_index()
    
    # Ensure column names are strings and match target exactly
    df_pivot.columns.name = None # Remove column index name
    
    # Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target month columns exist (fill NaN with 0 if a month is missing for an hour)
    for col in target_columns[1:]:
        if col not in df_pivot.columns:
            df_pivot[col] = 0.0
            
    # Select and order columns
    df_result = df_pivot[target_columns]
    
    # Sort by hour to ensure correct order (1-24)
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # Ensure hour is integer
    df_result['hour'] = df_result['hour'].astype(int)
    
    return df_result