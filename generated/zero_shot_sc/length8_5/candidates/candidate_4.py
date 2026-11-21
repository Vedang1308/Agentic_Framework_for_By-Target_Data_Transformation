import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing daily hourly load data 
    into a target DataFrame aggregated by hour and month.
    """
    # 1. Parse the date column to extract month information
    source = source.copy()
    source['date_parsed'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month_num'] = source['date_parsed'].dt.month
    
    # 2. Define the mapping from month number to target column name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # 3. Melt the value columns (value1...value24) into long format
    # Identify value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # Melt the dataframe
    # id_vars keeps date and month_num, value_vars are the hours, var_name becomes hour_idx, value_name becomes load
    df_long = source.melt(
        id_vars=['month_num'], 
        value_vars=value_cols, 
        var_name='hour_idx', 
        value_name='load'
    )
    
    # 4. Extract the hour number from the hour_idx string (e.g., 'value1' -> 1)
    df_long['hour'] = df_long['hour_idx'].str.replace('value', '', regex=False).astype(int)
    
    # 5. Map month numbers to month names
    df_long['month_name'] = df_long['month_num'].map(month_map)
    
    # 6. Aggregate by hour and month_name
    # We calculate the mean of the load for each hour in each month
    df_agg = df_long.groupby(['hour', 'month_name'])['load'].mean().reset_index()
    
    # 7. Pivot the data to wide format
    # Index: hour, Columns: month_name, Values: load
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='load')
    
    # 8. Clean up the pivot table
    # Remove the column axis name if present
    df_pivot.columns.name = None
    
    # Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 9. Ensure the hour column is integer
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 10. Define the target columns in the correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 11. Reorder columns to match target schema exactly
    # Note: If a month is missing from the source data, it won't be in df_pivot. 
    # We need to ensure all target columns exist, filling missing ones with NaN.
    for col in target_columns:
        if col not in df_result.columns:
            df_result[col] = np.nan
            
    df_result = df_result[target_columns]
    
    # 12. Sort by hour to match typical output expectations (1-24)
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    return df_result[target_columns]