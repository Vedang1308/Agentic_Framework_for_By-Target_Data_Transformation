import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse SEASON DAY TYPE into season and daytype
    # Example: "June WE" -> Month: "June", Type: "WE"
    parts = df['SEASON DAY TYPE'].str.split(' ', n=1, expand=True)
    month_str = parts[0]
    day_type_code = parts[1]
    
    # Map months to seasons
    month_to_season = {
        'January': 'WINTER', 'February': 'WINTER', 'December': 'WINTER',
        'March': 'SPRING', 'April': 'SPRING', 'May': 'SPRING',
        'June': 'SUMMER', 'July': 'SUMMER', 'August': 'SUMMER',
        'September': 'AUTUMN', 'October': 'AUTUMN', 'November': 'AUTUMN'
    }
    df['season'] = month_str.map(month_to_season)
    
    # Map day type codes to full names
    day_type_map = {
        'WE': 'WEEKEND',
        'WD': 'WEEKDAY'
    }
    df['daytype'] = day_type_code.map(day_type_map)
    
    # 2. Map numeric columns
    # Assuming the target uses the first set of variables (_1)
    df['hour'] = df['HOUR']
    df['low_end'] = df['T_MIN_1']
    df['high_end'] = df['T_MAX_1']
    df['constant'] = df['CONSTANT_1']
    df['coefficient'] = df['TEMP_1']
    
    # 3. Calculate temperature_range
    df['temperature_range'] = df['high_end'] - df['low_end']
    
    # 4. Select and order target columns
    target_columns = ['season', 'daytype', 'hour', 'temperature_range', 'constant', 'coefficient', 'low_end', 'high_end']
    
    return df[target_columns]