#!/usr/bin/env python3
import configparser
from Qso import Qso
from Cat import Cat
from Cat import bands, modes
from LastQSOs import LastQSOs
from UdpSocket import UdpSocket
from ConfigWindow import ConfigWindow
from LogDatabase import LogDatabase as Db
from pathlib import Path
from datetime import datetime, timezone
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


appVersion = "0.5"
app = Tk()
app.title('Contest Log Book by W9EN - v' + appVersion)

POLL_INTERVAL_MS = 2000  # Update the Radio Settings periodically (if connected)

# Some global variables
band_var = StringVar(app)
band_var.set(bands[0]) # default value

mode_var = StringVar(app)
mode_var.set(modes[0]) # default value

sections = ["CT", "EMA", "ME", "NH", "RI", "VT", "WMA", 
            "ENY", "NLI", "NNJ", "NNY", "SNJ", "WNY", 
            "DE", "EPA", "MDC", "WPA", 
            "AL", "GA", "KY", "NC", "NFL", "SC", "SFL", "TN", "VA", "WCF", "PR", "VI",
            "AR", "LA", "MS", "NM", "NTX", "OK", "STX", "WTX",
            "EB", "LAX", "ORG", "SB", "SCV", "SDG", "SF", "SJV", "SV", "PAC",
            "AK", "AZ", "EWA", "ID", "MT", "NV", "OR", "UT", "WWA", "WY",
            "MI", "OH", "WV",
            "IL", "IN", "WI",
            "CO", "IA", "KS", "MN", "MO", "NE", "ND", "SD",
            "AB", "BC", "GH", "MB", "NB", "NL", "NS", "ONE", "ONN", "ONS", "PE", "QC", "SK", "TER",
            "DX"]
sections_var = StringVar(app)
sections_var.set(sections[0]) # default value

cat_connected = False
cat = None

udp_socket = None
multi_station_enabled = False


# Application exit function
def app_exit():
    close = messagebox.askyesno("Exit?", "Are you sure you want to exit the application?", parent=app)
    if close:
        ldb.close()
        if cat and cat_connected:
            cat.disconnect()
        if udp_socket:
            udp_socket.stop()
        app.destroy()

app.protocol("WM_DELETE_WINDOW", app_exit)


# Message box functions
def showInfo(message):
    response = messagebox.showinfo("Status", message, parent=app)
    return response

def showWarning(message):
    response = messagebox.showwarning("Warning", message, parent=app)
    return response

def showError(message):
    response = messagebox.showerror("Error", message, parent=app)
    return response


# A basic type-to-complete behavior for a ttk.Combobox in state='normal'
def attach_autocomplete_to_combobox(cb, values):
    type_buffer = {"last": 0}

    def on_keyrelease(event):
        # Ignore nav/control keys so we don't fight the user
        if event.keysym in ("BackSpace","Left","Right","Home","End","Up","Down",
                            "Return","Escape","Tab"):
            return

        typed = cb.get()
        if not typed:
            return

        # Find first prefix match
        match = next((v for v in values if v.lower().startswith(typed.lower())), None)
        if match:
            cb.set(match)
            # put the cursor after what the user typed, and select the remainder
            cb.icursor(len(typed))
            cb.select_range(len(typed), "end")

    cb.bind("<KeyRelease>", on_keyrelease)


# To accommodate custom <Tab> order
def focus_next_widget(event, next_widget):
    next_widget.focus_set()
    return "break"  # prevent default tab behavior


# Read config file
config = configparser.ConfigParser()
config_file = 'config.ini'
if Path(config_file).exists():
    config.read(config_file)
else:
    showError("No config file found. Please create a config.ini file.")


# Open the Log Database
if 'MY_DETAILS' in config:
    ldb = Db(config, appVersion)
else:
    showWarning("Config file is missing MY_DETAILS. Please update the config.ini file.")
    ldb = Db()  # Use default values


# Initialize Multi-Station UDP if enabled
def enable_disable_multi_station():
    global udp_socket, multi_station_enabled
    multi_station_enabled = config.getboolean('MULTI_TX', 'enabled', fallback=False)
    if multi_station_enabled:
        multicast_group = config['MULTI_TX'].get('multicast_group', fallback='239.2.3.1')
        multicast_port = config['MULTI_TX'].getint('multicast_port', fallback=6969)
        interface_ip = config['MULTI_TX'].get('interface_ip', fallback=None)
        if udp_socket is None:
            udp_socket = UdpSocket(multicast_group, multicast_port, log_qso_from_udp, interface_ip)
            udp_socket.start()
    else:
        if udp_socket:
            udp_socket.stop()
            udp_socket = None


# Root view
previewFrame = LabelFrame(app, text="Recent Contacts", padx=5, pady=5)
previewFrame.grid(row=0, column=0, padx=5, pady=5)  # Set the frame position

statsFrame = LabelFrame(app, text="Statistics", padx=5, pady=5)
statsFrame.grid(row=1, column=0, padx=5, pady=5)  # Set the frame position
minColumnWidth = 106
statsFrame.grid_columnconfigure(0, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(1, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(2, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(3, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(4, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(5, minsize=minColumnWidth)
statsFrame.grid_columnconfigure(6, minsize=minColumnWidth)

qsoFrame = LabelFrame(app, text="QSO Entry", padx=5, pady=5)
qsoFrame.grid(row=2, column=0, padx=5, pady=5)  # Set the frame position
minColumnWidth = 106
qsoFrame.grid_columnconfigure(0, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(1, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(2, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(3, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(4, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(5, minsize=minColumnWidth)
qsoFrame.grid_columnconfigure(6, minsize=minColumnWidth)

# Statistics Frame
count_all, count_cw, count_phone, count_digi, count_hour = ldb.get_current_stats()

totalQsoLabel = Label(statsFrame, text="QSO Total")
totalQsoLabel.grid(row=0, column=0, padx=5, pady=5)
totalQsoValue = Label(statsFrame, text=str(count_all))
totalQsoValue.grid(row=1, column=0, padx=5, pady=5)

totalCwLabel = Label(statsFrame, text="CW")
totalCwLabel.grid(row=0, column=1, padx=5, pady=5)
totalCwValue = Label(statsFrame, text=str(count_cw))
totalCwValue.grid(row=1, column=1, padx=5, pady=5)

totalPhoneLabel = Label(statsFrame, text="Phone")
totalPhoneLabel.grid(row=0, column=2, padx=5, pady=5)
totalPhoneValue = Label(statsFrame, text=str(count_phone))
totalPhoneValue.grid(row=1, column=2, padx=5, pady=5)

totalDigiLabel = Label(statsFrame, text="DIGI")
totalDigiLabel.grid(row=0, column=3, padx=5, pady=5)
totalDigiValue = Label(statsFrame, text=str(count_digi))
totalDigiValue.grid(row=1, column=3, padx=5, pady=5)

lastHourRateLabel = Label(statsFrame, text="Rate (Last Hr)")
lastHourRateLabel.grid(row=0, column=4, padx=5, pady=5)
lastHourRateValue = Label(statsFrame, text=str(count_hour))
lastHourRateValue.grid(row=1, column=4, padx=5, pady=5)

# QSO Entry Frame
qsoNumberLabel = Label(qsoFrame, text="QSO")  # Create a label widget
qsoNumberLabel.grid(row=0, column=0)  # Put the label into the window
qsoNumberEntry = Entry(qsoFrame, width=10, borderwidth=2)  # Create an input box
qsoNumberEntry.grid(row=1, column=0)  # Set the input box

callsignLabel = Label(qsoFrame, text="Callsign")  # Create a label widget
callsignLabel.grid(row=0, column=1)  # Put the label into the window
callsignEntry = Entry(qsoFrame, width=10, borderwidth=2)  # Create an input box
callsignEntry.grid(row=1, column=1)  # Set the input box position

exchRcvdLabel = Label(qsoFrame, text="Exchange Rcvd")  # Create a label widget
exchRcvdLabel.grid(row=0, column=2, columnspan=2)  # Put the label into the window
exchRcvdEntry = Entry(qsoFrame, width=24, borderwidth=2)  # Create an input box
exchRcvdEntry.grid(row=1, column=2,columnspan=2)  # Set the input box position

freqLabel = Label(qsoFrame, text="Freq MHz")  # Create a label widget
freqLabel.grid(row=0, column=4)  # Put the label into the window
freqEntry = Entry(qsoFrame, width=10, borderwidth=2)  # Create an input box
freqEntry.grid(row=1, column=4)  # Set the input box position

bandLabel = Label(qsoFrame, text="Band")  # Create a label widget
bandLabel.grid(row=0, column=5)  # Put the label into the window
bandMenu = ttk.Combobox(qsoFrame, textvariable=band_var, values=bands, state="normal")
bandMenu.grid(row=1, column=5, padx=5, pady=5)
bandMenu.config(width=9)
attach_autocomplete_to_combobox(bandMenu, bands)

modeLabel = Label(qsoFrame, text="Mode")  # Create a label widget
modeLabel.grid(row=0, column=6)  # Put the label into the window
modeMenu = ttk.Combobox(qsoFrame, textvariable=mode_var, values=modes, state="normal")
modeMenu.grid(row=1, column=6, padx=5, pady=5)
modeMenu.config(width=9)
attach_autocomplete_to_combobox(modeMenu, modes)

dateLabel = Label(qsoFrame, text="Date")  # Create a label widget
dateLabel.grid(row=2, column=0)  # Put the label into the window
dateEntry = Entry(qsoFrame, width=10, borderwidth=2)  # Create an input box
dateEntry.grid(row=3, column=0)  # Set the input box position

timeLabel = Label(qsoFrame, text="Time")  # Create a label widget
timeLabel.grid(row=2, column=1)  # Put the label into the window
timeEntry = Entry(qsoFrame, width=10, borderwidth=2)  # Create an input box
timeEntry.grid(row=3, column=1)  # Set the input box position

exchSentLabel = Label(qsoFrame, text="Exchange Sent")  # Create a label widget
exchSentLabel.grid(row=2, column=2, columnspan=2)  # Put the label into the window
exchSentEntry = Entry(qsoFrame, width=24, borderwidth=2)  # Create an input box
exchSentEntry.grid(row=3, column=2,columnspan=2)  # Set the input box position


# CAT Connect
def cat_connect():
    global cat_connected, cat
    # Check if already connected
    if cat and cat_connected:
        showInfo("Already connected to CAT")
        return
    config.read(config_file)
    try:
        cat = Cat(config)
        cat_connected = cat.connect()
        if cat_connected:
            showInfo(f"Successfully connected {cat._com_port} at {cat._baudrate} baud.")
        else:
            showError(f"Failed to connect on {cat._com_port}.")
    except Exception as e:
        showError(f"An error occurred during CAT connection: {str(e)}")

# Update the exchange sent
def update_exch_sent():
    exch_sent = config["MY_DETAILS"].get("exch_sent", "")
    if '<qso>' in exch_sent:
        qso_number = qsoNumberEntry.get().strip()
        exch_sent = exch_sent.replace('<qso>', qso_number)
    exchSentEntry.delete(0, END)
    exchSentEntry.insert(0, exch_sent)
 
# Menu functions
def export_log():
    cbr_file = filedialog.asksaveasfilename(initialdir=".", title="Save .cbr File", defaultextension=".cbr", filetypes=(("Cabrillo files", "*.cbr"), ("all files", "*.*")))
    # Create a popup telling the user that the imporexport is in progress
    popup = Toplevel(app)
    popup.title("Exporting Log")
    Label(popup, text="Exporting log in Cabrillo format, please wait...").pack(padx=20, pady=20)
    app.update_idletasks()  # Ensure the popup is drawn before starting the export

    success, reason = ldb.export_to_cabrillo(cbr_file, appVersion)
    popup.destroy()  # Close the popup after export is done
    if success:
        showInfo("Log exported successfully.")
    else:
        showError(f"Failed to export log: {reason}")


def config_settings():
    global qrz_logged_in, qrz, cat_connected, cat
    dlg = ConfigWindow(app, config)
    app.wait_window(dlg.top)
    # If CAT was connected, reconnect with new settings
    if cat and cat_connected:
        if config.getboolean('CAT', 'auto_con', fallback=False):
            if cat.reload_config(config):
                showInfo(f"Successfully reconnected {cat._com_port} at {cat._baudrate} baud.")
            else:
                showError(f"Failed to reconnect on {cat._com_port}.")
        else:
            cat.disconnect()
            cat_connected = False
            showInfo("CAT disconnected due to configuration change.")
    # If CAT was not connected, check if auto connect is now enabled
    elif config.getboolean('CAT', 'auto_con', fallback=False):
        cat_connect()
    # Update grid_locator in the database if it was changed
    if 'MY_DETAILS' in config:
        ldb.update_config(config)
        update_exch_sent()
    else:
        showWarning("Config file is missing [MY_DETAILS]. Please update the config.ini file.")
    # Enable or disable multi-station UDP
    enable_disable_multi_station()


# Create the File menu
menubar = Menu(app)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="Export Cabrillo", command=export_log)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app_exit)
menubar.add_cascade(label="File", menu=file_menu)

# Create the Connect menu
connect_menu = Menu(menubar, tearoff=0)
connect_menu.add_command(label="Connect CAT", command=cat_connect)
menubar.add_cascade(label="Connect", menu=connect_menu)

# Create the Config menu
config_menu = Menu(menubar, tearoff=0)
config_menu.add_command(label="Settings", command=config_settings)
menubar.add_cascade(label="Config", menu=config_menu)


# Update the QSO number to the next available
def display_qso_number(id: int):
    qsoNumberEntry.delete(0, END)
    qsoNumberEntry.insert(0, str(id))


# Recent Contacts Frame
last_qsos = LastQSOs(previewFrame, ldb.conn, display_qso_number)
last_qsos.pack(fill="both", expand=True)
last_qsos.refresh()


# Button function (Clear)
def clear_entries():
    display_qso_number(ldb.get_last_rowid() + 1)
    last_qsos.refresh()
    callsignEntry.delete(0, END)
    exchRcvdEntry.delete(0, END)
    # Keep previous freq, band and mode selections
    #freqEntry.delete(0, END)
    #freqEntry.insert(0, "")
    #band_var.set(bands[0])
    #mode_var.set(modes[0])
    dateEntry.delete(0, END)
    timeEntry.delete(0, END)
    update_exch_sent()    
    callsignEntry.focus_set()


# Periodic CAT update
def update_radio_settings():
    if cat and cat_connected:
        try:
            freq, band, mode = cat.get_freq_band_mode()
            freqEntry.delete(0, END)
            freqEntry.insert(0, freq)
            band_var.set(band)
            mode_var.set(mode)
        except Exception as e:
            showError(f"An error occurred while updating radio settings: {str(e)}")
    app.after(POLL_INTERVAL_MS, update_radio_settings)


# Update the statistics display
def update_statistics():
    count_all, count_cw, count_phone, count_digi, count_hour = ldb.get_current_stats()
    totalQsoValue.config(text=str(count_all))
    totalCwValue.config(text=str(count_cw))
    totalPhoneValue.config(text=str(count_phone))
    totalDigiValue.config(text=str(count_digi))
    lastHourRateValue.config(text=str(count_hour))


# Lookup function
def lookup_call(event=None):
    callsignEntry_value = callsignEntry.get().strip().upper()
    if callsignEntry_value == "":
        showWarning("Please enter a callsign.")
        callsignEntry.focus_set()
        return "break"
    callsignEntry.delete(0, END)
    callsignEntry.insert(0, callsignEntry_value)
    try:
        current_time = datetime.now(timezone.utc)
        dateEntry.delete(0, END)
        dateEntry.insert(0, current_time.strftime('%Y-%m-%d'))
        timeEntry.delete(0, END)
        timeEntry.insert(0, current_time.strftime('%H%M'))

        if cat_connected:
            freq, band, mode = cat.get_freq_band_mode()
            freqEntry.delete(0, END)
            freqEntry.insert(0, freq)
            band_var.set(band)
            mode_var.set(mode)
        else:
            freq = freqEntry.get().strip()
            band = band_var.get()
            mode = mode_var.get()

        if last_qsos.lookup(callsignEntry_value, band, mode):
            showWarning(f"Duplicate QSO for {callsignEntry_value}")
            callsignEntry.focus_set()
            return "break"

        exchRcvdEntry.focus_set()
        return "break"

    except Exception as e:
        showError(f"An error occurred callsign lookup: {str(e)}")


# Button function (Log QSO)
def log_qso(event=None):
    new_qso = Qso(
        qso_id = qsoNumberEntry.get().strip(),
        freq=freqEntry.get().strip(),
        band = band_var.get(),
        mode = mode_var.get(),
        date = dateEntry.get().strip(),
        time = timeEntry.get().strip(),
        my_call = config['MY_DETAILS']['my_call'].upper() if 'MY_DETAILS' in config and 'my_call' in config['MY_DETAILS'] else '',
        exch_sent = exchSentEntry.get().strip().upper(),
        callsign = callsignEntry.get().strip().upper(),
        exch_rcvd = exchRcvdEntry.get().strip().upper(),
        xmtr_id = config['MY_DETAILS']['xmtr_id'] if 'MY_DETAILS' in config and 'xmtr_id' in config['MY_DETAILS'] else ''
    )

    if not new_qso.is_valid():
        showWarning("Please fill in at least Callsign, Date, Time, Band and Mode fields.")
        return
    try:
        if int(new_qso.qso_id) > ldb.get_last_rowid():
            ldb.insert_qso(new_qso)
            #showInfo(f"QSO with {new_qso.callsign} logged successfully.")
        else:
            ldb.update_qso(new_qso)
            #showInfo(f"QSO ID {new_qso.qso_id} updated successfully.")

        # Send QSO to other stations if multi-station is enabled
        if multi_station_enabled and udp_socket:
            udp_socket.send(new_qso.to_string())

    except Exception as e:
        showError(f"An error occurred while logging the QSO: {str(e)}")

    clear_entries()
    update_statistics()
    return "break"  # Prevent default behavior
    

# Function to log QSO received via UDP
def log_qso_from_udp(cbr_text, addr, ts):
    """
    Handler called from UDP thread. Schedules database operations
    to run in the main thread to avoid SQLite threading issues.
    """
    def _do_insert():
        try:
            new_qso = Qso.from_string(cbr_text)
            if new_qso.is_valid():
                ldb.insert_qso(new_qso)
                display_qso_number(ldb.get_last_rowid() + 1)
                last_qsos.refresh()
                update_statistics()
            else:
                print(f"Received invalid QSO data from {addr}, ignoring.")
        except Exception as e:
            print(f"An error occurred while logging the QSO from {addr}: {str(e)}")

    # Schedule the database operation to run in the main thread
    app.after(0, _do_insert)


def next_qso_in_db():
    display_qso_number(ldb.get_last_rowid() + 1)
    

def load_qso_from_db():
    rowid = qsoNumberEntry.get().strip()
    if rowid == "":
        showWarning("Please enter a QSO number to load.")
        return
    try:
        qso = ldb.fetch_qso_by_id(rowid)
        if qso is None:
            showWarning(f"No QSO found with ID {rowid}.")
            return
        callsignEntry.delete(0, END)
        callsignEntry.insert(0, qso[Db.columns.index("Callsign")])
        exchRcvdEntry.delete(0, END)
        exchRcvdEntry.insert(0, qso[Db.columns.index("Exch_Rcvd")])
        freqEntry.delete(0, END)
        freqEntry.insert(0, qso[Db.columns.index("Freq")])
        band_var.set(qso[Db.columns.index("Band")])
        mode_var.set(qso[Db.columns.index("Mode")])
        dateEntry.delete(0, END)
        dateEntry.insert(0, qso[Db.columns.index("Date")])
        timeEntry.delete(0, END)
        timeEntry.insert(0, qso[Db.columns.index("Time")])
        exchSentEntry.delete(0, END)
        exchSentEntry.insert(0, qso[Db.columns.index("Exch_Sent")])
    except Exception as e:
        showError(f"An error occurred while loading QSO: {str(e)}")


def delete_qso_from_db():
    rowid = qsoNumberEntry.get().strip()
    if rowid == "":
        showWarning("Please enter a QSO number to delete.")
        return
    try:
        qso = ldb.fetch_qso_by_id(rowid)
        if qso is None:
            showWarning(f"No QSO found with ID {rowid}.")
            return
        confirm = messagebox.askyesno("Delete QSO Entry", f"Are you sure you want to delete QSO ID {rowid}?", parent=app)
        if confirm:
            ldb.delete_qso(rowid)
            showInfo(f"QSO ID {rowid} has been deleted.")
            clear_entries()
    except Exception as e:
        showError(f"An error occurred while deleting QSO: {str(e)}")


# Buttons
logButton = Button(qsoFrame, text="Log QSO", command=log_qso)
logButton.grid(row=4, column=0, padx=5, pady=5)
logButton.config(width=8)
logButton.bind("<Return>", lambda e: log_qso())

clearButton = Button(qsoFrame, text="Clear", command=clear_entries)
clearButton.grid(row=4, column=1, padx=5, pady=5)
clearButton.config(width=8)
clearButton.bind("<Return>", lambda e: clear_entries())

nextButton = Button(qsoFrame, text="Next", command=next_qso_in_db)
nextButton.grid(row=4, column=4, padx=5, pady=5)
nextButton.config(width=8)
nextButton.bind("<Return>", lambda e: next_qso_in_db())

loadButton = Button(qsoFrame, text="Edit", command=load_qso_from_db)
loadButton.grid(row=4, column=5, padx=5, pady=5)
loadButton.config(width=8)
loadButton.bind("<Return>", lambda e: load_qso_from_db())

deleteButton = Button(qsoFrame, text="Delete", command=delete_qso_from_db)
deleteButton.grid(row=4, column=6, padx=5, pady=5)
deleteButton.config(width=8)
deleteButton.bind("<Return>", lambda e: delete_qso_from_db())


# Set the focus order when <Tab> is pressed
callsignEntry.bind("<Tab>", lambda e: lookup_call(e))
exchRcvdEntry.bind("<Tab>", lambda e: focus_next_widget(e, logButton))
callsignEntry.focus_set()


# Configure the menu bar
app.config(menu=menubar)

# Load initial data
display_qso_number(ldb.get_last_rowid() + 1)
update_exch_sent()
update_statistics()

app.attributes('-topmost', True)
app.update()

# Check auto connect and auto upload settings
if config.getboolean('CAT', 'auto_con', fallback=False):
    cat_connect()

# Enable or disable multi-station UDP
enable_disable_multi_station()

# Start periodic CAT updates
#app.after(POLL_INTERVAL_MS, update_radio_settings)

# Keep the window open
app.mainloop()
