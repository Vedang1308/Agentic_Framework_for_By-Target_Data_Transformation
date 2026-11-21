import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Transform the date column
    # Source format: %m/%d/%Y
    # Target format: %Y-%m-%d %H:%M:%S
    dt = pd.to_datetime(df['date'])
    df['date'] = dt.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Rename hourly columns
    # Source columns: '1:00 AM', '2:00 AM', ..., '12:00 AM', '1:00 PM', ..., '11:00 PM'
    # Target columns: 'Hour 1', 'Hour 2', ..., 'Hour 24'
    # Mapping:
    # 12:00 AM -> Hour 1
    # 1:00 AM  -> Hour 2
    # ...
    # 11:00 AM -> Hour 12
    # 12:00 PM -> Hour 13
    # 1:00 PM  -> Hour 14
    # ...
    # 11:00 PM -> Hour 24
    
    rename_dict = {}
    for col in df.columns:
        if col in ['date', 'DSL']:
            continue
        if col.endswith('AM'):
            hour_str = col.split(':')[0]
            hour = int(hour_str)
            if hour == 12:
                target_hour = 1
            else:
                target_hour = hour + 1
        elif col.endswith('PM'):
            hour_str = col.split(':')[0]
            hour = int(hour_str)
            if hour == 12:
                target_hour = 13
            else:
                target_hour = hour + 13
        else:
            continue
            
        rename_dict[col] = f'Hour {target_hour}'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Select target columns
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    return df[target_columns]