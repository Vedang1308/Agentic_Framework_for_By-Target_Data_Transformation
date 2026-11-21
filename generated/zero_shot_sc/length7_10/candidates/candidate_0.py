import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse the date column
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M')
    
    # 2. Extract features
    df['month'] = df['datetime'].dt.strftime('%B')
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    
    # 3. Determine daytype
    # 0-4: Weekday, 5-6: Weekend
    df['daytype'] = df['dayofweek'].apply(lambda x: 'weekday' if x < 5 else 'weekend')
    
    # 4. Create 1-based hour index for pivoting
    df['hr_index'] = df['hour'] + 1
    
    # 5. Aggregate by month, daytype, and hour
    # We take the mean of cerc_logger_1 for each group
    agg_df = df.groupby(['month', 'daytype', 'hr_index'])['cerc_logger_1'].mean().reset_index()
    
    # 6. Pivot the table
    # Index: month, daytype
    # Columns: hr_index (1-24)
    # Values: cerc_logger_1
    pivot_df = agg_df.pivot_table(index=['month', 'daytype'], columns='hr_index', values='cerc_logger_1')
    
    # 7. Rename columns to hr1, hr2, ..., hr24
    pivot_df.columns = [f'hr{col}' for col in pivot_df.columns]
    
    # 8. Reset index to bring month and daytype back as columns
    result_df = pivot_df.reset_index()
    
    # 9. Ensure column order matches target exactly
    target_columns = ['month', 'daytype', 'hr1', 'hr2', 'hr3', 'hr4', 'hr5', 'hr6', 'hr7', 'hr8', 'hr9', 'hr10', 'hr11', 'hr12', 'hr13', 'hr14', 'hr15', 'hr16', 'hr17', 'hr18', 'hr19', 'hr20', 'hr21', 'hr22', 'hr23', 'hr24']
    
    # Fill any potential NaNs if necessary, though pivot_table usually handles existing groups.
    # The target sample shows no NaNs, so we assume complete data or leave as is.
    
    return result_df[target_columns]