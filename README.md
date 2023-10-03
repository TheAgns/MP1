# Mini Project 1: Web Services and Communication Protocols
Our solution consits of the following 4 parts

## 1
Names, mail addresses, and IP addresses of partners are read from a csv file.

## 2
For every entry in the csv file the participants location is found by calling an API at: http://wsgeoip.lavasoft.com/ipservice.asmx
This soap API takes our requests of the following form:
<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <GetIpLocation xmlns="http://lavasoft.com/">
        <sIp>{ip}</sIp>
        </GetIpLocation>
    </soap12:Body>
    </soap12:Envelope>

where {ip} is the ip of the participant. Participants location is extracted from the resulting response.

## 3
https://api.genderize.io?name={name}&country={country} is used to find the gender of the participant from their name and location

## 4
smtplib is used to build the email (message, subject and attachment) and send it to the given participants email.
