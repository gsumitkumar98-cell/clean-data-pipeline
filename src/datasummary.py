# default logger module
import logging

# pandas module
import pandas as pd

logger = logging.getLogger(__name__)


def data_summary(
    df: pd.DataFrame
) -> dict:
    """
    Generate summary statistics for dataframe.

    Parameters:
        df (pd.DataFrame):
            Input dataframe.

    Returns:
        dict:
            Dictionary containing dataframe
            summary information.

    Raises:
        TypeError:
            If input is not pandas DataFrame.

        ValueError:
            If summary generation fails.
    """

    try:

        # validate dataframe input
        if not isinstance(df, pd.DataFrame):

            raise TypeError(
                "df must be a pandas DataFrame"
            )

        # handle empty dataframe
        if df.empty:

            logger.warning(
                "Empty dataframe received for summary generation"
            )

        logger.info(
            "Started dataframe summary generation"
        )

        # convert column labels safely
        safe_columns = [
            str(col)
            for col in df.columns
        ]

        # generate summary
        summary = {

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "memory_usage_bytes": int(
                df.memory_usage(
                    deep=True
                ).sum()
            ),

            "missing_values": {
                str(col): int(count)
                for col, count in df.isnull()
                .sum()
                .items()
            },

            "missing_percentage": {
                str(col): round(
                    (count / len(df)) * 100,
                    2
                )
                if len(df) > 0 else 0
                for col, count in df.isnull()
                .sum()
                .items()
            },

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "unique_values": {
                str(col): int(
                    df[col].nunique()
                )
                for col in df.columns
            },

            "column_types": {
                str(col): str(dtype)
                for col, dtype in df.dtypes.items()
            },

            "numeric_summary": (
                df.describe(
                    include=["number"]
                )
                .fillna(0)
                .round(2)
                .to_dict()
            )
            if not df.select_dtypes(
                include=["number"]
            ).empty
            else {}
        }

        logger.info(
            "Summary generated successfully for dataframe with %s rows",
            len(df)
        )

        return summary

    except TypeError:
        raise

    except Exception as e:

        logger.exception(
            "Error while generating dataframe summary"
        )

        raise ValueError(
            f"Summary generation failed: {str(e)}"
        )