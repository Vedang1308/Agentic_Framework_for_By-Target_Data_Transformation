import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column to extract month information
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month'] = df['date_dt'].dt.month
    
    # 2. Identify hour columns
    hour_cols = [col for col in df.columns if col.startswith('Hour ')]
    
    # 3. Melt the dataframe to long format
    # We keep 'month' as an identifier, melt the hour columns
    df_melted = df.melt(
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_col', 
        value_name='value'
    )
    
    # 4. Extract the hour number from the column name (e.g., 'Hour 1' -> 1)
    df_melted['hour'] = df_melted['hour_col'].str.extract('(\d+)').astype(int)
    
    # 5. Group by month and hour, and calculate the mean value
    # This aggregates the daily data into monthly hourly profiles
    grouped = df_melted.groupby(['month', 'hour'])['value'].mean().reset_index()
    
    # 6. Pivot the data to have months as columns and hours as index
    pivot_df = grouped.pivot(index='hour', columns='month', values='value')
    
    # 7. Reset index to make 'hour' a column again
    pivot_df = pivot_df.reset_index()
    
    # 8. Rename month columns to lowercase full names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    pivot_df.rename(columns=month_names, inplace=True)
    
    # 9. Define the target column order
    target_columns = ['hour'] + [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # 10. Ensure all target month columns exist (fill missing with NaN if data doesn't cover them)
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 11. Sort by hour to match the typical target order (1, 2, ..., 24)
    # Note: The target sample shows hours 1, 10, 11... but standard pivot usually sorts by index.
    # Let's sort by hour numerically.
    pivot_df = pivot_df.sort_values(by='hour').reset_index(drop=True)
    
    # 12. Ensure 'hour' is integer type
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    return pivot_df[target_columns]