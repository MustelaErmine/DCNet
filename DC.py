class DC_Net:
    def __init__(self):
        self.clients: list[DC_Client] = []
    
    def add_client(self, name: str):
        new_client = DC_Client(name)
        self.clients.append(new_number)
        new_number = len(self.clients) - 1
        
        for i in range(len(self.clients)):
            self.clients[i].adapters[name] = NetworkAdapter(self.clients[i], new_client)
            new_client.adapters[self.clients[i].name] = NetworkAdapter(new_client, self.clients[i])

class DC_Client:
    def __init__(self, name):
        self.name = name
        self.adapters: dict[str, NetworkAdapter] = {}
        self.files: dict[str, str] = {}

    def add_file(self, name: str, content):
        self.files[name] = content

    def recieve(self, source, content):
        pass

    def request_file(self, name) -> str:
        pass

class NetworkAdapter:
    def __init__(self, client_from: DC_Client, client_to: DC_Client):
        self.client_from: DC_Client = client_from
        self.client_to: DC_Client = client_to

    def tranfer(self, content):
        with open('logs.txt', '+a') as file:
            file.write(f'{self.client_from.name} ===> {self.client_to} : "{content}"')
        self.client_to.recieve(self.client_from, content)