import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse date and extract month
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
    df['month_num'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.month_name().str.lower()
    
    # 2. Identify hourly columns and map to integer hours
    # Source columns are like '1:00 AM', '12:00 PM', etc.
    # We need to map these to 1-24 (or 0-23).
    # 12:00 AM is midnight (0), 1:00 AM is 1, ..., 11:00 AM is 11
    # 12:00 PM is noon (12), 1:00 PM is 13, ..., 11:00 PM is 23
    
    hour_mapping = {}
    for col in df.columns:
        if col in ['date', 'DSL', 'month_num', 'month_name']:
            continue
        try:
            # Parse '1:00 AM' -> 1, '12:00 AM' -> 0, '1:00 PM' -> 13, '12:00 PM' -> 12
            parts = col.split(':')
            time_val = int(parts[0])
            ampm = parts[1].strip()
            
            if ampm == 'AM':
                if time_val == 12:
                    hour = 0
                else:
                    hour = time_val
            else: # PM
                if time_val == 12:
                    hour = 12
                else:
                    hour = time_val + 12
            hour_mapping[col] = hour
        except Exception:
            pass
            
    # 3. Melt the dataframe
    # Keep date, month_name, month_num. Melt the hourly columns.
    melt_cols = [c for c in df.columns if c in hour_mapping]
    
    df_melted = df.melt(
        id_vars=['date', 'month_name', 'month_num'],
        value_vars=melt_cols,
        var_name='hour_col',
        value_name='value'
    )
    
    # 4. Map hour_col to integer hour
    df_melted['hour'] = df_melted['hour_col'].map(hour_mapping)
    
    # 5. Group by month and hour, and calculate mean
    # The target seems to be the average value for each hour in each month
    df_agg = df_melted.groupby(['month_name', 'hour'])['value'].mean().reset_index()
    
    # 6. Pivot to get months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month_name', values='value')
    
    # 7. Rename columns to match target exactly (lowercase month names)
    # The pivot columns are already lowercase month names from step 1
    df_pivot.columns.name = None
    
    # 8. Reset index to make 'hour' a column
    df_result = df_pivot.reset_index()
    
    # 9. Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # Ensure all target columns exist, filling with NaN if a month is missing in data
    for col in target_columns:
        if col not in df_result.columns:
            df_result[col] = np.nan
            
    # Sort by hour to ensure deterministic order (assuming standard ascending order)
    # Note: The sample target order was 1, 10, 11, 12, 6, 7, 8, 9 which is non-standard.
    # However, without explicit instruction on row ordering, sorting by the key 'hour' is standard.
    # If the source column order is required, we would need to map hours back to source column indices.
    # Given the ambiguity, standard sort is the most robust generalization.
    df_result = df_result.sort_values(by='hour').reset_index(drop=True)
    
    # 10. Return only the target columns
    return df_result[target_columns]