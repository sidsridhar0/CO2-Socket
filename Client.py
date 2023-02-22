import json
import socket
import Server
import Graphics
import tkinter as tk
import UI


def client_program(portnumber):
    print("Hi")
    host = socket.gethostname()
    port = portnumber
    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_socket.send("State".encode())

    ind = json.loads(client_socket.recv(1024).decode())
    state = None
    root = tk.Tk()
    app = UI.StateSelector(master=root)
    while True:
        selected_state = None
        if app.selected_state is not None:
            state = app.selected_state
            app.selected_state = None
        try:
            app.update()
        except tk.TclError:
            break
        client_socket.send(state.encode())
        data = json.loads(client_socket.recv(1024).decode())
        #print(ind)
        print(data)
        # temp = Graphic(ind, data)
        # temp.makeGraphic()

    client_socket.close()


# db = Server.setupDB()
# Server.server_program(5000, db)
client_program(5000)
# db.query_builder("close")
# db.query_builder("deleteDB")
