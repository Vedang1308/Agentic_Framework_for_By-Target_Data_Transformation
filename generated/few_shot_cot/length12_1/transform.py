import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    df = source.copy()
    
    # 1. Parse time and extract hour and season
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # Define seasons based on meteorological definitions
    # Winter: Dec, Jan, Feb (12, 1, 2)
    # Spring: Mar, Apr, May (3, 4, 5)
    # Summer: Jun, Jul, Aug (6, 7, 8)
    # Autumn: Sep, Oct, Nov (9, 10, 11)
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'
            
    df['season'] = df['month'].apply(get_season)
    
    # 2. Map source columns to target columns
    # HVAC: Sum of heating, cooling, fans, and pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh'
    ]
    df['hvac'] = df[hvac_cols].sum(axis=1)
    
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
    
    # Pool/Spa Pumps: Sum of pool pump and hot tub pump
    df['pool_spa_pumps'] = df['electricity_pool_pump_kwh'] + df['electricity_hot_tub_pump_kwh']
    
    # Interior Lighting
    df['interior_lighting'] = df['electricity_interior_lighting_kwh']
    
    # Exterior Lighting
    df['exterior_lighting'] = df['electricity_exterior_lighting_kwh']
    
    # Lighting: Sum of interior and exterior
    df['lighting'] = df['interior_lighting'] + df['exterior_lighting']
    
    # Plug Loads
    df['plug'] = df['electricity_plug_loads_kwh']
    
    # Pool/Spa Heaters: Sum of pool heater and hot tub heater
    df['pool_spa_heaters'] = df['electricity_pool_heater_kwh'] + df['electricity_hot_tub_heater_kwh']
    
    # 3. Aggregate by season and hour
    # The target has 72 rows, implying 3 seasons * 24 hours.
    # We group by season and hour and sum the values.
    agg_cols = [
        'hvac', 'water_heating', 'refrigerator', 'clothes_washer', 
        'clothes_dryer', 'dishwasher', 'cooking_range', 'pool_spa_pumps', 
        'interior_lighting', 'exterior_lighting', 'lighting', 'plug', 
        'pool_spa_heaters'
    ]
    
    df_grouped = df.groupby(['season', 'hour'], as_index=False)[agg_cols].sum()
    
    # 4. Format output
    # Ensure column order matches target
    target_columns = [
        'season', 'hour', 'hvac', 'water_heating', 'refrigerator', 
        'clothes_washer', 'clothes_dryer', 'dishwasher', 'cooking_range', 
        'pool_spa_pumps', 'interior_lighting', 'exterior_lighting', 
        'lighting', 'plug', 'pool_spa_heaters'
    ]
    
    # Sort by season and hour for consistency, though not strictly required if order doesn't matter for correctness
    # The target sample seems unordered, but standard practice is often sorted.
    # We will just return the columns.
    
    return df_grouped[target_columns]