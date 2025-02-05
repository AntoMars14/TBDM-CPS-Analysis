# TBDM-CPS-Analysis

## Table of contents:
1. [Introduction](#introduction)
2. [Technologies](#technologies)
3. [Prerequisites](#prerequisites)
4. [Installation & Configuration](#installation--configuration)
5. [Usage](#usage)
6. [Results](#results)




## Introduction
In the optimization of a dewatering CPS machine, several sensor are used to collect real-time data. The project is about the analysis of a Cyber-Physical System (CPS) data using Big Data Technologies.

This project implements a Big Data system that analyze the data in real-time. The data are published in Kafka using 2 different approaches:
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
### Start up Kafka
For Windows user, before starting, you need to replace the paths in row 76 and 77 with the absolute path of the folders connect-kafka-jars and connect-kafka-temp.

The jar files of the plugin Spooldir Source are already present in this repository, so you don't need to download the plugin.

- Go into the directory docker-compose:
  
  `cd docker-compose`

- Start up Kafka:
  
  `docker-compose up`
- Check if Spooldir Source connector is available:

  

###



## Usage
## Results
