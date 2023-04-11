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

| MQTT v.3 | MQTT v.5 | 
| --- | --- |
| Standartisiert in ISO/IEC 20922:2016 / Erster OASIS Standard | keine ISO Standardisierung |
| unterstützt Backward Kompatibilität | keine Backward Kompatibilität |

