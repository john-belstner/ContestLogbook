# ConfigWindow.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import configparser


contests = ["ARRL-10", "ARRL-10-GHZ", "ARRL-160", "ARRL-DIGI", "ARRL-DX-CW", "ARRL-DX-SSB", "ARRL-EME", "ARRL-FD", "ARRL-SS-CW", "ARRL-SS-SSB",
            "BARTG-RTTY", "CQ-160-CW", "CQ-160-SSB", "CQ-WPX-CW", "CQ-WPX-RTTY", "CQ-WPX-SSB", "CQ-VHF-SSBCW", "CQ-VHF-DIGI", "CQ-WW-CW", "CQ-WW-RTTY", "CQ-WW-SSB",
            "IARU-HF", "NAQP-CW", "NAQP-SSB", "NAQP-RTTY", "RDXC", "RSGB-IOTA", "SPDXC", "SPDXC-RTTY", "TARA-RTTY", "WAG", "WW-DIGI"]
category_assisteds = ["ASSISTED", "NON-ASSISTED"]
category_bands = ["ALL", "160M", "80M", "40M", "20M", "15M", "10M", "6M", "2M", "222", "432", "902", "1.2G", "2.3G", "3.4G", "5.7G", "10G", "24G", "47G", "75G", "122G", "134G", "241G",
                  "Light", "VHF-3-BAND", "VHF-FM-ONLY"]
category_modes = ["CW", "DIGI", "FM", "RTTY", "SSB", "MIXED"]
category_operators = ["SINGLE-OP", "MULTI-OP", "CHECKLOG"]
category_powers = ["HIGH", "LOW", "QRP"]
category_stations = ["DISTRIBUTED", "FIXED", "MOBILE", "PORTABLE", "ROVER", "ROVER-LIMITED", "ROVER-UNLIMITED", "EXPEDITION", "HQ", "SCHOOL", "EXPLORER"]
category_times = ["6-HOURS", "8-HOURS", "12-HOURS", "24-HOURS"]
category_transmitters = ["ONE", "TWO", "LIMITED", "UNLIMITED", "SWL"]
category_overlays = ["CLASSIC", "ROOKIE", "TB-WIRES", "YOUTH", "NOVICE-TECH", "YL"]
certificates = ["YES", "NO"]
locations = ["CT", "EMA", "ME", "NH", "RI", "VT", "WMA", 
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


class ConfigWindow:

    def __init__(self, parent, config: configparser.ConfigParser):
        self.parent = parent
        self.config = config
        self.top = Toplevel(parent)
        self.top.title("Configuration Settings")
        self.top.transient(parent) # stay on top of parent
        self.contests_var = StringVar(self.top)
        self.contests_var.set(contests[0]) # default value
        self.category_assisteds_var = StringVar(self.top)
        self.category_assisteds_var.set(category_assisteds[0]) # default value
        self.category_bands_var = StringVar(self.top)
        self.category_bands_var.set(category_bands[0]) # default value
        self.category_modes_var = StringVar(self.top)
        self.category_modes_var.set(category_modes[0]) # default value
        self.category_operators_var = StringVar(self.top)
        self.category_operators_var.set(category_operators[0]) # default value
        self.category_powers_var = StringVar(self.top)
        self.category_powers_var.set(category_powers[0]) # default value
        self.category_stations_var = StringVar(self.top)
        self.category_stations_var.set(category_stations[0]) # default value
        self.category_times_var = StringVar(self.top)
        self.category_times_var.set(category_times[0]) # default value
        self.category_transmitters_var = StringVar(self.top)
        self.category_transmitters_var.set(category_transmitters[0]) # default value
        self.category_overlays_var = StringVar(self.top)
        self.category_overlays_var.set(category_overlays[0]) # default value
        self.certificates_var = StringVar(self.top)
        self.certificates_var.set(certificates[0]) # default value
        self.locations_var = StringVar(self.top)
        self.locations_var.set(locations[0]) # default value
        self.top.grab_set()        # modal
        self._build_ui()


    # A basic type-to-complete behavior for a ttk.Combobox in state='normal'
    def attach_autocomplete_to_combobox(self, cb, values):
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


    def save_config(self):
        # Write to config file
        self.config['MY_DETAILS']['my_call'] = self.myCallEntry.get().strip().upper()
        self.config['MY_DETAILS']['contest'] = self.contests_var.get().strip().upper()
        self.config['MY_DETAILS']['category_assisted'] = self.category_assisteds_var.get().strip().upper()
        self.config['MY_DETAILS']['category_band'] = self.category_bands_var.get().strip().upper()
        self.config['MY_DETAILS']['category_mode'] = self.category_modes_var.get().strip().upper()
        self.config['MY_DETAILS']['category_operator'] = self.category_operators_var.get().strip().upper()
        self.config['MY_DETAILS']['category_power'] = self.category_powers_var.get().strip().upper()
        self.config['MY_DETAILS']['category_station'] = self.category_stations_var.get().strip().upper()
        self.config['MY_DETAILS']['category_time'] = self.category_times_var.get().strip().upper()
        self.config['MY_DETAILS']['category_transmitter'] = self.category_transmitters_var.get().strip().upper()
        self.config['MY_DETAILS']['category_overlay'] = self.category_overlays_var.get().strip().upper()
        self.config['MY_DETAILS']['certificate'] = self.certificates_var.get().strip().upper()
        self.config['MY_DETAILS']['claimed_score'] = self.claimedScoreEntry.get().strip()
        self.config['MY_DETAILS']['club'] = self.clubEntry.get().strip()
        self.config['MY_DETAILS']['email'] = self.emailEntry.get().strip()
        self.config['MY_DETAILS']['grid_locator'] = self.gridLocatorEntry.get().strip().upper()
        self.config['MY_DETAILS']['location'] = self.locations_var.get().strip().upper()
        self.config['MY_DETAILS']['name'] = self.nameEntry.get().strip()
        self.config['MY_DETAILS']['address'] = self.addressEntry.get().strip()
        self.config['MY_DETAILS']['address_city'] = self.addressCityEntry.get().strip()
        self.config['MY_DETAILS']['address_state_province'] = self.addressStateProvinceEntry.get().strip()
        self.config['MY_DETAILS']['address_postalcode'] = self.addressPostalCodeEntry.get().strip()
        self.config['MY_DETAILS']['address_country'] = self.addressCountryEntry.get().strip()
        self.config['MY_DETAILS']['operators'] = self.operatorsEntry.get().strip()
        self.config['MY_DETAILS']['exch_sent'] = self.myExchangeEntry.get().strip()
        self.config['MY_DETAILS']['xmtr_id'] = self.xmtrIdEntry.get().strip()
 
        self.config['CAT']['com_port'] = self.comPortEntry.get().strip()
        self.config['CAT']['baudrate'] = self.baudrateEntry.get().strip()
        self.config['CAT']['freq_cmd'] = self.freqCmdEntry.get().strip()
        self.config['CAT']['band_cmd'] = self.bandCmdEntry.get().strip()
        self.config['CAT']['mode_cmd'] = self.modeCmdEntry.get().strip()
        self.config['CAT']['auto_con'] = str(self.autoConCatVar.get())
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        messagebox.showinfo("Settings Saved", "Configuration settings have been saved.", parent=self.top)
        self.top.destroy()


    def _build_ui(self):
        self.detailsFrame = LabelFrame(self.top, text="My Details", padx=5, pady=5)
        self.detailsFrame.grid(row=0, column=0, padx=5, pady=5)

        self.myCallLabel = Label(self.detailsFrame, text="CALLSIGN:")
        self.myCallLabel.grid(row=0, column=0, sticky=W)
        self.myCallEntry = Entry(self.detailsFrame, width=20)
        self.myCallEntry.grid(row=0, column=1, padx=5, pady=2, sticky=W)
        self.myCallEntry.insert(0, self.config.get('MY_DETAILS', 'my_call', fallback=""))

        self.contestLabel = Label(self.detailsFrame, text="CONTEST:")
        self.contestLabel.grid(row=1, column=0, sticky=W)
        self.contestMenu = ttk.Combobox(self.detailsFrame, textvariable=self.contests_var, values=contests, state="normal")
        self.contestMenu.grid(row=1, column=1, padx=5, pady=5)
        self.contestMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, contests)
        self.contests_var.set(self.config.get('MY_DETAILS', 'contest', fallback=contests[0]))

        self.categoryAssistedLabel = Label(self.detailsFrame, text="CATEGORY-ASSISTED:")
        self.categoryAssistedLabel.grid(row=2, column=0, sticky=W)
        self.categoryAssistedMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_assisteds_var, values=category_assisteds, state="normal")
        self.categoryAssistedMenu.grid(row=2, column=1, padx=5, pady=5)
        self.categoryAssistedMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_assisteds)
        self.category_assisteds_var.set(self.config.get('MY_DETAILS', 'category_assisted', fallback=category_assisteds[0]))

        self.categoryBandLabel = Label(self.detailsFrame, text="CATEGORY-BAND:")
        self.categoryBandLabel.grid(row=3, column=0, sticky=W)
        self.categoryBandMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_bands_var, values=category_bands, state="normal")
        self.categoryBandMenu.grid(row=3, column=1, padx=5, pady=5)
        self.categoryBandMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_bands)
        self.category_bands_var.set(self.config.get('MY_DETAILS', 'category_band', fallback=category_bands[0]))

        self.categoryModeLabel = Label(self.detailsFrame, text="CATEGORY-MODE:")
        self.categoryModeLabel.grid(row=4, column=0, sticky=W)
        self.categoryModeMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_modes_var, values=category_modes, state="normal")
        self.categoryModeMenu.grid(row=4, column=1, padx=5, pady=5)
        self.categoryModeMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_modes)
        self.category_modes_var.set(self.config.get('MY_DETAILS', 'category_mode', fallback=category_modes[0]))

        self.categoryOperatorLabel = Label(self.detailsFrame, text="CATEGORY-OPERATOR:")
        self.categoryOperatorLabel.grid(row=5, column=0, sticky=W)
        self.categoryOperatorMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_operators_var, values=category_operators, state="normal")
        self.categoryOperatorMenu.grid(row=5, column=1, padx=5, pady=5)
        self.categoryOperatorMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_operators)
        self.category_operators_var.set(self.config.get('MY_DETAILS', 'category_operator', fallback=category_operators[0]))

        self.categoryPowerLabel = Label(self.detailsFrame, text="CATEGORY-POWER:")
        self.categoryPowerLabel.grid(row=6, column=0, sticky=W)
        self.categoryPowerMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_powers_var, values=category_powers, state="normal")
        self.categoryPowerMenu.grid(row=6, column=1, padx=5, pady=5)
        self.categoryPowerMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_powers)
        self.category_powers_var.set(self.config.get('MY_DETAILS', 'category_power', fallback=category_powers[0]))

        self.categoryStationLabel = Label(self.detailsFrame, text="CATEGORY-STATION:")
        self.categoryStationLabel.grid(row=7, column=0, sticky=W)
        self.categoryStationMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_stations_var, values=category_stations, state="normal")
        self.categoryStationMenu.grid(row=7, column=1, padx=5, pady=5)
        self.categoryStationMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_stations)
        self.category_stations_var.set(self.config.get('MY_DETAILS', 'category_station', fallback=category_stations[0]))

        self.categoryTimeLabel = Label(self.detailsFrame, text="CATEGORY-TIME:")
        self.categoryTimeLabel.grid(row=8, column=0, sticky=W)
        self.categoryTimeMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_times_var, values=category_times, state="normal")
        self.categoryTimeMenu.grid(row=8, column=1, padx=5, pady=5)
        self.categoryTimeMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_times)
        self.category_times_var.set(self.config.get('MY_DETAILS', 'category_time', fallback=category_times[0]))

        self.categoryTransmitterLabel = Label(self.detailsFrame, text="CATEGORY-TRANSMITTER:")
        self.categoryTransmitterLabel.grid(row=9, column=0, sticky=W)
        self.categoryTransmitterMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_transmitters_var, values=category_transmitters, state="normal")
        self.categoryTransmitterMenu.grid(row=9, column=1, padx=5, pady=5)
        self.categoryTransmitterMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_transmitters)
        self.category_transmitters_var.set(self.config.get('MY_DETAILS', 'category_transmitter', fallback=category_transmitters[0]))

        self.categoryOverlayLabel = Label(self.detailsFrame, text="CATEGORY-OVERLAY:")
        self.categoryOverlayLabel.grid(row=10, column=0, sticky=W)
        self.categoryOverlayMenu = ttk.Combobox(self.detailsFrame, textvariable=self.category_overlays_var, values=category_overlays, state="normal")
        self.categoryOverlayMenu.grid(row=10, column=1, padx=5, pady=5)
        self.categoryOverlayMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, category_overlays)
        self.category_overlays_var.set(self.config.get('MY_DETAILS', 'category_overlay', fallback=category_overlays[0]))

        self.certificateLabel = Label(self.detailsFrame, text="CERTIFICATE:")
        self.certificateLabel.grid(row=11, column=0, sticky=W)
        self.certificateMenu = ttk.Combobox(self.detailsFrame, textvariable=self.certificates_var, values=certificates, state="normal")
        self.certificateMenu.grid(row=11, column=1, padx=5, pady=5)
        self.certificateMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.contestMenu, certificates)
        self.certificates_var.set(self.config.get('MY_DETAILS', 'certificate', fallback=certificates[0]))

        self.claimedScoreLabel = Label(self.detailsFrame, text="CLAIMED-SCORE:")
        self.claimedScoreLabel.grid(row=12, column=0, sticky=W)
        self.claimedScoreEntry = Entry(self.detailsFrame, width=20)
        self.claimedScoreEntry.grid(row=12, column=1, padx=5, pady=2, sticky=W)
        self.claimedScoreEntry.insert(0, self.config.get('MY_DETAILS', 'claimed_score', fallback=""))

        self.clubLabel = Label(self.detailsFrame, text="CLUB:")       
        self.clubLabel.grid(row=13, column=0, sticky=W)
        self.clubEntry = Entry(self.detailsFrame, width=20)
        self.clubEntry.grid(row=13, column=1, padx=5, pady=2, sticky=W)
        self.clubEntry.insert(0, self.config.get('MY_DETAILS', 'club', fallback=""))

        self.emailLabel = Label(self.detailsFrame, text="EMAIL:")       
        self.emailLabel.grid(row=14, column=0, sticky=W)
        self.emailEntry = Entry(self.detailsFrame, width=20)
        self.emailEntry.grid(row=14, column=1, padx=5, pady=2, sticky=W)
        self.emailEntry.insert(0, self.config.get('MY_DETAILS', 'email', fallback=""))

        self.gridLocatorLabel = Label(self.detailsFrame, text="GRID-LOCATOR:")       
        self.gridLocatorLabel.grid(row=15, column=0, sticky=W)
        self.gridLocatorEntry = Entry(self.detailsFrame, width=20)
        self.gridLocatorEntry.grid(row=15, column=1, padx=5, pady=2, sticky=W)
        self.gridLocatorEntry.insert(0, self.config.get('MY_DETAILS', 'grid_locator', fallback=""))

        self.locationLabel = Label(self.detailsFrame, text="LOCATION:")       
        self.locationLabel.grid(row=16, column=0, sticky=W)
        self.locationMenu = ttk.Combobox(self.detailsFrame, textvariable=self.locations_var, values=locations, state="normal")
        self.locationMenu.grid(row=16, column=1, padx=5, pady=5)
        self.locationMenu.config(width=20)
        self.attach_autocomplete_to_combobox(self.locationMenu, locations)
        self.locations_var.set(self.config.get('MY_DETAILS', 'location', fallback=locations[0]))

        self.nameLabel = Label(self.detailsFrame, text="NAME:")       
        self.nameLabel.grid(row=17, column=0, sticky=W)
        self.nameEntry = Entry(self.detailsFrame, width=20)
        self.nameEntry.grid(row=17, column=1, padx=5, pady=2, sticky=W)
        self.nameEntry.insert(0, self.config.get('MY_DETAILS', 'name', fallback=""))

        self.addressLabel = Label(self.detailsFrame, text="ADDRESS:")       
        self.addressLabel.grid(row=18, column=0, sticky=W)
        self.addressEntry = Entry(self.detailsFrame, width=20)
        self.addressEntry.grid(row=18, column=1, padx=5, pady=2, sticky=W)
        self.addressEntry.insert(0, self.config.get('MY_DETAILS', 'address', fallback=""))

        self.addressCityLabel = Label(self.detailsFrame, text="ADDRESS-CITY:")       
        self.addressCityLabel.grid(row=19, column=0, sticky=W)
        self.addressCityEntry = Entry(self.detailsFrame, width=20)
        self.addressCityEntry.grid(row=19, column=1, padx=5, pady=2, sticky=W)
        self.addressCityEntry.insert(0, self.config.get('MY_DETAILS', 'address_city', fallback=""))

        self.addressStateProvinceLabel = Label(self.detailsFrame, text="ADDRESS-STATE-PROVINCE:")       
        self.addressStateProvinceLabel.grid(row=20, column=0, sticky=W)
        self.addressStateProvinceEntry = Entry(self.detailsFrame, width=20)
        self.addressStateProvinceEntry.grid(row=20, column=1, padx=5, pady=2, sticky=W)
        self.addressStateProvinceEntry.insert(0, self.config.get('MY_DETAILS', 'address_state_province', fallback=""))

        self.addressPostalCodeLabel = Label(self.detailsFrame, text="ADDRESS-POSTALCODE:")       
        self.addressPostalCodeLabel.grid(row=21, column=0, sticky=W)
        self.addressPostalCodeEntry = Entry(self.detailsFrame, width=20)
        self.addressPostalCodeEntry.grid(row=21, column=1, padx=5, pady=2, sticky=W)
        self.addressPostalCodeEntry.insert(0, self.config.get('MY_DETAILS', 'address_postalcode', fallback=""))

        self.addressCountryLabel = Label(self.detailsFrame, text="ADDRESS-COUNTRY:")       
        self.addressCountryLabel.grid(row=22, column=0, sticky=W)
        self.addressCountryEntry = Entry(self.detailsFrame, width=20)
        self.addressCountryEntry.grid(row=22, column=1, padx=5, pady=2, sticky=W)
        self.addressCountryEntry.insert(0, self.config.get('MY_DETAILS', 'address_country', fallback=""))

        self.operatorsLabel = Label(self.detailsFrame, text="OPERTORS:")       
        self.operatorsLabel.grid(row=23, column=0, sticky=W)
        self.operatorsEntry = Entry(self.detailsFrame, width=20)
        self.operatorsEntry.grid(row=23, column=1, padx=5, pady=2, sticky=W)
        self.operatorsEntry.insert(0, self.config.get('MY_DETAILS', 'operators', fallback=""))

        self.myExchangeLabel = Label(self.detailsFrame, text="EXCH-SENT:")       
        self.myExchangeLabel.grid(row=24, column=0, sticky=W)
        self.myExchangeEntry = Entry(self.detailsFrame, width=20)
        self.myExchangeEntry.grid(row=24, column=1, padx=5, pady=2, sticky=W)
        self.myExchangeEntry.insert(0, self.config.get('MY_DETAILS', 'exch_sent', fallback=""))

        self.xmtrIdLabel = Label(self.detailsFrame, text="XMTR-ID:")       
        self.xmtrIdLabel.grid(row=25, column=0, sticky=W)
        self.xmtrIdEntry = Entry(self.detailsFrame, width=20)
        self.xmtrIdEntry.grid(row=25, column=1, padx=5, pady=2, sticky=W)
        self.xmtrIdEntry.insert(0, self.config.get('MY_DETAILS', 'xmtr_id', fallback=""))

        self.soapboxLabel = Label(self.detailsFrame, text="SOAPBOX:")       
        self.soapboxLabel.grid(row=26, column=0, sticky=W)
        self.soapboxEntry = Entry(self.detailsFrame, width=20)
        self.soapboxEntry.grid(row=26, column=1, padx=5, pady=2, sticky=W)
        self.soapboxEntry.insert(0, self.config.get('MY_DETAILS', 'soapbox', fallback=""))


        self.catFrame = LabelFrame(self.top, text="CAT Interface Settings", padx=5, pady=5)
        self.catFrame.grid(row=0, column=1, padx=5, pady=5)  # Set the frame position

        self.comPortLabel = Label(self.catFrame, text="COM Port:")
        self.comPortLabel.grid(row=0, column=0, sticky=W)
        self.comPortEntry = Entry(self.catFrame, width=20)
        self.comPortEntry.grid(row=0, column=1, padx=5, pady=2)
        self.comPortEntry.insert(0, self.config.get('CAT', 'com_port', fallback=""))

        self.baudrateLabel = Label(self.catFrame, text="Baudrate:")
        self.baudrateLabel.grid(row=1, column=0, sticky=W)
        self.baudrateEntry = Entry(self.catFrame, width=20)
        self.baudrateEntry.grid(row=1, column=1, padx=5, pady=2)
        self.baudrateEntry.insert(0, self.config.get('CAT', 'baudrate', fallback=""))

        self.freqCmdLabel = Label(self.catFrame, text="Freq Cmd:")
        self.freqCmdLabel.grid(row=2, column=0, sticky=W)
        self.freqCmdEntry = Entry(self.catFrame, width=20)
        self.freqCmdEntry.grid(row=2, column=1, padx=5, pady=2)
        self.freqCmdEntry.insert(0, self.config.get('CAT', 'freq_cmd', fallback=""))

        self.bandCmdLabel = Label(self.catFrame, text="Band Cmd:")
        self.bandCmdLabel.grid(row=3, column=0, sticky=W)
        self.bandCmdEntry = Entry(self.catFrame, width=20)
        self.bandCmdEntry.grid(row=3, column=1, padx=5, pady=2)
        self.bandCmdEntry.insert(0, self.config.get('CAT', 'band_cmd', fallback=""))

        self.modeCmdLabel = Label(self.catFrame, text="Mode Cmd:")
        self.modeCmdLabel.grid(row=4, column=0, sticky=W)
        self.modeCmdEntry = Entry(self.catFrame, width=20)
        self.modeCmdEntry.grid(row=4, column=1, padx=5, pady=2)
        self.modeCmdEntry.insert(0, self.config.get('CAT', 'mode_cmd', fallback=""))

        auto_con_cat = self.config.getboolean('CAT', 'auto_con', fallback=False)
        self.autoConCatVar = BooleanVar(value=auto_con_cat)
        self.autoConCatCheck = Checkbutton(
            self.catFrame,
            text="Autoconnect to CAT",
            variable=self.autoConCatVar,
            onvalue=True,
            offvalue=False
        )
        self.autoConCatCheck.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))

        self.saveButton = Button(self.top, text="Save", command=self.save_config)
        self.saveButton.grid(row=1, column=0, columnspan=2, pady=10) # Centered below all frames

        self.top.protocol("WM_DELETE_WINDOW", self._config_exit)


    def _config_exit(self):
        close = messagebox.askyesno("Quit?", "Are you sure you want to quit without saving?", parent=self.top)
        if close:
            self.top.destroy()

