import pandas as pd
import pytest
import pyarrow.dataset as ds
import os
from polars.testing import assert_frame_equal
from pathlib import Path
import pyarrow as pa
import pyarrow.parquet as pq


TEST_DIR = Path(__file__).parent
ROOT = "./output_parquet"
PARQUET_ROOT = TEST_DIR.parent / ROOT
MARKET_DATA = './market_data/market_data_multi.csv'
MARKET_DATA_ROOT = TEST_DIR.parent / MARKET_DATA

@pytest.fixture
def dataset():
    return ds.dataset(PARQUET_ROOT,
                      format="parquet",
                      partitioning="hive"
                      )

def test_partition_parquet(dataset):
    assert os.path.exists(PARQUET_ROOT)

    files = [d for d in os.listdir(PARQUET_ROOT) if d.startswith("ticker=")]
    assert len(files) == 5

    for f in files:
        assert f.split("=")[0] == "ticker"


def test_schema_data(dataset):
    original_df = pd.read_csv(MARKET_DATA_ROOT)

    table = pa.Table.from_pandas(original_df, preserve_index=False)
    pq.write_to_dataset(
        table,
        root_path="output_parquet_test",
        partition_cols=["ticker"]
    )
    df = table.to_pandas()

    #check numbers of rows is consistent
    assert len(df) == len(original_df)

    #check integrity
    df = df.sort_values(["ticker", "timestamp"]).reset_index(drop=True)
    original_df = original_df.sort_values(["ticker", "timestamp"]).reset_index(drop=True)

    same_cols = [col for col in df.columns if col in original_df.columns]

    #check query df and original df are the same
    pd.testing.assert_frame_equal(df[same_cols], original_df[same_cols])






