import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse the Date column
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 2. Extract month name from the Date
    df['month_name'] = df['Date'].dt.month_name()
    
    # 3. Melt the hourly columns (1-24) into a long format
    # Identify the hourly columns
    hour_cols = [str(i) for i in range(1, 25)]
    
    df_melted = df.melt(
        id_vars=['month_name'], 
        value_vars=hour_cols, 
        var_name='hour', 
        value_name='value'
    )
    
    # 4. Convert hour to integer
    df_melted['hour'] = df_melted['hour'].astype(int)
    
    # 5. Group by hour and month, calculate the mean
    # Note: We assume we want the average value for that hour across all days in that month
    grouped = df_melted.groupby(['hour', 'month_name'])['value'].mean().reset_index()
    
    # 6. Pivot the data so months become columns
    df_pivoted = grouped.pivot(index='hour', columns='month_name', values='value').reset_index()
    
    # 7. Rename columns to lowercase
    df_pivoted.columns.name = None # Remove column axis name
    rename_map = {col: col.lower() for col in df_pivoted.columns}
    df_pivoted = df_pivoted.rename(columns=rename_map)
    
    # 8. Define target columns
    target_columns = ['hour', 'january', 'february', 'march', 'april', 'may', 'june', 
                      'july', 'august', 'september', 'october', 'november', 'december']
    
    # 9. Ensure all target columns exist (fill missing months with NaN if any)
    for col in target_columns:
        if col not in df_pivoted.columns:
            df_pivoted[col] = np.nan
            
    # 10. Sort by hour to ensure deterministic order
    df_pivoted = df_pivoted.sort_values('hour').reset_index(drop=True)
    
    # 11. Return the final dataframe with exact target columns
    return df_pivoted[target_columns]