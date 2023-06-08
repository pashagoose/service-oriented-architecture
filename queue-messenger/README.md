# Простой текстовый мессенджер поверх RabbitMQ на Go

CLI утилита, есть 2 функции:
* Отправить текстовое сообщение в чат с определенным названием
* Начать слушать сообщения из чата с определенным названием

Сообщение корректно рассылаются каждому получателю. Под капотом для каждого чата заводится exchange, в режиме fanout - то есть он разрабрасывает сообщения во все очереди, которые к нему привязаны. На старте приложения создается временная очередь с уникальным названием, которая привязывается к exchange с названием чата.

[Video Demo](https://youtu.be/LShosjPH1qs)

```console
^^/C/s/queue-messenger >>> go run cmd.go --help                                                                                                                                    (main+12) 16:30:22 
Connect to chat and emit or listen messages

Usage:
  messenger [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  help        Help about any command
  listen      Listen messages from selected chat
  send        Send message to selected chat

Flags:
  -h, --help          help for messenger
      --host string   Rabbit mq broker host (default "localhost")
      --pass string   Rabbit mq user password (default "guest")
  -p, --port uint32   Rabbit mq port to connect to (default 5672)
  -u, --user string   Rabbit mq user (default "guest")

Use "messenger [command] --help" for more information about a command.
```

