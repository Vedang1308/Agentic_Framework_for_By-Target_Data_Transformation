import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month Name
    df['Hour'] = df['datetime'].dt.hour
    df['Month'] = df['datetime'].dt.strftime('%B')
    
    # 3. Pivot the data
    # Rows: Hour, Columns: Month, Values: zone_016_cooling_sp
    # Using mean to aggregate if there are multiple entries for same hour/month
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Month', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 4. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 5. Ensure all hours 0-23 are present
    all_hours = range(24)
    pivot_df = pivot_df.set_index('Hour').reindex(all_hours).reset_index()
    
    # 6. Define target columns verbatim
    target_columns = ['Hour', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    # 7. Select and return
    return pivot_df[target_columns]