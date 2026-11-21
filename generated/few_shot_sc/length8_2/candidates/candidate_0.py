import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the date column
    df['datetime'] = pd.to_datetime(df['date'])
    
    # 2. Extract Hour and Month
    df['Hour'] = df['datetime'].dt.hour
    df['Month_Num'] = df['datetime'].dt.month
    
    # 3. Map Month numbers to Names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['Month_Name'] = df['Month_Num'].map(month_map)
    
    # 4. Aggregate by Hour and Month
    # We group by Hour and Month_Name, then take the mean of zone_016
    # Using unstack to pivot Month_Name into columns
    pivot_df = df.groupby(['Hour', 'Month_Name'])['zone_016'].mean().unstack(fill_value=np.nan)
    
    # 5. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 6. Ensure all hours 0-23 are present
    all_hours = pd.DataFrame({'Hour': range(24)})
    pivot_df = all_hours.merge(pivot_df, on='Hour', how='left')
    
    # 7. Define target columns verbatim
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 8. Select and return
    return pivot_df[target_columns]