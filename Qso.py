
class Qso:
    def __init__(self, qso_id, freq="", band="", mode="", date="", time="", my_call="", exch_sent="", callsign="", exch_rcvd="", xmtr_id=""):
        self.qso_id = qso_id
        self.freq = freq
        self.band = band
        self.mode = mode
        self.date = date
        self.time = time
        self.my_call = my_call
        self.exch_sent = exch_sent
        self.callsign = callsign
        self.exch_rcvd = exch_rcvd
        self.xmtr_id = xmtr_id
    
    def is_valid(self):
        if self.qso_id == "" or not self.qso_id.isdigit() or self.callsign == "" or self.date == "" or self.time == "" or self.band == "" or self.mode == "" or self.exch_rcvd == "":
            return False
        return True

    def mode_to_cabrillo(self):
        mode_map = {
            "SSB": "PH",
            "CW": "CW",
            "RTTY": "RY",
            "FT8": "DG",
            "FT4": "DG",
            "PSK31": "DG",
            "PSK63": "DG",
            "JT65": "DG",
            "JT9": "DG",
            "FM": "FM",
            "AM": "PH"
        }
        return mode_map.get(self.mode.upper(), "PH")  # Default to PH if mode not found
    
    def freq_to_cabrillo(self):
        freq_map = {
            "160M": str(int(float(self.freq) * 1000)),
             "80M": str(int(float(self.freq) * 1000)),
             "40M": str(int(float(self.freq) * 1000)),
             "20M": str(int(float(self.freq) * 1000)),
             "15M": str(int(float(self.freq) * 1000)),
             "10M": str(int(float(self.freq) * 1000)),
              "6M": "50",
              "2M": "144",
             "222": "222",
             "432": "432",
             "902": "902",
            "1.2G": "1.2G",
            "2.3G": "2.3G",
            "3.4G": "3.4G",
            "5.7G": "5.7G",
             "10G": "10G",
             "24G": "24G",
             "47G": "47G",
             "75G": "75G",
            "122G": "122G",
            "134G": "134G",
            "241G": "241G"
        }
        return freq_map.get(self.band.upper(), "14000")  # Default to 20M if not found
 
    def freq_to_band(self):
       # Derive band from frequency (in kHz)
        try:
            freq_khz = int(self.freq)
            if 1800 <= freq_khz < 2000:
                self.band = "160M"
            elif 3500 <= freq_khz < 4000:
                self.band = "80M"
            elif 5330 <= freq_khz < 5405:
                self.band = "60M"
            elif 7000 <= freq_khz < 7300:
                self.band = "40M"
            elif 10100 <= freq_khz < 10150:
                self.band = "30M"
            elif 14000 <= freq_khz < 14350:
                self.band = "20M"
            elif 18068 <= freq_khz < 18168:
                self.band = "17M"
            elif 21000 <= freq_khz < 21450:
                self.band = "15M"
            elif 24890 <= freq_khz < 24990:
                self.band = "12M"
            elif 28000 <= freq_khz < 29700:
                self.band = "10M"
            elif 50000 <= freq_khz < 54000:
                self.band = "6M"
            elif 144000 <= freq_khz < 148000:
                self.band = "2M"
            elif 222000 <= freq_khz < 225000:
                self.band = "222"
            elif 420000 <= freq_khz < 450000:
                self.band = "432"
            else:
                self.band = "20M"  # Default fallback
        except (ValueError, IndexError):
            self.band = "20M"  # Default fallback

    def to_cabrillo(self):
        cbr_str = f"QSO: "
        if self.freq:
            cbr_str += f"{self.freq_to_cabrillo()} "
        if self.mode:
            cbr_str += f"{self.mode_to_cabrillo()} "
        if self.date:
            cbr_str += f"{self.date} "
        if self.time:
            cbr_str += f"{self.time} "
        if self.my_call:
            cbr_str += f"{self.my_call} "
        if self.exch_sent:
            cbr_str += f"{self.exch_sent} "
        if self.callsign:
            cbr_str += f"{self.callsign} "
        if self.exch_rcvd:
            cbr_str += f"{self.exch_rcvd} "
        if self.xmtr_id:
            cbr_str += f"{self.xmtr_id} "
        cbr_str += "\n"
        return cbr_str

    def to_string(self):
        return f"{self.qso_id},{self.freq},{self.band},{self.mode},{self.date},{self.time},{self.my_call},{self.exch_sent},{self.callsign},{self.exch_rcvd},{self.xmtr_id})"
    
    @staticmethod
    def from_string(qso_str):
        parts = qso_str.strip().split(",")
        if len(parts) != 11:
            raise ValueError("Invalid QSO string format")
        return Qso(
            qso_id=parts[0],
            freq=parts[1],
            band=parts[2],
            mode=parts[3],
            date=parts[4],
            time=parts[5],
            my_call=parts[6],
            exch_sent=parts[7],
            callsign=parts[8],
            exch_rcvd=parts[9],
            xmtr_id=parts[10]
        )