import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Map Time Period to Month Number
    month_map = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    
    # Create a copy to avoid modifying the original
    df = source.copy()
    
    # Map Time Period to month integer. If not in map (e.g., 'All'), set to NaN
    df['month'] = df['Time Period'].map(month_map)
    
    # 2. Prepare for Pivoting
    # We will group by month, hour, and End Use to aggregate across Day Types
    # Using mean for average demand
    pivot_df = df.groupby(['month', 'Hour Ending', 'End Use'])['Average Demand Per Home With This End Use [kW]'].mean().reset_index()
    
    # 3. Pivot the table
    # Index: month, Hour Ending
    # Columns: End Use
    # Values: Average Demand
    pivot_df = pivot_df.pivot_table(
        index=['month', 'Hour Ending'],
        columns='End Use',
        values='Average Demand Per Home With This End Use [kW]',
        aggfunc='mean'
    ).reset_index()
    
    # 4. Map End Use column names to Target Column names
    # Define mapping based on common end-use categories
    end_use_mapping = {
        'HVAC': 'hvac',
        'Water Heating': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator', # Often grouped
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Stove': 'cooking_range',
        'Pool/Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting', # Generic lighting
        'Plug Loads': 'plug',
        'Miscellaneous Plug Loads': 'plug',
        'Pool/Spa Heater': 'pool_spa_heater'
    }
    
    # Rename columns
    pivot_df.rename(columns=end_use_mapping, inplace=True)
    
    # 5. Rename Hour Ending to hour
    pivot_df.rename(columns={'Hour Ending': 'hour'}, inplace=True)
    
    # 6. Define Target Columns
    target_columns = [
        'month', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heater'
    ]
    
    # 7. Fill NaNs with 0 for appliance columns
    # month and hour might be NaN if not present in source, but we keep them as is for now
    # The target sample shows 0 for appliances when not present
    for col in target_columns:
        if col in ['month', 'hour']:
            continue
        if col in pivot_df.columns:
            pivot_df[col] = pivot_df[col].fillna(0)
        else:
            # If column doesn't exist, create it with 0
            pivot_df[col] = 0
            
    # 8. Cast types according to target schema
    # month: float64 (to handle NaN)
    pivot_df['month'] = pivot_df['month'].astype('float64')
    
    # hour: int64. Need to handle NaN if any.
    # If hour is NaN, we might need to decide what to do. 
    # Assuming hour is always present and valid integer in valid rows.
    # If there are NaN hours, we might need to fill or drop. 
    # Given the target sample has valid hours, we assume valid data.
    # However, to be safe, if hour is float due to NaN, we can't cast to int64 directly.
    # Let's check if hour has NaN. If so, fill with 0 or keep as float? 
    # Target schema says int64.
    if pivot_df['hour'].isnull().any():
        pivot_df['hour'] = pivot_df['hour'].fillna(0).astype('int64')
    else:
        pivot_df['hour'] = pivot_df['hour'].astype('int64')
        
    # Appliance columns:
    # hvac: float64
    pivot_df['hvac'] = pivot_df['hvac'].astype('float64')
    
    # Others: int64
    int_columns = [
        'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 
        'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 
        'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater'
    ]
    
    for col in int_columns:
        if col in pivot_df.columns:
            # Fill any remaining NaNs with 0 before casting to int
            pivot_df[col] = pivot_df[col].fillna(0).astype('int64')
            
    # 9. Select and Order Columns
    result_df = pivot_df[target_columns]
    
    # 10. Sort by month and hour to match typical time-series order
    # Note: month might be NaN. NaN sorts last or first depending on implementation.
    # The target sample shows NaN months first, then month 3.
    # Pandas sort_index or sort_values handles NaNs.
    # Let's sort by month (na_last=False to put NaNs first if desired, or default)
    # Default sort_values puts NaNs last. The sample has NaNs first.
    # We can use na_position='first'
    result_df = result_df.sort_values(by=['month', 'hour'], na_position='first').reset_index(drop=True)
    
    return result_df