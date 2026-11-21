import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the same schema and contents as target.csv."""
    
    # 1. Parse time and extract hour and month
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # 2. Define season mapping
    # Winter: 12, 1, 2; Spring: 3, 4, 5; Summer: 6, 7, 8; Fall: 9, 10, 11
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'
            
    df['season'] = df['month'].apply(get_season)
    
    # 3. Construct target columns by aggregating source columns
    # HVAC: Sum of heating and cooling electricity, including fans and pumps
    df['hvac'] = (df['electricity_heating_kwh'] + 
                  df['electricity_cooling_kwh'] + 
                  df['electricity_fans_heating_kwh'] + 
                  df['electricity_fans_cooling_kwh'] + 
                  df['electricity_pumps_heating_kwh'] + 
                  df['electricity_pumps_cooling_kwh'])
    
    # Water Heating
    df['water_heating'] = df['electricity_water_systems_kwh']
    
    # Refrigerator
    df['refrigerator'] = df['electricity_refrigerator_kwh']
    
    # Clothes Washer
    df['clothes_washer'] = df['electricity_clothes_washer_kwh']
    
    # Clothes Dryer
    df['clothes_dryer'] = df['electricity_clothes_dryer_kwh']
    
    # Dishwasher
    df['dishwasher'] = df['electricity_dishwasher_kwh']
    
    # Cooking Range
    df['cooking_range'] = df['electricity_cooking_range_kwh']
    
    # Pool/Spa Pumps
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # Total Lighting
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug Loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Heaters
    df['pool_spa_heaters'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 4. Group by season and hour, and sum the values
    target_columns = ['season', 'hour', 'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
                      'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
                      'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 'pool_spa_heaters']
    
    # Select only the columns needed for aggregation to avoid summing irrelevant ones
    agg_cols = [c for c in target_columns if c not in ['season', 'hour']]
    
    df_grouped = df.groupby(['season', 'hour'], as_index=False)[agg_cols].sum()
    
    # 5. Ensure correct column order and types
    # The groupby result might have different order, so we select explicitly
    df_result = df_grouped[target_columns]
    
    # Ensure hour is int64
    df_result['hour'] = df_result['hour'].astype('int64')
    
    return df_result