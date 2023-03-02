from pyspark.sql import SparkSession

# /Users/mardy/soft/jar/mysql-connector-java-8.0.11.jar

# connect spark
spark = SparkSession.builder.appName('My first app') \
    .config('spark.executor.extraClassPath', '/Users/mardy/pyspark/*') \
    .config('spark.driver.extraClassPath', '/Users/mardy/pyspark/*') \
    .getOrCreate()

url = 'jdbc:mysql://127.0.0.1:3306/test?&useSSL=false'
properties = {'user': 'root', 'password': ''}

table = "(select * from test.test_hjp limit 1) temp"  # 写sql
# sql_test = 'select * from test_hjp limit 1'
df = spark.read.jdbc(url=url, table=table, properties=properties)
df.show()

df.write.jdbc(url, 'test_hjp', model='append', properties=properties)


# from pyspark.sql.types import Row
# from pyspark.sql.types import StructType
# from pyspark.sql.types import StructField
# from pyspark.sql.types import StringType
# from pyspark.sql.types import IntegerType
# studentRDD = spark.sparkContext.parallelize(["3 Rongcheng M 26","4 Guanhua M 27"]).map(lambda line : line.split(" "))
