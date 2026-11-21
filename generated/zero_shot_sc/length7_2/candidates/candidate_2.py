import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column to extract month
    # DT_STRATA format is '%m/%d/%Y'
    dt_series = pd.to_datetime(source['DT_STRATA'], format='%m/%d/%Y')
    
    # Extract month name (e.g., "January", "July")
    month_names = dt_series.dt.month_name()
    
    # 2. Map DOW to daytype
    # 1-5: weekday, 6-7: weekend, H: holiday
    # D: Assuming 'D' maps to weekday based on common dataset conventions where it's not a weekend/holiday
    dow_map = {
        '1': 'weekday',
        '2': 'weekday',
        '3': 'weekday',
        '4': 'weekday',
        '5': 'weekday',
        '6': 'weekend',
        '7': 'weekend',
        'H': 'holiday',
        'D': 'weekday' # Defaulting D to weekday as it's not a weekend or holiday
    }
    
    daytypes = source['DOW'].map(dow_map)
    
    # 3. Select and rename hourly columns
    # Source columns are PCT_HOURLY_0100 to PCT_HOURLY_2400
    # Target columns are hr1 to hr24
    
    hourly_source_cols = [f'PCT_HOURLY_{i:04d}' for i in range(1, 25)]
    hourly_target_cols = [f'hr{i}' for i in range(1, 25)]
    
    # Create a rename dictionary
    rename_dict = {src: tgt for src, tgt in zip(hourly_source_cols, hourly_target_cols)}
    
    # Filter source to only include necessary columns for the target structure
    # We keep the new calculated columns and the renamed hourly columns
    df = source.copy()
    
    # Assign new columns
    df['month'] = month_names
    df['daytype'] = daytypes
    
    # Rename hourly columns
    df = df.rename(columns=rename_dict)
    
    # Define the exact target column order
    target_columns = ['month', 'daytype'] + hourly_target_cols
    
    # Return the dataframe with the correct columns
    return df[target_columns]