import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from wide format (daily hourly data) 
    to a target DataFrame showing the average value for each hour of the day 
    for each month of the year.
    """
    # 1. Identify hour columns (all columns except 'Segment' and 'Date')
    hour_cols = [col for col in source.columns if col not in ['Segment', 'Date']]
    
    # 2. Melt the DataFrame to long format
    # id_vars keeps 'Date', value_vars are the hour columns
    df_long = pd.melt(
        source, 
        id_vars=['Date'], 
        value_vars=hour_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Parse the Date column to extract the month
    # Format is '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    df_long['date_parsed'] = pd.to_datetime(df_long['Date'], format='%a %m/%d/%Y')
    df_long['month'] = df_long['date_parsed'].dt.month
    
    # 4. Extract the hour integer from the column name string
    # Column names are like '1:00', '2:00', ..., '24:00:00'
    # We split by ':' and take the first part, then convert to int
    df_long['hour'] = df_long['hour_str'].str.split(':').str[0].astype(int)
    
    # 5. Group by hour and month, and calculate the mean value
    # This aggregates all days in a specific month for a specific hour
    df_agg = df_long.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot the table so that:
    # - Rows are hours
    # - Columns are months
    # - Values are the mean values
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value')
    
    # 7. Rename month columns to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_pivot = df_pivot.rename(columns=month_names)
    
    # 8. Reset index to make 'hour' a column again
    df_result = df_pivot.reset_index()
    
    # 9. Ensure correct column order and types
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Sort by hour to ensure deterministic order (1-24)
    df_result = df_result.sort_values('hour').reset_index(drop=True)
    
    # Ensure 'hour' is integer
    df_result['hour'] = df_result['hour'].astype(int)
    
    # Ensure month columns are float
    for col in target_columns[1:]:
        if col in df_result.columns:
            df_result[col] = df_result[col].astype(float)
            
    return df_result[target_columns]