import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract the month
    # The date format is '%m/%d/%Y'
    source = source.copy()
    source['date'] = pd.to_datetime(source['date'], format='%m/%d/%Y')
    source['month'] = source['date'].dt.month
    
    # 2. Identify hourly columns
    # Exclude 'date', 'month' (just added), and 'DSL'
    hourly_cols = [col for col in source.columns if col not in ['date', 'month', 'DSL']]
    
    # 3. Melt the DataFrame to long format
    # Each row will represent a specific date, hour, and value
    melted = source.melt(
        id_vars=['date', 'month'],
        value_vars=hourly_cols,
        var_name='time_label',
        value_name='value'
    )
    
    # 4. Map time_label strings to integer hours (1-12)
    # Mapping logic:
    # 1:00 AM -> 1, ..., 11:00 AM -> 11
    # 12:00 PM -> 12
    # 1:00 PM -> 1, ..., 11:00 PM -> 11
    # 12:00 AM -> 12
    
    def parse_hour(time_label):
        # Split by space to get "1:00" and "AM"
        parts = time_label.split()
        time_str = parts[0]
        am_pm = parts[1]
        
        # Extract hour number
        hour = int(time_str.split(':')[0])
        
        if am_pm == 'AM':
            if hour == 12:
                return 12  # 12:00 AM is 12
            else:
                return hour
        else: # PM
            if hour == 12:
                return 12  # 12:00 PM is 12
            else:
                return hour
                
    melted['hour'] = melted['time_label'].apply(parse_hour)
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour and month combination
    agg_df = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot the DataFrame
    # Index: hour, Columns: month, Values: value
    pivoted = agg_df.pivot(index='hour', columns='month', values='value')
    
    # 7. Map month numbers to month names
    month_names = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june',
        7: 'july', 8: 'august', 9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    
    pivoted.rename(columns=month_names, inplace=True)
    
    # 8. Reset index to make 'hour' a column
    df = pivoted.reset_index()
    
    # 9. Ensure hour is integer
    df['hour'] = df['hour'].astype(int)
    
    # 10. Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 11. Sort by hour to ensure deterministic output order (optional but good practice)
    df = df.sort_values(by='hour').reset_index(drop=True)
    
    # 12. Return the DataFrame with exact target columns
    return df[target_columns]