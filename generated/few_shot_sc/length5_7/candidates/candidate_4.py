import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse Date and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date').sort_index()
    
    # 2. Create a complete daily date range from min to max date
    start_date = df.index.min()
    end_date = df.index.max()
    full_index = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 3. Reindex to fill missing dates
    df = df.reindex(full_index)
    
    # 4. Fill missing values (forward fill then backward fill to handle edges)
    df = df.ffill().bfill()
    
    # 5. Rename numeric columns from '1'..'24' to 'value1'..'value24'
    rename_dict = {str(i): f'value{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)
    
    # 6. Reset index and format date column
    df = df.reset_index()
    df = df.rename(columns={'index': 'date'})
    df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 7. Define target columns and return
    target_columns = ['date'] + [f'value{i}' for i in range(1, 25)]
    return df[target_columns]