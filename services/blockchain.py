from pathlib import Path
from secret_sdk.client.lcd.wallet import Wallet
from secret_sdk.key.mnemonic import MnemonicKey
from secret_sdk.client.lcd import LCDClient
from secret_sdk.core.tx import StdFee
from secret_sdk.core.wasm.msgs import MsgExecuteContract

def get_value(file_name):
    """Read value from a file in the root directory"""
    try:
        file_path = Path(__file__).parent.parent / file_name
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading {file_name}: {str(e)}")
        return None

def initialize_wallet():
    """Initialize Secret Network wallet from mnemonic or key"""
    wallet_key = get_value("WALLET_KEY.txt")
    
    if not wallet_key:
        raise ValueError("Failed to load wallet key")
    
    # Create wallet from mnemonic or key
    # Note: This implementation might need adjustment based on how secret-sdk-python 
    # handles wallet creation compared to secretjs
    mk = MnemonicKey(mnemonic=wallet_key)
    wallet = Wallet(
        lcd=LCDClient(
            url="https://lcd.erth.network",
            chain_id="secret-4"
        ),
        key=mk
    )
    
    # Check wallet balance
    check_balance(wallet)
    
    return wallet

def check_balance(wallet):
    """Check the balance of the wallet"""
    try:
        balance = wallet.lcd.bank.balance(wallet.key.acc_address)
        print(f"Wallet balance: {balance}")
        return balance
    except Exception as e:
        print(f"Error checking balance: {str(e)}")
        return None

def contract_interaction(wallet, contract_address, code_hash, message):
    """Execute a contract interaction with the Secret Network"""
    try:
        # Create message for contract execution
        execute_msg = MsgExecuteContract.from_data({
            "sender": wallet.key.acc_address,
            "contract": contract_address,
            "code_hash": code_hash,
            "msg": message
        })
        
        # Broadcast transaction
        tx = wallet.create_and_sign_tx(
            msgs=[execute_msg],
            fee=StdFee(
                gas=1000000,
                amount=[{"denom": "uscrt", "amount": "100000"}]
            ),
            memo="User registration via Python SDK"
        )
        
        # Execute transaction
        result = wallet.lcd.tx.broadcast(tx)
        print(f"Transaction result: {result}")
        
        # Prepare response similar to JS version
        response = {
            "code": result.code,
            "txhash": result.txhash,
            "raw_log": result.raw_log
        }
        
        return response
    except Exception as e:
        print(f"RPC error during contract interaction: {str(e)}")
        raise Exception("Contract interaction failed due to RPC error")