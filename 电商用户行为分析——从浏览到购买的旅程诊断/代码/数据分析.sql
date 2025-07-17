USE firm_data;
SHOW tables;
SET FOREIGN_KEY_CHECKS = 0;
SET FOREIGN_KEY_CHECKS = 1;


select count(distinct user_id) from user_behavior where behavior_type = 'pv';
select count(distinct user_id) from user_behavior where behavior_type = 'cart';
select count(distinct user_id) from user_behavior where behavior_type = 'buy';
select * from user_behavior;



-- 1.计算关键指标：浏览-加购与喜欢-购买转化率
WITH metrics AS (
    SELECT 
        COUNT(DISTINCT CASE WHEN behavior_type = 'pv' THEN user_id END) AS pv_users,
        COUNT(DISTINCT CASE WHEN behavior_type = 'cart' THEN user_id END) AS cart_users,
        COUNT(DISTINCT CASE WHEN behavior_type = 'buy' THEN user_id END) AS buy_users
    FROM user_behavior
)
SELECT 
    pv_users AS '浏览人数',
    cart_users AS '加购人数',
    buy_users AS '购买人数',
    ROUND(100.0 * cart_users / NULLIF(pv_users, 0), 2) AS '浏览到加购转化率(%)',
    ROUND(100.0 * buy_users / NULLIF(cart_users, 0), 2) AS '加购到购买转化率(%)'
FROM metrics;


-- 2. 找出流失用户所占比例
WITH 
-- 计算加购但未购买的用户数
bad_users AS (
  SELECT COUNT(DISTINCT user_id) AS bad_num
  FROM user_behavior
  WHERE behavior_type = 'cart'
  AND user_id NOT IN (
    SELECT user_id 
    FROM user_behavior 
    WHERE behavior_type = 'buy'
  )
),
-- 计算总加购用户数
total_cart_users AS (
  SELECT COUNT(DISTINCT user_id) AS total_num
  FROM user_behavior
  WHERE behavior_type = 'cart'
)

-- 计算流失率
SELECT 
  bad_num AS '流失用户数',
  total_num AS '总加购用户数',
  ROUND(100.0 * bad_num / NULLIF(total_num, 0), 2) AS '流失率百分比'
FROM bad_users, total_cart_users;

-- 高价值用户
select user_id,count(behavior_type) as buy_num
from user_behavior
where behavior_type='buy'
group by user_id
order by buy_num desc
limit 100;