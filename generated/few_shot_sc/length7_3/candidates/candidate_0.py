import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # Map abbreviated months to numbers
    month_abbr_to_num = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    # Map numbers to full month names
    num_to_month_full = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    
    # Apply shift: New Month = (Old Month Index + 6) % 12, with 0 treated as 12
    def shift_month(m):
        num = month_abbr_to_num[m]
        new_num = (num + 6) % 12
        if new_num == 0:
            new_num = 12
        return num_to_month_full[new_num]
        
    df['month'] = df['Month'].apply(shift_month)
    
    # Map Daytype
    daytype_map = {'WD': 'weekday', 'WE': 'weekend'}
    df['day'] = df['Daytype'].map(daytype_map)
    
    # Rename hourly columns
    rename_dict = {}
    for i in range(1, 25):
        old_col = f'{i}:00'
        new_col = f'hr{i}'
        if old_col in df.columns:
            rename_dict[old_col] = new_col
            
    df = df.rename(columns=rename_dict)
    
    # Define target columns
    target_columns = ['month', 'day'] + [f'hr{i}' for i in range(1, 25)]
    
    return df[target_columns]