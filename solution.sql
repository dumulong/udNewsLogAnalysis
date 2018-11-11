-- ================================================
-- Question 1:
-- ================================================

select articles.title, count(*) as cnt
from log
inner join articles on '/article/' || articles.slug = log.path
group by articles.title
order by count(*) desc
limit 3;

-- ================================================
-- Question 2:
-- ================================================

select authors.name, count(*) as cnt
from log
inner join articles on '/article/' || articles.slug = log.path
inner join authors on articles.author = authors.id
group by authors.name
order by count(*) desc;


-- ================================================
-- Question 3:
-- ================================================

drop view vLogStats;

create view vLogStats
as
select log.time::date as myDate, to_number(log.status, '999') as status
from log;

-- List of ALL requests on days with errors
select trim(to_char(summary.myDate, 'Month')) || to_char(summary.myDate, ' DD, YYYY') as myDate,
    to_char(summary.errorPct, '999D0%') as errorPct
from (
    select myDate,
        errorCountSubQ.errorCount,
        count(*) as requestCount,
        errorCountSubQ.errorCount * 100.0 / count(*) AS errorPct
    from vLogStats
    inner join (
        select myDate as errorDay, count (*) as errorCount
        from vLogStats
        where status >= 400
        group by myDate
    ) errorCountSubQ on errorCountSubQ.errorDay = myDate
    group by myDate, errorCountSubQ.errorCount
) summary
where errorPct > 1.0
order by summary.myDate;