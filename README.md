# Fire In The Hole!

* This project aims to automate an alert system to help families keep safe and constantly monitor by providing a Home automation solution by employing IoT based approach to automate the monitoring effort and alerting people to reduce the impact.
* We will use sensor to measure heat(temperature and smoke) in an area and feed it to gateway device which pushes data to cloud for analytics and data to edge device which controls alert system.


## Design Overview
* Topology: -Hub & Spoke is used since our design is for Home environment.
Hub & Spoke is used because we are doing most of the processing locally and just having remote cloud for analytics(* Future Scope)
* Overhead is placed on Server (CoAP Protocol) which handles the data and forward to edge device & cloud service using MQTT protocol
* Cloud Service : Ubidots Cloud is used to capture the data and store in its DB.
Smart Lighting System (SLS) Yogesh Suresh
* Edge Tier : Actuation(MQTT Subscriber) & Sensing(CoAP Client) comes in this tier
* Gateway Tier : CoAP server & MQTT publisher (cloud ,Actuator) for sits here
