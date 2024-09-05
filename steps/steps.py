import behave
from web3 import Web3
from eth_tester import EthereumTester, PyEVMBackend
from solcx import compile_source
from solcx import compile_standard, install_solc

#Test

# Configuración inicial
ethereum_tester = EthereumTester(backend=PyEVMBackend())
w3 = Web3(Web3.EthereumTesterProvider(ethereum_tester))

@given(u'I have 5 Ethereum nodes')
def step_impl(context):
    # Crear cuentas y desplegar contrato
    context.accounts = w3.eth.accounts
    context.account_a = context.accounts[0]
    context.account_b = context.accounts[1]
    context.initial_balance = 100

    # Código del contrato inteligente
    contract_source_code = '''
    pragma solidity ^0.5.0;
    contract MyToken {
        mapping(address => uint) public balances;
        constructor() public {
            balances[msg.sender] = 100;
        }
        function transfer(address to, uint amount) public {
            require(balances[msg.sender] >= amount, "Insufficient balance.");
            balances[msg.sender] -= amount;
            balances[to] += amount;
        }
    }
    '''

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:MyToken']

    # Desplegar contrato
    MyToken = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = MyToken.constructor().transact({'from': context.account_a})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    context.contract_address = tx_receipt.contractAddress
    context.token_contract = w3.eth.contract(
        address=context.contract_address,
        abi=contract_interface['abi'],
    )



@when(u'I mine a block with 5 transactions')
def step_impl(context):
  context.token_contract.functions.transfer(context.account_b, 10).transact({'from': context.account_a})
    
@then(u'the block should be added to the blockchain')
def step_impl(context):
  balance = context.token_contract.functions.balances(context.account_a).call()
  assert balance == 90