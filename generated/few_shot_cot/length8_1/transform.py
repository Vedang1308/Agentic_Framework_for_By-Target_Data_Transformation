import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Parse date
    df['date'] = pd.to_datetime(df['date'])
    
    # Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # Map month numbers to names
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month'].map(month_names)
    
    # Group by Hour and Month_Name, calculate mean of cerc_logger_1
    # Using mean as the aggregation function
    grouped = df.groupby(['Hour', 'Month_Name'])['cerc_logger_1'].mean()
    
    # Unstack to pivot months into columns
    pivot_df = grouped.unstack()
    
    # Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # Define target columns
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
    
    # Ensure all target columns exist
    for col in target_columns[1:]:
        if col not in pivot_df.columns:
            pivot_df[col] = 0 # Default to 0 if month is missing entirely
            
    # Sort by Hour
    pivot_df = pivot_df.sort_values('Hour').reset_index(drop=True)
    
    # Select and return
    return pivot_df[target_columns]