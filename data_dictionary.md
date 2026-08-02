# Mutual Fund Data Dictionary

## nav_history

|Column|Type|Definition|
|------|----|----------|
|amfi_code|INTEGER|Unique AMFI Scheme Code|
|date|DATE|NAV Date|
|nav|REAL|Net Asset Value|

Source:
AMFI Historical NAV

---

## investor_transactions

|Column|Type|Definition|
|------|----|----------|
|transaction_id|INTEGER|Transaction ID|
|investor_id|INTEGER|Investor|
|transaction_type|TEXT|SIP/Lumpsum/Redemption|
|amount|REAL|Transaction Amount|
|transaction_date|DATE|Investment Date|
|kyc_status|TEXT|KYC Verification Status|

Source:
Investor Transaction Dataset

---

## scheme_performance

|Column|Type|Definition|
|------|----|----------|
|amfi_code|INTEGER|Fund Identifier|
|return_1y|REAL|1-Year Return (%)|
|return_3y|REAL|3-Year Return (%)|
|return_5y|REAL|5-Year Return (%)|
|expense_ratio|REAL|Expense Ratio (%)|

Source:
Scheme Performance Dataset