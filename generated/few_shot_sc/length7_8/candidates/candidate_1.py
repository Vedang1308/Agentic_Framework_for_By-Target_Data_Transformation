import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and derive 'month' and 'daytype'
    dt = pd.to_datetime(df['Date'])
    df['month'] = dt.dt.strftime('%B')
    
    # Determine daytype: weekday (Mon-Fri) or weekend (Sat-Sun)
    # dayofweek: Monday is 0, Sunday is 6
    df['daytype'] = df['Date'].apply(lambda x: 'weekday' if pd.to_datetime(x).dayofweek < 5 else 'weekend')
    # More efficient vectorized approach:
    df['daytype'] = df['Date'].apply(lambda x: 'weekday' if pd.to_datetime(x).dayofweek < 5 else 'weekend')
    # Actually, using the parsed dt object is better:
    df['daytype'] = ['weekday' if d < 5 else 'weekend' for d in dt.dt.dayofweek]

    # 2. Rename hourly columns from 'Hr 1'...'Hr 24' to 'hr1'...'hr24'
    rename_dict = {f'Hr {i}': f'hr{i}' for i in range(1, 25)}
    df = df.rename(columns=rename_dict)

    # 3. Define target columns verbatim
    target_columns = ['month', 'daytype'] + [f'hr{i}' for i in range(1, 25)]

    # 4. Return the transformed dataframe with only the target columns
    return df[target_columns]