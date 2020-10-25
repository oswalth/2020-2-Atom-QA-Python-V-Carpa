# Nginx access log parser
* Parser could be ran using both python and bash.
* Script scans current directory or directory provided by user as an argument, and processes all files with .log extension.
* !!!IMPORTANT - if  you specify logs directory, all logs should be placed in folder called `logs`

## Bash 
1. Run script 
   ```bash
   script.sh [log_directory_path]
   ```
2. Checkout bash_output folder for results. Resulting files are formed following this template `log_name.result`
3. Results are files with the following structure:
    ```
   Operation_1 output
   =========
   ...
   =========
   Operation_5 output
   ```

## Python
1. Install requirements from project's root:
    ```bash
    pip install -r requirements.txt
    ```
2. Run script: 
    ```bash
    python3 py_script.py [log_directory_path]
    ```
3. Checkout python_output folder for results. Resulting files are formed following this template `log_name.result`
4. Result files are json format where keys are operations' names and values are results of such operations.
5. Example:
    ```json
    {"count_requests": 225133, "count_requests_by_type": {"GET": 122095, "HEAD": 528, "POST": 102503, "PUT": 6}}
    ```