import pika


class MessageBroker:
    def __init__(self):
        """Create a connection"""
        self.credentials = pika.PlainCredentials("guest", "guest")
        self.connection_params = pika.ConnectionParameters("localhost", 15672)
        self.connection = pika.BlockingConnection(self.connection_params)

    def get_channel(self):
        # Get the channel from the connection params
        return self.connection.channel()

    def close_connection(self):
        # Close the current connection
        self.connection.close()


if __name__ == "__main__":
    # Code inside the block will only be executed if
    # the module is run directly, not if it is imported.
    message_broker = MessageBroker()
    message_broker.get_channel()
    message_broker.close_connection()
