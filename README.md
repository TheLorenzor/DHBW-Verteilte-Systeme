# Matrikelnummern

* 5470239
* 2447899
* 1360712

# Aufgabe 1

## a)

**Welches Pattern aus der Softwareentwicklung fällt Ihnen zu den Grundprinzipien von MQTT ein?**

Publish-Subscribe-Pattern

**Wie kann ich beispielsweise alle Topics unter `/weather` abonnieren?**

1. In den Ordner wechseln wo Mosquito installiert ist
2. Mit der Kommandozeil im Ordner öffnen
3. `mosquitto_sub.exe -h 10.50.12.150 -v -t /weather/#` in die Konsole eingeben
4. dadurch werden alle Wetterdaten (Stuttgart, Mergentheim, Mosbach) gepullt

**Was ist der "Last Will"?**

Die Clients werden regelmäßig von MQTT Message Broker abgefragt, oib diese noch online sind. Wenn diese nicht mehr
online sind und unerwartet vom Internet getrennt wurden, schickt der Message Broker den Last Will des jeweiligen
Clients. Dies ist eine beliebige Nachricht. Wenn der Client normal Disconnected wird der Last Will entsprechend
gelöscht.

**Was sind die wichtigsten zwischedn MQTT v3 und v5?**

Unterschiede:

| MQTT v.3                                                     | MQTT v.5                                            | 
|--------------------------------------------------------------|-----------------------------------------------------|
| Standartisiert in ISO/IEC 20922:2016 / Erster OASIS Standard | keine ISO Standardisierung                          |
| unterstützt Backward Kompatibilität                          | keine Backward Kompatibilität                       |
| limitierte Funktionalität                                    | viele neue Funktionen                               |
| Disconnect darf nur von Clioentseite aus kommen              | Disconnect darf auch von Serverseite gegeben werden |
| Server hat keine Informationen darüber was schief lief       | Server gibt Errorcodes zurück + ACK Nachrichten     |

## b)

**Wie können Sie alle Topics abonnieren, auch ohne diese alle im Vorraus zu kennen?**

* Mit `-t /#` werden alle Topics abonniert --> unser Beispiel: `mosquitto_sub.exe -v -h 10.50.12.150 -t /#`

**Welche Topics und Werte können Sie sehen?**

* `/weather/mergentheim` {"tempCurrent":.670013,"tempMax":11.119995,"tempMin":8.75,"comment":"Publ.Id 261118","
  timeStamp":"2023-04-11T08:37:06.063+00:00","city":"Bad Mergentheim","cityId":2953402}
* `/weather/stuttgart` {"tempCurrent":9.779999,"tempMax":11.029999,"tempMin":8.670013,"comment":"Publ.Id 261118","
  timeStamp":"2023-04-11T08:36:06.055+00:00","city":"Stuttgart","cityId":2825297}
* `/weather/mosbach` {"tempCurrent":10.959991,"tempMax":11.959991,"tempMin":9.480011,"comment":"Publ.Id 261118","
  timeStamp":"2023-04-11T08:36:36.029+00:00","city":"Mosbach","cityId":2869120}
* `/siemens/1200CPU/OPC/iRcv1` +13333
* `/siemens/1200CPU/OPC/sRcv` Hallo ET20B ;-))
* `/siemens/1200CPU/Time` S7-1200 Time: +9h +39min +16sec
* `/siemens/1200CPU/Poti` +16996
* `/siemens/1200CPU/IO` +0

**Wie können Sie ein bestimmtes Topic abonnieren, z.B. das Wetter für Mosbach?**

1. In den Ordner wechseln wo Mosquito installiert ist
2. Mit der Kommandozeil im Ordner öffnen
3. `mosquitto_sub.exe -h 10.50.12.150 -v -t /weather/mosbach` in die Konsole eingeben

**In welchem Datenformat werden die Wetterdaten bereitgestellt?**

* JSON Format:

| JSON-Key    | Type     |
|-------------|----------|
| tempCurrent | number   |
| tempMax     | number   |
| tempMin     | number   |
| comment     | string   |
| timeStamp   | DateTime |
| city        | string   |
| cityId      | number   |

# Aufgabe 2

## a)

**Was sind Gemeinsamkeiten und Unterschiede zwischen Kafka und MQTT-Brokern**

| Gemeinsamkeiten                          | Unterschiede                                                                          |
|------------------------------------------|---------------------------------------------------------------------------------------|
| haben beide ein Publish subscribe Modell | MQTT ist für generelle Daten, Kafka ist fürs rum schaufeln großer Daten               |
| Sind eine Client-Server Architekture     | Kann zusätzlich daten abspeichern auf platte und processen --> MQTT leitet nur weiter |
| kann zu mehreren Topics subscriben       | unterschiedliche Familien von Brokern                                                 |
 | -                                        | MQTT ist Protokoll, Kafka ist Serverimplementierung                                   |
| -                                        | Kafka ist für High Volume low Value Daten zuständig                                   |

**Für welche Szenarien ist Kafka besser geeignet**
- für massive Datentransfer
- Batch Processing
- Abspeichern vieler Daten

**Man findet bei Vergleichen öfters die Aussage, Kafka würde das Modell “Dumb Broker / Smart Consumer” implementieren, während bei MQTT “Smart broker / Dumb Consumer” gilt. Was ist damit gemeint? Was muss ein Kafka-Consumer beachten?**
- im gegensatz zu RAbbitMQ registriert Kafka nicht welche Nachrichten durch Clients gelesen wurden
- Kafka hält nachrichten für gewisse Länge vor und löscht diese nicht

Kafka Consumer muss beachten:
- regelmäßig abfragen
- Consumer muss daten lesen 

**Was sind Partitionen? Für was kann man sie neben Load-Balancing noch verwenden?**
-  Ein Topic ist unterteilt in viele partitionen
- Eine Partition ist das kleinste Set an Daten die in einem Topic vorhanden sind
- Für Load balancing ist gut -> kann die Topics horizontal skalieren indem verschiedene Broker
gleichzeitig eine Partition schicken und diese beim Consumer alle auf einmal ankommen
- ein einzelnes Topic can dadurch von mehreren Consumern gelesen werden
- hoher Message Throuput
- durch Partition redundanz gegeben -> mehr als eine Partitino wird vorgehalten

## c
**Wozu dienen Key und Value beim Versenden von Kafka-Messages?**
- nutzen für Partitionen 
- keys genutzt um zu entscheiden innerhalb des Logs welche Partition wohin angefügt wurde
- Keys are used to determine the partition within a log to which a message get's appended to. While the value is the actual payload of the message
- Erhalt Nachrichtenreihenfolge

# Aufgabe 3
## a

**Wie sind die Daten organisiert**

**Was muss beachtet werden wenn maximal 10 Consumer**

**Partition mind. nötig?**

**Wann eignet sich standalone customer**