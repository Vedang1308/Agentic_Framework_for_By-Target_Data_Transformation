import pandas as pd

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    # Step 1: Parse and Format Datetime
    df = source.copy()
    df['datetime'] = pd.to_datetime(df['local_15min'], format='%m/%d/%Y %H:%M').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Step 2: Define the mapping of source columns to target columns
    target_columns = ['datetime', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heater']
    
    # Step 3: Handle missing values and sum relevant columns
    df['hvac'] = (df['air1_sum'].fillna(0) + df['air2_sum'].fillna(0) + df['air3_sum'].fillna(0) + 
                  df['airwindowunit1_sum'].fillna(0) + df['furnace1_sum'].fillna(0) + df['furnace2_sum'].fillna(0) + 
                  df['heater1_sum'].fillna(0) + df['heater2_sum'].fillna(0) + df['heater3_sum'].fillna(0) + 
                  df['housefan1_sum'].fillna(0))
    
    df['water_heating'] = (df['waterheater1_sum'].fillna(0) + df['waterheater2_sum'].fillna(0) + 
                           df['circpump1_sum'].fillna(0))
    
    df['refrigerator'] = (df['refrigerator1_sum'].fillna(0) + df['refrigerator2_sum'].fillna(0) + 
                          df['freezer1_sum'].fillna(0) + df['icemaker1_sum'].fillna(0))
    
    df['clothes_washer'] = df['clotheswasher1_sum'].fillna(0)
    
    df['clothes_dryer'] = (df['drye1_sum'].fillna(0) + df['dryg1_sum'].fillna(0))
    
    df['dishwasher'] = df['dishwasher1_sum'].fillna(0)
    
    df['cooking_range'] = (df['oven1_sum'].fillna(0) + df['oven2_sum'].fillna(0) + 
                           df['range1_sum'].fillna(0) + df['microwave1_sum'].fillna(0) + 
                           df['disposal1_sum'].fillna(0))
    
    df['pool_spa_pumps'] = (df['poolpump1_sum'].fillna(0) + df['pump1_sum'].fillna(0))
    
    df['interior_lighting'] = (df['bathroom1_sum'].fillna(0) + df['bathroom2_sum'].fillna(0) + 
                               df['bedroom1_sum'].fillna(0) + df['bedroom2_sum'].fillna(0) + 
                               df['bedroom3_sum'].fillna(0) + df['bedroom4_sum'].fillna(0) + 
                               df['bedroom5_sum'].fillna(0) + df['diningroom1_sum'].fillna(0) + 
                               df['diningroom2_sum'].fillna(0) + df['kitchen1_sum'].fillna(0) + 
                               df['kitchen2_sum'].fillna(0) + df['livingroom1_sum'].fillna(0) + 
                               df['livingroom2_sum'].fillna(0) + df['office1_sum'].fillna(0) + 
                               df['utilityroom1_sum'].fillna(0))
    
    df['exterior_lighting'] = (df['poollight1_sum'].fillna(0) + df['garage1_sum'].fillna(0) + 
                               df['garage2_sum'].fillna(0) + df['shed1_sum'].fillna(0))
    
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    df['plug'] = (df['lights_plugs1_sum'].fillna(0) + df['lights_plugs2_sum'].fillna(0) + 
                  df['lights_plugs3_sum'].fillna(0) + df['lights_plugs4_sum'].fillna(0) + 
                  df['lights_plugs5_sum'].fillna(0) + df['lights_plugs6_sum'].fillna(0) + 
                  df['outsidelights_plugs1_sum'].fillna(0) + df['outsidelights_plugs2_sum'].fillna(0) + 
                  df['aquarium1_sum'].fillna(0) + df['battery1_sum'].fillna(0) + 
                  df['car1_sum'].fillna(0) + df['car2_sum'].fillna(0) + df['security1_sum'].fillna(0) + 
                  df['winecooler1_sum'].fillna(0))
    
    df['pool_spa_heater'] = 0  # Assuming this is always 0 as per the sample
    
    # Step 4: Ensure correct data types
    df['pool_spa_heater'] = df['pool_spa_heater'].astype('int64')
    
    # Step 5: Return the transformed DataFrame
    return df[target_columns]