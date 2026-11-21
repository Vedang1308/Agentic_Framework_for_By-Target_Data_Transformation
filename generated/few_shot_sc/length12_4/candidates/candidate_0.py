import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Map Time Period (Month) to Season
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'December': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    df['season'] = df['Time Period'].map(month_to_season)
    
    # 2. Calculate Total Demand
    # Fill NaN in Average Demand with 0 before multiplication
    df['avg_demand'] = df['Average Demand Per Home With This End Use [kW]'].fillna(0)
    df['num_homes'] = df['Number of Homes in Bin With This End Use Metered'].astype(float)
    df['total_demand'] = df['avg_demand'] * df['num_homes']
    
    # 3. Map End Use to Target Column Names
    end_use_map = {
        'HVAC': 'hvac',
        'Water Heater': 'water_heating',
        'Refrigerator': 'refrigerator',
        'Freezer': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Oven': 'cooking_range',
        'Pool/Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Plug Loads': 'plug',
        'Miscellaneous Plug Loads': 'plug',
        'Pool/Spa Heater': 'pool_spa_heater'
    }
    
    # Map the End Use column to the target column name
    df['target_col'] = df['End Use'].map(end_use_map)
    
    # Drop rows where End Use doesn't map to a target column (e.g., 'Remaining Load')
    df = df.dropna(subset=['target_col'])
    
    # 4. Aggregate
    # Group by season, hour, and target column name, summing the total demand
    agg_df = df.groupby(['season', 'Hour Ending', 'target_col'])['total_demand'].sum().reset_index()
    
    # 5. Pivot to wide format
    pivot_df = agg_df.pivot(index='season', columns='target_col', values='total_demand').reset_index()
    
    # Rename 'Hour Ending' if it's in the index, but here we grouped by it, so it's a column in agg_df?
    # Wait, pivot uses 'season' as index. 'Hour Ending' is a column in agg_df. 
    # We need to include 'Hour Ending' in the pivot index or handle it separately.
    # Let's pivot on both season and hour.
    
    # Re-grouping to ensure hour is part of the index for pivoting
    agg_df = df.groupby(['season', 'Hour Ending', 'target_col'])['total_demand'].sum().reset_index()
    
    # Pivot with multi-index
    pivot_df = agg_df.pivot(index=['season', 'Hour Ending'], columns='target_col', values='total_demand').reset_index()
    
    # Rename 'Hour Ending' to 'hour'
    pivot_df = pivot_df.rename(columns={'Hour Ending': 'hour'})
    
    # 6. Ensure all target columns exist and fill NaN with 0
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    for col in target_columns:
        if col not in pivot_df.columns:
            pivot_df[col] = 0
            
    # Fill any remaining NaNs (from missing combinations) with 0
    pivot_df = pivot_df.fillna(0)
    
    # 7. Format Types
    # 'season' is object, 'hour' is int64
    pivot_df['season'] = pivot_df['season'].astype(str)
    pivot_df['hour'] = pivot_df['hour'].astype(int)
    
    # Specific columns are int64 in target schema
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    for col in int_cols:
        if col in pivot_df.columns:
            pivot_df[col] = pivot_df[col].astype(int)
            
    # Float columns
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    for col in float_cols:
        if col in pivot_df.columns:
            pivot_df[col] = pivot_df[col].astype(float)
            
    # 8. Select and Return
    # Sort by season and hour for consistency (optional but good)
    # Define season order if needed, but simple sort is likely fine
    pivot_df = pivot_df.sort_values(by=['season', 'hour']).reset_index(drop=True)
    
    return pivot_df[target_columns]