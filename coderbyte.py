import string
import pandas as pd
from io import StringIO

NONALPHABETICAL = string.punctuation+string.digits
NONALPHA_TABLE = str.maketrans('', '', NONALPHABETICAL)

data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'

def transform_data(data):
    df = pd.read_csv(data, sep=';')

    # fill in missing FlightCodes in increments of 10
    df.FlightCodes.interpolate(method='linear', inplace=True)
    df.FlightCodes = df.FlightCodes.astype('int64')

    # split up To From columns and normalize casing
    df[["To", "From"]] = df.To_From.str.split('_', expand=True)
    df.To = df.To.str.upper()
    df.From = df.From.str.upper()
    df = df.drop(['To_From'], axis=1)

    # remove punctuation and leading/trailing whitespace from Airline Codes
    df['Airline Code'] = df['Airline Code'].apply(lambda s: s.translate(NONALPHA_TABLE)).str.strip()

    # return stringified transformed table
    return df.to_csv(sep=';', index=False)

transformed_data = transform_data(StringIO(data))
