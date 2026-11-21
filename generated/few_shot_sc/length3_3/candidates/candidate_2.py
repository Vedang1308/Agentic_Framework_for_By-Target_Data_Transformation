import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Create the target date string format '%m/%d/%Y'
    df['target_date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract hour and map to target column names
    # Mapping: Hour 0 -> 'Hour 24', Hour 1 -> 'Hour 1', ..., Hour 23 -> 'Hour 23'
    df['hour_int'] = df['dt'].dt.hour
    
    def map_hour_to_col(h):
        if h == 0:
            return 'Hour 24'
        else:
            return f'Hour {h}'
            
    df['target_hour_col'] = df['hour_int'].apply(map_hour_to_col)
    
    # 4. Group by target_date and target_hour_col, then aggregate zone_016
    # Using mean aggregation. If there are multiple records per hour, average them.
    grouped = df.groupby(['target_date', 'target_hour_col'])['zone_016'].mean().reset_index()
    
    # 5. Pivot to get hours as columns
    pivot_df = grouped.pivot(index='target_date', columns='target_hour_col', values='zone_016')
    
    # 6. Reset index to make date a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'target_date': 'date'}, inplace=True)
    
    # 7. Ensure all Hour columns exist and are in order
    target_hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # Fill missing columns with NaN if any hour is missing for a date
    for col in target_hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # Select and order the final columns
    final_cols = ['date'] + target_hour_cols
    result = pivot_df[final_cols]
    
    # Sort by date to match typical output order (though not strictly required by schema, good practice)
    # The target sample shows 01/02 before 01/01, which is descending or arbitrary. 
    # Usually, we just return the data. Let's keep the order from the pivot (which follows groupby order).
    # To be safe and deterministic, we can sort by date.
    result = result.sort_values('date').reset_index(drop=True)
    
    return result