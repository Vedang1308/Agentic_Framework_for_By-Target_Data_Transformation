import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse date
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # Map month numbers to names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['Month'].map(month_map)
    
    # Aggregate by Hour and MonthName using mean
    # We use unstack to pivot MonthName into columns
    aggregated = df.groupby(['Hour', 'MonthName'])['cerc_logger_1'].mean()
    
    # Unstack to create columns for each month
    pivot_df = aggregated.unstack()
    
    # Fill missing values with 85 as seen in the target sample
    pivot_df = pivot_df.fillna(85)
    
    # Reset index to bring Hour back as a column
    pivot_df = pivot_df.reset_index()
    
    # Ensure column names match exactly. 
    # The unstack creates columns based on MonthName. 
    # We need to ensure the order matches the target: Hour, Jan, Feb, ... Dec
    
    target_month_cols = ['January', 'February', 'March', 'April', 'May', 'June', 
                         'July', 'August', 'September', 'October', 'November', 'December']
    
    # Reorder columns to match target schema
    # Hour is the first column from reset_index (level_0)
    # The rest are the month columns
    
    # Rename 'MonthName' level if necessary, but unstack usually uses the name of the column being unstacked
    # Let's ensure the column names are correct
    pivot_df.columns.name = None # Remove the column name index if any
    
    # Select and order columns
    # The 'Hour' column might be named 'Hour' or 'level_0' depending on groupby key name
    # We explicitly named the groupby key 'Hour' and 'MonthName'
    
    final_cols = ['Hour'] + target_month_cols
    
    # Check if all target month columns exist in pivot_df
    # If a month had no data at all, it might not be in the columns. 
    # We should ensure they exist and fill with 85 if missing entirely.
    for col in target_month_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 85
            
    return pivot_df[final_cols]