# Phone Pool Manager

A minimal CLI application to manage a telecommunications operator's pool of phone numbers, based on ranges assigned by ARCEP.

## 📦 Features

- Initialize a database with the allocated ARCEP number ranges
- Allocate a phone number to a customer
- List currently allocated numbers
- Do a yearly usage report
- Cancel a customer's subscription
- Release expired numbers

## 🚀 Getting Started

### Installation

(Optional) Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Usage

#### Initialize the database and populate the number pool:

```bash
./scripts/setup-db.py
```

#### Use the CLI

```bash
python -m src.main --help
```
