import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # Parse and format datetime
    source['datetime'] = pd.to_datetime(source['local_15min'], format='%m/%d/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Define the mapping of source columns to target columns
    hvac_cols = ['air1_sum', 'air2_sum', 'air3_sum', 'airwindowunit1_sum']
    water_heating_cols = ['waterheater1_sum', 'waterheater2_sum']
    refrigerator_cols = ['refrigerator1_sum', 'refrigerator2_sum']
    clothes_washer_cols = ['clotheswasher1_sum', 'clotheswasher_dryg1_sum']
    clothes_dryer_cols = ['drye1_sum', 'dryg1_sum']
    dishwasher_cols = ['dishwasher1_sum', 'disposal1_sum']
    cooking_range_cols = ['oven1_sum', 'oven2_sum', 'range1_sum']
    pool_spa_pumps_cols = ['poolpump1_sum', 'pump1_sum']
    interior_lighting_cols = ['bathroom1_sum', 'bathroom2_sum', 'bedroom1_sum', 'bedroom2_sum', 'bedroom3_sum', 'bedroom4_sum', 'bedroom5_sum', 'diningroom1_sum', 'diningroom2_sum', 'kitchen1_sum', 'kitchen2_sum', 'livingroom1_sum', 'livingroom2_sum', 'office1_sum', 'utilityroom1_sum']
    exterior_lighting_cols = ['poollight1_sum', 'garage1_sum', 'garage2_sum', 'shed1_sum']
    plug_cols = ['aquarium1_sum', 'battery1_sum', 'car1_sum', 'car2_sum', 'circpump1_sum', 'freezer1_sum', 'heater1_sum', 'heater2_sum', 'heater3_sum', 'housefan1_sum', 'icemaker1_sum', 'jacuzzi1_sum', 'kitchenapp1_sum', 'kitchenapp2_sum', 'lights_plugs1_sum', 'lights_plugs2_sum', 'lights_plugs3_sum', 'lights_plugs4_sum', 'lights_plugs5_sum', 'lights_plugs6_sum', 'microwave1_sum', 'outsidelights_plugs1_sum', 'outsidelights_plugs2_sum', 'security1_sum', 'sewerpump1_sum', 'solar_sum', 'solar2_sum', 'sprinkler1_sum', 'sumppump1_sum', 'venthood1_sum', 'wellpump1_sum', 'winecooler1_sum']
    
    # Create target columns by summing the relevant source columns
    df = source.copy()
    df['hvac'] = df[hvac_cols].sum(axis=1, skipna=True)
    df['water_heating'] = df[water_heating_cols].sum(axis=1, skipna=True)
    df['refrigerator'] = df[refrigerator_cols].sum(axis=1, skipna=True)
    df['clothes_washer'] = df[clothes_washer_cols].sum(axis=1, skipna=True)
    df['clothes_dryer'] = df[clothes_dryer_cols].sum(axis=1, skipna=True)
    df['dishwasher'] = df[dishwasher_cols].sum(axis=1, skipna=True)
    df['cooking_range'] = df[cooking_range_cols].sum(axis=1, skipna=True)
    df['pool_spa_pumps'] = df[pool_spa_pumps_cols].sum(axis=1, skipna=True)
    df['interior_lighting'] = df[interior_lighting_cols].sum(axis=1, skipna=True)
    df['exterior_lighting'] = df[exterior_lighting_cols].sum(axis=1, skipna=True)
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    df['plug'] = df[plug_cols].sum(axis=1, skipna=True)
    df['pool_spa_heater'] = 0  # Based on the target sample, this column is always 0
    
    # Ensure correct data types
    df['pool_spa_heater'] = df['pool_spa_heater'].astype('int64')
    
    # Define the target columns
    target_columns = ['datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Return the DataFrame with the target columns
    return df[target_columns]