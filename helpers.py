import streamlit as st
from solcx import compile_standard, install_solc #solidity compiler in python
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from PIL import Image
from deploy import *
# == Logo
def logo():
    # source: jason-leung from unsplash
    logo = "images/ktlogo3.png"
    logo = Image.open(logo)
    size=(100,100)
    #resize image
    logo = logo.resize(size)
    st.sidebar.image(logo)
    st.sidebar.subheader("Smart Storage")


# == Home =======================================================================================
def home():
    st.markdown("""
   **Diabetes** is one of the diseases that affects many people in the world, detecting it early will allow effective 
   care taking of patient. This application  allows automatic and rapid prediction of diabetes in **prediabetic stage** 
   using certain symptom measurements.
    """)

    image = Image.open('images/diabete_cover.png')
    st.image(image, caption='Machine Learning Project by Rekidiang Data', use_column_width=True)

    st.markdown("""
        To navigate the application, in slider bar  select **About** to have info about the project, **App** to detect if patient have 
        diabetes or not accordingly to symptom measurement, **Analysis** to know more about data, analysis and ML model
        use in this project and **Prediction Result** to see results records.

        """)
## Smmart Contract Function
def build_trans(smartStorage, el):
    transaction = smartStorage.constructor().buildTransaction(
        {
            "chainId": el[0],
            "gasPrice": el[1],
            "from": el[2],
            "nonce": el[3],
        }
    )
    return transaction

def sign_tx(RPC_SERVER, transaction, PRIVATE_KEY):
            w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
            signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)
            return signed_txn

def compile_contract(simple_storage_file):
    compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"smartStorage.sol": {"content": simple_storage_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    } 
                },
            },
            solc_version="0.6.0",
        )
    ## GRABE SMART CONTRACT AS JSON FILE #################################
    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)
    return compiled_sol

def create_contract(RPC_SERVER,abi, bytecode):
    w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
    smartStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
    return smartStorage

def bytecode_abi(compiled_sol):
    # Extract compiled smart contract
    # get bytecode and abi
    bytecode = compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["evm"]["bytecode"]["object"]
    abi = json.loads(compiled_sol["contracts"]["smartStorage.sol"]["smartStorage"]["metadata"])["output"]["abi"]
    return bytecode, abi

RPC_SERVER = "HTTP://127.0.0.1:7545"


# == App ======================================================================================
def app():
    # Data input --------------------------------------------------------------------------
    #def input_feature():
    st.subheader("1. Compile Smart Contract")
    
    with open("smartStorage.sol", "r") as file:
        simple_storage_file = file.read()
    

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pass
    with col2:
        if st.button("Install Solidity Compiler"):
            install_solc("0.6.0")
            st.write("Compiler Intalled ")
    with col3:
        if st.button("Compile Smart Contract"):
            pass
    with col4:
        pass
        
    ## GRABE SMART CONTRACT FILE #################################
    
    # Extract compiled smart contract
    if st.checkbox("Smart Contact in Solidity"):
        st.write(simple_storage_file)

    compiled_sol = compile_contract(simple_storage_file)
    if st.checkbox("Smart contract Compiled"):
        st.write(compiled_sol)

    st.markdown("---")
    st.subheader("2. Build and Deploy Smart Contract")
    
    # get bytecode and abi
    bytecode, abi = bytecode_abi(compiled_sol)
    menu = ["Ganache (Local Network)", "Goerli (Testnet)"]
    st.markdown("##### 2.1. Select Blockchain Network")
    choice = st.radio("", menu)
    if choice == "Ganache (Local Network)":
        RPC_SERVER = "HTTP://127.0.0.1:7545"
        w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
    
    st.markdown("##### 2.2. Create Smart contract")
    st.write("To create or build a Smart contract we need RPC_SERVER, abi and bytecode")
    if st.checkbox("Create Contract"):
        smartStorage = create_contract(RPC_SERVER,abi, bytecode)        
        st.write("Contract Created Successfully")
        
        st.markdown("---")
        
        

        ## Make contract deployment transaction #################################
        # 1. Build a deployment Transaction
        st.markdown("##### 2.3. Build contract Deployment Transaction")
        st.write("Element need to build a contract")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            NETWORK_ID = int(st.text_input("Enter Chain-ID", '0'))
        with col2:
            if st.checkbox("Get GasPrice"):
                gasPrice = w3.eth.gas_price
                st.write(gasPrice)
        with col3:
            MY_ADDRESS = st.text_input("Public Key")
        with col4:
            if st.checkbox("Get Nonce"):
                nonce = w3.eth.getTransactionCount(MY_ADDRESS)
                st.write(nonce)
                # user_input = st.text_input("Patient Name")    
        
        if st.checkbox("Look at builded transaction"):
            el = [NETWORK_ID, gasPrice, MY_ADDRESS, nonce]  
            transaction = build_trans(smartStorage, el)
            st.write(transaction)
        st.markdown("---")
        
        st.markdown("##### 2.4. Sign Contract Deployment Transaction")
        PRIVATE_KEY = st.text_input("Privale Key")
        if st.button("Sign Transaction"):
            el = [NETWORK_ID, gasPrice, MY_ADDRESS, nonce]  
            transaction = build_trans(smartStorage, el)
            signed_txn = sign_tx(RPC_SERVER, transaction, PRIVATE_KEY)
            #st.write(signed_txn)
        st.markdown("---")

        st.markdown("#### Send Contract Deployment Transaction to the block") 
        if st.checkbox("Deploy"):
            el = [NETWORK_ID, gasPrice, MY_ADDRESS, nonce]  
            transaction = build_trans(smartStorage, el)
            signed_txn = sign_tx(RPC_SERVER, transaction, PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            #Wait for block confirmations
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            st.balloons() 
            st.sidebar.markdown("---")
            st.sidebar.write(f"Contrad Deployed at : {tx_receipt['contractAddress']}")
            st.sidebar.write(f"Current Stored Value : {simple_storage.functions.retrieve().call()}")

                
        st.markdown("---")
        

                
    elif choice == "Goerli (Testnet)":
        st.subheader("2.1.2. Goerli (Testnet)")
        RPC_SERVER = "https://goerli.infura.io/v3/48ee1345cc204db38ca412dcffbc44ca"
        NETWORK_ID = 5
        st.write("RPC Server : https://goerli.infura.io/v3/48... || Chain-ID : 5")

        

        
        
        

        

        

        
    






    
    

    
        
        
          
        

        


# == Analysis =============================================================================================
def analysis():
   
    st.subheader("Interact with Smart Contract")
    w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = smartStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    

    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col2:
        st.subheader(f"Current Value : {simple_storage.functions.retrieve().call()}")
        #if st.button("Initial Value"):
            #install_solc("0.6.0")
            #st.write("Compiler Intalled ")
    with col3:
            pass
   

    st.markdown("#### 2. Update stored value")
    PRIVATE_KEY = st.text_input("Enter value for update")
    st.markdown("###### Element need to build a contract")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        NETWORK_ID = int(st.text_input("Enter Chain-ID", '0'))
    with col2:
        if st.checkbox("Get GasPrice"):
            gasPrice = w3.eth.gas_price
            st.write(gasPrice)
    with col3:
        MY_ADDRESS = st.text_input("Public Key")
    with col4:
        if st.checkbox("Get Nonce"):
            nonce = w3.eth.getTransactionCount(MY_ADDRESS)
            st.write(nonce)
            # user_input = st.text_input("Patient Name")    
    
    if st.checkbox("Look at builded transaction"):
        el = [NETWORK_ID, gasPrice, MY_ADDRESS, nonce]  
        transaction = build_trans(smartStorage, el)
        st.write(transaction)

    PRIVATE_KEY = st.text_input("Privale Key")
    if st.button("Sign Transaction"):
        signed_greeting_txn = w3.eth.account.sign_transaction(
                greeting_transaction, private_key=private_key
        )
        tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
        print("Updating stored Value...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
        #st.write(signed_txn)
        st.balloons() 
    st.markdown("---")
    st.subheader(f"Current Stored Value : {simple_storage.functions.retrieve().call()}")
""""
    st.markdown("### 1. Update value value")
    # Working with deployed Contracts
    w3 = Web3(Web3.HTTPProvider(RPC_SERVER))
    with open("smartStorage.sol", "r") as file:
        simple_storage_file = file.read()
    compiled_sol = compile_contract(simple_storage_file)
    bytecode, abi = bytecode_abi(compiled_sol)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    #Wait for block confirmations
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    smartStorage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(f"Initial Stored Value {smartStorage.functions.retrieve().call()}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        NETWORK_ID = int(st.text_input("Enter Chain-ID", '0'))
    with col2:
        if st.checkbox("Get GasPrice"):
            gasPrice = w3.eth.gas_price
            st.write(gasPrice)
    with col3:
        MY_ADDRESS = st.text_input("Public Key")
    with col4:
        if st.checkbox("Get Nonce"):
            nonce = w3.eth.getTransactionCount(MY_ADDRESS)
            st.write(nonce)
            # user_input = st.text_input("Patient Name")\
    newValue = st.text_input("Insert new value")  
    if st.checkbox("See builded transaction"):
        el = [NETWORK_ID, gasPrice, MY_ADDRESS, nonce]  
        transaction = build_trans(smartStorage, el) 
        greeting_transaction = smartStorage.functions.store(newValue).buildTransaction(
        {
            "chainId": el[0],
            "gasPrice": el[1],
            "from": el[2],
            "nonce": el[3] + 1,
        }
    )
    signed_greeting_txn = w3.eth.account.sign_transaction(greeting_transaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(smartStorage.functions.retrieve().call())
    """


    

  

# == All Result ===============================================================================================

def all_data():
    # retrive data
    retrive_data()


# == About ======================================================================
def about():
    st.markdown("""
    ### Motivation

    **Diabetes** is one of the diseases that affects many people in the world, detecting it early will allow effective 
   care taking of patient. This application  allows automatic and rapid prediction of diabetes in **prediabetic stage** 
   using certain symptom measurements.
   """)

    st.markdown("""
    ### Reading

    * [ papers that cite this data set](https://archive.ics.uci.edu/ml/support/Diabetes)
    * [PIMA Dataset and for Diabetes Analysis Review](https://ijsret.com/wp-content/uploads/2021/05/IJSRET_V7_issue3_495.pdf)
   """)

    st.markdown("""
    ### author

    I’m  Data and technology passionate person, Artificial Intelligence enthusiast, lifelong learner. Since my childhood I was interested to technology and science, but I didn’t get access to it, by the lack of resource and opportunities hopefully grace to massive learning resource available on the Internet I’m getting close to my dream. My pleasure is to motivate, guide and teach people with less or without resource accomplish their dream in the world of technology specially kids and young. For more information about me go to my **Website** and **Social Network** platform (👇)
    """)

# == Footer ==========================================================================================
def footer():
    st.markdown("""---""")
   
    footerr = """
            <div style="background-color:black;padding:1px">
            <h5 style="color:white;text-align:center;">My name is Kiese Diangebeni Reagan</h5>
            <p style="color:white;text-align:center;font-size:14px;">I'm Data Science Analyst, technology passionate person, Artificial Intelligence enthusiast and lifelong learner. </p>
            
            <p style="color:red;text-align:center;">
            <a href="https://kiese.tech">www.kiese.tech</a> -
            <a href="https://twitter.com/ReaganKiese">Twitter</a> - 
            <a href="https://www.linkedin.com/in/kiese-diangebeni-reagan-82992216a/">Linkedin</a> - 
            <a href="https://github.com/RekidiangData-S">Github</a> - 
            <a href="https://medium.com/@rkddatas">Medium</a> - 
            <a href="https://www.kaggle.com/rekidiang">Kaggle</a></p>
            </div><br>"""
    st.markdown(footerr, unsafe_allow_html=True)
    st.markdown('<style>h1{color: blue;}</style>', unsafe_allow_html=True)
