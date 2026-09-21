# K-DATA HUB

A Django site for selling MTN, AirtelTigo and Telecel data bundles in Ghana.
Customers pick a bundle, pay through Paystack, and get SMS updates via Arkesel.

Live at <https://k-datahub.vercel.app/>.

## Apps

| App | What it holds |
|---|---|
| `orders` | The `Order` model, the checkout flow, order tracking, and the manager dashboard |
| `payments` | Paystack initialisation, callback and webhook handling |
| `accounts` | `CustomUser` (with `is_manager` / `is_agent`), manager login, profile |
| `kdatahub` | Settings, root URLs, the home page, SMS helpers, rate limiting |

## The price catalog

**All bundle prices live in one place: [`orders/catalog.py`](orders/catalog.py).**

The home page grid, the checkout dropdown and server-side price validation all
read from that table, so a price change is a one-line edit. Agent pricing is
derived from the retail price (`AGENT_MULTIPLIER`, currently 10% off) rather
than kept as a second list that can drift.

Prices are never read from the browser. `create_order` looks up `unit_price`
from the catalog using the submitted `item_name`; the checkout form has no
price field at all. If you add a field to that form, do not add the price back.

Clicking a bundle on the home page links to
`/orders/create/?package=10GB%20MTN`, which preselects it.

## Running it locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then fill in the values
python manage.py migrate
python manage.py createcachetable
python manage.py runserver
```

Leave `DATABASE_URL` empty to use the local SQLite database.

Create a manager account (the password is prompted for, never stored in a file):

```bash
python create_manager.py yourname you@example.com
```

## Tests

```bash
python manage.py test
```

The suite covers the things that must not regress: a buyer cannot set their own
price, unknown packages are rejected, the Paystack webhook refuses unsigned or
wrongly-priced callbacks and is idempotent, and guest orders are not readable by
other logged-in users.

## Environment variables

See [`.env.example`](.env.example) for the full list. These are required in
production, and the app refuses to start without the first two:

| Variable | Notes |
|---|---|
| `SECRET_KEY` | Generate with `python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"` |
| `ALLOWED_HOSTS` | Exact hostnames, comma separated, e.g. `k-datahub.vercel.app`. Wildcards like `.vercel.app` are deliberately not accepted — that namespace is open to anyone. |
| `DATABASE_URL` | Postgres connection string; falls back to SQLite when empty |
| `BASE_DOMAIN` | Used to build the Paystack callback URL, e.g. `https://k-datahub.vercel.app` |
| `PAYSTACK_PUBLIC_KEY`, `PAYSTACK_SECRET_KEY` | From the Paystack dashboard |
| `ARKESEL_API_KEY`, `SMS_SENDER_ID` | SMS delivery; without the key, messages print to the console instead of sending |
| `MANAGER_PHONE`, `ADMIN_PHONE` | Where order and traffic alerts go |

## Paystack

Set the webhook URL in the Paystack dashboard to:

```
https://k-datahub.vercel.app/payments/webhook/
```

The webhook verifies the `x-paystack-signature` HMAC against
`PAYSTACK_SECRET_KEY` and rejects anything unsigned with a 401, then re-verifies
the charge with Paystack and checks the amount and currency against the order
before marking it paid. It is safe to receive the same event twice.

## Deploying

Vercel builds from [`vercel.json`](vercel.json): `build_files.sh` installs
requirements and runs `collectstatic` into `staticfiles_build/`, and
`kdatahub/wsgi.py` serves everything else.

After the first deploy of a new environment, run `python manage.py migrate` and
`python manage.py createcachetable` against the production database. Without the
cache table the rate limiter fails open — nothing breaks, but login, checkout
and order-tracking throttling will not engage.
