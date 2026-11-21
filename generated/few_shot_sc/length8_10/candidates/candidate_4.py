import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column to extract month
    # Format is 'Day MM/DD/YYYY', e.g., 'Thu 10/01/2009'
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%a %m/%d/%Y')
    df['month_num'] = df['parsed_date'].dt.month
    
    # 2. Identify hourly columns
    # Columns are '1:00', '2:00', ..., '24:00:00'
    # We exclude 'Segment', 'Date', and the helper columns we just added
    hour_cols = [c for c in df.columns if c not in ['Segment', 'Date', 'parsed_date', 'month_num']]
    
    # 3. Melt the dataframe to long format
    # value_vars are the hour columns
    melted = df.melt(id_vars=['month_num'], value_vars=hour_cols, var_name='hour_str', value_name='value')
    
    # 4. Clean the hour string to extract integer hour
    # '1:00' -> 1, '24:00:00' -> 24
    def extract_hour(h_str):
        # Split by ':' and take the first part
        return int(h_str.split(':')[0])
    
    melted['hour'] = melted['hour_str'].apply(extract_hour)
    
    # 5. Group by hour and month, calculate mean
    # We want the average value for each hour in each month
    grouped = melted.groupby(['hour', 'month_num'])['value'].mean().reset_index()
    
    # 6. Map month numbers to month names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    grouped['month_name'] = grouped['month_num'].map(month_map)
    
    # 7. Pivot the table
    # Index: hour, Columns: month_name, Values: value
    pivoted = grouped.pivot(index='hour', columns='month_name', values='value')
    
    # 8. Clean up the pivoted dataframe
    pivoted = pivoted.reset_index()
    
    # Ensure hour is int64
    pivoted['hour'] = pivoted['hour'].astype('int64')
    
    # Sort by hour numerically
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    # Ensure all month columns are present (in case some months are missing for some hours)
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    for m in target_months:
        if m not in pivoted.columns:
            pivoted[m] = 0.0 # Or NaN, but 0 is safer if expected
            
    # Reorder columns to match target schema
    target_columns = ['hour'] + target_months
    
    # Select and return
    return pivoted[target_columns]