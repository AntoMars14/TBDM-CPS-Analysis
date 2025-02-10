# TBDM-CPS-Analysis

## Table of contents:
1. [Introduction](#introduction)
2. [Technologies](#technologies)
4. [Prerequisites](#prerequisites)
5. [Installation & Configuration](#installation--configuration)
   
   I. [Kafka](#kafka)
   
   II. [ThingsBoard](#thingsboard)
   
   III. [ThingsBoard IoT Gateway](#thingsboard-iot-gateway)
7. [Usage](#usage)
8. [Results](#results)




## Introduction
In the optimization of a dewatering CPS machine, several sensor are used to collect real-time data. The project is about the analysis of a Cyber-Physical System (CPS) data using Big Data Technologies.

This project implements a Big Data system that analyze the data in real-time. The data are published in Kafka using the following 2 different approaches.
#### First approach:
Uses a Spooldir connector to read data from a csv file and publish them in Kafka.
#### Second approach:

Then the data are read(consumed) by the (subscriber) Thingsboard IoT Gateway, using a custom plug-in, and are sent to Thingsboard. In Thingsboard the data are visualized using charts and other visual representation into a dashboard. Alarms have also been implemented in Thingsboard and they can be monitored from the dashbord.

## Technologies
### [Apache Kafka](https://kafka.apache.org/)
Apache Kafka is an open-source distributed event streaming platform used by thousands of companies for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications. 
Apache Kafka combines three key capabilities so you can implement your use cases for event streaming end-to-end with a single battle-tested solution:

1. To publish (write) and subscribe to (read) streams of events, including continuous import/export of your data from other systems.
2. To store streams of events durably and reliably for as long as you want.
3. To process streams of events as they occur or retrospectively.
    
And all this functionality is provided in a distributed, highly scalable, elastic, fault-tolerant, and secure manner. Kafka can be deployed on bare-metal hardware, virtual machines, and containers, and on-premises as well as in the cloud. You can choose between self-managing your Kafka environments and using fully managed services offered by a variety of vendors.

### [ThingsBoard IoT Gateway](https://thingsboard.io/docs/iot-gateway/)
The ThingsBoard IoT Gateway is an open-source solution that allows you to integrate devices connected to legacy and third-party systems with ThingsBoard. For example, you can extract data from devices that are connected to external MQTT brokers, OPC-UA servers, Sigfox Backend, Modbus slaves or CAN nodes.
### Architecture

The IoT Gateway is a software component that is designed to run on a Linux based microcomputers that support Python 3.7+. The main components of ThingsBoard IoT Gateway are listed below.

#### Connector

The purpose of this component is to connect to external system (e.g. MQTT broker or OPC-UA server) or directly to devices (e.g. Modbus, BLE or CAN). Once connected, the connector either poll data from those systems or subscribe to updates. Poll vs subscribe depends on the protocol capabilities. For example, we use subscription model for MQTT connectors and polling for Modbus and CAN. The connector is also able to push updates to devices either directly or via external systems.

It is possible to define your own connector using the customization guide.

#### Converter

Converters are responsible for converting data from protocol specific format to/from ThingsBoard format. Converters are invoked by Connectors. Converters are often specific to protocol supported by Connector. There are uplink and downlink converters. The uplink converter is used to convert data from specific protocol to ThingsBoard format. The downlink converter is used to convert messages from ThingsBoard to specific protocol format.

It is possible to define your own converter using the customization guide.

#### Event Storage

The Event Storage is used to temporary store the telemetry and other events produced by Connectors until they are delivered to ThingsBoard. The Event Storage supports two implementations: in-memory queue and persistent file storage. Both implementations make sure that your device data is eventually delivered in case of network outages. In-memory queue minimizes the IO operations but may lose messages in case of gateway process restart.
Persistent file storage survives the restart of the process but executes IO operations to the file system.

#### ThingsBoard Client

The Gateway communicates to ThingsBoard via MQTT protocol and uses API described here. ThingsBoard Client is a separate thread that polls Event Storage and delivers messages once connection to ThingsBoard is active.
ThingsBoard Client supports monitoring of the connectivity, batching the events for performance improvement and many other features.

#### Gateway Service

The Gateway Service is responsible for bootstrapping the Connectors, Event Storage and ThingsBoard Client. This Service collects and periodically reports statistics to ThingsBoard about incoming messages and connected devices. Gateway Service persists list of connected devices to be able to re-subscribe to device configuration updates in case of the restart of the gateway.

### [ThingsBoard](https://thingsboard.io/docs/getting-started-guides/what-is-thingsboard/)

ThingsBoard is an open-source IoT platform that enables rapid development, management, and scaling of IoT projects. Our goal is to provide the out-of-the-box IoT cloud or on-premises solution that will enable server-side infrastructure for your IoT applications.
#### Features

With ThingsBoard, you are able to:

- Provision devices, assets and customers, and define relations between them.
- Collect and visualize data from devices and assets.
- Analyze incoming telemetry and trigger alarms with complex event processing.
- Control your devices using remote procedure calls (RPC).
- Build work-flows based on a device life-cycle event, REST API event, RPC request, etc.
- Design dynamic and responsive dashboards and present device or asset telemetry and insights to your customers.
- Enable use-case specific features using customizable rule chains.
- Push device data to other systems.

#### Architecture

ThingsBoard is designed to be:

- scalable: the horizontally scalable platform, built using leading open-source technologies.
- fault-tolerant: no single-point-of-failure, every node in the cluster is identical.
- robust and efficient: a single server node can handle tens or even hundreds of thousands of devices, depending on the use-case. ThingsBoard cluster can handle millions of devices.
- customizable: adding new functionality is easy with customizable widgets and rule engine nodes.
- durable: never lose your data.

## Prerequisites
- `Docker`
- `git clone https://github.com/AntoMars14/TBDM-CPS-Analysis`

## Installation & Configuration
### Kafka
For Windows user, before starting, you need to replace the paths in row 76 and 77 with the absolute path of the folders `connect-kafka-jars` and `connect-kafka-temp`.

- Go into the directory docker-compose:
  
  ```
  cd docker-compose
  ```

- Start up Kafka:
  
  ```
  docker-compose up
  ```

For further information: [Kafka installation guide (using docker)](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/)
#### First approach (using csv file as producer):
The jar files of the plugin Spooldir Source are already present in this repository, so you don't need to download the plugin.

- Import in postman the postman collection `KafkaSpoolirSourceConnector.postman_collection.json` present into the folder `docker-compose`

- Create into `docker-compose/connect-kafka-temp` two folders: `error-csv` and `finished-csv` (folder that will contain the processed csv files).

- Check if Spooldir Source connector is available:

  send the request `connector-plugins`

- Send the Spooldir Source connector configuration for our csv file (the configuration is customized for this specific project):

  send the request `post_spooldir_source` (change localhost in the request with your kafka ip address)

It is also possible to verify the status of the Spooldir connector sending the request `connector_spooldir_status`, and delete our Spooldir Source connector configuration for our csv file sending the request `del_file_spooldir_source`. With the request `connector` is possible to get the list of the running connectors.

For further informations: [Spooldir Source Connector Documentation](https://docs.confluent.io/kafka-connectors/spooldir/current/connectors/csv_source_connector.html#spooldir-csv-source-connector)

#### Second approach (using IoT Simulator as producer):

### ThingsBoard 
Windows users should use docker managed volume for ThingsBoard Database. Create docker volume (for ex. mytb-data) before executing docker run command: Open “Docker Quickstart Terminal”. Execute the following command to create docker volume:

```
docker volume create mytb-data

docker volume create mytb-logs
```

- Go into the directory `docker-compose-thingsboard` (from the root of the project):
  
  ```
  cd docker-compose-thingsboard
  ```

- Start up ThingsBoard:
  
  ```
  docker-compose up
  ```

- To stop the container:

  ```
  docker compose stop mytb
  ```

- To start the container (after stopping it):

  ```
  docker compose start mytb
  ```

For further information: [Thingsboard installation guide (using docker)](https://thingsboard.io/docs/user-guide/install/docker-windows/)

### ThingsBoard IoT Gateway
- Use
  
- Go into ThingsBoard gateways and select Gateway, then click on launch command and download the configuration file.
  
- Go into the directory `docker-compose-thingsboard/iot-gateway` (from the root of the project):
  
  ```
  cd docker-compose-thingsboard/iot-gateway
  ```
  
- Copy the accessToken from the downloaded configuration file, and paste it into the `docker-compose` file in the current folder(at row 26, substituting the one present)

- Start up ThingsBoard:
  
  ```
  docker-compose up
  ```

For further information: [Thingsboard IoT Gateway installation guide (using docker)](https://thingsboard.io/docs/iot-gateway/install/docker-windows/)
#### Add custom connector for Kafka in ThingsBoard IoT Gateway
- Access to a bash shell into the container of the IoT Gateway:
  
  ```
  docker exec -it tb-gateway bash
  ```

- Install `kafka-python` library in the IoT Gateway (required for the implementation of the custom kafka connector):

  ```
  pip install kafka-python
  ```

- Install `pytz` library in the IoT Gateway (required for the implementation of the custom kafka connector):

  ```
  pip install pytz
  ```

- Go into the directory `thingsboard_gateway/config`:
  
  ```
  cd thingsboard_gateway/config
  ```

- Create the kafka connector configuration file:
  
  ```
  touch custom_kafka.json
  ```

- Edit the file:
    
  ```
  nano custom_kafka.json
  ```
  copying and pasting the code from the file `custom_kafka.json` present in the folder `docker-compose-thingsboard/iot-gateway`.

- Add the custom connector to the IoT Gateway editing the file `tb_gateway.json`:
    
  ```
  nano tb_gateway.json
  ```
  copying and pasting the code from the file `tb_gateway-connectors.json` present in the folder `docker-compose-thingsboard/iot-gateway`, into the field connectors of the file.

- Return to the root
- - Go into the directory `thingsboard_gateway/extensions`:
  
  ```
  cd thingsboard_gateway/config
  ```

- Create the kafka connector folder:
  
  ```
  mkdir kafka
  ```

- Create the kafka connector implementation and converter files:
  
  ```
  touch custom_kafka_connector.py
  touch custom_kafka_converter.py
  ```
  
- Edit the files:
    
  ```
  nano custom_kafka_connector.py
  ```

  ```
  nano custom_kafka_converter.py
  ```
  copying and pasting the code respectively from the files `custom_kafka_connector.py` and `custom_kafka_converter.py` present in the folder `docker-compose-thingsboard/iot-gateway`.

- To apply the changes, activating the custom kafka connector, stop and restart the IoT Gateway:

  ```
  docker compose stop tb-gateway
  ```
  
  ```
  docker compose start tb-gateway
  ```

For further information: [Thingsboard IoT Gateway configuration guide](https://thingsboard.io/docs/iot-gateway/getting-started/) and [IoT Gateway Customization (custom connector)](https://thingsboard.io/docs/iot-gateway/custom/serial-connector/)
## Usage
## Results
