import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide format (daily rows, hourly columns)
    to a target format (hourly rows, monthly columns) with aggregated values.
    """
    # 1. Parse the Date column to extract month information
    source = source.copy()
    source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y')
    source['month_num'] = source['Date'].dt.month
    
    # 2. Map month numbers to lowercase month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month'] = source['month_num'].map(month_map)
    
    # 3. Identify the hourly columns (1 through 24)
    hour_cols = [str(i) for i in range(1, 25)]
    
    # 4. Melt the DataFrame from wide to long format
    # Keep 'Date', 'Class', 'month_num', 'month' as id_vars
    # Melt the hour columns
    df_long = pd.melt(
        source,
        id_vars=['Date', 'Class', 'month_num', 'month'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # 5. Convert 'hour' to integer
    df_long['hour'] = df_long['hour'].astype(int)
    
    # 6. Aggregate by hour and month
    # We calculate the mean of the 'value' for each hour and month combination
    df_agg = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot the data so that 'month' becomes columns and 'hour' is the index
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 8. Reset index to make 'hour' a column again
    df_pivot = df_pivot.reset_index()
    
    # 9. Ensure column names are strings and match target exactly
    # The pivot columns are already the month names from the map
    df_pivot.columns.name = None # Remove the column index name
    
    # 10. Define the target column order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 11. Ensure all target month columns exist (fill with NaN if missing)
    for col in target_columns[1:]:
        if col not in df_pivot.columns:
            df_pivot[col] = np.nan
            
    # 12. Select and order the columns
    df_result = df_pivot[target_columns]
    
    # 13. Ensure 'hour' is int64
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 14. Sort by hour for deterministic output
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    return df_result[target_columns]