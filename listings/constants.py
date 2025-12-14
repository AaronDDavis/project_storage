"""
Defines physical dimensions and location data for the inventory system.
"""

from decimal import Decimal

# Physical dimensions (in centimeters) for a standard shelf unit.
SHELF_LENGTH = 50
SHELF_WIDTH = 46
SHELF_HEIGHT = 42

# Define a comprehensive list of locations used throughout the system.
# Each tuple contains: (Short Code, Full Name, Associated Rate).
LOCATION_DEFS = [
    ("AMK", "Ang Mo Kio", Decimal("6.99")),
    ("BDK", "Bedok", Decimal("6.99")),
    ("BSH", "Bishan", Decimal("6.99")),
    ("BLY", "Boon Lay", Decimal("6.99")),
    ("BBK", "Bukit Batok", Decimal("6.99")),
    ("BMR", "Bukit Merah", Decimal("6.99")),
    ("BPN", "Bukit Panjang", Decimal("6.99")),
    ("BTM", "Bukit Timah", Decimal("6.99")),
    ("CWC", "Central Water Catchment", Decimal("6.99")),
    ("CGI", "Changi", Decimal("6.99")),
    ("CGB", "Changi Bay", Decimal("6.99")),
    ("CLE", "Clementi", Decimal("6.99")),
    ("DTC", "Downtown Core", Decimal("6.99")),
    ("GEY", "Geylang", Decimal("6.99")),
    ("HOU", "Hougang", Decimal("6.99")),
    ("JES", "Jurong East", Decimal("6.99")),
    ("JWS", "Jurong West", Decimal("6.99")),
    ("KLL", "Kallang", Decimal("6.99")),
    ("LCK", "Lim Chu Kang", Decimal("6.99")),
    ("MAN", "Mandai", Decimal("6.99")),
    ("MAE", "Marina East", Decimal("6.99")),
    ("MAS", "Marina South", Decimal("6.99")),
    ("MPA", "Marine Parade", Decimal("6.99")),
    ("MUS", "Museum", Decimal("6.99")),
    ("NEW", "Newton", Decimal("6.99")),
    ("NEI", "North-Eastern Islands", Decimal("6.99")),
    ("NOV", "Novena", Decimal("6.99")),
    ("ORC", "Orchard", Decimal("6.99")),
    ("OUT", "Outram", Decimal("6.99")),
    ("PBL", "Paya Lebar", Decimal("6.99")),
    ("PIO", "Pioneer", Decimal("6.99")),
    ("PGL", "Punggol", Decimal("6.99")),
    ("PRS", "Pasir Ris", Decimal("6.99")),
    ("QTN", "Queenstown", Decimal("6.99")),
    ("RVL", "River Valley", Decimal("6.99")),
    ("RCH", "Rochor", Decimal("6.99")),
    ("SEL", "Seletar", Decimal("6.99")),
    ("SBW", "Sembawang", Decimal("6.99")),
    ("SKG", "Sengkang", Decimal("6.99")),
    ("SRG", "Serangoon", Decimal("6.99")),
    ("SMP", "Simpang", Decimal("6.99")),
    ("SGR", "Singapore River", Decimal("6.99")),
    ("SIS", "Southern Islands", Decimal("6.99")),
    ("SKT", "Sungei Kadut", Decimal("6.99")),
    ("STV", "Straits View", Decimal("6.99")),
    ("TMP", "Tampines", Decimal("6.99")),
    ("TGL", "Tanglin", Decimal("6.99")),
    ("TGH", "Tengah", Decimal("6.99")),
    ("TPY", "Toa Payoh", Decimal("6.99")),
    ("TUA", "Tuas", Decimal("6.99")),
    ("WIS", "Western Islands", Decimal("6.99")),
    ("WWC", "Western Water Catchment", Decimal("6.99")),
    ("WDL", "Woodlands", Decimal("6.99")),
    ("YSH", "Yishun", Decimal("6.99")),
]
