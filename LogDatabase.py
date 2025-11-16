import sqlite3
from Qso import Qso


class LogDatabase:
    columns = ["row_id", "Freq", "Band", "Mode", "Date", "Time", "My_Call", "RST_Sent", "Exch_Sent", "Callsign", "RST_Rcvd", "Exch_Rcvd", "Xmtr_Id"]

    def __init__(self, config, appVersion="1.0"):
        self.db_file = "contest_log.db"
        self.table_name = "logbook"
        self.config = config
        self.appVersion = appVersion
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            rowid INTEGER PRIMARY KEY AUTOINCREMENT,
            Freq TEXT NOT NULL,
            Band TEXT NOT NULL,
            Mode TEXT NOT NULL,
            Date TEXT NOT NULL,
            Time TEXT NOT NULL,
            My_Call TEXT NOT NULL,
            RST_Sent TEXT,
            Exch_Sent TEXT NOT NULL,
            Callsign TEXT NOT NULL,
            RST_Rcvd TEXT,
            Exch_Rcvd TEXT NOT NULL,
            Xmtr_Id TEXT NOT NULL
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
    
    def update_config(self, config):
        self.config = config

    def get_current_row_count(self):
        count_sql = f'SELECT COUNT(*) FROM {self.table_name};'
        self.cursor.execute(count_sql)
        count = self.cursor.fetchone()[0]
        if count is None:
            return 0  # Table is empty
        return count

    def get_last_rowid(self):
        last_id_sql = f'SELECT rowid FROM {self.table_name} ORDER BY rowid DESC LIMIT 1;'
        self.cursor.execute(last_id_sql)
        result = self.cursor.fetchone()
        if result is None:
            return 0 # No rows in table 
        return result[0]

    def get_current_stats(self):
        # Get total count
        count_sql = f"SELECT COUNT(*) FROM {self.table_name};"
        self.cursor.execute(count_sql)
        count_all = self.cursor.fetchone()[0]
        if count_all is None:
            count_all = 0
        # Get CW count
        count_cw_sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE Mode='CW';"
        self.cursor.execute(count_cw_sql)
        count_cw = self.cursor.fetchone()[0]
        if count_cw is None:
            count_cw = 0
        # Get Phone count
        count_phone_sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE Mode IN ('SSB','AM','FM');"
        self.cursor.execute(count_phone_sql)
        count_phone = self.cursor.fetchone()[0]
        if count_phone is None:
            count_phone = 0
        # Get DIGI count
        count_digi_sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE Mode='DIGI';"
        self.cursor.execute(count_digi_sql)
        count_digi = self.cursor.fetchone()[0]
        if count_digi is None:
            count_digi = 0
        # Get Last Hour Rate
        count_hour_sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE Date GLOB '????????' AND Time GLOB '????' AND julianday( substr(Date,1,4) || '-' || substr(Date,5,2) || '-' || substr(Date,7,2) || ' ' || substr(Time,1,2) || ':' || substr(Time,3,2) || ':00') >= julianday('now','-1 hour');"
        self.cursor.execute(count_hour_sql)
        count_hour = self.cursor.fetchone()[0]
        if count_hour is None:
            count_hour = 0
        return count_all, count_cw, count_phone, count_digi, count_hour

    def insert_qso(self, qso: Qso):
        insert_sql = f'''
        INSERT INTO {self.table_name} (Freq, Band, Mode, Date, Time, My_Call, RST_Sent, Exch_Sent, Callsign, RST_Rcvd, Exch_Rcvd, Xmtr_Id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        '''
        self.cursor.execute(insert_sql, (qso.freq, qso.band, qso.mode, qso.date, qso.time, qso.my_call, qso.rst_sent, qso.exch_sent, qso.callsign, qso.rst_rcvd, qso.exch_rcvd, qso.xmtr_id))
        self.conn.commit()

    def update_qso(self, qso: Qso):
        update_sql = f'''
        UPDATE {self.table_name}
        SET Freq = ?, Band = ?, Mode = ?, Date = ?, Time = ?, My_Call = ?, RST_Sent = ?, Exch_Sent = ?, Callsign = ?, RST_Rcvd = ?, Exch_Rcvd = ?, Xmtr_Id = ?
        WHERE rowid = ?;
        '''
        self.cursor.execute(update_sql, (qso.freq, qso.band, qso.mode, qso.date, qso.time, qso.my_call, qso.rst_sent, qso.exch_sent, qso.callsign, qso.rst_rcvd, qso.exch_rcvd, qso.xmtr_id, qso.qso_id))
        self.conn.commit()  

    def fetch_qso_by_id(self, qso_id):
        fetch_sql = f'SELECT * FROM {self.table_name} WHERE rowid = ?;'
        self.cursor.execute(fetch_sql, (qso_id,))
        return self.cursor.fetchone()
    
    def delete_qso(self, qso_id):
        delete_sql = f'DELETE FROM {self.table_name} WHERE rowid = ?;'
        self.cursor.execute(delete_sql, (qso_id,))
        self.conn.commit()

    def fetch_all_qsos(self):
        fetch_sql = f'SELECT * FROM {self.table_name};'
        self.cursor.execute(fetch_sql)
        return self.cursor.fetchall()
    
    def export_to_cabrillo(self, cbr_file, appVersion="1.0"):
        try:
            with open(cbr_file, 'w') as f:
                # Write ADIF header
                f.write(f"START-OF-LOG: 3.0\n")
                f.write(f"CONTEST: {self.config['MY_DETAILS'].get('contest_id','')}\n")
                f.write(f"CALLSIGN: {self.config['MY_DETAILS'].get('my_call','')}\n")
                f.write(f"LOCATION: {self.config['MY_DETAILS'].get('location','')}\n")
                f.write(f"CATEGORY-OPERATOR: {self.config['MY_DETAILS'].get('category_operator','')}\n")
                f.write(f"CATEGORY-ASSISTED: {self.config['MY_DETAILS'].get('category_assisted','')}\n")
                f.write(f"CATEGORY-BAND: {self.config['MY_DETAILS'].get('category_band','')}\n")
                f.write(f"CATEGORY-POWER: {self.config['MY_DETAILS'].get('category_power','')}\n")
                f.write(f"CATEGORY-MODE: {self.config['MY_DETAILS'].get('category_mode','')}\n")
                f.write(f"CATEGORY-TRANSMITTER: {self.config['MY_DETAILS'].get('category_transmitter','')}\n")
                f.write(f"CATEGORY-OVERLAY: {self.config['MY_DETAILS'].get('category_overlay','')}\n")
                f.write(f"GRID-LOCATOR: {self.config['MY_DETAILS'].get('grid_locator','')}\n")
                f.write(f"CLAIMED-SCORE: {self.config['MY_DETAILS'].get('claimed_score','')}\n")
                f.write(f"CLUB: {self.config['MY_DETAILS'].get('club','')}\n")
                f.write(f"CREATED-BY: ContestLogBook v{self.appVersion}\n")
                f.write(f"NAME: {self.config['MY_DETAILS'].get('name','')}\n")
                f.write(f"ADDRESS: {self.config['MY_DETAILS'].get('address_street','')}\n")
                f.write(f"ADDRESS-CITY: {self.config['MY_DETAILS'].get('address_city','')}\n")
                f.write(f"ADDRESS-STATE-PROVINCE: {self.config['MY_DETAILS'].get('address_state_province','')}\n")
                f.write(f"ADDRESS-POSTALCODE: {self.config['MY_DETAILS'].get('address_postalcode','')}\n")
                f.write(f"ADDRESS-COUNTRY: {self.config['MY_DETAILS'].get('address_country','')}\n")
                f.write(f"OPERATORS: {self.config['MY_DETAILS'].get('operators','')}\n")
                f.write(f"SOAPBOX: {self.config['MY_DETAILS'].get('soapbox','')}\n")

                # Write each QSO
                for row in self.fetch_all_qsos():
                    qso = Qso(
                        qso_id=row[self.columns.index("row_id")],
                        freq=row[self.columns.index("Freq")],
                        band=row[self.columns.index("Band")],
                        mode=row[self.columns.index("Mode")],
                        date=row[self.columns.index("Date")],
                        time=row[self.columns.index("Time")],
                        my_call=row[self.columns.index("My_Call")],
                        rst_sent=row[self.columns.index("RST_Sent")],
                        exch_sent=row[self.columns.index("Exch_Sent")],
                        callsign=row[self.columns.index("Callsign")],
                        rst_rcvd=row[self.columns.index("RST_Rcvd")],
                        exch_rcvd=row[self.columns.index("Exch_Rcvd")],
                        xmtr_id=row[self.columns.index("Xmtr_Id")]
                    )
                    f.write(qso.to_cabrillo())

                f.write(f"END-OF-LOG:\n")
        except Exception as e:
            return False, str(e)
    
        return True, "Export successful"


    def close(self):
        self.conn.close()