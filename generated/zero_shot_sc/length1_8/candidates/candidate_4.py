import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    # The source format is '%m/%d/%Y %H:%M'
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract components
    # We need the date for grouping and formatting
    source['date_dt'] = source['datetime'].dt.date
    
    # We need the hour for pivoting
    source['hour'] = source['datetime'].dt.hour
    
    # 3. Map hour to target column names
    # Hour 0 -> '24:00'
    # Hour 1 -> '1:00'
    # ...
    # Hour 23 -> '23:00'
    def map_hour(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    source['hour_col'] = source['hour'].apply(map_hour)
    
    # 4. Aggregate
    # Group by date and hour_col, take the mean of cerc_logger_1
    aggregated = source.groupby(['date_dt', 'hour_col'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot
    # Rows: date_dt
    # Columns: hour_col
    # Values: cerc_logger_1
    pivoted = aggregated.pivot(index='date_dt', columns='hour_col', values='cerc_logger_1')
    
    # 6. Format the date index to match target 'cst' format: '%a %m/%d/%Y'
    # Convert index to datetime for formatting
    pivoted.index = pd.to_datetime(pivoted.index)
    pivoted.index = pivoted.index.strftime('%a %m/%d/%Y')
    
    # 7. Reset index to make 'cst' a column
    pivoted = pivoted.reset_index()
    pivoted = pivoted.rename(columns={'index': 'cst'})
    
    # 8. Fill missing values with 0
    # The target sample shows 0 for missing data (e.g., Sat 02/16/2019)
    # Identify the hour columns to fill
    hour_columns = [f'{h}:00' for h in range(1, 24)] + ['24:00']
    pivoted[hour_columns] = pivoted[hour_columns].fillna(0)
    
    # 9. Ensure column order
    # Target columns: 'cst', '1:00', ..., '24:00'
    target_columns = ['cst'] + [f'{h}:00' for h in range(1, 24)] + ['24:00']
    
    # Select only existing columns to avoid KeyError if some hours are missing entirely
    existing_cols = [col for col in target_columns if col in pivoted.columns]
    
    # If some columns are missing (e.g., no data for hour 5), we should still include them filled with 0
    for col in target_columns:
        if col not in pivoted.columns:
            pivoted[col] = 0
            
    return pivoted[target_columns]