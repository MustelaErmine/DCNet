class DC_Net:
    def __init__(self):
        self.clients: list[DC_Client] = []
    
    def add_client(self, name: str):
        self.clients.append(DC_Client(name))
        new_number = len(self.clients) - 1
        
        # todo: add adapters

class DC_Client:
    def __init__(self, name):
        self.name = name
        self.adapters: dict[int, NetworkAdapter] = {}
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
        self.client_to.recieve(self.client_from, content)