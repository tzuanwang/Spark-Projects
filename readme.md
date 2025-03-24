# Spark Docker Standalone Cluster

## Overview
This project uses Docker Compose to manage a Standalone Spark cluster. The `Makefile` provides several commands to build, run, and manage the cluster.

## Getting Started
Before running any commands, please refer to the `Makefile` for available targets and their descriptions.

## Makefile Commands

### Build Commands
- `make build`: Build the Docker images.
- `make build-nc`: Build the Docker images without cache.
- `make build-progress`: Build the Docker images without cache and show plain progress.

### Run Commands
- `make run`: Bring up the cluster after taking it down.
- `make run-scaled`: Bring up the cluster with scaled Spark workers.
- `make run-d`: Bring up the cluster in detached mode.

### Management Commands
- `make down`: Take down the cluster and remove volumes.
- `make stop`: Stop the running containers.

### Spark Submit
- `make submit app=<app_name>`: Submit a Spark application to the cluster.

## Usage
To use the commands, simply run `make <target>` in your terminal. For example:
```sh
make build
make run
make submit app=your_spark_app.py
```

## Instructions

First, build the Docker containers using the following command:
```sh
make build
```

When you want to use the cluster, you have two options:
- To bring up the cluster with 3 Spark workers, run:
    ```sh
    make run-scaled
    ```
- To bring up the cluster with 1 Spark worker, run:
    ```sh
    make run
    ```

Once the containers are up, shared volumes will be created as folders on your host machine. These folders include:

- `./data`: For Spark data.
- `./spark_apps`: For Spark applications.
- `./spark-logs`: For Spark event logs.
- `./spark-worker-logs`: For Spark worker logs.

You can find these folders in the project directory.

Once the containers are up, you can access the Spark Master UI at `http://localhost:8080` and the Spark History UI at `http://localhost:18080`.

Once you finish writing your Spark application in the `/spark_apps` folder, you can use `make submit` to test it. For example, to test if everything works properly after compose up with the provided `employee_transform.py` example application, run:
```sh
make submit example-employee_transform.py
```

So do the same for testing the connection to AWS and Snowflake with the provided example applications, run:
```sh
make submit example-read-csv-from-S3.py
```
and
```sh
make submit example-read-table-from-Snowflake.py
```


**Note**: Ensure you update the `.env.spark` file with your own `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and all Snowflake configs before docker compose-up for the project to work properly or you can simply update and do `make run` or `make run-scaled`.

**Note:** This project uses Spark version `3.4.4`. If you wanna run the driver on your local machine, you might need to set up a virtual environment (venv) or ensure that your `pyspark` version is also `3.4.4`.