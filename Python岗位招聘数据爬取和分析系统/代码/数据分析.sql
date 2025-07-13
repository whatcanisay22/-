create database find_job;
show databases;
use find_job;
select * from job_positions;
drop table job_positions;

    
    
-- 分析城市与经验对薪资的影响
    
WITH grouped_data AS (
SELECT
	city,
	CASE
		WHEN experience LIKE '%10年以上%' THEN '10年以上'
		WHEN experience LIKE '%5-10年%' THEN '5-10年'
		WHEN experience LIKE '%3-5年%' THEN '3-5年'
		WHEN experience LIKE '%1-3年%' THEN '1-3年'
		WHEN experience IN ('经验不限', '不限') THEN '经验不限'
		WHEN experience LIKE '%在校%' OR experience LIKE '%应届%' THEN '在校/应届'
		ELSE '其他'
	END AS experience_group,
	(salary_min + salary_max)/2 AS salary_avg
FROM job_positions
)

SELECT 
    city,
    ROUND(AVG(CASE WHEN experience_group = '10年以上' THEN salary_avg END), 1) AS '10年以上',
    ROUND(AVG(CASE WHEN experience_group = '5-10年' THEN salary_avg END), 1) AS '5-10年',
    ROUND(AVG(CASE WHEN experience_group = '3-5年' THEN salary_avg END), 1) AS '3-5年',
    ROUND(AVG(CASE WHEN experience_group = '1-3年' THEN salary_avg END), 1) AS '1-3年',
    ROUND(AVG(CASE WHEN experience_group = '经验不限' THEN salary_avg END), 1) AS '经验不限',
    ROUND(AVG(CASE WHEN experience_group = '在校/应届' THEN salary_avg END), 1) AS '在校/应届'
FROM grouped_data
WHERE city IN ('北京', '上海', '深圳', '南京','广州','杭州')
GROUP BY city
ORDER BY 
    CASE city
        WHEN '北京' THEN 1
        WHEN '上海' THEN 2
        WHEN '深圳' THEN 3
        WHEN '南京' THEN 4
        when '广州' THEN 5
        WHEN '杭州' THEN 6
        ELSE 7
    END;
    

    
    
-- 分析城市与学历对薪资的影响
    
    WITH grouped_data AS (
    SELECT
        city,
        CASE
            WHEN education = '博士' THEN '博士'
            WHEN education = '硕士' THEN '硕士'
            WHEN education = '本科' THEN '本科'
            WHEN education = '大专' THEN '大专'
            WHEN education IN ('不限', '经验不限') THEN '学历不限'
            ELSE '其他'
        END AS education_level,
        (salary_min + salary_max)/2 AS salary_avg
    FROM job_positions
)

SELECT 
    city,
    ROUND(AVG(CASE WHEN education_level = '博士' THEN salary_avg END), 1) AS '博士',
    ROUND(AVG(CASE WHEN education_level = '硕士' THEN salary_avg END), 1) AS '硕士',
    ROUND(AVG(CASE WHEN education_level = '本科' THEN salary_avg END), 1) AS '本科',
    ROUND(AVG(CASE WHEN education_level = '大专' THEN salary_avg END), 1) AS '大专',
    ROUND(AVG(CASE WHEN education_level = '学历不限' THEN salary_avg END), 1) AS '学历不限',
    ROUND(AVG(CASE WHEN education_level = '其他' THEN salary_avg END), 1) AS '其他'
FROM grouped_data
WHERE city IN ('北京', '上海', '深圳', '南京', '广州', '杭州')
GROUP BY city
ORDER BY 
    CASE city
        WHEN '北京' THEN 1
        WHEN '上海' THEN 2
        WHEN '深圳' THEN 3
        WHEN '南京' THEN 4
        WHEN '广州' THEN 5
        WHEN '杭州' THEN 6
        ELSE 7
    END;