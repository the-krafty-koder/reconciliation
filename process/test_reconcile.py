import numpy as np
import pandas as pd
import pytest

from process.reconcile import fill_rows_and_cols, pre_process, reconcile


class TestReconcile:
    index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    brands = [
        "Peugeot",
        "VW",
        "Mercedes",
        "Toyota",
        "BMW",
        "Nissan",
        "Skoda",
        "Audi",
        "Subaru",
        "Tata",
    ]
    first_quarter_data = {
        "id": index,
        "brands": brands,
        "employees": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "sales_volume": [
            "20000",
            "60000",
            "80000",
            "120000",
            "70000",
            "100000",
            "10000",
            "50000",
            "90000",
            "30000",
        ],
    }
    second_quarter_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "brands": brands[:9],
        "sales_volume": [
            "10000",
            "65000",
            "70000",
            "120000",
            "80000",
            "13000",
            "40000",
            "90000",
            "38000",
        ],
    }

    def test_if_error_is_thrown_if_both_files_are_empty(self):
        df1 = pd.DataFrame({})
        df2 = pd.DataFrame({})

        with pytest.raises(TypeError):
            pre_process(df1, df2)

    def test_if_empty_file_is_prefilled_with_null_values(self):
        df1 = pd.DataFrame(self.first_quarter_data)
        df1.set_index("id", inplace=True)
        df2 = pd.DataFrame({})
        df3 = pd.DataFrame(
            np.nan,
            index=pd.Series(name="id", data=self.first_quarter_data["id"]),
            columns=["brands", "employees", "sales_volume"],
        )

        _, proc2 = pre_process(df1, df2)

        assert proc2.equals(df3) is True

    def test_if_empty_record_is_prefilled_with_null_values(self):
        df1 = pd.DataFrame(self.first_quarter_data)
        df1.set_index("id", inplace=True)
        df2 = pd.DataFrame(self.second_quarter_data)
        df2.set_index("id", inplace=True)

        proc1 = fill_rows_and_cols(df2, df1)
        proc2 = fill_rows_and_cols(df1, df2)

        assert proc1.equals(df1) is True
        assert "employees" in proc2.columns.values

    def test_reconcile(self):
        df1 = pd.DataFrame(self.first_quarter_data)
        df1.name = "File1"
        df1.set_index("id", inplace=True)
        df2 = pd.DataFrame(self.second_quarter_data)
        df2.name = "File2"
        df2.set_index("id", inplace=True)

        proc1, proc2 = pre_process(df1, df2)
        diff = reconcile(proc2, proc1)

        # brand Tata present in file 1 but missing in file 2
        assert diff == {
            "brands": [("Tata", None)],
            "employees": [
                (10, None),
                (20, None),
                (30, None),
                (40, None),
                (50, None),
                (60, None),
                (70, None),
                (80, None),
                (90, None),
                (100, None),
            ],
            "sales_volume": [
                ("20000", "10000"),
                ("60000", "65000"),
                ("80000", "70000"),
                ("70000", "80000"),
                ("100000", "13000"),
                ("10000", "40000"),
                ("50000", "90000"),
                ("90000", "38000"),
                ("30000", None),
            ],
        }
