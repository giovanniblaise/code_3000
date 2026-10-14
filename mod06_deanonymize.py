import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    matched = pd.DataFrame(columns = ['anon_id', 'matched_name'])
    seen = {}
    count = {}

    for i in range(len(anon_df)):
        for j in range(len(aux_df)):
            if (
                anon_df.iloc[i]['age'] == aux_df.iloc[j]['age'] and
                anon_df.iloc[i]['zip3'] == aux_df.iloc[j]['zip3'] and
                anon_df.iloc[i]['gender'] == aux_df.iloc[j]['gender']
                ):
                anon_id = anon_df.iloc[i]['anon_id']
                matched_name = aux_df.iloc[j]['name']

                if anon_id not in seen:
                    seen[anon_id] = matched_name
                    count[anon_id] = 1
                else:
                    count[anon_id] += 1

    for anon_id, matched_name in seen.items():
        if count[anon_id] == 1:
            matched.loc[len(matched)] = [anon_id, matched_name]

    return matched


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    return len(matches_df) / len(anon_df)