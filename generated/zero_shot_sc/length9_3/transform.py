import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse 'SEASON DAY TYPE' into 'season' and 'daytype'
    # Example: "June WE" -> Month: June, Type: WE
    parts = source['SEASON DAY TYPE'].str.split(' ', n=1, expand=True)
    month_str = parts[0]
    day_type_str = parts[1]
    
    # Map months to seasons
    # Winter: Dec, Jan, Feb
    # Spring: Mar, Apr, May
    # Summer: Jun, Jul, Aug
    # Autumn: Sep, Oct, Nov
    month_to_season = {
        'January': 'WINTER', 'February': 'WINTER', 'March': 'SPRING',
        'April': 'SPRING', 'May': 'SPRING', 'June': 'SUMMER',
        'July': 'SUMMER', 'August': 'SUMMER', 'September': 'AUTUMN',
        'October': 'AUTUMN', 'November': 'AUTUMN', 'December': 'WINTER'
    }
    
    # Map day types
    day_type_map = {
        'WD': 'WEEKDAY',
        'WE': 'WEEKEND'
    }
    
    df = source.copy()
    
    # Create season column
    df['season'] = month_str.map(month_to_season)
    
    # Create daytype column
    df['daytype'] = day_type_str.map(day_type_map)
    
    # 2. Map 'HOUR' to 'hour'
    df['hour'] = df['HOUR'].astype('int64')
    
    # 3. Map 'T_MIN_1' to 'low_end' and 'T_MAX_1' to 'high_end'
    # Based on the 1-to-1 row mapping and typical schema conventions, we use the _1 suffix.
    # We convert to int64 as per target schema.
    df['low_end'] = df['T_MIN_1'].astype('int64')
    df['high_end'] = df['T_MAX_1'].astype('int64')
    
    # 4. Calculate 'temperature_range'
    df['temperature_range'] = (df['high_end'] - df['low_end']).astype('int64')
    
    # 5. Set 'constant' and 'coefficient' to NaN
    # The target sample shows these as nan. The source has values, but the target schema
    # for this benchmark seems to ignore them or expects them to be null.
    df['constant'] = np.nan
    df['coefficient'] = np.nan
    
    # 6. Select and order columns as per target schema
    target_columns = ['season', 'daytype', 'hour', 'temperature_range', 'constant', 'coefficient', 'low_end', 'high_end']
    
    return df[target_columns]