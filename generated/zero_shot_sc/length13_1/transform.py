import pandas as pd
import numpy as np

def transform(source: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms the source DataFrame containing detailed electricity usage
    into a target DataFrame with aggregated categories.
    """
    df = source.copy()

    # 1. Define source columns for each target category
    
    # HVAC: Heating, Cooling, and associated fans/pumps
    hvac_cols = [
        'electricity_heating_kwh',
        'electricity_central_system_heating_kwh',
        'electricity_fans_heating_kwh',
        'electricity_pumps_heating_kwh',
        'electricity_central_system_pumps_heating_kwh',
        'electricity_cooling_kwh',
        'electricity_central_system_cooling_kwh',
        'electricity_fans_cooling_kwh',
        'electricity_pumps_cooling_kwh',
        'electricity_central_system_pumps_cooling_kwh'
    ]
    
    # Domestic Water Heating
    dwhe_cols = [
        'electricity_water_systems_kwh'
    ]
    
    # Major Appliances
    major_appl_cols = [
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
    
    # Miscellaneous Plug Loads (including pool/hot tub and other fans)
    misc_plug_cols = [
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

    # 2. Compute aggregated columns
    # Use sum with axis=1 and fillna(0) to handle potential missing columns or NaNs
    df['hvac'] = df[hvac_cols].sum(axis=1)
    df['domestic_water_heating'] = df[dwhe_cols].sum(axis=1)
    df['major_appliances'] = df[major_appl_cols].sum(axis=1)
    df['lighting'] = df[lighting_cols].sum(axis=1)
    df['miscellaneous_plug_loads'] = df[misc_plug_cols].sum(axis=1)
    
    # Total is directly available
    df['total'] = df['net_site_electricity_kwh']

    # 3. Format Datetime
    # Parse the 'time' column, which includes milliseconds
    df['datetime'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # 4. Select and order target columns
    target_columns = [
        'datetime', 
        'hvac', 
        'domestic_water_heating', 
        'major_appliances', 
        'lighting', 
        'miscellaneous_plug_loads', 
        'total'
    ]
    
    # Ensure the output matches the target schema exactly
    result_df = df[target_columns]
    
    return result_df