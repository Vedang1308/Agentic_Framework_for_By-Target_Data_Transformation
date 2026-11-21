import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame with columns ['date', 'cerc_logger_1']
    into a target DataFrame with columns ['Date', 'Hr 1', ..., 'Hr 24'].
    
    The transformation involves:
    1. Parsing the date string.
    2. Extracting date and hour.
    3. Grouping by date and hour, averaging the sensor values.
    4. Pivoting the data so hours become columns.
    5. Formatting the output to match the target schema.
    """
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # 1. Parse the date column
    # The format is inferred as '%m/%d/%Y %H:%M'
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hour (0-23) to target hour index (1-24)
    # Hr 1 corresponds to 0:00-0:59, Hr 2 to 1:00-1:59, etc.
    df['target_hour'] = df['hour'] + 1
    
    # 4. Group by date and target_hour, and aggregate the sensor values
    # We use mean() as is standard for sensor data reduction from minute-level to hour-level
    df_agg = df.groupby(['date_only', 'target_hour'])['cerc_logger_1'].mean().reset_index()
    
    # 5. Pivot the table
    # Index: date_only, Columns: target_hour, Values: cerc_logger_1
    df_pivot = df_agg.pivot(index='date_only', columns='target_hour', values='cerc_logger_1')
    
    # 6. Clean up the pivot result
    # Reset index to make date_only a column
    df_pivot = df_pivot.reset_index()
    
    # Rename the 'date_only' column to 'Date'
    df_pivot = df_pivot.rename(columns={'date_only': 'Date'})
    
    # Format the Date column to '%m/%d/%Y'
    # Note: 'Date' is currently a date object or datetime. We convert to string.
    df_pivot['Date'] = df_pivot['Date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    
    # Rename the hour columns to match the target schema 'Hr 1', 'Hr 2', ...
    # The columns are currently integers 1, 2, ..., 24
    df_pivot.columns = ['Date'] + [f'Hr {col}' for col in df_pivot.columns[1:]]
    
    # 7. Ensure the column order matches the target exactly
    target_columns = ['Date', 'Hr 1', 'Hr 2', 'Hr 3', 'Hr 4', 'Hr 5', 'Hr 6', 'Hr 7', 'Hr 8', 'Hr 9', 'Hr 10', 'Hr 11', 'Hr 12', 'Hr 13', 'Hr 14', 'Hr 15', 'Hr 16', 'Hr 17', 'Hr 18', 'Hr 19', 'Hr 20', 'Hr 21', 'Hr 22', 'Hr 23', 'Hr 24']
    
    # Select only the columns that exist in the target schema to handle potential missing hours
    # and ensure correct order
    existing_cols = [col for col in target_columns if col in df_pivot.columns]
    df_pivot = df_pivot[existing_cols]
    
    # If any target columns are missing (e.g., no data for Hr 5 on a specific day), 
    # we should probably fill with NaN or 0 depending on requirements, but usually 
    # pandas pivot leaves them as NaN. The target schema implies float64, so NaN is acceptable.
    # However, to strictly match the column set if some hours are missing in the data entirely:
    for col in target_columns:
        if col not in df_pivot.columns:
            df_pivot[col] = float('nan')
            
    df_pivot = df_pivot[target_columns]
    
    return df_pivot[target_columns]