package main

import (
	"context"
	"fmt"
	"log"
	"os"

	amqp "github.com/rabbitmq/amqp091-go"
	"github.com/spf13/cobra"
)

type (
	ChatChannel struct {
		Channel  *amqp.Channel
		ChatName string
		Queue    *amqp.Queue
	}
)

func NewChatChannel(chatName string, conn *amqp.Connection) (*ChatChannel, error) {
	ch, err := conn.Channel()
	if err != nil {
		return nil, err
	}

	queue, err := ch.QueueDeclare("", true, false, false, false, nil)
	if err != nil {
		return nil, err
	}

	err = ch.ExchangeDeclare(chatName, "fanout", true, false, false, false, nil)
	if err != nil {
		return nil, err
	}

	err = ch.QueueBind(queue.Name, "", chatName, false, nil)
	if err != nil {
		return nil, err
	}

	return &ChatChannel{Channel: ch, ChatName: chatName, Queue: &queue}, nil
}

func (c *ChatChannel) SendMessage(text string) error {
	return c.Channel.PublishWithContext(
		context.Background(),
		c.ChatName,
		"",
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(text),
		},
	)
}

func (c *ChatChannel) ListenMessages() error {
	msgs, err := c.Channel.Consume(
		c.Queue.Name, // queue
		"",           // consumer
		true,         // auto-ack
		false,        // exclusive
		false,        // no-local
		false,        // no-wait
		nil,          // args
	)
	if err != nil {
		return err
	}

	for d := range msgs {
		log.Printf("Received a message: `%s`", d.Body)
	}

	return nil
}

func (c *ChatChannel) Close() error {
	return c.Channel.Close()
}

var (
	rootCmd = &cobra.Command{
		Use:           "messenger",
		Short:         "Connect to chat and emit or listen messages",
		SilenceUsage:  true,
		SilenceErrors: true,
	}

	brokerHost     string
	brokerPort     *uint32
	brokerUser     string
	brokerPassword string

	sendMessageCmd = &cobra.Command{
		Use:   "send <chat_name> <message_text>",
		Short: "Send message to selected chat",
		RunE: func(_ *cobra.Command, args []string) error {
			conn, err := amqp.Dial(
				fmt.Sprintf(
					"amqp://%s:%s@%s:%d/",
					brokerUser,
					brokerPassword,
					brokerHost,
					*brokerPort,
				),
			)

			if err != nil {
				return err
			}

			chatChannel, err := NewChatChannel(args[0], conn)
			if err != nil {
				return err
			}
			defer chatChannel.Close()

			err = chatChannel.SendMessage(args[1])
			if err != nil {
				return err
			}

			log.Printf("Successfully sent message: `%s` to queue `%s`", args[1], args[0])

			return err
		},
	}

	listenMessagesCmd = &cobra.Command{
		Use:   "listen <chat_name>",
		Short: "Listen messages from selected chat",
		RunE: func(_ *cobra.Command, args []string) error {
			conn, err := amqp.Dial(
				fmt.Sprintf(
					"amqp://%s:%s@%s:%d/",
					brokerUser,
					brokerPassword,
					brokerHost,
					*brokerPort,
				),
			)

			if err != nil {
				return err
			}

			chatChannel, err := NewChatChannel(args[0], conn)
			if err != nil {
				return err
			}
			defer chatChannel.Close()

			return chatChannel.ListenMessages()
		},
	}
)

func init() {
	rootCmd.Flags().StringVar(&brokerHost, "host", "localhost", "Rabbit mq broker host")
	brokerPort = rootCmd.Flags().Uint32P("port", "p", 5672, "Rabbit mq port to connect to")
	rootCmd.Flags().StringVarP(&brokerUser, "user", "u", "guest", "Rabbit mq user")
	rootCmd.Flags().StringVar(&brokerPassword, "pass", "guest", "Rabbit mq user password")

	rootCmd.AddCommand(sendMessageCmd)
	rootCmd.AddCommand(listenMessagesCmd)
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func main() {
	Execute()
}
