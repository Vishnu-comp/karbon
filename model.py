from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json


def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    # Get the latest financial index (i.e., the most recent financial year)
    latest_financial_index_value = latest_financial_index(data)

    # Evaluate the flags based on financial data
    total_revenue_5cr_flag_value = total_revenue_5cr_flag(data, latest_financial_index_value)
    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(data, latest_financial_index_value)
    iscr_flag_value = iscr_flag(data, latest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }


if __name__ == "__main__":
    try:
        # Read the data.json file
        with open("data.json", "r") as file:
            content = file.read()

        # Parse the JSON content into a dictionary
        data = json.loads(content)

        # Pass the financial data to probe_model_5l_profit and print the results
        results = probe_model_5l_profit(data["data"])
        print(json.dumps(results, indent=4))

    except FileNotFoundError:
        print("Error: data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data from data.json.")
    except KeyError as e:
        print(f"Error: Missing key in the financial data - {e}")
