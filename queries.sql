-- Q1: Total revenue by region
SELECT region, COUNT(*) AS orders, ROUND(SUM(total_amount), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Q2: Top 5 products by revenue
SELECT product, SUM(quantity) AS units_sold, ROUND(SUM(total_amount), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC
LIMIT 5;

-- Q3: Monthly revenue with month-over-month growth % (window function: LAG)
WITH monthly AS (
    SELECT order_month, SUM(total_amount) AS revenue
    FROM sales
    GROUP BY order_month
)
SELECT order_month,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY order_month))
             / LAG(revenue) OVER (ORDER BY order_month), 1) AS mom_growth_pct
FROM monthly
ORDER BY order_month;

-- Q4: Top 2 customers in each region (window function: RANK)
SELECT * FROM (
    SELECT region, customer_name, ROUND(SUM(total_amount), 2) AS revenue,
           RANK() OVER (PARTITION BY region ORDER BY SUM(total_amount) DESC) AS rnk
    FROM sales
    GROUP BY region, customer_name
)
WHERE rnk <= 2
ORDER BY region, rnk;

-- Q5: Revenue share by category
SELECT category,
       ROUND(SUM(total_amount), 2) AS revenue,
       ROUND(100.0 * SUM(total_amount) / (SELECT SUM(total_amount) FROM sales), 1) AS pct_of_total
FROM sales
GROUP BY category
ORDER BY revenue DESC;
