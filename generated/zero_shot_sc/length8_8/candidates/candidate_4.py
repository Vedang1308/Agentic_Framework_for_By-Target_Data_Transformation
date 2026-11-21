import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with daily hourly data into a monthly hourly summary.
    
    Steps:
    1. Parse the 'date' column to extract month information.
    2. Unpivot (melt) the 'Hour 1'...'Hour 24' columns into a long format.
    3. Aggregate the values by month and hour (using mean).
    4. Pivot the data so that hours are rows and months are columns.
    5. Format column names and ensure correct types.
    """
    
    # 1. Parse dates and extract month name
    # The date format is %m/%d/%Y
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['date'].dt.strftime('%B').str.lower()
    
    # 2. Identify hour columns
    hour_cols = [f'Hour {i}' for i in range(1, 25)]
    
    # 3. Melt the DataFrame
    # We keep 'date' and 'month' as identifiers, but we really only need 'month' for grouping.
    # We melt the hour columns.
    df_melted = source.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract numeric hour from 'Hour X' column name
    df_melted['hour'] = df_melted['hour_col'].str.extract(r'(\d+)').astype(int)
    
    # 5. Aggregate by month and hour
    # Using mean to handle multiple days in a month. 
    # If values are consistent, mean preserves them.
    df_agg = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month, Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 7. Reset index to make 'hour' a column again
    df_result = df_pivot.reset_index()
    
    # 8. Ensure all months are present, even if NaN
    expected_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                       'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to ensure all months are present and in correct order
    # The pivot might miss months if no data exists, but we want them as NaN
    df_result = df_result.reindex(columns=['hour'] + expected_months)
    
    # 9. Ensure 'hour' is integer
    df_result['hour'] = df_result['hour'].astype(int)
    
    # 10. Sort by hour numerically
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # 11. Define target columns verbatim
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    return df_result[target_columns]