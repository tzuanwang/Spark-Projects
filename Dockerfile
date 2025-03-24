FROM python:3.11-bullseye AS spark-base

ARG SPARK_VERSION=3.4.4

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh \
      iputils-ping &&\
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

RUN curl https://dlcdn.apache.org/spark/spark-3.4.4/spark-3.4.4-bin-hadoop3.tgz -o spark-3.4.4-bin-hadoop3.tgz \
 && tar xvzf spark-3.4.4-bin-hadoop3.tgz --directory /opt/spark --strip-components 1 \
 && rm -rf spark-3.4.4-bin-hadoop3.tgz

ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/3.3.4/hadoop-common-3.3.4.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1034/aws-java-sdk-bundle-1.11.1034.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/net/snowflake/snowflake-jdbc/3.23.1/snowflake-jdbc-3.23.1.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/net/snowflake/spark-snowflake_2.12/2.16.0-spark_3.4/spark-snowflake_2.12-2.16.0-spark_3.4.jar /opt/spark/jars/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
ENV SPARK_HOME="/opt/spark"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

COPY entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]