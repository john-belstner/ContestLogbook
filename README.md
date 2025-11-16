# 📘 ContestLogBook

**ContestLogBook** is a lightweight logging application tailored for contest operations, written in **Python 3** using **Tkinter** and **SQLite**.  
It manages station configuration, logs QSOs locally, keeps track of critical statistics and exports to **Cabrillo** format.

---

![Contest LogBook Image](https://raw.githubusercontent.com/john-belstner/ContestLogBook/main/contestlogbook_image.png)

---

## 🧑‍💻 Author
**John M. Belstner (W9EN)**  
© 2025 – Open-source for educational and Amateur Radio use, GNU General Public License v3.0 (GPL-3.0)

---

## ✨ Key Features

- 🗂️ **Local QSO Database**  
  - Logs all QSOs to a local SQLite database (`contest_log.db`).  
  - Supports full CRUD (Create, Read, Update, Delete) operations.  
  - Exports to **Cabrillo 3.0** format.

- 📡 **CAT Radio Control**  
  - Connects to your transceiver via serial CAT interface.  
  - Automatically reads frequency, mode, and band information.  

- 🧭 **Graphical User Interface**
  - Built with Tkinter and ttk for a clean, cross-platform experience.  
  - Displays recent QSOs, provides quick entry forms, and integrates lookup tools.  
  - Includes a dedicated **Configuration Settings** dialog.

---

## 📁 Project Structure

```
ContestLogBook.py      # Main application
ConfigWindow.py        # Configuration GUI (reads/writes config.ini)
LogDatabase.py         # SQLite database handler for QSO records
LastQSOs.py            # Recent QSOs table display (Treeview)
Cat.py                 # CAT serial interface for radio control
Qso.py                 # QSO record object (ADIF generation, validation)
config.ini             # Configuration file (encrypted credentials)
contest_log.db         # SQLite QSO database
```

---

## ⚙️ Installation and Setup

### 1️⃣ Prerequisites
Ensure the following are installed:
- Python **3.9+**
- `pip install pyserial configparser pathlib datetime tkinter sqlite3`

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/john-belstner/ContestLogBook.git
cd ContestLogBook
```

### 3️⃣ Create or Edit `config.ini`
An example is included. Update with your callsign, credentials, and paths:

```ini
[MY_DETAILS]
my_call = W9EN
contest = ARRL-FD
category_assisted = NON-ASSISTED
category_band = 15M
category_mode = CW
category_operator = SINGLE-OP
category_power = QRP
category_station = FIXED
category_time = 6-HOURS
category_transmitter = ONE
category_overlay = CLASSIC
certificate = NO
claimed_score = 0
club = 
email = john@w9en.com
grid_locator = DM43BS
location = AZ
name = John M. Belstner
address = 33636 N 86th St.
address_city = Scottsdale
address_state_province = AZ
address_postalcode = 85266
address_country = USA
operators = 
exch_sent = 1E AZ
xmtr_id = 0
soapbox = 

[CAT]
com_port = /dev/ttyUSB0
baudrate = 38400
freq_cmd = FA
band_cmd = BN
mode_cmd = MD
auto_con = True
```

---

## 🪟 Running the Application

Launch the main program:
```bash
python3 ContestLogBook.py
```

You’ll see the main GUI containing:
- **Recent Contacts** panel (top)
- **Statistics** panel (middle)
- **QSO Entry Form** (bottom)
- **Menu Bar** with options to connect, configure, export, and exit.

---

## 🧭 Typical Workflow

1. **Connect Services**  
   - From the *Connect* menu:  
     - “Connect CAT” → open serial link to your radio.

2. **Lookup a Callsign**  
   - Enter a callsign and hit **Tab**.  
   - The program fills date, time .

3. **Log a QSO**  
   - Verify date/time (UTC) and band/mode fields.  
   - Click **Log QSO** or keep hitting **Tab**.  
   - The entry is stored in `contest_log.db`.

4. **Review and Edit**  
   - The “Recent Contacts” list shows the latest QSOs.  
   - Enter/Select a QSO number and choose “Edit” or “Delete”.

5. **Export Cabrillo**  
   - Use the *File* menu to export logs for upload.

---

## 🧰 Developer Notes

- Database table: `logbook`
- Primary key: `rowid` (auto-incremented)
- Cabrillo fields follow Cabrillo Specification `3.0` standard.
- GUI uses only the built-in `tkinter` and `ttk` libraries—no extra dependencies.
- Pythonic modular design: each subsystem (Qso, CAT, Database) is isolated for clarity and testability.

---

## 🛠️ Troubleshooting

| Problem | Likely Cause | Solution |
|----------|---------------|-----------|
| Config window opens but fields are blank | Incorrect section/field name in `config.ini` | Ensure `[MY_DETAILS]`, `[CAT]`, etc. match code. |
| CAT connection fails | Wrong COM port or baud rate | Verify settings in *Settings → CAT Interface*. |

