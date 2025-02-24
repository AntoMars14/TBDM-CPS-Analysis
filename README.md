# TBDM-CPS-Analysis

## Table of contents:
1. [Introduction](#introduction)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Installation & Configuration](#installation--configuration)
   
   I. [Kafka](#kafka)
   
      1. [Csv File](#csv-file)
   
      2. [IoT-Simulator](#iot-simulator)
   
   II. [ThingsBoard](#thingsboard)
   
   III. [ThingsBoard IoT Gateway](#thingsboard-iot-gateway)
6. [Usage](#usage)
7. [Results](#results)




## Introduction
In the optimization of a dewatering CPS machine, several sensor are used to collect real-time data. This project is about the analysis of a Cyber-Physical System (CPS) data using Big Data Technologies. The objectives of this project are to study an IoT platform for handling the data of the CPS, to study the framework (ThingsBoard), its features, dashboard and alarms.

This project implements a Big Data system that analyze the data in real-time. The data are published in Kafka using the following 2 different approaches.
#### First approach:
Uses a Spooldir connector to read data from a csv file and publish them in Kafka.
#### Second approach:
Uses an IoT-Simulator to generate data and publish them in Kafka.

Then the data are read(consumed) by the (subscriber) Thingsboard IoT Gateway, using a custom plug-in, and are sent to Thingsboard. In Thingsboard the data are visualized using charts and other visual representation into a dashboard. Alarms have also been implemented in Thingsboard and they can be monitored from the dashbord.

The system architecture is depicted in the following figure

![Architecture](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/Architecture.png?raw=true)

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

![thingsboardiotgateway](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboardiotgateway.png?raw=true)

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

![thingsboardarchitecture](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboardarchitecture.png?raw=true)

ThingsBoard is designed to be:

- scalable: the horizontally scalable platform, built using leading open-source technologies.
- fault-tolerant: no single-point-of-failure, every node in the cluster is identical.
- robust and efficient: a single server node can handle tens or even hundreds of thousands of devices, depending on the use-case. ThingsBoard cluster can handle millions of devices.
- customizable: adding new functionality is easy with customizable widgets and rule engine nodes.
- durable: never lose your data.

### [IoT-Simulator](https://github.com/massimocallisto/iot-simulator)

IoT data simulator that generates data in real-time.

#### Architecture
The Generator has the following basic architecture:

- `JsonDataGenerator` - The main application that loads configurations and runs simulations.
- `Simulation Configuration` - A json file that represents your over all simulation you would like to run.
- `Workflow Definitions` - Json files that define a workflow that is run by your Simulation.

When you start the JsonDataGenerator, you specify your Simulation Configuration which also references one or many Workflow Definitions. The Simulation is loaded and the Workflows are created within the application and each workflow is started within its own thread. Json events are generated and sent to the defined Producers.

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

Kafka web-application user interface is available at http://localhost:7777.

For further information: [Kafka installation guide (using docker)](https://developer.confluent.io/confluent-tutorials/kafka-on-docker/)
#### Csv File:

#### First approach using csv file as producer

The jar files of the plugin Spooldir Source are already present in this repository, so you don't need to download the plugin.

- Import in postman the postman collection `KafkaSpoolirSourceConnector.postman_collection.json` present into the folder `docker-compose`

- Create into `docker-compose/connect-kafka-temp` two folders: `error-csv` and `finished-csv` (folder that will contain the processed csv files).

- Check if Spooldir Source connector is available:

  send the request `connector-plugins`

For further informations: [Spooldir Source Connector Documentation](https://docs.confluent.io/kafka-connectors/spooldir/current/connectors/csv_source_connector.html#spooldir-csv-source-connector)

#### IoT-Simulator:

#### Second approach using the iot-simulator as producer

The IoT-Simulator is customized, some custom function was added:

- integerString
- doubleString
- LongString
- randomIncrementDouble
- randomIncrementDoubleString
- randomIncrementLongString
  
The configuration files are present into the folder `docker-compose/conf`. The `simple_Simulator.json` is the simulation configuration file and the `cpsWorkflow.json` is the workflow configuration file.

For further informations: [IoT-Simulator Documentation](https://github.com/massimocallisto/iot-simulator/blob/master/README.md)

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

For further information: [Thingsboard installation guide (using docker)](https://thingsboard.io/docs/user-guide/install/docker-windows/)
#### Access to thingsboard ui

The web-application user interface is available at http://localhost:8080 and these are the default credentials:

- System Administrator: sysadmin@thingsboard.org - password: sysadmin
    
- Tenant Administrator: tenant@thingsboard.org - password: tenant
    
- Customer User: customer@thingsboard.org - password: customer

#### Configure version control in thingsboard and import entities

Login as the tenant administrator, go to 'Advanced features', then 'Version control', and put this repository URL and the main branch into the configuration configs. 
You can flag 'Read-only' and skip the authentication settings, if you want only to import the data without commiting your modifications.

Click 'Check access' to check the successful verification of the repository. Save your repository settings.

![versioncontrol](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/versioncontrol.png?raw=true)

From the commit list, click the 'Restore version' button and choose entities to restore, by default they're all selected(advised), and restore them.

![versioncontrolrestore](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/versioncontrolrestore.png?raw=true)

For further information: [Version Control](https://thingsboard.io/docs/user-guide/version-control/)

### ThingsBoard IoT Gateway
After have restored all the entities you can start the iot gateway and configure it.
  
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

### Kafka

- Go into the directory docker-compose:
  
  ```
  cd docker-compose
  ```

- Start up Kafka:
  
  ```
  docker-compose up
  ```
  
Kafka is now active.
  
- To stop Kafka:
  
  ```
  docker stop
  ```

#### First approach: Csv File (SpoolDir Connector)
To start reading the csv file and publish the data on Kafka do the following step.

- Send the Spooldir Source connector configuration for our csv file (the configuration is customized for this specific project):

  send the request `post_spooldir_source` (change localhost in the request with your kafka ip address)

It is also possible to verify the status of the Spooldir connector sending the request `connector_spooldir_status`, and delete our Spooldir Source connector configuration for our csv file sending the request `del_file_spooldir_source`. With the request `connector` is possible to get the list of the running connectors.

#### Second approach: IoT-Simulator

Start the IoT-Simulator container do the following steps.

- Go into the directory `docker-compose` (from the root of the project):
  
  ```
  cd docker-compose
  ```

- Start up the container iotsimulator:
  
  ```
  docker compose --profile iotsimulator up
  ```
The iot-simulator will start to produce data an to publish them in Kafka.


- To stop simulator container:
  
  ```
  docker stop simulator
  ```

### ThingsBoard

To start thingsboard container do the following steps.

- Go into the directory `docker-compose-thingsboard` (from the root of the project):
  
  ```
  cd docker-compose-thingsboard
  ```

- Start up ThingsBoard:
  
  ```
  docker-compose up
  ```

Thingsboard is now active.

- To stop the container:

  ```
  docker compose stop mytb
  ```

- To start the container (after stopping it):

  ```
  docker compose start mytb
  ```

#### Create dashboard

In thingsboard is possible to create dashboard to visualize the data. In a dashboard you can add widgets that can be charts, cards, alarm widgets, etc.

- To create a dashboard go to dashboard page, select + and create new dashboard.

![createdashboard](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/createdashboard.png?raw=true)

- Fill the fields and confirm the creation.

#### Add widget to the dashboard
- Select the created dashboard, and click on edit.

- Select add widget and choose the widget bundle and the widget to add to the dashboard.
  
![thingsboarddashboardaddwidget](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboarddashboardaddwidget.png?raw=true)

- Configure the widget adding the datasource, the key and all the other optional settings.

![thingsboarddashboardwidgetconf](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboarddashboardwidgetconf.png?raw=true)

For further information: [Dashboard Usage](https://thingsboard.io/docs/user-guide/dashboards/)

#### Add an alarm

In thingsboard is also possible to add alarms (alarm rules) to a specific device profile and visualize them into the dashboard.

- To add an alarm rule, go into the device profile page and select the profile associated with your device. in our case the profile associated with the CPS device is default.

![deviceprofiles](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/deviceprofiles.png?raw=true)

- Then click on alarm rules, add your alarm condition and save clicking on add alarm rule.

![alarmcondition](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/alarmcondition.png?raw=true)


For further information: [Alarm Usage](https://thingsboard.io/docs/user-guide/alarms/)

### ThingsBoard IoT-Gateway

To start thingsboard iot-gateway container do the following steps.

- Go into the directory `docker-compose-thingsboard/iot-gateway` (from the root of the project):
  
  ```
  cd docker-compose-thingsboard/iot-gateway
  ```
  
- Start up ThingsBoard IoT-Gateway:
  
  ```
  docker-compose up
  ```
  
The iot-gateway is now active.

- To stop and restart the IoT Gateway:

  ```
  docker compose stop tb-gateway
  ```
  
  ```
  docker compose start tb-gateway
  ```
## Results

The project objectives are met. The data produced by the iot-simulator or extracted from the csv file is published on kafka. Then the thingsboard iot-gateway reads and consumes data from kafka and forwards it to thingsboard. In thingsboard we managed the visualization of the data in the dashboard and the alarms.

In the following images of this section are present the dashboard realized for this project to analyze the data from the CPS device and the alarms visualized into the dashboard.

### Dashboard

In the following 2 figures are present all the widget used to visualize the data form the CPS device. The main widget used are time series charts, line charts, point charts, cards and card charts.
![thingsboarddashboard](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboarddashboard.png?raw=true)

![thingsboarddashboard1](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboarddashboard1.png?raw=true)

In the following figure are visible the widget used into the dashboard to monitor the alarms.

![thingsboarddashboardalarms](https://github.com/AntoMars14/TBDM-CPS-Analysis/blob/images/thingsboarddashboardalarms.png?raw=true)

### Alarms
