# Invoice Approval Tracker

## About the Project

The Invoice Approval Tracker is a web-based application developed using Python, Flask, and SQLite. It helps users manage invoices and track their approval status through a simple dashboard.

## Features

- Add new invoices.
- View all invoices on the dashboard.
- Edit invoice details.
- Validate invoice information.
- Track invoice approval status.
- View invoice status history.
- Delete invoices.
- Store invoice records using an SQLite database.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS

## Project Structure

```text
Invoice-Approval-Tracker/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── index.html
    ├── edit.html
    └── history.html
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/rashipandey2105/Invoice-Approval-Tracker.git
```

### 2. Open the project folder

```bash
cd Invoice-Approval-Tracker
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python database.py
```

### 5. Run the application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## Author

**Rashi Pandey**

GitHub: [rashipandey2105](https://github.com/rashipandey2105)