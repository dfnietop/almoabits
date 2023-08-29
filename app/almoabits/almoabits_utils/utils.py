import uuid
from datetime import datetime

import pandas as pd


def synthetic_uuid(df: pd.DataFrame, field: str = "uuid") -> pd.DataFrame:
    """
    Controls the synthetic UUID generation for a dataframe.
    Returns:
        (pd.DataFrame): a copy of the dataframe including the new field with uuids
    """
    uuids = []
    for row in range(len(df)):
        # in case we want to build our uuid, we have row values here
        uuids.append(uuid.uuid4())
    # Adding uuids as column
    df.loc[:, field] = uuids
    return df


csv_dtype = {'CDR_ID': str, 'ICCID': str, 'TYPE': str, 'CONNECT_TIME': str, 'CLOSE_TIME': str, 'DURATION': int,
             'DIRECTION': str, 'CALLED_PARTY': str,
             'CALLING_PARTY': str, 'COUNTRY_ISO3': str, 'COUNTRY_NAME': str, 'MCC': str, 'MNC': str, 'IMSI_ID': str,
             'IMSI_NO': str, 'INVENTORY_ID': str,
             'COMPANY_NAME': str, 'PACKAGE_ID': str}
