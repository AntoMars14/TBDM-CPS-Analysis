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
## Prerequisites
## Installation & Configuration
## Usage
## Results
