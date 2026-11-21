import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Identify hour columns (all columns except 'date' and 'DSL')
    hour_cols = [c for c in df.columns if c not in ['date', 'DSL']]
    
    # Melt the dataframe to long format
    melted = df.melt(id_vars=['date'], value_vars=hour_cols, var_name='time_label', value_name='value')
    
    # Helper function to convert time label to hour (1-24)
    # 12:00 AM -> 1, 1:00 AM -> 2, ..., 11:00 AM -> 11, 12:00 PM -> 12, 1:00 PM -> 13, ..., 11:00 PM -> 24
    def parse_hour(label):
        # Split by space to get time part and AM/PM
        parts = label.split(' ')
        time_part = parts[0]
        ampm = parts[1]
        
        h_str, m_str = time_part.split(':')
        h = int(h_str)
        
        if ampm == 'AM':
            if h == 12:
                return 1
            else:
                return h + 1
        else: # PM
            if h == 12:
                return 12
            else:
                return h + 12

    melted['hour'] = melted['time_label'].apply(parse_hour)
    
    # Extract month name from date
    # Date format is M/D/YYYY
    dates = pd.to_datetime(melted['date'], format='%m/%d/%Y')
    melted['month'] = dates.dt.strftime('%B').str.lower()
    
    # Group by hour and month, and calculate the mean
    grouped = melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # Pivot the table
    pivoted = grouped.pivot(index='hour', columns='month', values='value').reset_index()
    
    # Rename columns to match target schema (months are already lowercase from strftime)
    # Ensure 'hour' is integer
    pivoted['hour'] = pivoted['hour'].astype(int)
    
    # Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Select and return
    return pivoted[target_columns]