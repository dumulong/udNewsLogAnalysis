# News Log Analysis

The News Log Analysis programs generate some stats about the use of the new databadse.

## Installation

Clone the GitHub repository.

```
$ git clone https://github.com/dumulong/udNewsLogAnalysis.git
$ cd udNewsLogAnalysis
```

## Usage

In order to generate the statistical analysis report, you will need first to create a view:

```
create view vLogStats
as
    select log.time::date as myDate, to_number(log.status, '999') as status
    from log;
```

then, run our python file:
```
python NewsReport.py
```

You will then receive the result from our statistical anylysis:
```

-----------------------------------
What are the most popular three articles of all time?
-----------------------------------

Candidate is jerk, alleges rival - 338647 views
Bears love berries, alleges bear - 253801 views
Bad things gone, say good people - 170098 views

-----------------------------------
Who are the most popular article authors of all time?
-----------------------------------

Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views

-----------------------------------
On which days did more than 1% of requests lead to errors?
-----------------------------------

July 17, 2016 -    2.3% errors

```

## License

udNewsLogAnalysis is distributed under the MIT license.
