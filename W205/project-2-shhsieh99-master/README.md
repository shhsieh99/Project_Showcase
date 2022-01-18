# Project 2: Tracking User Activity

In this project, I work at an ed tech firm. This is a service that
delivers assessments, and now lots of different customers (e.g., Pearson) want
to publish their assessments on it. I get ready for data scientists
who work for these customers to run queries on the data. 

## Data

To get the data, run 
```
curl -L -o assessment-attempts-20180128-121051-nested.json https://goo.gl/ME6hjp`
```

Note on the data: This is a nested JSON file, where you need to unwrap it
carefully to understand what's really being displayed. There are many fields
that are not that important for analysis. The main problem will be the multiple questions field. 
We recommend for you to read schema implementation in Spark [Here is the documenation from
Apache](https://spark.apache.org/docs/2.3.0/sql-programming-guide.html).

Here are some questions to get started/thinking.

1. How many assesstments are in the dataset?
2. What's the name of your Kafka topic? How did you come up with that name?
3. How many people took *Learning Git*?
4. What is the least common course taken? And the most common?

## Files

- History of my commands in the terminal and Spark
    - `shhsieh99-history.txt`
    - `shhsieh99-spark-history.txt`
- Example of docker-compose.yml files
    - `docker-compose.yml`
- My report
  - `Report.ipynb`
  -  The report describes your queries and spark SQL to answer business questions that I selected. It describes my assumptions, my thinking, what the parts of the pipeline do. What is given? What do I set up myself? What issues did I find with the data? Do I find ways to solve it? How? If not describe what the problem is.
