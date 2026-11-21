import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    source = source.copy()
    source['datetime'] = pd.to_datetime(source['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    source['Hour'] = source['datetime'].dt.hour
    source['MonthNum'] = source['datetime'].dt.month
    
    # 3. Map Month Number to Month Name
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    source['MonthName'] = source['MonthNum'].map(month_map)
    
    # 4. Pivot the table
    # Index: Hour, Columns: MonthName, Values: zone_016_cooling_sp
    # Aggregation: mean (to handle multiple entries for same hour/month)
    pivot_df = source.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='zone_016_cooling_sp', 
        aggfunc='mean'
    )
    
    # 5. Define target columns and hours
    target_months = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    target_hours = list(range(24))
    
    # 6. Reindex to ensure all hours (0-23) and all months are present
    pivot_df = pivot_df.reindex(index=target_hours, columns=target_months)
    
    # 7. Reset index to make 'Hour' a column
    pivot_df = pivot_df.reset_index()
    
    # 8. Rename the index column to 'Hour' if it's not already (reset_index names it 'Hour' if index was named 'Hour')
    # The pivot index was named 'Hour', so reset_index creates a column 'Hour'.
    
    # 9. Ensure column order matches target exactly
    target_columns = ['Hour'] + target_months
    
    # 10. Select and return
    df = pivot_df[target_columns]
    
    # 11. Ensure types match target schema
    # Hour: int64
    df['Hour'] = df['Hour'].astype('int64')
    # Months: float64 (already float due to NaNs in pivot/reindex)
    
    return df