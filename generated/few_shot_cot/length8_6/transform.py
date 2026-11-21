import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and extract month name
    df['date_dt'] = pd.to_datetime(df['date'])
    df['month_num'] = df['date_dt'].dt.month
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month_name'] = df['month_num'].map(month_map)
    
    # 2. Identify hourly columns (all except date, DSL, and our new cols)
    # The source has columns like '1:00 AM', '2:00 AM', etc.
    # We can identify them by excluding known non-hourly columns.
    exclude_cols = ['date', 'DSL', 'date_dt', 'month_num', 'month_name']
    hourly_cols = [c for c in df.columns if c not in exclude_cols]
    
    # 3. Melt the dataframe to long format
    # id_vars keep the date info, value_vars are the hours
    melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hourly_cols, 
        var_name='hour_label', 
        value_name='value'
    )
    
    # 4. Parse hour_label to integer hour (1-24)
    # Format is "H:00 AM/PM"
    # 12:00 AM -> 0 hour -> 1
    # 1:00 AM -> 1 hour -> 2
    # ...
    # 12:00 PM -> 12 hour -> 13
    # ...
    # 11:00 PM -> 23 hour -> 24
    
    def parse_hour(label):
        # Parse the time string
        # Using pd.to_datetime with format %I:%M %p
        # Note: label might have spaces, e.g., "1:00 AM"
        try:
            t = pd.to_datetime(label, format='%I:%M %p')
            h = t.hour
            # Convert 0-23 to 1-24
            return h + 1
        except:
            return np.nan
            
    melted['hour'] = melted['hour_label'].apply(parse_hour)
    
    # 5. Aggregate by hour and month
    # Calculate mean value for each hour and month combination
    agg_df = melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot to wide format
    # Index: hour, Columns: month_name, Values: value
    pivoted = agg_df.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Clean up and format
    pivoted = pivoted.reset_index()
    
    # Rename columns to match target exactly
    # The pivot creates columns named after month_name
    # Ensure all 12 months are present, even if NaN
    target_months = ['january', 'february', 'march', 'april', 'may', 'june', 
                     'july', 'august', 'september', 'october', 'november', 'december']
    
    # Reindex columns to ensure all months are present
    pivoted = pivoted.reindex(columns=['hour'] + target_months)
    
    # Sort by hour for deterministic output
    pivoted = pivoted.sort_values('hour').reset_index(drop=True)
    
    # Ensure hour is int64
    pivoted['hour'] = pivoted['hour'].astype('int64')
    
    # Define final target columns
    target_columns = ['hour'] + target_months
    
    return pivoted[target_columns]