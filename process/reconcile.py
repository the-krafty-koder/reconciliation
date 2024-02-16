import pandas as pd
import numpy as np


def fill_rows_and_cols(df1, df2):
    """
    This function prepares both dataframes for comparison by merging missing
    rows and columns and setting them to np.nan

    Parameters
    ----------
    df1 : Dataframe
        First dataframe .
    df2 : Dataframe
        Second dataframe.

    Returns
    -------
    Dict
        The union of df1 and df2 with missing values in df1
        added to df2 as np.Nan

    """
    _, merged = df1.align(df2)

    return merged


def pre_process(df1, df2):
    """
    This functoon compares data between two dataframes
    and reconciles them

    Parameters
    ----------
    df1 : Dataframe
        First dataframe to compare.
    df2 : Dataframe
        Second datafrane to compare.

    Returns
    -------
    Dict
        The difference in df1 and df2.
    """

    if df1.empty and df2.empty:
        raise TypeError("Cannot compare two empty files")

    if df1.empty:
        df1 = pd.DataFrame(np.nan, index=df2.index, columns=df2.columns)

    if df2.empty:
        df2 = pd.DataFrame(np.nan, index=df1.index, columns=df1.columns)

    merged_df1 = fill_rows_and_cols(df2, df1)
    merged_df2 = fill_rows_and_cols(df1, df2)

    return merged_df1.reindex(
        columns=sorted(merged_df1.columns)
    ), merged_df2.reindex(columns=sorted(merged_df2.columns))


def reconcile(df1, df2):
    """
    This functoon compares data between two dataframes
    and reconciles them

    Parameters
    ----------
    df1 : Dataframe
        First dataframe to compare.
    df2 : Dataframe
        Second datafrane to compare.

    Returns
    -------
    Dict
        The difference in df1 and df2.
    """
    difference = df2.compare(df1)
    results = {}

    # both dataframes have same colummns from pre_process
    for column in df1.columns:
        # drop values that are similar in both files
        cleaned = (
            difference[column]
            .dropna(subset=["self", "other"], how="all")
            .replace(np.nan, None)
        )

        # store the difference as tuples
        difference_as_tuple = list(cleaned.itertuples(index=True, name=None))
        results[column] = difference_as_tuple

    return results
