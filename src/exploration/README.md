# Exploration Project

This part of the project is to test various algorithm and provide a devlopment setup with jupyter notebook to allow further understanding before real implementation. It is a stepping stone to further modelise a proper library to use in the trading and investing projects.

## Installation
This part of the project is comprised of various jupyter notebooks and thus is bind to a lot of dependencies. Please don't forget to add those dependencies to help track them, directly in the readme of the home directory.

1. Make sure you have followed the installation in the readme in the home directory.
2. Activate your virtual-env and cd to the exploration directory.
3. Install jupyter notebook.
    ```
    pip3 install jupyter
    ```
4. Run jupyter notebook.
    ```
    jupyter notebook
    ```
5. It is possible to make the ipython kernel directly in vscode. I have no idea how though.

## How to
- *I want to create a jupyter notebook to work on a specific exploration.*
    1. If there is no folder made for the new exploration, please create one to make organisation clear.
    2. Else create a ipynb file in the existing folder.
- *I have private credentials I want to use in a notebook.*
    1. A credential file "setup.env" is created to stock and manage properly all credentials and environment variable. This file is gitignored to make sure it is not leaked. However, to make understandable the credentials needed to make the notebook runs, a "fake.env" is created to track the variable names, please fill them with XXX to signify those are fake.
    2. When wanting to use those credentials in a notebook :
        ```
        from dotenv import load_dotenv
        import os

        load_dotenv(dotenv_path = 'path/to/setup.env')

        api_user_key = os.get('ENV_VAR_USR')
        api_user_secret = os.get('ENV_VAR_PWD')
        ```
    3. You can now safely use those credentials in the notebook by using those variables