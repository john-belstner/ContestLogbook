# CwopsRoster.py
import csv
from pathlib import Path


class CwopsRoster:
    """
    Loads the CWops roster CSV and provides callsign lookup for CWT contests.
    Returns the member's name and number for pre-filling exchange received.
    """

    def __init__(self, csv_path: str = None):
        """
        Initialize the roster by loading the CSV file.

        Args:
            csv_path: Path to the CWops roster CSV file. If None, looks for
                      'Shareable CWops data - Roster.csv' in /tmp.
        """
        self._roster = {}  # callsign -> (name, number)

        if csv_path is None:
            csv_path = Path('/tmp') / 'Shareable CWops data - Roster.csv'
        else:
            csv_path = Path(csv_path)

        if csv_path.exists():
            self._load_csv(csv_path)

    def _load_csv(self, csv_path: Path):
        """Load the roster from the CSV file."""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                # Skip header row
                next(reader, None)

                for row in reader:
                    if len(row) >= 4:
                        # CSV columns: (empty), Callsign, Number, Name, ...
                        callsign = row[1].strip().upper()
                        number = row[2].strip()
                        name = row[3].strip()

                        if callsign and number and name:
                            self._roster[callsign] = (name, number)
        except Exception as e:
            print(f"Error loading CWops roster: {e}")

    def lookup(self, callsign: str) -> str:
        """
        Look up a callsign in the roster.

        Args:
            callsign: The callsign to look up (case-insensitive)

        Returns:
            Exchange string "NAME NUMBER" if found, None otherwise
        """
        callsign = callsign.strip().upper()
        if callsign in self._roster:
            name, number = self._roster[callsign]
            return f"{name} {number}"
        return None

    def get_member_count(self) -> int:
        """Return the number of members loaded in the roster."""
        return len(self._roster)
