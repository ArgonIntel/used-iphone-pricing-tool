import pandas as pd
import glob
import os

def concatinate_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """Concatinates DataFrames into one. Multiple Dataframes are result of
    multiple .csv files

    Args:
        dfs (list[pd.DataFrame]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    dataframe = pd.concat(dfs, ignore_index=True)
    dataframe.drop(["Unnamed: 0"], axis=1, inplace=True)

    return dataframe


def drop_shop(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Returns only rows advertised by individuals and omiting shop ads
    Args:
        dataframe (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return dataframe.drop(
        index=dataframe[
            dataframe["store_private"].str.contains("trgovine")
        ].index,
        axis=0,
    )


def create_text_series(dataframe: pd.DataFrame) -> pd.Series:
    """Concatinates Ad title and Ad description into pd.Series

    Args:
        dataframe (pd.DataFrame): _description_

    Returns:
        pd.Series: _description_
    """
    text_series = pd.Series()
    text_series = dataframe["ad_title"] + " " + dataframe["ad_description"]

    return text_series


def drop_trash(pipeline: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe without useless rows such as locked phones

    Args:
        pipeline (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    pipeline.dropna(subset=["rom"], inplace=True)
    pipeline.drop(
        index=pipeline[pipeline["locked"] == True].index, axis=0, inplace=True
    )
    return pipeline


def extract_data(text_series: pd.Series) -> pd.DataFrame:
    """Extracts data such as iPhone model, ROM size, Battery health, locked status
    warranty information from Text of the ad

    Args:
        text_series (pd.Series): _description_

    Returns:
        pd.DataFrame: _description_
    """
    pipeline_data = pd.DataFrame()
    pipeline_data["model"] = text_series.str.extract(
        r".phone\s?(\d{2}\s?(?:pro)?\s?(?:max)?)", expand=True
    )
    pipeline_data["model"].replace(to_replace=" ", value="", regex=True, inplace=True)
    pipeline_data["rom"] = text_series.str.extract(r"(\d{2,3})\s?gb", expand=True)
    pipeline_data["battery"] = text_series.str.extract(r"(\d{2,3})\s?%", expand=True)
    pipeline_data["warranty"] = text_series.str.contains(
        r"garanc", regex=True
    ) & ~text_series.str.contains(r"istekla", regex=True)
    pipeline_data["locked"] = text_series.str.contains(r"zakljucan", regex=True)
    return pipeline_data


def drop_nas(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Drops all NaN rows from DataFrame

    Args:
        dataframe (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    dataframe.dropna(subset=["rom"], inplace=True)
    dataframe.drop(
        index=dataframe[dataframe["battery"].isna()].index, axis=0, inplace=True
    )
    return dataframe


def type_to_int(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Converts battery and rom columns into "int"

    Args:
        dataframe (pd.DataFrame): 

    Returns:
        pd.DataFrame: 
    """
    dataframe["battery"] = dataframe["battery"].astype("int")
    dataframe["rom"] = dataframe["rom"].astype("int")

    return dataframe


def info_extractor(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Main function of the cleaning module and handles each operation 

    Args:
        raw_data (pd.DataFrame): Scpared data ready for cleaning.

    Returns:
        pd.DataFrame: DataFrame with all useful data for further analysis
    """
    raw_data = drop_shop(raw_data)
    text_series = create_text_series(raw_data)
    pipeline = extract_data(text_series)
    pipeline["price"] = raw_data["price"]
    pipeline = drop_trash(pipeline)
    pipeline = drop_nas(pipeline)
    pipeline = type_to_int(pipeline)
    return pipeline


def load_from_csv(path: str) -> list[pd.DataFrame]:
    """Loading multiple .csv files into a Dataframe

    Args:
        filenames (list[str]): List of file paths

    Returns:
        list[pd.DataFrame]: List of dataframes reflecting .csv files
    """
    df_list = []
    current_path = os.getcwd()
    os.chdir(path)
    print(os.getcwd())
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for filename in csv_files:
        df_list.append(pd.read_csv(filename))
    os.chdir(current_path)
    return df_list

