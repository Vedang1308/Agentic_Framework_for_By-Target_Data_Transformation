import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms source daily hourly data into a table aggregated by hour and month.
    """
    df = source.copy()
    
    # 1. Parse Date and Extract Month
    df['Date'] = pd.to_datetime(df['Date'])
    df['month_num'] = df['Date'].dt.month
    
    # 2. Melt the dataframe to unpivot hours 1-24
    # Identify hour columns (strings '1' through '24')
    hour_cols = [str(i) for i in range(1, 25)]
    
    # Melt: keep Date and month_num as id_vars, unpivot hour columns
    df_melted = df.melt(
        id_vars=['Date', 'month_num'],
        value_vars=hour_cols,
        var_name='hour',
        value_name='value'
    )
    
    # Convert hour to integer
    df_melted['hour'] = df_melted['hour'].astype(int)
    
    # 3. Aggregate by hour and month
    # Calculate the mean value for each hour and month combination
    agg_df = df_melted.groupby(['hour', 'month_num'])['value'].mean().reset_index()
    
    # 4. Pivot to get months as columns
    # Index: hour, Columns: month_num, Values: value
    pivot_df = agg_df.pivot(index='hour', columns='month_num', values='value')
    
    # 5. Map month numbers to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    # Rename columns using the map
    pivot_df.rename(columns=month_map, inplace=True)
    
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure hour is int64
    pivot_df['hour'] = pivot_df['hour'].astype('int64')
    
    # Sort by hour for deterministic output
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # 6. Select target columns verbatim
    target_columns = [
        'hour', 'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    return pivot_df[target_columns]