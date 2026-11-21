import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract month
    # The date format is '%m/%d/%Y'
    source['date_parsed'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    
    # 2. Melt the value columns (value1 to value24) into long format
    # Identify the value columns
    value_cols = [f'value{i}' for i in range(1, 25)]
    
    # Melt the dataframe
    # id_vars: columns to keep as identifiers (date_parsed, and maybe others if needed, but we only need date for month)
    # var_name: name for the new column holding the original column names
    # value_name: name for the new column holding the values
    long_df = source.melt(
        id_vars=['date_parsed'], 
        value_vars=value_cols, 
        var_name='hour_col', 
        value_name='load'
    )
    
    # 3. Extract hour from 'hour_col' (e.g., 'value1' -> 1)
    long_df['hour'] = long_df['hour_col'].str.replace('value', '').astype(int)
    
    # 4. Extract month from date_parsed and map to month name
    long_df['month_num'] = long_df['date_parsed'].dt.month
    
    # Map month numbers to lowercase month names as required by target columns
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    long_df['month_name'] = long_df['month_num'].map(month_map)
    
    # 5. Aggregate by hour and month_name
    # We calculate the mean load for each hour in each month
    agg_df = long_df.groupby(['hour', 'month_name'])['load'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: hour, Columns: month_name, Values: load
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='load')
    
    # 7. Clean up and format
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Rename columns to ensure exact match (remove any multi-index names if present)
    pivot_df.columns.name = None
    
    # Ensure 'hour' is integer
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Define the target columns in the correct order
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target columns exist (they should, due to pivot, but some might be NaN if no data)
    # Sort by hour for consistent output
    pivot_df = pivot_df.sort_values(by='hour').reset_index(drop=True)
    
    # Select and return the target columns
    return pivot_df[target_columns]