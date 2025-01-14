import pymysql
import os
from web3 import Web3
import logging

# Setting up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("Started.")


def lambda_handler():
    # Environment variables for credentials
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = int(os.getenv('DB_PORT', 8889)) 
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'root')
    db_name = os.getenv('DB_NAME', 'altdrx')

    # Database connection
    connection = pymysql.connect(host=db_host, port=db_port, user=db_user, password=db_password, db=db_name,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    logging.info("Connected to the database successfully.")
    print("Connected to the database successfully.")


    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `fullName`, `cid` FROM `investor` WHERE `cid` IS NOT NULL"
            print(f"Transaction sent successfully. Hash: {sql}")
            cursor.execute(sql)
            results = cursor.fetchall()
            logging.info(f"Fetched {len(results)} records from the database.")
            print(f"Fetched {len(results)} records from the database.")
          
            
            keys, names, cids = [], [], []
            for result in results:
                keys.append(str(result['id']))
                names.append(result['fullName'])
                cids.append(result['cid'])

            if keys:
                logging.info("Updating the Ethereum contract...")
                print("Updating the Ethereum contract...")
                update_contract(keys, names, cids)

    finally:
        connection.close()
        logging.info("Database connection closed.")



def update_contract(keys, names, cids):
    # Ensure private key is securely fetched from environment
    web3 = Web3(Web3.HTTPProvider('https://linea-mainnet.infura.io/v3/f3119f0f20214f95b5caecc8e366a489'))

    private_key = "746c158f2fbe16409e3645023f1f06cd8172b2ab1245f24e19c7c5e9e842c970"
    if not private_key:
        raise EnvironmentError("ETH_PRIVATE_KEY environment variable not set")
    contract_address = "0x51c4975a5c3f947dc40ed20b024db43a26cd7bb5"
    contract_abi = [{"anonymous": False, "inputs": [{"indexed": False, "internalType": "string", "name": "key", "type": "string"}, {"indexed": False, "internalType": "string", "name": "name", "type": "string"}, {"indexed": False, "internalType": "string", "name": "cid", "type": "string"}], "name": "InvestorUpdated", "type": "event"}, {"inputs": [{"internalType": "string[]", "name": "keys", "type": "string[]"}, {"internalType": "string[]", "name": "names", "type": "string[]"}, {"internalType": "string[]", "name": "cids", "type": "string[]"}], "name": "updateLedger", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "string", "name": "key", "type": "string"}], "name": "viewMyLedger", "outputs": [{"internalType": "string", "name": "message", "type": "string"}, {"internalType": "string", "name": "link", "type": "string"}], "stateMutability": "view", "type": "function"}]

    # Convert to checksum address and set sender address
    checksum_address = Web3.to_checksum_address(contract_address)
    sender_address = Web3.to_checksum_address('0x60b7afedfa218f9035e460ecbcd1156d18866ed3')  # Replace with your address

    # Create contract instance
    contract = web3.eth.contract(address=checksum_address, abi=contract_abi)

    # Build transaction
    nonce = web3.eth.get_transaction_count(sender_address)
    tx = contract.functions.updateLedger(keys, names, cids).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 1000000,
        'gasPrice': web3.to_wei('1', 'gwei')
    })

    
    # Sign and send the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logging.info(f"Transaction sent successfully. Hash: {tx_hash.hex()}")
    print(f"Transaction sent successfully. Hash: {tx_hash.hex()}")


# This is where the script execution begins
if __name__ == "__main__":
    # result = lambda_handler()
    print("Function executed successfully.")