from time import sleep

import bluetooth
import socket
import proxy

# bluetooth server initialization
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

# TODO allow multiple connections
port = server_sock.getsockname()[1]
uuid = "f331dead-1234-4321-9999-785340612afe"

bluetooth.advertise_service(server_sock, "SSH server", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )
print("Waiting for connection on RFCOMM channel", port)


# forward everything
connection = None
while True:
    try:
        print("Waiting for connection")
        # server accept
        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)

        # connect to ssh
        ssh_socket = socket.socket()
        ssh_socket.connect(("127.0.0.1", 8022))

        # create and wait to finish proxy
        connection = proxy.MyConnection(ssh_socket, client_sock)
        connection.start()
        connection.join()
    except KeyboardInterrupt:
        print("Shutting down server")
        if connection is not None:
            connection.stop()
        break



