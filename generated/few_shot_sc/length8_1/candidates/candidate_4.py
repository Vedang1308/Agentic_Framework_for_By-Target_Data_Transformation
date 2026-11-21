import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month number
    df['Hour'] = df['datetime'].dt.hour
    df['Month_Num'] = df['datetime'].dt.month
    
    # 3. Map Month number to Month name
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_map)
    
    # 4. Aggregate and Pivot
    # Group by Hour and Month_Name, calculate mean of cerc_logger_1
    # Using mean is standard for sensor data unless specified otherwise.
    agg_df = df.groupby(['Hour', 'Month_Name'])['cerc_logger_1'].mean().reset_index()
    
    # Pivot the table: index=Hour, columns=Month_Name, values=cerc_logger_1
    pivot_df = agg_df.pivot(index='Hour', columns='Month_Name', values='cerc_logger_1')
    
    # 5. Format the output
    # Reset index to bring Hour back as a column
    pivot_df = pivot_df.reset_index()
    
    # Rename columns to match target exactly
    # The pivot columns are currently MultiIndex or just names, reset_index makes them columns
    # Ensure column names are strings
    pivot_df.columns.name = None # Remove column axis name
    
    # Define target columns order
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure Hour is int64
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # Select and order columns
    # Note: pivot might not have all months if data is missing, resulting in NaNs.
    # We should ensure all target columns exist.
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = float('nan')
            
    return pivot_df[target_columns]