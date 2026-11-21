import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source hourly data table into a summary table with mean values 
    for each hour of the day, aggregated by month.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract month from the date
    df['month'] = df['date'].dt.month
    
    # 3. Identify hour columns
    hour_cols = [col for col in df.columns if col.startswith('Hour ')]
    
    # 4. Melt the dataframe to long format
    # id_vars: columns to keep as identifiers
    # value_vars: columns to unpivot
    # var_name: name for the new column that will contain the old column names
    # value_name: name for the new column that will contain the values
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 5. Extract the hour number from the 'hour_label' (e.g., 'Hour 1' -> 1)
    df_melted['hour'] = df_melted['hour_label'].str.replace('Hour ', '').astype(int)
    
    # 6. Group by hour and month, and calculate the mean
    # We dropna=True to ignore rows with NaN values in the aggregation
    grouped = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot the table to have hours as rows and months as columns
    # index: 'hour'
    # columns: 'month'
    # values: 'value'
    df_pivot = grouped.pivot(index='hour', columns='month', values='value')
    
    # 8. Rename month columns to lowercase month names
    month_mapping = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot.columns = [month_mapping.get(col, col) for col in df_pivot.columns]
    
    # 9. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 10. Sort by hour to ensure correct order (1-24)
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    # 11. Define target columns in the exact required order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 12. Ensure all target columns exist (fill NaNs for months not present in source if any)
    for col in target_columns:
        if col not in df_result.columns:
            df_result[col] = np.nan
            
    # 13. Return only the target columns in the correct order
    return df_result[target_columns]