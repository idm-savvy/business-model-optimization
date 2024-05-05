import os

import pandas as pd
import hiplot as hip


def load(filename):
    df = pd.read_csv(filename)
    return df

def filter(df):
    print("filtering")
    result = df.query("break_even_month >= 2 and slope > 1000")
    print(f"filtered results: {result.shape[0]}")
    return result

def plot(df, filename):
    h = hip.Experiment.from_dataframe(df)
    # h.parameters_definition["net_zero"].type = hip.ValueType.NUMERIC_LOG
    h.parameters_definition["starting_pol"].type = hip.ValueType.NUMERIC
    h.to_html(filename)


if __name__ == "__main__":
    timestamp = "20240505-163334"
    path = os.path.abspath('.')
    df = load(os.path.join(path, f"var/{timestamp}/merged.csv.gz"))
    df = filter(df)
    plot(df, filename=os.path.join(path, f"docs/result-{timestamp}.html"))
