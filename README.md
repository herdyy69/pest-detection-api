Berikut adalah file README dalam format Markdown (`.md`):

````markdown
# Pest Detection API

This is a Flask-based application for detecting pests using YOLOv8.

## How to Run

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/herdy3/pest-detection-api.git
   ```
````

2. Navigate to the project directory:

   ```bash
   cd pest-detection-api
   ```

3. Check your Python and pip versions:

   - Check Python version:
     ```bash
     python --version
     ```
     or
     ```bash
     python3 --version
     ```
   - Check pip version:
     ```bash
     pip --version
     ```
   - If pip is not installed:
     ```bash
     python -m ensurepip --upgrade
     ```

4. Activate a virtual environment:

   - Create a virtual environment:
     ```bash
     python3 -m venv pestenv
     ```
   - Activate the virtual environment:
     - **On Windows:**
       ```bash
       pestenv\Scripts\activate
       ```
     - **On macOS/Linux:**
       ```bash
       source pestenv/bin/activate
       ```

5. Install dependencies (only if they are not already installed):

   - Install the required packages:
     ```bash
     pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
     pip install -r requirements.txt
     ```
   - Verify installation:
     ```bash
     pip list
     ```

6. Run the application:
   ```bash
   python main.py
   ```

---

## Notes

- Make sure to have Python 3.7 or higher installed on your system.
- If you encounter any issues with the dependencies, you may want to update pip:
  ```bash
  pip install --upgrade pip
  ```
