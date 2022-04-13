# kafka-producer-container
The repo just a template which emulate how to produce data to kafka.

## Folder Sturcture
```
|-- example_producer/
    |-- __init__.py
    |-- main.py
|-- helpers/
    |-- __init__.py
    |-- kafka_helper.py
|-- project_configs/
    |-- example_config.yaml
|-- project_libs/
    |-- __init__.py
    |-- common/
        |-- __init__.py
        |-- loadconfig.py
|-- Dockerfile
|-- docker-compose.yaml
|-- entry.sh
|-- requirements.txt
```
* `example_producer/`: Includes main script.
* `helpers/`: Includes kafka helper script which process schema registry, sent message and delivery callback.
* `project_configs/`: schema registy, kafka endpoint config and topic.
* `project_libs/`: load yaml config script.
* `Dockerfile`: it can build related image for container.
* `docker-compose.yaml`: build container.
* `entry.sh`: entry point script of the image.
* `requirements.txt`: install related lib of the container.

## Setup Steps
1. Need to replace related endpoint config.
2. execute cli: `docker build -t example_producer_img .`
3. start docker-compose: `docker-compose up && docker logs -f example_producer`
