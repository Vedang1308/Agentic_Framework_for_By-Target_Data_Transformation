import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Identify hour columns
    hour_cols = [col for col in source.columns if col.startswith('Hour')]
    
    # 2. Parse dates and extract Day of Week
    # Source dates are in 'MM/DD/YYYY' format
    df = source.copy()
    df['date_dt'] = pd.to_datetime(df['date'])
    df['dow'] = df['date_dt'].dt.weekday  # 0=Monday, ..., 6=Sunday
    
    # 3. Aggregate by Day of Week to get the typical profile
    # The source contains 182 days (26 weeks), providing multiple samples for each DOW.
    # We take the mean to establish the canonical profile for each day of the week.
    # This handles any minor floating point inconsistencies if present, though data seems clean.
    profiles = df.groupby('dow')[hour_cols].mean()
    
    # 4. Define the target date range
    # Based on the sample, the target covers Jan 1, 2015 to July 2, 2015 (183 days).
    # This is the period preceding the source data (Jul 3 - Dec 31).
    target_dates = pd.date_range(start='2015-01-01', end='2015-07-02', freq='D')
    
    # 5. Construct the target DataFrame
    result = pd.DataFrame({'date': target_dates})
    result['dow'] = result['date'].dt.weekday
    
    # 6. Map the profiles to the target dates based on DOW
    # Rename 'dow' in profiles index to match merge key if necessary, but groupby result has 'dow' as index
    # Merge on 'dow'
    result = result.merge(profiles, left_on='dow', right_index=True)
    
    # 7. Format the date column 'cst' as '%a %m/%d/%Y'
    # e.g., 'Thu 01/01/2015'
    result['cst'] = result['date'].dt.strftime('%a %m/%d/%Y')
    
    # 8. Rename hour columns from 'Hour 1' to '1:00', etc.
    rename_map = {f'Hour {i}': f'{i}:00' for i in range(1, 25)}
    result = result.rename(columns=rename_map)
    
    # 9. Select and order the target columns verbatim
    target_columns = ['cst'] + [f'{i}:00' for i in range(1, 25)]
    
    # Ensure integer types for columns that were int in target (9:00 to 16:00)
    # The target schema specifies int64 for 9:00-16:00.
    # Pandas merge might keep them as float if the mean resulted in floats, but they are integers (0).
    # We should cast them back to int if they are effectively integers.
    int_cols = [f'{i}:00' for i in range(9, 17)]
    for col in int_cols:
        if col in result.columns:
            # Check if all values are integers
            if (result[col] % 1 == 0).all():
                result[col] = result[col].astype('int64')
                
    return result[target_columns]