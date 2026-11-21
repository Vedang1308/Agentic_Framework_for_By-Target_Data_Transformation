import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    df = source.copy()
    
    # 1. Parse Date and Extract Month
    df['Date'] = pd.to_datetime(df['Date'])
    df['month_num'] = df['Date'].dt.month
    
    # Map month numbers to lowercase names
    month_map = {
        1: 'january', 2: 'february', 3: 'march', 4: 'april', 
        5: 'may', 6: 'june', 7: 'july', 8: 'august', 
        9: 'september', 10: 'october', 11: 'november', 12: 'december'
    }
    df['month'] = df['month_num'].map(month_map)
    
    # 2. Identify Hour Columns
    hour_cols = [f'Hr {i}' for i in range(1, 25)]
    
    # 3. Melt the DataFrame to Long Format
    # We only need 'month' and the hour values for aggregation
    # Other columns like Company, Rate, etc. are aggregated over (ignored in mean)
    melted_df = pd.melt(
        df, 
        id_vars=['month'], 
        value_vars=hour_cols, 
        var_name='hour_label', 
        value_name='rate'
    )
    
    # 4. Extract Hour Number from Label (e.g., 'Hr 1' -> 1)
    melted_df['hour'] = melted_df['hour_label'].str.replace('Hr ', '', regex=False).astype(int)
    
    # 5. Aggregate: Mean rate by hour and month
    agg_df = melted_df.groupby(['hour', 'month'])['rate'].mean().reset_index()
    
    # 6. Pivot to Wide Format
    # Index: hour, Columns: month, Values: rate
    target_df = agg_df.pivot(index='hour', columns='month', values='rate')
    
    # 7. Clean up and Format
    target_df = target_df.reset_index()
    
    # Ensure column names are strings and match target verbatim
    target_df.columns.name = None
    
    # Define target columns order
    target_columns = ['hour'] + [
        'january', 'february', 'march', 'april', 'may', 'june', 
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    
    # Sort by hour to ensure 1-24 order
    target_df = target_df.sort_values('hour').reset_index(drop=True)
    
    # Ensure 'hour' is int
    target_df['hour'] = target_df['hour'].astype(int)
    
    # Select and return only the required columns
    return target_df[target_columns]