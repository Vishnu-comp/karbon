import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # Display purpose only
    WHITE = 4  # Data is missing for this field

# This is already written for your reference
def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.
    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.
    """
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int):
    """
    Calculate the total revenue from the financial data at the given index.
    This function accesses the "financials" list in the data dictionary at the specified index.
    It retrieves the net revenue from the "pnl" (Profit and Loss) section under "lineItems".
    """
    try:
        return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]
    except KeyError:
        return 0

def total_borrowing(data: dict, financial_index: int):
    """
    Calculate the total borrowings from the financial data at the given index.
    This function sums the long-term and short-term borrowings from the balance sheet ("bs") section.
    """
    try:
        long_term_borrowings = data["financials"][financial_index]["bs"]["liabilities"].get("long_term_borrowings", 0)
        short_term_borrowings = data["financials"][financial_index]["bs"]["liabilities"].get("short_term_borrowings", 0)
        total_revenue_value = total_revenue(data, financial_index)
        
        if total_revenue_value == 0:
            return None  # Avoid division by zero

        return (long_term_borrowings + short_term_borrowings) / total_revenue_value
    except KeyError:
        return None

def iscr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the ISCR value.
    If ISCR >= 2, return GREEN flag, otherwise RED.
    """
    try:
        iscr_value = iscr(data, financial_index)
        if iscr_value >= 2:
            return FLAGS.GREEN
        else:
            return FLAGS.RED
    except (KeyError, TypeError):
        return FLAGS.WHITE

def total_revenue_5cr_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on whether the total revenue exceeds 50 million (5 Crores).
    If total revenue >= 50,000,000, return GREEN flag, otherwise RED.
    """
    total_revenue_value = total_revenue(data, financial_index)
    if total_revenue_value >= 50000000:
        return FLAGS.GREEN
    else:
        return FLAGS.RED

def iscr(data: dict, financial_index: int):
    """
    Calculate the Interest Service Coverage Ratio (ISCR).
    ISCR = (Profit before interest, tax, and depreciation + 1) / (Interest + 1)
    """
    try:
        pnl_data = data["financials"][financial_index]["pnl"]["lineItems"]
        profit_before_interest_and_tax = pnl_data.get("profit_before_interest_and_tax", 0)
        depreciation = pnl_data.get("depreciation", 0)
        interest = pnl_data.get("interest", 1)  # Adding 1 to avoid division by zero
        
        iscr_value = (profit_before_interest_and_tax + depreciation + 1) / (interest + 1)
        return iscr_value
    except KeyError:
        return 0

def borrowing_to_revenue_flag(data: dict, financial_index: int):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    If borrowing/revenue ratio <= 0.25, return GREEN flag, otherwise AMBER.
    """
    try:
        borrowing_to_revenue_ratio = total_borrowing(data, financial_index)
        if borrowing_to_revenue_ratio is None:
            return FLAGS.WHITE  # Data is missing

        if borrowing_to_revenue_ratio <= 0.25:
            return FLAGS.GREEN
        else:
            return FLAGS.AMBER
    except (KeyError, TypeError):
        return FLAGS.WHITE
