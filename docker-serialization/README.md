# Serialization + docker

## Форматы данных

* JSON
* MessagePack
* Protobuf
* XML
* Pickle (native Python)
* YAML
* Apache Avro

## Структура данных

Тестируемая структура данных описана в файле `src/testing_data/data.py`

## Как работает?

Запускаем отдельный контейнер на каждый формат сериализации, который сначала проводит 100 итераций сериализации и десереализации, замеряя среднее время. Затем запускаем HTTP сервер по указанному порту, отвечающий в ручку `/get_result` в таком формате формате:

```console
>> curl "localhost:9000/get_result"                                               xml-562535-117.169ms-12.699ms⏎
```

Также есть контейнер с прокси, который перенаправляет запросы на соответствующие контейнеры.

```console
>> curl "localhost:2000/get_result?format=xml"                                               xml-562535-117.169ms-12.699ms⏎
```

## Запуск

Из данной директории:

```console
>> docker-compose up
```

## Самостоятельная сборка docker образов

Контейнер с сериализацией:

```console
>> docker build -f serialization_format.dockerfile -t proto_serialization --build-arg FORMAT=proto
```

Контейнер с proxy:

```console
>> docker build -f proxy.dockerfile -t proxy_serialization
```

