# smart storage with web3py
Smart contract build with solidity and web3 python library. This project was made to help beginners in blockchain development to exercese their skills

## Technology & Tools

### [Solidity](https://docs.soliditylang.org/en/v0.8.17/)
> Solidity is an object-oriented, high-level language for implementing smart contracts. Smart contracts are programs which govern the behaviour of accounts within the Ethereum state.

### [Python](https://docs.soliditylang.org/en/v0.8.17/)
> Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation. Python is dynamically-typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.
> 
### [web3.py](https://web3py.readthedocs.io/en/v5/)
> Web3.py is a Python library for interacting with Ethereum.

### [Nodejs](https://nodejs.org/en/)
> Node.js is an open-source, cross-platform JavaScript runtime environment with a focus on server-side and networking applications. Node.js allows developers to build fast, scalable network applications using easy-to-understand code. It runs on Windows OS, Mac OSX, Linux, Unix, and other operating systems.

### [Visual Studio Code](https://code.visualstudio.com/)
> Visual Studio Code, also commonly referred to as VS Code, is a source-code editor made by Microsoft with the Electron Framework, for Windows, Linux and macOS. Features include support for debugging, syntax highlighting, intelligent code completion, snippets, code refactoring, and embedded Git. Users can change the theme, keyboard shortcuts, preferences, and install extensions that add additional functionality.

### [Truffle](https://trufflesuite.com/)
> Truffle Suite provides world class development environment for blockchain dapps.
### [Ganache](https://trufflesuite.com/ganache/)
> Quickly fire up a personal Ethereum blockchain which you can use to run tests, execute commands, and inspect state while controlling how the chain operates.

### [MetaMask](https://metamask.io/)
> MetaMask is a software cryptocurrency wallet used to interact with the Ethereum blockchain. It allows users to access their Ethereum wallet through a browser extension or mobile app, which can then be used to interact with decentralized applications. (MetaMask chrom extension ID : nkbihfbeogaeaoehlefnkodbefgpgknn)

### Ethereum Testnet fauset
- Goerli testnet (https://goerli-faucet.pk910.de/) (https://goerlifaucet.com/)
## Steps
### Installation and settings
1. Install python
2. Create a virtual environment (python -m venv venv)
3. Install IDE (visual studio code or other)
4. install vs code extension :  install python intellisense, solidity, and ..
5. Check python installation open terminal include in vs code check python's version by python --version
6. set python formatting provider to black (vs code settings)
7. create smartStorage.sol which will contain our smart contract code
8. Install ganache ([Click Here](https://trufflesuite.com/ganache/))
### Deploy our smart contract with python
1. create deploy.py which will contain our smart contract deployment code 
2. Install py-solc-s (solidity compiler) pip install py-solc-x
3. Open Ganache UI (local blockchain for development testing)
4. Install web3.py (pip install web3) to deploy and interact with the smart contract via python
5. Install python-dotenv (pip install python-dotenv) to reads key-value pairs from a .env file and can set them as environment variables.

## How to run
