"""
Held-out Demonstrations for Few-Shot CoT Prompting
Contains the 5 fixed demonstration cases set aside from the Smart Building benchmark:
length1_1, length2_1, length3_1, length4_1, length5_1.
These demonstrations illustrate clear step-by-step reasoning (visible CoT)
and clean, deterministic Python transform() functions.
"""

HELD_OUT_CASES = [
    "length1_1",
    "length2_1",
    "length3_1",
    "length4_1",
    "length5_1"
]

DEMONSTRATIONS = [
    {
        "case_id": "length1_1",
        "description": "Convert date format to '%a %m/%d/%Y', map hourly percentage columns to 'H:00', and drop unused metadata columns.",
        "source_schema": "Strata_ID (int64), Strata (object), DT_STRATA (object), DOW (object), PCT_HOURLY_0100..PCT_HOURLY_2500 (float64)",
        "target_schema": "cst (object), 1:00..24:00 (float64)",
        "source_sample": "DT_STRATA sample: ['7/2/2016', '7/3/2016']; PCT_HOURLY_0100 sample: [0.000701, 0.000761]",
        "target_sample": "cst sample: ['Fri 01/01/2016', 'Sat 01/02/2016']; 1:00 sample: [0.001222, 0.001313]",
        "reasoning": (
            "1. Analyze schemas: Source has date column 'DT_STRATA' and hourly columns 'PCT_HOURLY_0100' through 'PCT_HOURLY_2500'.\n"
            "2. Target schema requires column 'cst' with formatted date strings like 'Fri 01/01/2016' (%a %m/%d/%Y).\n"
            "3. Parse 'DT_STRATA' to datetime and format as '%a %m/%d/%Y' in column 'cst'.\n"
            "4. Rename hourly columns: 'PCT_HOURLY_0100' -> '1:00', ..., 'PCT_HOURLY_2400' -> '24:00'.\n"
            "5. Drop extra columns ('Strata_ID', 'Strata', 'DOW', 'PCT_HOURLY_2500') and align returned columns verbatim to target."
        ),
        "code": (
            "import pandas as pd\n\n"
            "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
            "    df = source.copy()\n"
            "    dt = pd.to_datetime(df['DT_STRATA'])\n"
            "    df['cst'] = dt.dt.strftime('%a %m/%d/%Y')\n"
            "    rename_dict = {f'PCT_HOURLY_{i:02d}00': f'{i}:00' for i in range(1, 25)}\n"
            "    df = df.rename(columns=rename_dict)\n"
            "    target_cols = ['cst'] + [f'{i}:00' for i in range(1, 25)]\n"
            "    return df[target_cols]\n"
        )
    },
    {
        "case_id": "length2_1",
        "description": "Extract date string, compute ISO day-of-week, rename hourly columns to 'pct_hourly_HH00', and add zero-filled 'pct_hourly_2500'.",
        "source_schema": "CST (object), 1:00..24:00:00 (float64)",
        "target_schema": "dt_strata (object), dow (int64), pct_hourly_0100..pct_hourly_2500 (float64)",
        "source_sample": "CST sample: ['Sat 12/01/2012', 'Sun 12/02/2012']; 1:00 sample: [0.9841, 0.9012]",
        "target_sample": "dt_strata sample: ['04/01/2009', '04/02/2009']; dow sample: [3, 4]; pct_hourly_0100 sample: [1.02, 0.93]",
        "reasoning": (
            "1. Inspect date: Source 'CST' has format 'Day MM/DD/YYYY'. Split by whitespace to extract the date part.\n"
            "2. Convert to datetime, then format as '%m/%d/%Y' for 'dt_strata'.\n"
            "3. Compute 'dow' (day of week) where Monday=1 ... Sunday=7 using `dt.dt.dayofweek + 1`.\n"
            "4. Rename hourly columns: '1:00' -> 'pct_hourly_0100', ..., '24:00'/'24:00:00' -> 'pct_hourly_2400'.\n"
            "5. Target includes 'pct_hourly_2500' filled with 0. Add this column and select target columns verbatim."
        ),
        "code": (
            "import pandas as pd\n\n"
            "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
            "    df = source.copy()\n"
            "    date_str = df['CST'].str.split(' ').str[-1]\n"
            "    dt = pd.to_datetime(date_str, format='%m/%d/%Y')\n"
            "    df['dt_strata'] = dt.dt.strftime('%m/%d/%Y')\n"
            "    df['dow'] = dt.dt.dayofweek + 1\n"
            "    rename_dict = {f'{i}:00': f'pct_hourly_{i:02d}00' for i in range(1, 24)}\n"
            "    if '24:00:00' in df.columns:\n"
            "        rename_dict['24:00:00'] = 'pct_hourly_2400'\n"
            "    elif '24:00' in df.columns:\n"
            "        rename_dict['24:00'] = 'pct_hourly_2400'\n"
            "    df = df.rename(columns=rename_dict)\n"
            "    df['pct_hourly_2500'] = 0\n"
            "    target_cols = ['dt_strata', 'dow'] + [f'pct_hourly_{i:02d}00' for i in range(1, 26)]\n"
            "    return df[target_cols]\n"
        )
    },
    {
        "case_id": "length3_1",
        "description": "Convert date format to '%m/%d/%Y', map hourly percentage columns to 'Hour H', and filter target schema.",
        "source_schema": "Strata_ID (int64), Strata (object), DT_STRATA (object), DOW (object), PCT_HOURLY_0100..PCT_HOURLY_2500 (float64)",
        "target_schema": "date (object), Hour 1..Hour 24 (float64)",
        "source_sample": "DT_STRATA sample: ['7/2/2016']; PCT_HOURLY_0100 sample: [0.000701]",
        "target_sample": "date sample: ['01/01/2016']; Hour 1 sample: [0.001222]",
        "reasoning": (
            "1. Analyze date: Source column 'DT_STRATA' has dates formatted as M/D/YYYY. Format as '%m/%d/%Y' in column 'date'.\n"
            "2. Map hour columns: 'PCT_HOURLY_{i:02d}00' maps to 'Hour {i}' for i=1..24.\n"
            "3. Select columns: 'date' followed by 'Hour 1' through 'Hour 24'. Drop unused columns."
        ),
        "code": (
            "import pandas as pd\n\n"
            "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
            "    df = source.copy()\n"
            "    dt = pd.to_datetime(df['DT_STRATA'])\n"
            "    df['date'] = dt.dt.strftime('%m/%d/%Y')\n"
            "    rename_dict = {f'PCT_HOURLY_{i:02d}00': f'Hour {i}' for i in range(1, 25)}\n"
            "    df = df.rename(columns=rename_dict)\n"
            "    target_cols = ['date'] + [f'Hour {i}' for i in range(1, 25)]\n"
            "    return df[target_cols]\n"
        )
    },
    {
        "case_id": "length4_1",
        "description": "Parse date to '%m/%d/%Y', map 24-hour columns to 12-hour AM/PM column labels, and align output.",
        "source_schema": "CST (object), 1:00..24:00:00 (float64)",
        "target_schema": "date (object), 1:00 AM..12:00 AM, 1:00 PM..12:00 PM (float64)",
        "source_sample": "CST sample: ['Sat 12/01/2012']; 1:00 sample: [3.3507]",
        "target_sample": "date sample: ['04/01/2009']; 1:00 AM sample: [3.75]",
        "reasoning": (
            "1. Extract date from 'CST' and convert to '%m/%d/%Y' format in column 'date'.\n"
            "2. Identify hourly mapping: 1..12 map to '1:00 AM' through '12:00 AM'; 13..24 map to '1:00 PM' through '12:00 PM'.\n"
            "3. Rename source hourly columns to match the target 12-hour AM/PM names.\n"
            "4. Return DataFrame with exactly the target column names."
        ),
        "code": (
            "import pandas as pd\n\n"
            "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
            "    df = source.copy()\n"
            "    date_str = df['CST'].str.split(' ').str[-1]\n"
            "    dt = pd.to_datetime(date_str, format='%m/%d/%Y')\n"
            "    df['date'] = dt.dt.strftime('%m/%d/%Y')\n"
            "    src_hours = [f'{i}:00' for i in range(1, 24)] + (['24:00:00'] if '24:00:00' in df.columns else ['24:00'])\n"
            "    tgt_hours = [f'{i}:00 AM' for i in range(1, 13)] + [f'{i}:00 PM' for i in range(1, 13)]\n"
            "    rename_dict = dict(zip(src_hours, tgt_hours))\n"
            "    df = df.rename(columns=rename_dict)\n"
            "    target_cols = ['date'] + tgt_hours\n"
            "    return df[target_cols]\n"
        )
    },
    {
        "case_id": "length5_1",
        "description": "Convert date format to '%m/%d/%Y', map hourly percentage columns to 'value1'..'value24', and align output.",
        "source_schema": "Strata_ID (int64), Strata (object), DT_STRATA (object), DOW (object), PCT_HOURLY_0100..PCT_HOURLY_2500 (float64)",
        "target_schema": "date (object), value1..value24 (float64)",
        "source_sample": "DT_STRATA sample: ['7/2/2016']; PCT_HOURLY_0100 sample: [0.000701]",
        "target_sample": "date sample: ['01/01/2016']; value1 sample: [0.001222]",
        "reasoning": (
            "1. Parse date from 'DT_STRATA' and format as '%m/%d/%Y' in column 'date'.\n"
            "2. Map hourly columns 'PCT_HOURLY_{i:02d}00' directly to 'value{i}' for i=1..24.\n"
            "3. Select 'date' and 'value1' through 'value24', dropping extra metadata columns."
        ),
        "code": (
            "import pandas as pd\n\n"
            "def transform(source: pd.DataFrame) -> pd.DataFrame:\n"
            "    df = source.copy()\n"
            "    dt = pd.to_datetime(df['DT_STRATA'])\n"
            "    df['date'] = dt.dt.strftime('%m/%d/%Y')\n"
            "    rename_dict = {f'PCT_HOURLY_{i:02d}00': f'value{i}' for i in range(1, 25)}\n"
            "    df = df.rename(columns=rename_dict)\n"
            "    target_cols = ['date'] + [f'value{i}' for i in range(1, 25)]\n"
            "    return df[target_cols]\n"
        )
    }
]


def format_demonstrations_text(n: int = 3) -> str:
    """Format n demonstrations into prompt text."""
    selected = DEMONSTRATIONS[:n]
    lines = ["Here are worked examples demonstrating step-by-step reasoning and valid Python code:\n"]
    for idx, demo in enumerate(selected, 1):
        lines.append(f"### Example {idx} (Case {demo['case_id']})")
        lines.append(f"Source Schema: {demo['source_schema']}")
        lines.append(f"Target Schema: {demo['target_schema']}")
        lines.append(f"Source Sample: {demo['source_sample']}")
        lines.append(f"Target Sample: {demo['target_sample']}")
        lines.append("Step-by-Step Reasoning Plan:")
        lines.append(demo["reasoning"])
        lines.append("Generated Code:")
        lines.append("```python")
        lines.append(demo["code"].strip())
        lines.append("```\n")
    return "\n".join(lines)
