import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract date and hour
    df['date_only'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    
    # 3. Map hours to target column labels
    # Hour 0 -> '24:00'
    # Hour 1 -> '1:00'
    # ...
    # Hour 23 -> '23:00'
    def map_hour(h):
        if h == 0:
            return '24:00'
        else:
            return f'{h}:00'
            
    df['hour_label'] = df['hour'].apply(map_hour)
    
    # 4. Pivot the table
    # Index: date_only, Columns: hour_label, Values: zone_016, Aggfunc: sum
    pivot_df = df.pivot_table(
        index='date_only', 
        columns='hour_label', 
        values='zone_016', 
        aggfunc='sum'
    )
    
    # 5. Fill NaNs with 0
    pivot_df = pivot_df.fillna(0)
    
    # 6. Define target column names for hours
    hour_cols = [f'{h}:00' for h in range(1, 24)] + ['24:00']
    
    # 7. Ensure all hour columns exist (even if empty in data)
    for col in hour_cols:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # 8. Select and order the hour columns
    pivot_df = pivot_df[hour_cols]
    
    # 9. Format the date index to 'cst' string format
    # Convert date_only back to datetime for formatting, then to string
    pivot_df = pivot_df.reset_index()
    pivot_df['cst'] = pd.to_datetime(pivot_df['date_only']).dt.strftime('%a %m/%d/%Y')
    
    # 10. Drop the intermediate date_only column
    pivot_df = pivot_df.drop(columns=['date_only'])
    
    # 11. Reorder columns: cst first, then hours
    final_columns = ['cst'] + hour_cols
    pivot_df = pivot_df[final_columns]
    
    # 12. Ensure data types match target (float64 for hours)
    for col in hour_cols:
        pivot_df[col] = pivot_df[col].astype(float)
        
    # Define target columns verbatim
    target_columns = ['cst', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00', '24:00']
    
    return pivot_df[target_columns]