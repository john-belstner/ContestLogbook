import pandas as pd

def parse_cabrillo_qsos(filepath):
    """Parse QSO lines from a Cabrillo file into a DataFrame."""
    qsos = []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('QSO:'):
                parts = line.strip().split()
                # parts[0] is 'QSO:'
                qso = {
                    'band': int(int(parts[1])/1000),
                    'mode': parts[2],
                    'date': parts[3],
                    'time': parts[4],
                    'my_call': parts[5],
                    'my_name': parts[6],
                    'my_state': parts[7],
                    'their_call': parts[8],
                    'their_name': parts[9] if len(parts) > 9 else '',
                    'their_state': parts[10] if len(parts) > 10 else '',
                    'xmtr_id': parts[11] if len(parts) > 11 else '0'
                }
                qsos.append(qso)

    return pd.DataFrame(qsos)

# Parse the file
df = parse_cabrillo_qsos('W9EN_NAQP_CW.cbr')
qsos = len(df)
multipliers = df[['band', 'their_state']].drop_duplicates().shape[0]
score = qsos * multipliers

print(f"QSOs: {qsos}")
print(f"Multipliers: {multipliers}")
print(f"Score: {score}")