import hashlib


class Block:
    '''Represents a block of the blockchain'''


    # slots with the class' properties. This will save memory ;)
    __slots__ = ('_data', '_previous_hash', '_time_stamp', '_nonce',  '_hash')


    def __init__(self, data, previous_hash: str, time_stamp: float):
        '''Constructor'''

        self._data = data
        self._previous_hash = previous_hash
        self._time_stamp = int(time_stamp)
        self._nonce = 0
        self._hash = self.calculate_hash()


    @property
    def data(self):
        '''Gets the data of the block.'''
        return self._data


    @property
    def previous_hash(self) -> str:
        '''Gets the previous hash.'''
        return self._previous_hash


    @property
    def time_stamp(self) -> float:
        '''Gets the timestamp of the block.'''
        return self._time_stamp

    
    @property
    def hash(self) -> str:
        '''Gets the hash of the block.'''
        return self._hash


    @property
    def nonce(self) -> int:
        '''Gest the nunce value.'''
        return self._nonce


    def is_hash_valid(self, prefix: int) -> bool:
        prefix_str = '0' * prefix
        return self.hash[:prefix] == prefix_str


    def mine(self, prefix: int) -> str:
        '''Do the mine process of the block and returns the correct hash.'''
        prefix_str = '0' * prefix
        while not self.hash[:prefix] == prefix_str:
            self._nonce += 1
            self._hash = self.calculate_hash()
        return hash


    def calculate_hash(self) -> str:
        '''Calculates the hash of the block'''
        str_to_hash = (self.previous_hash or '') + str(self.time_stamp) + str(self.nonce) + self.data.hash()
        bytes_to_hash = bytes(str_to_hash, 'utf-8')
        return hashlib.sha256(bytes_to_hash).hexdigest().upper()


    def is_data_valid(self) -> bool:
        return self.hash == self.calculate_hash()


class Data:
    __slots__ = ('_content', '_hash')
    @property 
    def content(self): pass
    def hash(self) -> str: pass


class StrData(Data):
    '''Represents a String data of the Block'''


    __slots__ = ()


    def __init__(self, content: str):
        '''Constructor.'''
        self._content = content


    @property
    def content(self) -> str:
        '''The Data Content.'''
        return self._content


    def hash(self) -> str:
        '''Gets the hash of the data.'''
        return hashlib.sha256(bytes(self.content, 'utf-8')).hexdigest().upper()


    def __str__(self):
        return str(self.content)
