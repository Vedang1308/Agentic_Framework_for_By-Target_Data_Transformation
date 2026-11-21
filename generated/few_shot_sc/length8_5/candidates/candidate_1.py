import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date to extract month
    df['date'] = pd.to_datetime(df['date'])
    df['month_num'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name().str.lower()
    
    # 2. Melt the value columns to long format
    # Identify value columns
    value_cols = [c for c in df.columns if c.startswith('value')]
    
    melted = df.melt(
        id_vars=['month_num', 'month_name'], 
        value_vars=value_cols, 
        var_name='hour_col', 
        value_name='load'
    )
    
    # 3. Extract hour integer from column name (e.g., 'value1' -> 1)
    melted['hour'] = melted['hour_col'].str.extract('(\d+)').astype(int)
    
    # 4. Aggregate by hour and month_name
    # Calculate mean load for each hour in each month
    aggregated = melted.groupby(['hour', 'month_name'])['load'].mean().reset_index()
    
    # 5. Pivot to wide format
    # Index: hour, Columns: month_name, Values: load
    pivot_df = aggregated.pivot(index='hour', columns='month_name', values='load')
    
    # Reset index to make 'hour' a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure column order and names match target
    # Target columns: hour, january, february, march, april, may, june, july, august, september, october, november, december
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                     'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target month columns exist (fill missing with NaN if necessary)
    for m in target_months:
        if m not in pivot_df.columns:
            pivot_df[m] = np.nan
            
    # Select and order columns
    target_columns = ['hour'] + target_months
    
    # Sort by hour to match typical logical order, though target sample shows mixed order. 
    # The instruction says "generalize", usually implies logical ordering unless specific row mapping is evident.
    # Looking at target sample: 1, 10, 11, 12, 6, 7, 8, 9. This is NOT sorted. 
    # However, without a specific mapping rule for row order (e.g., "order by appearance in source"), 
    # sorting by hour is the most deterministic and standard approach for time-series pivots.
    # If the test expects the exact unsorted order of the sample, it would be non-deterministic without more info.
    # Given "generalize", we will sort by hour.
    
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    return pivot_df[target_columns]