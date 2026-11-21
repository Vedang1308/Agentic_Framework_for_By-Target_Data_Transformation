import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # Parse the date column to datetime
    df['dt'] = pd.to_datetime(df['date'])
    
    # Extract date string in target format
    df['Date'] = df['dt'].dt.strftime('%m/%d/%Y')
    
    # Extract hour and map to 1-24 scale (0->1, 1->2, ..., 23->24)
    df['Hour'] = df['dt'].dt.hour + 1
    
    # Aggregate by Date and Hour. Using mean to handle multiple entries per hour.
    # If there's only one value per hour, mean is that value.
    pivot = df.pivot_table(
        index='Date', 
        columns='Hour', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # Rename columns to match target schema 'Hr 1', 'Hr 2', ...
    pivot.columns = [f'Hr {col}' for col in pivot.columns]
    
    # Ensure all hours 1-24 are present as columns, filling missing with NaN
    expected_hours = [f'Hr {i}' for i in range(1, 25)]
    pivot = pivot.reindex(columns=expected_hours)
    
    # Reset index to make 'Date' a column
    pivot = pivot.reset_index()
    
    # Define target columns verbatim
    target_columns = ['Date'] + expected_hours
    
    return pivot[target_columns]