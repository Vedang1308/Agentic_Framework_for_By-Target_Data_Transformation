import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Map Time Period to Season
    month_to_season = {
        'January': 'Winter', 'February': 'Winter', 'December': 'Winter',
        'March': 'Spring', 'April': 'Spring', 'May': 'Spring',
        'June': 'Summer', 'July': 'Summer', 'August': 'Summer',
        'September': 'Fall', 'October': 'Fall', 'November': 'Fall'
    }
    
    # Handle potential variations in month names (e.g., 'Jan', 'Jan.') if necessary, 
    # but sample shows full names.
    df = source.copy()
    df['season'] = df['Time Period'].map(month_to_season)
    
    # 2. Map End Use to Target Column Names
    end_use_map = {
        'HVAC': 'hvac',
        'Remaining Load': 'hvac', # Common mapping in CBECC-Com datasets
        'Water Heating': 'water_heating',
        'Freezer': 'refrigerator',
        'Refrigerator': 'refrigerator',
        'Clothes Washer': 'clothes_washer',
        'Clothes Dryer': 'clothes_dryer',
        'Dishwasher': 'dishwasher',
        'Cooking Range': 'cooking_range',
        'Pool/Spa Pumps': 'pool_spa_pumps',
        'Interior Lighting': 'interior_lighting',
        'Exterior Lighting': 'exterior_lighting',
        'Lighting': 'lighting',
        'Plug Loads': 'plug',
        'Pool/Spa Heater': 'pool_spa_heater'
    }
    
    df['target_col'] = df['End Use'].map(end_use_map)
    
    # 3. Filter for valid target columns and required data
    target_cols_list = ['hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
                        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
                        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 
                        'pool_spa_heater']
    
    # Keep only rows that map to a target column
    df = df[df['target_col'].isin(target_cols_list)]
    
    # 4. Pivot/Aggregate
    # Group by season and hour, sum the average demand for each end use
    # Note: The source has 'Average Demand Per Home...'. The target values look like sums 
    # or averages across the bin. Given the magnitude (2000+ kW), it's likely a sum 
    # of demands or an aggregate metric. The prompt implies a direct transformation.
    # We will sum the 'Average Demand...' column for each group.
    
    pivot_df = df.groupby(['season', 'Hour Ending', 'target_col'])['Average Demand Per Home With This End Use [kW]'].sum().reset_index()
    
    # Pivot to wide format
    pivot_wide = pivot_df.pivot_table(index=['season', 'Hour Ending'], columns='target_col', values='Average Demand Per Home With This End Use [kW]', aggfunc='sum').reset_index()
    
    # Rename Hour Ending to hour
    pivot_wide.rename(columns={'Hour Ending': 'hour'}, inplace=True)
    
    # 5. Ensure all target columns exist and fill NaNs with 0
    for col in target_cols_list:
        if col not in pivot_wide.columns:
            pivot_wide[col] = 0
        else:
            pivot_wide[col] = pivot_wide[col].fillna(0)
            
    # 6. Cast to specified types
    # Float columns
    float_cols = ['hvac', 'water_heating', 'refrigerator', 'dishwasher']
    # Int columns
    int_cols = ['clothes_washer', 'clothes_dryer', 'cooking_range', 'pool_spa_pumps', 
                'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    for col in float_cols:
        pivot_wide[col] = pivot_wide[col].astype(float)
        
    for col in int_cols:
        # Cast to int64. Note: This truncates decimals. 
        # If the data is expected to be integer, this is correct.
        pivot_wide[col] = pivot_wide[col].astype(int)
        
    # 7. Select and order columns
    final_cols = ['season', 'hour'] + target_cols_list
    result = pivot_wide[final_cols]
    
    return result