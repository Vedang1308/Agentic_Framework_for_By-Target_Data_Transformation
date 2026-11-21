import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source DataFrame with minute-level data into a daily hourly summary.
    """
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map source hour (0-23) to target column names
    # Based on sample analysis:
    # Source Hour 0 (midnight) -> Target '24:00'
    # Source Hour 1 -> Target '1:00'
    # ...
    # Source Hour 23 -> Target '23:00'
    def map_hour_to_col(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['target_hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Group by date and target hour column, summing the values
    # We group by 'date_only' and 'target_hour_col'
    grouped = df.groupby(['date_only', 'target_hour_col'])['zone_016'].sum().reset_index()
    
    # 5. Pivot the table to have hours as columns
    pivot_df = grouped.pivot(index='date_only', columns='target_hour_col', values='zone_016')
    
    # 6. Ensure all 24 hour columns exist and fill missing with 0
    target_hours = [f'{i}:00' for i in range(1, 24)] + ['24:00']
    for col in target_hours:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Reorder columns to match target schema order
    pivot_df = pivot_df[target_hours]
    
    # 7. Format the date index into the 'cst' column
    # Convert index back to datetime for formatting
    pivot_df.index = pd.to_datetime(pivot_df.index)
    pivot_df['cst'] = pivot_df.index.strftime('%a %m/%d/%Y')
    
    # 8. Reset index and select final columns
    pivot_df = pivot_df.reset_index(drop=True)
    
    # Define final column order
    final_cols = ['cst'] + target_hours
    
    return pivot_df[final_cols]