
class Qso:
    def __init__(self, qso_id, freq="", band="", mode="", date="", time="", my_call="", rst_sent="", exch_sent="", callsign="", rst_rcvd="", exch_rcvd="", xmtr_id=""):
        self.qso_id = qso_id
        self.freq = freq
        self.band = band
        self.mode = mode
        self.date = date
        self.time = time
        self.my_call = my_call
        self.rst_sent = rst_sent
        self.exch_sent = exch_sent
        self.callsign = callsign
        self.rst_rcvd = rst_rcvd
        self.exch_rcvd = exch_rcvd
        self.xmtr_id = xmtr_id
    
    def is_valid(self):
        if self.qso_id == "" or not self.qso_id.isdigit() or self.callsign == "" or self.date == "" or self.time == "" or self.band == "" or self.mode == "":
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
        if self.rst_sent:
            cbr_str += f"{self.rst_sent} "
        if self.exch_sent:
            cbr_str += f"{self.exch_sent} "
        if self.callsign:
            cbr_str += f"{self.callsign} "
        if self.rst_rcvd:
            cbr_str += f"{self.rst_rcvd} "
        if self.exch_rcvd:
            cbr_str += f"{self.exch_rcvd} "
        if self.xmtr_id:
            cbr_str += f"{self.xmtr_id} "
        cbr_str += "\n"
        return cbr_str
