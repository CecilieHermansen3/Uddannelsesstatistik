import pandas as pd

def valider_data(df, name):
    print(f"--- {name} ---")
    print(f"Rækker: {len(df)}, Kommuner: {df['kommune'].nunique()}")
    print(f"Manglende værdier:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    
    # sanity range checks
    if 'fravaer_pct' in df.columns:
        assert df['fravaer_pct'].between(0, 100).all(), "Fravær uden for forventet 0-100% interval!"
    if 'trivsel_score' in df.columns:
        assert df['trivsel_score'].between(1, 5).all(), "Trivsel-score uden for forventet 1-5 interval!"
    
    print("Alle tjek bestået.\n")

def kommune_antal(df, expected=98):
    unique_kommuner = df['kommune'].unique()
    n = len(unique_kommuner)
    print(f"Antal unikke kommuner: {n}")
    if n != expected:
        print(f"⚠️  Forventede {expected}, fandt {n}")
        print(sorted(unique_kommuner))
    return unique_kommuner

def sammenlign_kommuner_for_dataframes(dataframes: dict[str, pd.DataFrame]):
    """
    dataframes: dict mapping a label (e.g. 'trivsel') to its dataframe.
    Prints kommuner that are missing from at least one dataframe.
    """
    kommune_sets = {name: set(df['kommune'].unique()) for name, df in dataframes.items()}
    
    all_kommuner = set.union(*kommune_sets.values())
    common_kommuner = set.intersection(*kommune_sets.values())
    
    print(f"Kommuner i alt (union): {len(all_kommuner)}")
    print(f"Kommuner fælles for alle datasæt: {len(common_kommuner)}")
    
    inconsistent = all_kommuner - common_kommuner
    if inconsistent:
        print(f"\n⚠️  {len(inconsistent)} kommune(r) findes ikke i alle datasæt:")
        for kommune in sorted(inconsistent):
            present_in = [name for name, kset in kommune_sets.items() if kommune in kset]
            missing_from = [name for name in dataframes if name not in present_in]
            print(f"  - {kommune}: findes i {present_in}, mangler i {missing_from}")
    else:
        print("Alle kommuner er konsistente på tværs af datasæt.")
    
    return inconsistent