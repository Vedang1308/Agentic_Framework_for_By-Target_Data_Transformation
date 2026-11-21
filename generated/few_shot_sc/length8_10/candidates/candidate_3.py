import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Identify hourly columns
    # Columns are named '1:00', '2:00', ..., '24:00:00'
    hourly_cols = [c for c in df.columns if c[0].isdigit()]
    
    # 2. Melt the dataframe to long format
    # Keep Segment and Date as identifiers
    df_long = pd.melt(
        df, 
        id_vars=['Segment', 'Date'], 
        value_vars=hourly_cols, 
        var_name='hour_str', 
        value_name='value'
    )
    
    # 3. Parse Date to extract Month
    # Format: '%a %m/%d/%Y' e.g., 'Thu 10/01/2009'
    # We can parse the whole string or just extract the month part.
    # pd.to_datetime handles this format well.
    df_long['datetime'] = pd.to_datetime(df_long['Date'])
    df_long['month_num'] = df_long['datetime'].dt.month
    
    # Map month number to lowercase name
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df_long['month_name'] = df_long['month_num'].map(month_map)
    
    # 4. Parse Hour from column name
    # '1:00' -> 1, '24:00:00' -> 24
    df_long['hour'] = df_long['hour_str'].apply(lambda x: int(x.split(':')[0]))
    
    # 5. Aggregate
    # Group by hour and month_name, calculate mean
    # The target values look like means (averages across all years/days for that month/hour)
    agg_df = df_long.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivot_df = agg_df.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # 7. Clean up column names and types
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Ensure all month columns exist, fill NaN with 0 if necessary (though mean shouldn't be NaN if data exists)
    for m in month_map.values():
        if m not in pivot_df.columns:
            pivot_df[m] = np.nan
            
    # Sort by hour to ensure deterministic order
    pivot_df = pivot_df.sort_values('hour').reset_index(drop=True)
    
    # Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    
    return pivot_df[target_columns]