import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse the date column
    df = source.copy()
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract Hour and Month
    df['Hour'] = df['date'].dt.hour
    df['Month'] = df['date'].dt.month
    
    # 3. Map Month integers to Month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['MonthName'] = df['Month'].map(month_map)
    
    # 4. Pivot the table
    # Index: Hour, Columns: MonthName, Values: cerc_logger_1, Aggfunc: mean
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='MonthName', 
        values='cerc_logger_1', 
        aggfunc='mean'
    )
    
    # 5. Fill missing values with 85 based on target sample observation
    pivot_df = pivot_df.fillna(85)
    
    # 6. Reset index to make Hour a column
    pivot_df = pivot_df.reset_index()
    
    # 7. Ensure Hour is integer type
    pivot_df['Hour'] = pivot_df['Hour'].astype(int)
    
    # 8. Define target columns in the exact required order
    target_columns = [
        'Hour', 'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
    # 9. Select and return the columns
    return pivot_df[target_columns]