import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with columns ['date', 'cerc_logger_1']
    into a target DataFrame with daily hourly averages pivoted into columns
    'Hour 1' through 'Hour 24'.
    """
    # 1. Parse the date column
    # Source format: '%m/%d/%Y %H:%M'
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    # Target date format: '%m/%d/%Y'
    df['date_str'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23) and convert to 1-24 for target column naming
    # Hour 1 corresponds to 00:xx, Hour 24 corresponds to 23:xx
    df['hour_idx'] = df['datetime'].dt.hour + 1
    
    # 3. Aggregate
    # Group by date and hour, calculate the mean of cerc_logger_1
    # Using mean as a standard aggregation for sensor readings within an hour
    grouped = df.groupby(['date_str', 'hour_idx'])['cerc_logger_1'].mean().reset_index()
    
    # 4. Pivot
    # Pivot the table so that each hour becomes a column
    pivot_df = grouped.pivot(index='date_str', columns='hour_idx', values='cerc_logger_1')
    
    # 5. Rename columns
    # The columns are currently integers 1-24. Rename them to "Hour 1", "Hour 2", etc.
    pivot_df.columns = [f"Hour {int(col)}" for col in pivot_df.columns]
    
    # 6. Reset index to make 'date' a column
    pivot_df = pivot_df.reset_index()
    pivot_df.rename(columns={'date_str': 'date'}, inplace=True)
    
    # 7. Ensure all 24 hours are present, filling missing ones with NaN (or 0 if preferred, but NaN is standard for missing)
    # Define the expected columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence of all hours
    # If a day is missing an hour, it will be NaN.
    pivot_df = pivot_df.reindex(columns=target_columns)
    
    # 8. Return the final DataFrame
    return pivot_df[target_columns]