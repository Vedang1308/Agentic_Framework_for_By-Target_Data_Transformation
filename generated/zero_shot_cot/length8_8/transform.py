import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide format (dates with hourly columns)
    to a target DataFrame aggregated by hour and month.
    """
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Extract month name and convert to lowercase
    df['month'] = df['date'].dt.month_name().str.lower()
    
    # 3. Identify hour columns
    hour_cols = [col for col in df.columns if col.startswith('Hour ')]
    
    # 4. Melt the DataFrame to long format
    # id_vars: columns to keep as identifiers
    # value_vars: columns to unpivot
    # var_name: name for the new column containing the original column names
    # value_name: name for the new column containing the values
    long_df = df.melt(
        id_vars=['date', 'month'],
        value_vars=hour_cols,
        var_name='hour_label',
        value_name='value'
    )
    
    # 5. Extract the integer hour from the hour_label (e.g., "Hour 1" -> 1)
    long_df['hour'] = long_df['hour_label'].str.extract(r'(\d+)').astype(int)
    
    # 6. Group by hour and month, and calculate the mean
    # Using mean to aggregate values for the same hour across different days in the same month
    aggregated = long_df.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 7. Pivot the table to get months as columns
    # index: hour
    # columns: month
    # values: value
    pivot_df = aggregated.pivot(index='hour', columns='month', values='value')
    
    # 8. Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # 9. Define the target column names in the correct order
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 10. Ensure all target month columns exist, filling missing ones with NaN
    for col in target_columns[1:]: # Skip 'hour'
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 11. Select and order the columns as required
    result_df = pivot_df[target_columns]
    
    # 12. Ensure 'hour' is integer type
    result_df['hour'] = result_df['hour'].astype(int)
    
    return result_df