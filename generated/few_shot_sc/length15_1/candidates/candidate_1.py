import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    # 1. Parse time and extract hour and season
    df = source.copy()
    df['time_dt'] = pd.to_datetime(df['time'])
    df['hour'] = df['time_dt'].dt.hour
    df['month'] = df['time_dt'].dt.month
    
    # Define season mapping
    # Winter: 12, 1, 2
    # Spring: 3, 4, 5
    # Summer: 6, 7, 8
    # Fall: 9, 10, 11
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
    
    # 2. Define category columns and sum them
    
    # HVAC Components
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_heating_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Domestic Water Heating
    dwh_cols = [
        'electricity_water_systems_kwh'
    ]
    
    # Major Appliances
    appliance_cols = [
        'electricity_refrigerator_kwh',
        'electricity_clothes_washer_kwh',
        'electricity_clothes_dryer_kwh',
        'electricity_cooking_range_kwh',
        'electricity_dishwasher_kwh'
    ]
    
    # Lighting
    lighting_cols = [
        'electricity_interior_lighting_kwh',
        'electricity_exterior_lighting_kwh'
    ]
    
    # Miscellaneous Plug Loads
    # Includes general plug loads and specific fans/pools/hot tubs not in HVAC
    misc_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_heater_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_heater_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Create aggregated columns
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwh_cols].sum(axis=1)
    df['major_appliances'] = df[appliance_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_cols].sum(axis=1)
    
    # Total is net site electricity
    df['total'] = df['net_site_electricity_kwh']
    
    # 3. Group by season and hour and sum
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Select only the columns needed for grouping and aggregation
    agg_df = df[['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']]
    
    result = agg_df.groupby(['season', 'hour'], as_index=False).sum()
    
    # Ensure hour is integer
    result['hour'] = result['hour'].astype(int)
    
    # Return with exact column names
    return result[target_columns]