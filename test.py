from datetime import datetime
import unittest
from block import Block, StrData


class MainTest(unittest.TestCase):


    # For the blockchain, the proof of work will be the valid hash starting 
    # prefix number of 0. 
    PREFIX = 4
    PREFIX_STR = '0' * PREFIX


    def __init__(self, methodName):
        super().__init__(methodName)


    def setUp(self):
        '''Sets up the test.'''

        # Create the blockchain with the genesis block.
        self.blockchain = []
        genesis_block = self.create_genesis_block()
        self.blockchain.append(genesis_block)


    def tearDown(self):
        self.blockchain = None


    def test_01_genesis(self):
        self.assertTrue(self.blockchain, 'blockchain does not have genesis block' )
        b = self.blockchain[0]
        self.assertIsNotNone(b.hash, 'Hash None')
        self.assertTrue(b.is_hash_valid(MainTest.PREFIX), 'Hash isn\'t valid')


    def test_02_add_another(self):
        b = self.add_block()
        self.assertTrue(b.is_hash_valid(MainTest.PREFIX), 'Hash isn\'t valid')


    def test_03_validate_blockchain(self):
        for i in range(5):
            self.add_block()
        self.validate_blockchain()


    def test_04_validate_data_changed(self):
        for i in range(3):
            self.add_block()
        b = self.blockchain[-1]
        b.data._content = 'XXX'
        with self.assertRaises(AssertionError):
            self.validate_blockchain()  # This should throw an AssertioError.


    def test_05_validate_previuos_hash_changed(self):
        for i in range(3):
            self.add_block()
        b1 = self.blockchain[-1]
        b2 = self.blockchain[-3]
        b1._previous_hash = b2.hash
        with self.assertRaises(AssertionError):
            self.test_03_validate_blockchain()


    def create_genesis_block(self) -> Block:
        '''Creates the genesis Block, and returns it.'''
        b = Block(StrData('GENESIS'), '0', datetime.timestamp(datetime.now()))
        b.mine(MainTest.PREFIX)
        return b


    def add_block(self) -> Block:
        '''Create a test block, adds it to the blockchin and returns the block.'''
        self.assertTrue(self.blockchain, 'blockchain does not have genesis block' )
        last_block = self.blockchain[-1]
        ts = datetime.timestamp(datetime.now())
        b = Block(StrData('Another block ' + str(ts)), last_block.hash, ts)
        b.mine(MainTest.PREFIX)
        self.blockchain.append(b)
        return b


    def validate_blockchain(self):
        for i, b in enumerate(self.blockchain):
            correct_hash_prefix = b.hash[:MainTest.PREFIX] == MainTest.PREFIX_STR
            self.assertTrue(correct_hash_prefix, f'Incorrect hash prefix for block {i}.')
            block_integrity = b.hash == b.calculate_hash()
            self.assertTrue(block_integrity, f'Block integrity failed for block {i}.')
            previous_hash = '0' if i == 0 else self.blockchain[i - 1].hash
            chaining_correct = previous_hash == b.previous_hash
            self.assertTrue(chaining_correct, f'Incorrect chaining for block {i}.')


if __name__ == '__main__':
    unittest.main()
