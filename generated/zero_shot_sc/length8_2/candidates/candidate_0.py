import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['MonthNum'] = df['date'].dt.month
    
    # 3. Map Month Number to Month Name
    month_names = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['MonthNum'].map(month_names)
    
    # 4. Drop rows with NaN in the value column to ensure clean aggregation
    df_clean = df.dropna(subset=['zone_016'])
    
    # 5. Pivot the table
    # Index: Hour, Columns: MonthName, Values: zone_016, Aggfunc: mean
    pivot_df = df_clean.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='zone_016', 
        aggfunc='mean'
    )
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Define target columns
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 8. Ensure all target columns exist (fill with NaN if missing months)
    for col in target_columns[1:]: # Skip 'Hour'
        if col not in pivot_df.columns:
            pivot_df[col] = np.nan
            
    # 9. Select and order columns
    result_df = pivot_df[target_columns]
    
    # 10. Ensure correct data types
    result_df['Hour'] = result_df['Hour'].astype('int64')
    for col in target_columns[1:]:
        result_df[col] = result_df[col].astype('float64')
        
    # 11. Sort by Hour to match expected output order
    result_df = result_df.sort_values('Hour').reset_index(drop=True)
    
    return result_df[target_columns]