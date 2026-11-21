import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # Extract date string in target format
    df['Date'] = df['datetime'].dt.strftime('%m/%d/%Y')
    
    # Extract hour (0-23) and convert to 1-based index (1-24)
    df['Hour_Index'] = df['datetime'].dt.hour + 1
    
    # Pivot the table:
    # Index: Date
    # Columns: Hour_Index (1 to 24)
    # Values: zone_016_cooling_sp
    # Aggfunc: mean (handles the 5-minute intervals by averaging them)
    pivot_df = df.pivot_table(
        index='Date',
        columns='Hour_Index',
        values='zone_016_cooling_sp',
        aggfunc='mean'
    )
    
    # Rename columns to match target format 'Hr 1', 'Hr 2', ...
    pivot_df.columns = [f'Hr {i}' for i in pivot_df.columns]
    
    # Reset index to make 'Date' a column
    pivot_df = pivot_df.reset_index()
    
    # Define the exact target column order
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # Select and order columns. If any hour is missing for a day, it will be NaN.
    # Ensure all target columns exist, filling missing ones with NaN if necessary
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = pd.NA
            
    return pivot_df[target_columns]