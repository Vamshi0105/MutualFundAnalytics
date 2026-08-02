--1
SELECT fund_name,aum
FROM fact_aum
ORDER BY aum DESC
LIMIT 5;

--2
SELECT
strftime('%Y-%m',full_date),
AVG(nav)
FROM fact_nav
JOIN dim_date
ON fact_nav.date_key=dim_date.date_key
GROUP BY 1;

--3
SELECT
strftime('%Y',full_date),
SUM(amount)
FROM fact_transactions
JOIN dim_date
ON fact_transactions.date_key=dim_date.date_key
WHERE transaction_type='SIP'
GROUP BY 1;

--4
SELECT
investor_state,
COUNT(*)
FROM fact_transactions
GROUP BY investor_state;

--5
SELECT
fund_name,
expense_ratio
FROM fact_performance
JOIN dim_fund
USING(fund_key)
WHERE expense_ratio<1;

--6
SELECT
category,
AVG(return_5y)
FROM fact_performance
JOIN dim_fund
USING(fund_key)
GROUP BY category;

--7
SELECT
transaction_type,
SUM(amount)
FROM fact_transactions
GROUP BY transaction_type;

--8
SELECT
fund_name,
MAX(nav)
FROM fact_nav
JOIN dim_fund
USING(fund_key)
GROUP BY fund_name;

--9
SELECT
fund_house,
COUNT(*)
FROM dim_fund
GROUP BY fund_house;

--10
SELECT
AVG(expense_ratio)
FROM fact_performance;