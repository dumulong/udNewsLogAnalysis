#!/usr/bin python2.7

import psycopg2
import psycopg2.extras

DBNAME = "news"

conn = psycopg2.connect(database=DBNAME)

# --------------------------------------------------

qryMostReadArticles = \
    'select articles.title, count(*) as cnt ' \
    'from log ' \
    'inner join articles on \'/article/\' || articles.slug = log.path ' \
    'group by articles.title ' \
    'order by count(*) desc ' \
    'limit 3;'

curMostRead = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
curMostRead.execute(qryMostReadArticles)
print ""
print "-----------------------------------"
print "What are the most popular three articles of all time?"
print "-----------------------------------"
print ""
for record in curMostRead:
    print record['title'] + " - " + str(record['cnt']) + " views"

# --------------------------------------------------

qryMostPopAuthor = \
    'select authors.name, count(*) as cnt ' \
    'from log ' \
    'inner join articles on \'/article/\' || articles.slug = log.path ' \
    'inner join authors on articles.author = authors.id ' \
    'group by authors.name ' \
    'order by count(*) desc;'

curMostPop = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
curMostPop.execute(qryMostPopAuthor)
print ""
print "-----------------------------------"
print "Who are the most popular article authors of all time?"
print "-----------------------------------"
print ""
for record in curMostPop:
    print record['name'] + " - " + str(record['cnt']) + " views"

# --------------------------------------------------

qryErrorPct = \
    'select trim(to_char(summary.myDate, \'Month\')) || '\
    '    to_char(summary.myDate, \' DD, YYYY\') as myDate, ' \
    '    to_char(summary.errorPct, \'999D0%\') as errorPct ' \
    'from ( ' \
    '    select myDate, ' \
    '        errorCountSubQ.errorCount, ' \
    '        count(*) as requestCount,' \
    '        errorCountSubQ.errorCount * 100.0 / count(*) AS errorPct ' \
    '    from vLogStats ' \
    '    inner join ( ' \
    '        select myDate as errorDay, count (*) as errorCount ' \
    '        from vLogStats ' \
    '        where status >= 400 ' \
    '        group by myDate ' \
    '    ) errorCountSubQ on errorCountSubQ.errorDay = myDate ' \
    '    group by myDate, errorCountSubQ.errorCount ' \
    ') summary ' \
    'where errorPct > 1.0 ' \
    'order by summary.myDate;'

curErrorPct = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
curErrorPct.execute(qryErrorPct)
print ""
print "-----------------------------------"
print "On which days did more than 1% of requests lead to errors?"
print "-----------------------------------"
print ""
for record in curErrorPct:
    print record['mydate'] + " - " + record['errorpct'] + " errors"

print ""

conn.close()
