import os
import pandas as pd
from internal.db import database
import gc


def etl() -> int:
    try:
        base_path = os.path.join(os.getcwd(), "data")
        # Load CSV files
        compounds_df = pd.read_csv(os.path.join(base_path, "compounds.csv"))
        user_experiments_df = pd.read_csv(os.path.join(base_path, "user_experiments.csv"))
        users_df = pd.read_csv(os.path.join(base_path, "users.csv"))

        # Sanitize files
        user_experiments_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)
        compounds_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)
        users_df.replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"], value=["", ""], regex=True, inplace=True)

        # Remove tabs from the headers
        compounds_df.columns = compounds_df.columns.str.strip()
        user_experiments_df.columns = user_experiments_df.columns.str.strip()
        users_df.columns = users_df.columns.str.strip()

        # Process files to derive features
        total_experiments_per_user = list(list())
        ave_experiments_amount_per_user = list(list())
        most_user_compound_by_user = list(list())

        # Go through every user
        for user in users_df.loc[:, 'user_id']:
            # Count rows (experiments) where user was involved to see total experiments a user ran.
            rows_df = user_experiments_df.query(f'user_id == {user}')
            total_experiments_per_user.append([user, len(rows_df.index)])

            # Get the mean time of the experiments run by that user
            mean = rows_df["experiment_run_time"].mean()
            ave_experiments_amount_per_user.append([user, mean])

            # User's most commonly experimented compound
            # Dictionary incase id is not in order, so we don't waste array space
            compounds_dict = dict()
            for _, row in rows_df.iterrows():
                for compound_id in row['experiment_compound_ids'].split(';'):
                    # count how many times that compound was used by this user
                    if compound_id not in compounds_dict:
                        compounds_dict[compound_id] = 1
                    else:
                        compounds_dict[compound_id] += 1

            # Sort compound count in descending order
            sorted_compounds = sorted(compounds_dict.items(), key=lambda x: x[1], reverse=True)
            if sorted_compounds:
                # sorted_compounds[0] = most used compound with count respectively e.g. (1, 121)
                # Should only yield one row
                temp_comp_df = compounds_df.query(f'compound_id == {sorted_compounds[0][0]}')
                sanitized_compound_name = temp_comp_df['compound_name'].to_string(index=False)
                most_user_compound_by_user.append([user, sanitized_compound_name])
            else:
                most_user_compound_by_user.append([user, []])

        # Convert data to dataframe
        total_experiments_per_user_df = data_to_df(total_experiments_per_user,
                                                   ["user_id", "total_experiments"])
        ave_experiments_amount_per_user_df = data_to_df(ave_experiments_amount_per_user,
                                                        ["user_id", "average_experiments_time"])
        most_user_compound_by_user_df = data_to_df(most_user_compound_by_user,
                                                   ["user_id", "most_common_used_compound"])

        # Tell python garbage collector to free deleted memory
        gc.collect()

        # Merge dataframes together on user_id
        data_df = pd.merge(pd.merge(total_experiments_per_user_df,
                                    ave_experiments_amount_per_user_df,
                                    on='user_id'), most_user_compound_by_user_df,
                           on='user_id')

        # Replace user_id with name of user
        data_df['user_id'] = users_df['name']
        data_df.rename(columns={"user_id": "name"}, inplace=True)

        del total_experiments_per_user_df
        del ave_experiments_amount_per_user_df
        del most_user_compound_by_user_df
        # Tell python garbage collector to free deleted memory
        gc.collect()

        # Upload processed data into a database
        if database.insert_table_into_db(data_df):
            return 1

        return 0

    except Exception as e:
        print(e)
        return 1


def data_to_df(data: [[]], header: []) -> pd.DataFrame:
    df = pd.DataFrame(data)
    df.columns = header
    # Delete data object after load
    del data
    return df


# Your API that can be called to trigger your ETL process
def trigger_etl() -> ({}, int):
    # Trigger your ETL process here
    if etl():
        return {"message": "Error: ETL process not started"}, 400
    return {"message": "ETL process started"}, 200
