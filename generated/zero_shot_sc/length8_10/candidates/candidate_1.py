import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame from a wide format (daily hourly data) 
    to a pivot table format (average hourly values by month).
    """
    # 1. Parse the Date column to extract the month
    # The format is '%a %m/%d/%Y', e.g., 'Thu 10/01/2009'
    source = source.copy()
    source['parsed_date'] = pd.to_datetime(source['Date'], format='%a %m/%d/%Y')
    source['month_num'] = source['parsed_date'].dt.month
    
    # Map month numbers to lowercase month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    source['month_name'] = source['month_num'].map(month_names)
    
    # 2. Identify hourly columns
    # Columns are named '1:00' through '24:00:00'
    # We exclude 'Segment', 'Date', and the helper columns we added
    hour_cols = [col for col in source.columns if col not in ['Segment', 'Date', 'parsed_date', 'month_num', 'month_name']]
    
    # 3. Melt the DataFrame to long format
    # id_vars: columns to keep as identifiers (we need month_name)
    # value_vars: the hourly columns
    # var_name: name for the new column holding the old column names ('hour_str')
    # value_name: name for the new column holding the values ('value')
    df_long = source.melt(
        id_vars=['month_name'],
        value_vars=hour_cols,
        var_name='hour_str',
        value_name='value'
    )
    
    # 4. Clean the hour_str to extract integer hour
    # Examples: '1:00' -> 1, '24:00:00' -> 24
    df_long['hour'] = df_long['hour_str'].apply(lambda x: int(x.split(':')[0]))
    
    # 5. Aggregate
    # Group by hour and month, calculate the mean of the values
    # This creates the average hourly profile for each month
    df_agg = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: hour
    # Columns: month_name
    # Values: value
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Reset index to make 'hour' a column again
    df_pivot = df_pivot.reset_index()
    
    # 8. Ensure all month columns are present and in the correct order
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                     'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to ensure all months are present (filling NaN if missing data)
    df_pivot = df_pivot.reindex(columns=['hour'] + target_months)
    
    # Ensure 'hour' is integer type
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    
    # Define final target columns
    target_columns = ['hour'] + target_months
    
    return df_pivot[target_columns]