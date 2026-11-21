import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column to extract the month
    source = source.copy()
    source['date'] = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    source['month_num'] = source['date'].dt.month
    
    # Map month numbers to target column names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_map)
    
    # 2. Identify hourly columns to keep (1-24). Exclude 2500.
    hourly_cols = [col for col in source.columns if col.startswith('PCT_HOURLY_') and col != 'PCT_HOURLY_2500']
    
    # 3. Melt the hourly columns into long format
    # We need to extract the hour number from the column name
    # Column names are like 'PCT_HOURLY_0100', 'PCT_HOURLY_0200', ..., 'PCT_HOURLY_2400'
    # The hour is the first two digits of the last part, or simply int(last_part)/100
    
    df_melted = pd.melt(
        source, 
        id_vars=['month_name'], 
        value_vars=hourly_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # Extract hour integer from column name
    # 'PCT_HOURLY_0100' -> 1, 'PCT_HOURLY_1000' -> 10
    df_melted['hour'] = df_melted['hour_col'].apply(lambda x: int(x.split('_')[-1]) // 100)
    
    # 4. Aggregate by hour and month
    # Calculate the mean value for each hour and month combination
    df_agg = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 5. Pivot to wide format
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # 6. Ensure column order and names match target
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Rename 'hour' if necessary (it should already be named 'hour')
    # Ensure all target columns exist, fill NaN with 0 if any month is missing (though unlikely with full data)
    for col in target_columns:
        if col not in df_pivot.columns:
            df_pivot[col] = 0.0
            
    df_result = df_pivot[target_columns]
    
    # Sort by hour to ensure correct order (1-24)
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # Ensure data types match
    df_result['hour'] = df_result['hour'].astype(int)
    for col in target_columns[1:]:
        df_result[col] = df_result[col].astype(float)
        
    return df_result