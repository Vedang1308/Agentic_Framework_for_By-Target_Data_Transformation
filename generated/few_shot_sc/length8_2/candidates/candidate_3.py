import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.month
    
    # 3. Group by Hour and Month and calculate the mean of zone_016
    # Using mean as the standard aggregation for time-series downsampling
    grouped = df.groupby(['Hour', 'Month'])['zone_016'].mean().reset_index()
    
    # 4. Pivot the table so that Months become columns
    pivoted = grouped.pivot(index='Hour', columns='Month', values='zone_016')
    
    # 5. Rename month columns to full names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    pivoted = pivoted.rename(columns=month_names)
    
    # 6. Ensure all hours 0-23 are present
    all_hours = pd.RangeIndex(0, 24)
    pivoted = pivoted.reindex(all_hours)
    
    # 7. Reset index to make 'Hour' a column
    pivoted = pivoted.reset_index()
    pivoted.rename(columns={'index': 'Hour'}, inplace=True)
    
    # 8. Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # 9. Select and return the target columns
    return pivoted[target_columns]