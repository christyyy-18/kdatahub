"""Single source of truth for the data bundles K-DATA HUB sells.

The home page price grid, the order form and server-side price validation all
read from here, so a price only ever has to be changed in one place and a buyer
can never dictate what they pay.

``item_name`` keys keep the historic ``"<N>GB <Carrier>"`` shape (``10GB MTN``)
so existing Order rows and Order.carrier keep working unchanged.
"""

from decimal import Decimal, ROUND_HALF_UP

# Agents pay 10% less than the retail price.
AGENT_MULTIPLIER = Decimal('0.90')

# (internal name, label shown on the site, css class used by the price grid)
CARRIERS = [
    ('MTN', 'MTN', 'mtn'),
    ('Airtel', 'Airtel / AT', 'airtel'),
    ('Telecel', 'Telecel', 'telecel'),
]

# (carrier, volume in GB, retail price in GHS)
PACKAGES = [
    ('MTN', 1, '6.00'),
    ('MTN', 2, '12.00'),
    ('MTN', 3, '18.00'),
    ('MTN', 4, '23.00'),
    ('MTN', 5, '28.00'),
    ('MTN', 6, '33.00'),
    ('MTN', 8, '43.00'),
    ('MTN', 10, '50.00'),
    ('MTN', 12, '60.00'),
    ('MTN', 15, '75.00'),
    ('MTN', 20, '96.00'),
    ('MTN', 25, '116.00'),
    ('MTN', 30, '137.00'),
    ('MTN', 40, '180.00'),
    ('MTN', 50, '215.00'),
    ('MTN', 100, '420.00'),

    ('Airtel', 2, '10.00'),
    ('Airtel', 3, '15.00'),
    ('Airtel', 4, '18.00'),
    ('Airtel', 5, '23.00'),
    ('Airtel', 6, '28.00'),
    ('Airtel', 8, '35.00'),
    ('Airtel', 10, '45.00'),
    ('Airtel', 12, '50.00'),
    ('Airtel', 15, '65.00'),
    ('Airtel', 20, '80.00'),
    ('Airtel', 30, '95.00'),
    ('Airtel', 40, '105.00'),
    ('Airtel', 50, '120.00'),
    ('Airtel', 80, '165.00'),
    ('Airtel', 100, '195.00'),
    ('Airtel', 200, '350.00'),

    ('Telecel', 5, '26.00'),
    ('Telecel', 10, '47.00'),
    ('Telecel', 15, '70.00'),
    ('Telecel', 20, '90.00'),
    ('Telecel', 30, '135.00'),
    ('Telecel', 40, '180.00'),
]

# The largest number of a single bundle one order may contain.
MAX_QUANTITY = 10


def package_key(carrier, volume_gb):
    """The item_name stored on an Order, e.g. ``10GB MTN``."""
    return f'{volume_gb}GB {carrier}'


def _quantize(amount):
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


# Built once at import: {item_name: (carrier, volume_gb, retail price)}
_BY_KEY = {
    package_key(carrier, volume): (carrier, volume, Decimal(price))
    for carrier, volume, price in PACKAGES
}


def get_price(item_name, is_agent=False):
    """Retail (or agent) price for a package, or None if we do not sell it."""
    entry = _BY_KEY.get(item_name)
    if entry is None:
        return None
    price = entry[2]
    if is_agent:
        price = _quantize(price * AGENT_MULTIPLIER)
    return price


def is_valid_package(item_name):
    return item_name in _BY_KEY


def catalog_for(is_agent=False):
    """Packages grouped by carrier, ready to render in a template."""
    groups = []
    for carrier, label, css_class in CARRIERS:
        packages = []
        for entry_carrier, volume, _ in PACKAGES:
            if entry_carrier != carrier:
                continue
            key = package_key(carrier, volume)
            packages.append({
                'key': key,
                'carrier': carrier,
                'volume_gb': volume,
                'volume_label': f'{volume} GB',
                'price': get_price(key, is_agent=is_agent),
                'css_class': css_class,
            })
        groups.append({
            'carrier': carrier,
            'label': label,
            'css_class': css_class,
            'packages': packages,
        })
    return groups


def price_map(is_agent=False):
    """{item_name: "12.00"} for the order form's running total."""
    return {key: str(get_price(key, is_agent=is_agent)) for key in _BY_KEY}
