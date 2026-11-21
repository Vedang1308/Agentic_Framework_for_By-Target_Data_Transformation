import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to datetime
    source = source.copy()
    source['date_dt'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date string in the target format '%m/%d/%Y'
    source['date_only'] = source['date_dt'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour (0-23) and map to target column names 'value1'-'value24'
    source['hour'] = source['date_dt'].dt.hour
    source['col_name'] = 'value' + (source['hour'] + 1).astype(str)
    
    # 4. Determine the order of dates based on their first appearance in the source
    # This preserves the non-sorted order seen in the target sample
    unique_dates_ordered = source['date_only'].drop_duplicates().tolist()
    
    # 5. Aggregate the data
    # We group by date_only and col_name, then take the mean of the values.
    # Using mean handles the multiple records per hour (e.g., every 5 mins).
    agg_df = source.groupby(['date_only', 'col_name'])['zone_016_cooling_sp'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: date_only, Columns: col_name, Values: zone_016_cooling_sp
    pivot_df = agg_df.pivot_table(index='date_only', columns='col_name', values='zone_016_cooling_sp')
    
    # 7. Ensure all 24 value columns exist, filling missing ones with NaN
    target_value_cols = [f'value{i}' for i in range(1, 25)]
    for col in target_value_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 8. Reorder columns to match the target schema order
    pivot_df = pivot_df[target_value_cols]
    
    # 9. Reorder rows to match the order of first appearance in the source
    # Filter to only dates that were in the source (though pivot should only have those)
    # and reindex to enforce the order
    pivot_df = pivot_df.reindex(unique_dates_ordered)
    
    # 10. Reset index to make 'date_only' a column named 'date'
    pivot_df = pivot_df.reset_index()
    pivot_df = pivot_df.rename(columns={'date_only': 'date'})
    
    # 11. Define final target columns
    target_columns = ['date'] + target_value_cols
    
    # 12. Return the dataframe with the exact target column names
    return pivot_df[target_columns]