from random import randint

class DC_Net:
    def __init__(self):
        self.clients: list[DC_Client] = []
        self.checksums: dict[str, int] = {}
    
    def add_client(self, new_name: str):
        new_client = DC_Client(new_name)
        self.process_new_client(new_client)

    def add_violent_client(self, new_name: str):
        new_client = DC_Client_Violent(new_name)
        self.process_new_client(new_client)

    def process_new_client(self, new_client):
        self.clients.append(new_client)
        new_number = len(self.clients) - 1
        new_client.checksums = self.checksums
        
        for i in range(len(self.clients)):
            if i != new_number:
                self.clients[i].adapters[new_client.name] = NetworkAdapter(self.clients[i], new_client)
                new_client.adapters[self.clients[i].name] = NetworkAdapter(new_client, self.clients[i])
    
    def add_checksum(self, filename, sum):
        self.checksums[filename] = sum
        for client in self.clients:
            client.checksums[filename] = sum

max_length = 64

def random_key():
    return randint(1 << (max_length - 2), 1 << (max_length - 1))

def ordstr(string: str):
    return 0 if len(string) == 0 else (ord(string) if len(string) == 1 else (ord(string[0]) << 8 * (len(string) - 1)) | ordstr(string[1:]))

def chrstr(number: int):
    return chr(number) if number < 256 else chrstr(number // 256) + chr(number % 256)

def fastpow(a, b, p):
    if b <= 1:
        return a % p
    if b & 1 == 0:
        return fastpow((a * a) % p, b // 2, p)
    return (a * fastpow((a * a) % p, b // 2, p)) % p

def checksum(file: str):
    res = 0
    for let in file:
        res ^= ord(let)
    return res

class DC_Client:
    def __init__(self, name):
        self.name = name
        self.adapters: dict[str, NetworkAdapter] = {}
        self.files: dict[str, str] = {}
        self.keys: dict[str, int] = {}
        self.keys_kits: dict[str, tuple] = {}
        self.file: int = 0
        self.checksums: dict[str, int] = {}

    def add_file(self, name: str, content):
        if len(content) > max_length:
            raise ValueError()
        self.files[name] = content

    def recieve(self, source, content: str):
        if ';' in content:
            head, content = content.split(';')
        else:
            head = content[:]
            content = ''
        ret = self.adapters[source.name]
        if head == 'dh:1':
            g, p, g_a = map(int, content.split(','))
            b = random_key()
            g_b = fastpow(g,b,p)
            g_ab = fastpow(g_a, b, p)
            self.keys[source.name] = g_ab
            ret.transfer(f'dh:2;{g_b}')
        elif head == 'dh:2':
            g_b = int(content)
            g, p, a = self.keys_kits[source.name]
            g_ab = fastpow(g_b, a, p)
            self.keys[source.name] = g_ab
            del self.keys_kits[source.name]
        elif head == 'dh:rem':
            self.keys = {}
        elif head == 'dh:all':
            for dest in self.adapters.keys():
                if dest not in self.keys:
                    self.do_dh(dest)
        elif head == 'dc:filereq':
            ret.transfer(f'dc:fileres;{self.dcfilereq(content, ret)}')
        elif head == 'dc:fileres':
            file = content
            self.file ^= ordstr(file)

    def dcfilereq(self, content, ret):
        filename = content
        xor = 0
        for dest in self.keys:
            xor ^= self.keys[dest]
        if filename in self.files:
            xor ^= ordstr(self.files[filename])
        return chrstr(xor)

    def do_dh(self, dest: str):
        adapter: NetworkAdapter = self.adapters[dest]
        g, p, a = random_key(), random_key(), random_key()
        g_a = fastpow(g,a,p)
        self.keys_kits[dest] = (g, p, a)
        adapter.transfer(f'dh:1;{g},{p},{g_a}')

    def request_file(self, name) -> str:
        destinations = list(self.adapters.keys())
        for dest in destinations:
            self.adapters[dest].transfer('dh:rem')
        for dest in destinations:
            self.adapters[dest].transfer('dh:all')
        self.file = 0 if name not in self.files else ordstr(self.files[name])
        for dest in destinations:
            self.file ^= self.keys[dest]
            self.adapters[dest].transfer(f'dc:filereq;{name}')

        if checksum(chrstr(self.file)) != self.checksums[name]:
            raise ValueError()
        return chrstr(self.file)

class NetworkAdapter:
    def __init__(self, client_from: DC_Client, client_to: DC_Client):
        self.client_from: DC_Client = client_from
        self.client_to: DC_Client = client_to

    def transfer(self, content):
        #with open('logs.txt', '+a') as file:
        #    file.write(f'{self.client_from.name} ===> {self.client_to} : "{content}"')
        print(f'{self.client_from.name} ===> {self.client_to.name} : "{content}"')
        self.client_to.recieve(self.client_from, content)

class DC_Client_Violent(DC_Client):
    def dcfilereq(self, content, ret):
        return chrstr(ordstr(super().dcfilereq(content, ret)) ^ ordstr('mistake'))