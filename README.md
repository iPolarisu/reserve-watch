# ReserveWatch: Te pillamos po
Python app that checks if people exceeed the number of reservations for any given space available in ucampus.

### Disclaimer

When running the script, be sure to read what it does and how it does it. In short, it uses U-Campus credentials to access FCFM's sport zones reservations and calculate the amount of reservations of each user.

### Installing

It is highly advised that you use a **Python Virtual Environment** to install the modules.

1. Creating the virtual environment

    ```bash
    # installing virtualenv
    pip install virtualenv

    # create a virtual env for the project
    virtualenv .venv
    ```

2. Activating the virtual environment

    Windows

    ```powershell
    .venv\Scripts\activate
    ```

    Linux/MacOS

    ```bash
    source .venv/bin/activate
    ```

3. Installing modules via pip

    ```bash
    pip install -r requirements.txt
    ```

### Executing

```bash
python main.py
```
