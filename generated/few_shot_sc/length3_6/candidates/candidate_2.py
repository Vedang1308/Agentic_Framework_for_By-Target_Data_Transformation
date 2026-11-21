import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse and format the date column
    # Source format: M/D/YYYY (e.g., '7/3/2014')
    # Target format: YYYY-MM-DD 00:00:00
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # 2. Map hourly columns from 12-hour format to 'Hour 1'..'Hour 24'
    # Logic:
    # 12:00 AM (00:00) -> Hour 1
    # 1:00 AM (01:00)  -> Hour 2
    # ...
    # 11:00 AM (11:00) -> Hour 12
    # 12:00 PM (12:00) -> Hour 13
    # 1:00 PM (13:00)  -> Hour 14
    # ...
    # 11:00 PM (23:00) -> Hour 24
    
    rename_dict = {}
    
    # Handle 12:00 AM separately as it maps to Hour 1
    rename_dict['12:00 AM'] = 'Hour 1'
    
    # Handle 1:00 AM to 11:00 AM -> Hour 2 to Hour 12
    for h in range(1, 12):
        rename_dict[f'{h}:00 AM'] = f'Hour {h + 1}'
        
    # Handle 12:00 PM separately as it maps to Hour 13
    rename_dict['12:00 PM'] = 'Hour 13'
    
    # Handle 1:00 PM to 11:00 PM -> Hour 14 to Hour 24
    for h in range(1, 12):
        rename_dict[f'{h}:00 PM'] = f'Hour {h + 12}'
        
    df = df.rename(columns=rename_dict)
    
    # 3. Define target columns in the correct order
    target_columns = ['date'] + [f'Hour {i}' for i in range(1, 25)]
    
    # 4. Return the dataframe with only the target columns
    # This implicitly drops 'DSL' and any other unused columns
    return df[target_columns]