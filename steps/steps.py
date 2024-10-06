from behave import given, when, then
from web3 import Web3

# Conectar con un nodo Ethereum
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))  # Cambia a tu URL de nodo si es diferente

@given('I am connected to 1 Ethereum node')
def step_given_connected_node(context):
    assert w3.isConnected(), "Failed to connect to Ethereum node"

@when('I send a simple transaction')
def step_when_send_transaction(context):
    tx = {
        'from': w3.eth.accounts[0],  # Cuenta de origen
        'to': w3.eth.accounts[1],    # Cuenta de destino
        'value': w3.toWei(0.01, 'ether'),
        'gas': 2000000,
        'gasPrice': w3.toWei('50', 'gwei')
    }
    tx_hash = w3.eth.sendTransaction(tx)
    context.tx_hash = tx_hash
    assert tx_hash is not None, "Transaction failed"

@then('the transaction should be mined successfully')
def step_then_transaction_mined(context):
    tx_receipt = w3.eth.wait_for_transaction_receipt(context.tx_hash)
    assert tx_receipt is not None, "Transaction receipt not received"

@then('the block should be added to the blockchain')
def step_then_block_added(context):
    tx_receipt = w3.eth.wait_for_transaction_receipt(context.tx_hash)
    block = w3.eth.getBlock(tx_receipt['blockNumber'])
    assert block is not None, "Block not found"
