import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source electricity rate table into a summary table of average rates
    per hour for each month.
    """
    # 1. Parse the Date column
    df = source.copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    
    # 2. Extract month and map to lowercase string names
    month_mapping = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april',
        5: 'may', 6: 'june', 7: 'july', 8: 'august',
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month'] = df['Date'].dt.month.map(month_mapping)
    
    # 3. Identify Hour columns and melt them
    # Source columns are 'Hr 1', 'Hr 2', ..., 'Hr 24'
    hr_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # Select only the necessary columns for melting
    # We keep 'month' for grouping, and the hour columns.
    # Other columns (Company, Rate, etc.) are implicitly averaged over.
    df_melted = df[['month'] + hr_cols].melt(
        id_vars=['month'],
        value_vars=hr_cols,
        var_name='hour_str',
        value_name='value'
    )
    
    # 4. Convert hour_str ('Hr 1') to integer hour (1)
    df_melted['hour'] = df_melted['hour_str'].str.replace('Hr ', '').astype(int)
    
    # 5. Aggregate by hour and month
    # Calculate the mean value for each hour in each month
    df_agg = df_melted.groupby(['hour', 'month'])['value'].mean().reset_index()
    
    # 6. Pivot to get months as columns
    df_pivot = df_agg.pivot(index='hour', columns='month', values='value').reset_index()
    
    # 7. Ensure all month columns are present and named correctly
    # The pivot might not have all months if data is missing, but we should ensure the schema matches.
    # Also, rename columns to match target exactly.
    
    target_months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Reindex columns to ensure all target months are present, filling NaN if necessary
    # Note: The problem implies a dense target, so we assume data exists for all.
    # However, to be safe, we can reindex.
    df_pivot = df_pivot.reindex(columns=['hour'] + target_months)
    
    # 8. Sort by hour to match target order
    df_pivot = df_pivot.sort_values('hour').reset_index(drop=True)
    
    # 9. Define target columns
    target_columns = ['hour'] + target_months
    
    # 10. Ensure types: hour as int, others as float
    df_pivot['hour'] = df_pivot['hour'].astype(int)
    for col in target_months:
        df_pivot[col] = df_pivot[col].astype(float)
        
    return df_pivot[target_columns]