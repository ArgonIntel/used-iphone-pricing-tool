import pandas as pd


def clean_text_column(column):
    column = column.str.lower()
    char_mapping = {"č": "c", "ć": "c", "š": "s", "ž": "z", "đ": "dj"}
    column.replace(to_replace=char_mapping, regex=True, inplace=True)
    column.replace(to_replace=r"[^a-zA-Z0-9%.]", value=" ", regex=True, inplace=True)
    column.replace(to_replace=r"\s+", value=" ", regex=True, inplace=True)
    return column


def convert_to_int_columns(df, int_columns):
    df = df.astype(int_columns)
    return df


def convert_to_datetime_column(df, column):
    df[column] = pd.to_datetime(df[column], dayfirst=True, format="%d.%m.%Y")
    return df


def clean_number_column(column):
    column.replace(to_replace=r"\.?(\,.+)?", value="", regex=True, inplace=True)
    return column


def cleaner(content):
    df = pd.DataFrame.from_dict(content)
    try:
        text_columns = ["store_private", "ad_description", "ad_title"]
        for column in text_columns:
            df[column] = clean_text_column(df[column])
    except Exception as e:
        e
    try:
        df["price"] = clean_number_column(df["price"])
    except Exception as e:
        e
    try:
        int_columns = {"price": int, "ad_id": int, "number_of_showings": int}
        df = convert_to_int_columns(df, int_columns)
    except Exception as e:
        e
    try:
        df = convert_to_datetime_column(df, "date_of_publishing")
    except Exception as e:
        e

    return df
