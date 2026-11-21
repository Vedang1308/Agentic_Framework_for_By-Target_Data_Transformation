import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Parse the local_15min column to datetime
    source = source.copy()
    source['local_15min'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M')
    
    # Extract hour and season
    source['hour'] = source['local_15min'].dt.hour
    source['month'] = source['local_15min'].dt.month
    
    # Define season based on month
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
    
    source['season'] = source['month'].apply(get_season)
    
    # Define column mappings for each target category
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum', 'furnace1_sum', 'furnace2_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum', 'housefan1_sum', 'circpump1_sum']
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum', 'freezer1_sum', 'icemaker1_sum', 'winecooler1_sum']
    clothes_washer_cols = ['clotheswasher1_sum']
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    dishwasher_cols = ['dishwasher1_sum', 'disposal1_sum']
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum', 'microwave1_sum', 'venthood1_sum']
    pool_spa_pumps_cols = ['poolpump1_sum', 'pump1_sum', 'jacuzzi1_sum']
    interior_lighting_cols = ['bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum', 'diningroom2_sum', 'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum', 'office1_sum', 'utilityroom1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum', 'poollight1_sum', 'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum']
    exterior_lighting_cols = ['outsidelights_plugs1_sum', 'outsidelights_plugs2_sum']
    plug_cols = ['battery1_sum', 'car1_sum', 'car2_sum', 'aquarium1_sum', 'kitchenapp1_sum', 'kitchenapp2_sum', 'sumppump1_sum', 'sewerpump1_sum', 'wellpump1_sum']
    pool_spa_heaters_cols = ['pool1_sum', 'pool2_sum']
    
    # Create new columns by summing the relevant source columns
    source['hvac'] = source[hvac_cols].sum(axis=1)
    source['water_heating'] = source[water_heating_cols].sum(axis=1)
    source['refrigerator'] = source[refrigerator_cols].sum(axis=1)
    source['clothes_washer'] = source[clothes_washer_cols].sum(axis=1)
    source['clothes_dryer'] = source[clothes_dryer_cols].sum(axis=1)
    source['dishwasher'] = source[dishwasher_cols].sum(axis=1)
    source['cooking_range'] = source[cooking_range_cols].sum(axis=1)
    source['pool_spa_pumps'] = source[pool_spa_pumps_cols].sum(axis=1)
    source['interior_lighting'] = source[interior_lighting_cols].sum(axis=1)
    source['exterior_lighting'] = source[exterior_lighting_cols].sum(axis=1)
    source['plug'] = source[plug_cols].sum(axis=1)
    source['pool_spa_heaters'] = source[pool_spa_heaters_cols].sum(axis=1)
    
    # Calculate total lighting as sum of interior and exterior
    source['lighting'] = source['interior_lighting'] + source['exterior_lighting']
    
    # Group by season and hour, and sum the energy values
    df = source.groupby(['season', 'hour']).agg({
        'hvac': 'sum',
        'water_heating': 'sum',
        'refrigerator': 'sum',
        'clothes_washer': 'sum',
        'clothes_dryer': 'sum',
        'dishwasher': 'sum',
        'cooking_range': 'sum',
        'pool_spa_pumps': 'sum',
        'interior_lighting': 'sum',
        'exterior_lighting': 'sum',
        'lighting': 'sum',
        'plug': 'sum',
        'pool_spa_heaters': 'sum'
    }).reset_index()
    
    # Ensure the column order matches the target
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']
    
    return df[target_columns]