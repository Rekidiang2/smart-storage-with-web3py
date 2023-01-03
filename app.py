import streamlit as st
from solcx import compile_standard, install_solc #solidity compiler in python
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from helpers import app, analysis, all_data, about, footer, logo


# Sidebar Configuration
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#99ffcc,#99ffcc);
    color: purple;
}
</style>
""",
    unsafe_allow_html=True,
)

def main():
    logo()
    # basic layout
    menu = ["Home", "Create, Build and Deploy", "Interact with Smart Contract", "About"]
    choice = st.sidebar.radio("Menu", menu)
    # siderbar methods
    #st.write(dir(st.sidebar))

    html_temp = """
    <div style="background-color:black;padding:0.5px">
    <h1 style="color:white;text-align:center;">Smart Storage </h1>
    <h3 style="color:red;text-align:center;">Smart contract build with solidity deploy with python </h3>
    </div><br>"""
    st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown('<style>h1{color: blue;}</style>', unsafe_allow_html=True)

    if choice == "Home":
        pass

        #st.title("Home")
        #home()
    elif choice == "Create, Build and Deploy":
        app()
    elif choice == "Interact with Smart Contract":
        
        analysis()
    elif choice == "About":
        #st.title("About")
        about()


    footer()

if __name__ == '__main__':
    main()
