import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame into the target DataFrame.
    
    Steps:
    1. Parse the 'date' column to datetime.
    2. Extract the hour and map it to the target column labels (1:00-24:00).
       Mapping: Hour 0 -> '24:00', Hour 1 -> '1:00', ..., Hour 23 -> '23:00'.
    3. Format the date part for the 'cst' column.
    4. Group by 'cst' and the mapped hour label, summing 'zone_016'.
    5. Pivot/Unstack to create columns for each hour.
    6. Fill missing values with 0.
    7. Reorder columns to match target schema.
    """
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse date
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    df['hour'] = df['datetime'].dt.hour
    df['date_part'] = df['datetime'].dt.date
    
    # 3. Map hour to target column names
    # Mapping: 0 -> '24:00', 1 -> '1:00', ..., 23 -> '23:00'
    def map_hour_to_col(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['hour_col'] = df['hour'].apply(map_hour_to_col)
    
    # 4. Format the date for 'cst' column: '%a %m/%d/%Y'
    # Note: pd.to_datetime creates Timestamps. We can format them directly.
    df['cst'] = df['datetime'].dt.strftime('%a %m/%d/%Y')
    
    # 5. Aggregate
    # Group by 'cst' and 'hour_col', sum 'zone_016'
    agg_df = df.groupby(['cst', 'hour_col'])['zone_016'].sum().reset_index()
    
    # 6. Pivot to wide format
    # Index: cst, Columns: hour_col, Values: zone_016
    pivot_df = agg_df.pivot(index='cst', columns='hour_col', values='zone_016')
    
    # 7. Ensure all expected columns exist and fill NaNs with 0
    target_hours = [f'{h}:00' for h in range(1, 24)] + ['24:00']
    
    # Reindex columns to ensure order and presence
    pivot_df = pivot_df.reindex(columns=target_hours, fill_value=0)
    
    # Convert to float to ensure type consistency (sum might result in object if mixed, though unlikely here)
    pivot_df = pivot_df.astype(float)
    
    # Reset index to make 'cst' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Define final column order
    target_columns = ['cst'] + target_hours
    
    # Ensure the returned dataframe has exactly these columns
    result_df = pivot_df[target_columns]
    
    return result_df