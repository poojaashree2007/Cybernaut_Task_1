import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ============================================================
# CRYPTOCURRENCY PRICE TRACKER
# ============================================================

URL = "https://coinmarketcap.com/"


# ============================================================
# 1. CHROME OPTIONS
# ============================================================

options = Options()

# Keep Chrome visible
# This helps us see whether Chrome is opening correctly.
options.add_argument("--start-maximized")

# Stability options
options.add_argument("--disable-notifications")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

# Use a separate temporary Chrome profile
# This prevents conflicts with an already-open Chrome profile.
options.add_argument("--user-data-dir=C:/crypto_tracker_chrome")


# ============================================================
# 2. START CHROME
# ============================================================

print("Starting Chrome...")

driver = None

try:

    driver = webdriver.Chrome(options=options)

    print("Chrome started successfully.")

    # ========================================================
    # 3. OPEN COINMARKETCAP
    # ========================================================

    print("Opening CoinMarketCap...")

    driver.get(URL)

    print("Website requested successfully.")

    # Give the website time to load
    time.sleep(8)

    # ========================================================
    # 4. CHECK PAGE
    # ========================================================

    print("Checking page...")

    print("Page title:")
    print(driver.title)

    print()

    print("Current URL:")
    print(driver.current_url)

    # ========================================================
    # 5. GET TABLES
    # ========================================================

    print()
    print("Searching for cryptocurrency table...")

    tables = driver.find_elements("tag name", "table")

    print("Tables found:", len(tables))

    # ========================================================
    # 6. EXTRACT DATA
    # ========================================================

    crypto_data = []

    if len(tables) > 0:

        table = tables[0]

        rows = table.find_elements(
            "css selector",
            "tbody tr"
        )

        print("Rows found:", len(rows))

        for row in rows:

            try:

                cells = row.find_elements(
                    "tag name",
                    "td"
                )

                if len(cells) < 5:
                    continue

                values = []

                for cell in cells:

                    text = cell.text.strip()

                    values.append(text)


                # --------------------------------------------
                # Rank
                # --------------------------------------------

                rank = values[0]


                # --------------------------------------------
                # Cryptocurrency name
                # --------------------------------------------

                name = ""

                links = row.find_elements(
                    "tag name",
                    "a"
                )

                for link in links:

                    text = link.text.strip()

                    if text:

                        name = text

                        break


                # --------------------------------------------
                # Symbol
                # --------------------------------------------

                symbol = ""

                paragraphs = row.find_elements(
                    "tag name",
                    "p"
                )

                for paragraph in paragraphs:

                    text = paragraph.text.strip()

                    if text:

                        symbol = text

                        break


                # --------------------------------------------
                # Find price
                # --------------------------------------------

                price = ""

                for value in values:

                    if "$" in value:

                        price = value

                        break


                # --------------------------------------------
                # Find percentage change
                # --------------------------------------------

                change = ""

                for value in values:

                    if "%" in value:

                        change = value

                        break


                # --------------------------------------------
                # Market cap
                # --------------------------------------------

                market_cap = ""

                dollar_values = []

                for value in values:

                    if "$" in value:

                        dollar_values.append(value)


                if len(dollar_values) >= 2:

                    market_cap = dollar_values[0]


                # --------------------------------------------
                # Add cryptocurrency
                # --------------------------------------------

                if name != "":

                    crypto_data.append({

                        "Rank": rank,

                        "Cryptocurrency": name,

                        "Symbol": symbol,

                        "Price": price,

                        "24H Change": change,

                        "Market Cap": market_cap

                    })


                # Stop after 10
                if len(crypto_data) >= 10:

                    break


            except Exception:

                continue


    # ========================================================
    # 7. CREATE DATAFRAME
    # ========================================================

    df = pd.DataFrame(crypto_data)


    # ========================================================
    # 8. DISPLAY RESULT
    # ========================================================

    print()
    print("=" * 80)
    print("          CRYPTOCURRENCY PRICE TRACKER")
    print("=" * 80)

    if not df.empty:

        print()
        print("TOP 10 CRYPTOCURRENCIES")
        print()

        print(
            df.to_string(index=False)
        )

    else:

        print()
        print("No cryptocurrency table was found.")
        print()
        print("The browser opened, but CoinMarketCap")
        print("did not provide the table to Selenium.")


except Exception as error:

    print()
    print("=" * 80)
    print("ERROR")
    print("=" * 80)

    print(error)

    print()
    print("Chrome could not be controlled correctly.")


finally:

    # ========================================================
    # 9. CLOSE BROWSER
    # ========================================================

    if driver is not None:

        try:

            driver.quit()

        except:

            pass

    print()
    print("Program finished.")