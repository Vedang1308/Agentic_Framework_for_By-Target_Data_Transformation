import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # Aggregate zone_016 by Hour and Month using mean
    # This handles the multiple minutes per hour by averaging them
    aggregated = df.groupby(['Hour', 'Month'])['zone_016'].mean()
    
    # Pivot/Unstack to get Months as columns
    # Index will be Hour, Columns will be Month (1-12)
    pivoted = aggregated.unstack('Month')
    
    # Reset index to make Hour a column
    pivoted = pivoted.reset_index()
    
    # Rename the month columns to their full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivoted = pivoted.rename(columns=month_names)
    
    # Ensure all hours 0-23 are present
    # Create a full range of hours
    full_hours = pd.DataFrame({'Hour': range(24)})
    
    # Merge with pivoted data to ensure all hours are represented
    # Left join on Hour to keep all 24 hours
    result = full_hours.merge(pivoted, on='Hour', how='left')
    
    # Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure column order matches target
    result = result[target_columns]
    
    # Ensure Hour is int64
    result['Hour'] = result['Hour'].astype('int64')
    
    return result[target_columns]