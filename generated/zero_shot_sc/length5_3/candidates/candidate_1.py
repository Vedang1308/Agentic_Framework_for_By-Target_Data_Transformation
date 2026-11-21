import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with timestamped sensor readings 
    into a daily summary DataFrame with 24 hourly average values.
    """
    df = source.copy()
    
    # 1. Parse the date column to datetime
    # Source format: 'MM/DD/YYYY HH:MM'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract the date part for grouping and formatting
    # Target format: 'MM/DD/YYYY'
    df['date_group'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # 3. Extract the hour to determine the target column
    # Hour 0 -> value1, Hour 1 -> value2, ..., Hour 23 -> value24
    df['hour'] = df['datetime'].dt.hour
    df['value_col'] = 'value' + (df['hour'] + 1).astype(str)
    
    # 4. Aggregate
    # We group by the date and the target value column name, then take the mean.
    # This handles multiple readings per hour (e.g., every 10 mins) by averaging them.
    agg_df = df.groupby(['date_group', 'value_col'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the data
    # Rows: date_group, Columns: value_col, Values: cerc_logger_1
    pivot_df = agg_df.pivot(index='date_group', columns='value_col', values='cerc_logger_1')
    
    # 6. Clean up column names and index
    pivot_df.columns = pivot_df.columns.astype(str) # Ensure column names are strings
    pivot_df.index.name = 'date'
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure all 24 value columns exist, even if some hours have no data (fill with NaN or 0)
    target_columns = [f'value{i}' for i in range(1, 25)]
    
    # Reindex columns to ensure order and presence
    # If a column is missing in a specific day's pivot, it will be NaN.
    # We need to make sure the columns are in the correct order.
    existing_cols = [col for col in target_columns if col in pivot_df.columns]
    missing_cols = [col for col in target_columns if col not in pivot_df.columns]
    
    # Add missing columns as NaN if they don't exist (unlikely if data is dense)
    for col in missing_cols:
        pivot_df[col] = np.nan
        
    # Sort columns to match target order
    pivot_df = pivot_df[target_columns]
    
    # 8. Final formatting
    # The date column is already in 'MM/DD/YYYY' format from step 2
    
    # 9. Return only the target columns
    return pivot_df[['date'] + target_columns]