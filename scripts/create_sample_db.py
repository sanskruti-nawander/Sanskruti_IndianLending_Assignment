import sqlite3
from datetime import datetime

conn = sqlite3.connect('indian_lending.db')
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON;")

# -----------------------------
# Create tables
# -----------------------------
c.executescript('''
CREATE TABLE IF NOT EXISTS branches(
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch_name TEXT,
    state TEXT
);

CREATE TABLE IF NOT EXISTS collection_agents(
    agent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    branch_id INTEGER
);

CREATE TABLE IF NOT EXISTS borrowers(
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    branch_id INTEGER,
    state TEXT,
    cibil INTEGER
);

CREATE TABLE IF NOT EXISTS loans(
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrower_id INTEGER,
    loan_type TEXT,
    amount REAL,
    outstanding REAL,
    dpd INTEGER,
    status TEXT,
    FOREIGN KEY(borrower_id) REFERENCES borrowers(borrower_id)
);

CREATE TABLE IF NOT EXISTS payments(
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER,
    agent_id INTEGER,
    amount REAL,
    date TEXT
);

CREATE TABLE IF NOT EXISTS legal_actions(
    action_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER,
    action_type TEXT,
    date TEXT,
    notes TEXT
);
''')

# -----------------------------
# Insert branches
# -----------------------------
branches = [
    ('Mumbai Branch','Maharashtra'),
    ('Bengaluru Branch','Karnataka'),
    ('Delhi Branch','Delhi'),
    ('Chennai Branch','Tamil Nadu'),
    ('Hyderabad Branch','Telangana'),
    ('Pune Branch','Maharashtra')
]

c.executemany("INSERT INTO branches(branch_name,state) VALUES (?,?)", branches)

# -----------------------------
# Insert borrowers — IMPORTANT: fixed number, known IDs (1–15)
# -----------------------------
borrowers = [
    ('Ramesh',1,'Maharashtra',720),
    ('Sita',2,'Karnataka',680),
    ('Amit',3,'Delhi',630),
    ('Leela',4,'Tamil Nadu',760),
    ('Kumar',5,'Telangana',600),
    ('Priya',6,'Maharashtra',790),
    ('Vikram',1,'Maharashtra',650),
    ('Zoya',2,'Karnataka',710),
    ('Nikhil',3,'Delhi',550),
    ('Meera',4,'Tamil Nadu',670),
    ('Rohit',5,'Telangana',740),
    ('Anita',6,'Maharashtra',610),
    ('Sunil',1,'Maharashtra',700),
    ('Geeta',2,'Karnataka',640),
    ('Pavan',3,'Delhi',730)
]

c.executemany("INSERT INTO borrowers(name,branch_id,state,cibil) VALUES (?,?,?,?)", borrowers)

# -----------------------------
# Insert loans – now borrower IDs 1–15 are guaranteed valid
# -----------------------------
loans = [
    (1,'Personal',100000,50000,0,'Active'),
    (2,'Gold',50000,20000,95,'NPA'),
    (3,'Two-Wheeler',45000,45000,120,'NPA'),
    (4,'Education',200000,150000,10,'Active'),
    (5,'Business',500000,450000,0,'Active'),
    (6,'Home',1500000,1400000,0,'Active'),
    (7,'Personal',80000,40000,35,'SMA-1'),
    (8,'Gold',70000,70000,65,'SMA-2'),
    (9,'Microfinance',15000,5000,5,'Active'),
    (10,'Business',300000,250000,0,'Active'),
    (11,'Personal',120000,100000,2,'Active'),
    (12,'Two-Wheeler',60000,30000,45,'SMA-1'),
    (13,'Gold',90000,90000,92,'NPA'),
    (14,'Education',250000,200000,0,'Active'),
    (15,'Home',2000000,1900000,0,'Active'),
    (1,'LoanAgainstProperty',800000,700000,15,'Active'),
    (2,'Microfinance',20000,15000,0,'Active'),
    (3,'Business',150000,130000,75,'SMA-2'),
    (4,'Personal',70000,20000,0,'Active')
]

c.executemany("INSERT INTO loans(borrower_id,loan_type,amount,outstanding,dpd,status) VALUES (?,?,?,?,?,?)", loans)

# -----------------------------
# Insert payments
# -----------------------------
today = datetime.now().strftime("%Y-%m-%d")
payments = [
    (1,1,10000,today),
    (2,2,5000,today),
    (3,3,3000,today),
    (4,1,2000,today),
    (5,2,1000,today)
]

c.executemany("INSERT INTO payments(loan_id,agent_id,amount,date) VALUES (?,?,?,?)", payments)

# -----------------------------
# Insert legal action
# -----------------------------
c.execute("INSERT INTO legal_actions(loan_id,action_type,date,notes) VALUES (?,?,?,?)",
          (3,'SARFAESI', today, 'Initiated'))

conn.commit()
print("DB created successfully with valid foreign keys!")
conn.close()
