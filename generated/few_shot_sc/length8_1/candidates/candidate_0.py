import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['dt'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month Name
    df['Hour'] = df['dt'].dt.hour
    df['Month'] = df['dt'].dt.month.map({
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    })
    
    # 3. Pivot the data
    # Aggregate by mean. Based on the presence of 85 as a likely fill value for missing data
    # and the nature of the other values (decimals), mean is the standard aggregation.
    pivot_df = df.pivot_table(index='Hour', columns='Month', values='cerc_logger_1', aggfunc='mean')
    
    # 4. Fill missing values with 85
    pivot_df = pivot_df.fillna(85)
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure Hour is integer
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 7. Define target columns in the correct order
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 8. Select and return columns
    return pivot_df[target_columns]