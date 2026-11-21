import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame (hourly/15-min electricity data) into a 
    target DataFrame aggregated by season and hour, with specific end-use categories.
    """
    
    # 1. Parse the time column
    df = source.copy()
    df['time'] = pd.to_datetime(df['time'])
    
    # 2. Extract hour and month
    df['hour'] = df['time'].dt.hour
    df['month'] = df['time'].dt.month
    
    # 3. Define Season based on month
    # Winter: Dec(12), Jan(1), Feb(2)
    # Spring: Mar(3), Apr(4), May(5)
    # Summer: Jun(6), Jul(7), Aug(8)
    # Fall: Sep(9), Oct(10), Nov(11)
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
    
    # 4. Calculate End-Use Categories
    # HVAC: Heating + Cooling + associated fans and pumps
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
    dwh_cols = ['electricity_water_systems_kwh']
    
    # Major Appliances
    major_appliance_cols = [
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
    misc_plug_cols = [
        'electricity_plug_loads_kwh',
        'electricity_house_fan_kwh',
        'electricity_range_fan_kwh',
        'electricity_bath_fan_kwh',
        'electricity_ceiling_fan_kwh',
        'electricity_pool_pump_kwh',
        'electricity_hot_tub_pump_kwh'
    ]
    
    # Total
    total_col = ['net_site_electricity_kwh']
    
    # Helper to sum columns safely
    def sum_columns(cols):
        return df[cols].sum(axis=1)
        
    df['hvac'] = sum_columns(hvac_cols)
    df['domestic_water_heating'] = sum_columns(dwh_cols)
    df['major_appliances'] = sum_columns(major_appliance_cols)
    df['lighting'] = sum_columns(lighting_cols)
    df['miscellaneous_plug_loads'] = sum_columns(misc_plug_cols)
    df['total'] = sum_columns(total_col)
    
    # 5. Group by season and hour, and sum the aggregated values
    target_columns = ['season', 'hour', 'hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    # Select only the necessary columns for grouping
    group_cols = ['season', 'hour']
    agg_cols = ['hvac', 'domestic_water_heating', 'major_appliances', 'lighting', 'miscellaneous_plug_loads', 'total']
    
    df_agg = df.groupby(group_cols, as_index=False)[agg_cols].sum()
    
    # 6. Return the result with exact column names
    # Ensure the order matches the target schema
    return df_agg[target_columns]