import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse the date column
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    
    # 2. Define the mapping from source hour columns to target hour columns
    # Logic: 
    # 12:00 AM -> Hr 24 (Midnight, end of day)
    # 1:00 AM -> Hr 1
    # ...
    # 11:00 AM -> Hr 11
    # 12:00 PM -> Hr 12
    # 1:00 PM -> Hr 13
    # ...
    # 11:00 PM -> Hr 23
    
    rename_map = {}
    for i in range(1, 12):
        rename_map[f'{i}:00 AM'] = f'Hr {i}'
    rename_map['12:00 PM'] = 'Hr 12'
    for i in range(1, 12):
        rename_map[f'{i}:00 PM'] = f'Hr {12 + i}'
    rename_map['12:00 AM'] = 'Hr 24'
    
    # 3. Group by date and aggregate (mean) to handle potential duplicates
    # We select only the date and hour columns for grouping, excluding DSL
    hour_cols = [c for c in df.columns if c != 'date' and c != 'DSL']
    df_grouped = df.groupby('date')[hour_cols].mean()
    
    # 4. Handle missing dates by reindexing to a complete date range
    # This explains the row count increase (filling gaps)
    min_date = df_grouped.index.min()
    max_date = df_grouped.index.max()
    full_date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    df_grouped = df_grouped.reindex(full_date_range)
    
    # Fill NaNs with 0 for missing hours/dates
    df_grouped = df_grouped.fillna(0)
    
    # 5. Reset index to make 'date' a column
    df_grouped = df_grouped.reset_index()
    
    # 6. Rename columns
    df_grouped = df_grouped.rename(columns=rename_map)
    df_grouped = df_grouped.rename(columns={'date': 'Date'})
    
    # 7. Format the Date column as 'YYYY-MM-DD 00:00:00'
    df_grouped['Date'] = df_grouped['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 8. Define target columns
    target_columns = ['Date'] + [f'Hr {i}' for i in range(1, 25)]
    
    # 9. Return the DataFrame with target columns
    return df_grouped[target_columns]