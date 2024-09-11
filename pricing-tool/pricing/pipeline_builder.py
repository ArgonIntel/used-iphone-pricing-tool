import pandas as pd
import os
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, path: str) -> list[pd.DataFrame]:
        pass

class CSVDataLoader(DataLoader):
    def load_data(self, path: str) -> list[pd.DataFrame]:
        df_list = []
        csv_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.csv')]
        for filename in csv_files:
            df_list.append(pd.read_csv(filename))
        return df_list

class DataProcessor:
    def __init__(self, loader=CSVDataLoader()):
        self.loader = loader
        self.invalid_data = {"models": 0,
                             "roms": 0,
                             "battery": 0,
                             "locked": 0}

    def process_data(self, path: str) -> pd.DataFrame:
        dfs = self.loader.load_data(path)
        concatenated_df = self._concatenate_dfs(dfs)
        processed_df = self._get_useful_data_from_raw(concatenated_df)
        return processed_df

    def _concatenate_dfs(self, dfs: list[pd.DataFrame]) -> pd.DataFrame:
        """Concatenates DataFrames into one. Multiple Dataframes are result of
        multiple .csv files

        Args:
            dfs (list[pd.DataFrame]): List of DataFrames

        Returns:
            pd.DataFrame: Concatenated DataFrame
        """
        dataframe = pd.concat(dfs, ignore_index=True)
        dataframe.drop(["Unnamed: 0"], axis=1, inplace=True)

        return dataframe

    def _extract_data_from_text(self, text_series: pd.Series) -> pd.DataFrame:
        """Extracts data such as iPhone model, ROM size, Battery health, locked status
        warranty information from Text of the ad

        Args:
            text_series (pd.Series): _description_

        Returns:
            pd.DataFrame: _description_
        """
        pipeline_data = pd.DataFrame()
        pipeline_data["model"] = text_series.str.extract(
            r".phone\s?(\d{2}\s?(?:pro\s)?(?:max)?)", expand=True
        )
        pipeline_data["model"].replace(to_replace=" ", value="", regex=True, inplace=True)
        pipeline_data["rom"] = text_series.str.extract(r"(\d{2,3})\s?gb", expand=True)
        pipeline_data["battery"] = text_series.str.extract(r"(\d{2,3})\s?%", expand=True)
        pipeline_data["warranty"] = text_series.str.contains(
            r"garanc", regex=True
        ) & ~text_series.str.contains(r"istekla", regex=True)
        pipeline_data["locked"] = text_series.str.contains(r"zakljucan", regex=True)
        return pipeline_data

    def _manage_na_values(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """manages missing values in the DataFrame and also removes rows with
        irrelevant data

        Args:
            dataframe (pd.DataFrame): Dataframe to be cleaned

        Returns:
            pd.DataFrame: _description_
        """
        models = ['11', 
          '11pro', 
          '11promax', 
          '12', 
          '12pro', 
          '12promax', 
          '13', 
          '13pro', 
          '13promax', 
          '14', 
          '14pro', 
          '14promax']
        roms = ['64', '128', '256', '512']
        
        dataframe["model"].ffill(inplace=True)
        dataframe["rom"] = dataframe["rom"].fillna(dataframe["rom"].mode().iloc[0])
        df_len = len(dataframe)
        dataframe = dataframe[dataframe["model"].isin(models)]
        self.invalid_data["models"] += df_len - len(dataframe)
        df_len = len(dataframe)
        dataframe = dataframe[dataframe["rom"].isin(roms)]
        self.invalid_data["roms"] += df_len - len(dataframe)
        df_len = len(dataframe)
        dataframe = dataframe[~dataframe["battery"].isna()]
        self.invalid_data["battery"] += df_len - len(dataframe)
        return dataframe.reset_index(drop=True)

    def _get_useful_data_from_raw(self, raw_dataframe: pd.DataFrame) -> pd.DataFrame:
        """Main function of the cleaning module and handles each operation 

        Args:
            dataframe (pd.DataFrame): Scpared data ready for cleaning.

        Returns:
            pd.DataFrame: DataFrame with all useful data for further analysis
        """
        raw_dataframe = raw_dataframe[~raw_dataframe["store_private"].str.contains("trgovine")]
        text_series = raw_dataframe["ad_title"] + " " + raw_dataframe["ad_description"]
        pipeline = self._extract_data_from_text(text_series)
        pipeline["price"] = raw_dataframe["price"].astype("int")
        pipeline = pipeline[pipeline["locked"] == False]
        pipeline = self._manage_na_values(pipeline)
        pipeline["battery"] = pipeline["battery"].astype("int")
        return pipeline