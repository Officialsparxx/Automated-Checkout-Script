# Automated Checkout Script

A lightweight Python script to automatically check and purchase out-of-stock items on retail sites like Target using Selenium and undetected-chromedriver.

---

## 🚀 Features

* **Undetectable Browser**: Leverages `undetected-chromedriver` to mask automation fingerprints.
* **Realistic Polling**: Randomized refresh intervals and stealthed user-agents.
* **Bot-Throttle Detection**: Recognizes and backs off when Target shows the "This item is not available" banner.
* **Badge Verification**: Confirms successful add-to-cart by reading the cart icon badge.
* **Interactive Login**: Pauses for manual login (30s by default) and supports on-the-fly login during checkout.
* **Fault Tolerance**: Wrapped in a top-level exception handler to keep the console open on errors.

---

## 🧰 Prerequisites

* Python 3.10+
* Google Chrome (stable) installed
* **Dependencies**

  ```bash
  pip install setuptools undetected-chromedriver
  ```
  ```bash
  pip install selenium
  ```

---

## ⚙️ Configuration

1. **Clone the repo**:

   ```bash
   git clone https://github.com/<your-username>/Target-Automated-Checkout.git
   cd Target-Automated-Checkout
   ```

2. **Environment Variables**:
   Create a `.env` file in the project root:

   ```ini
   TARGET_EMAIL=you@example.com
   TARGET_PASSWORD=SuperSecret123
   TARGET_URL=https://www.target.com/p/YOUR-PRODUCT-SLUG
   ```

3. **Load `.env`**:
   At the top of `checkout.py`, add:

   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   EMAIL    = os.getenv("TARGET_EMAIL")
   PASSWORD = os.getenv("TARGET_PASSWORD")
   URL      = os.getenv("TARGET_URL")

   if not all([EMAIL, PASSWORD, URL]):
       raise RuntimeError("Set TARGET_EMAIL, TARGET_PASSWORD, and TARGET_URL in .env")
   ```

---

## ▶️ Usage

```bash
python checkout.py
```

1. Chrome will launch (in "undetected" mode).
2. You have 30 seconds to log into your Target account.
3. The script polls your configured product page until the "Add to cart" button is live.
4. Clicks "Add to cart", verifies via cart badge, and navigates to checkout.
5. If prompted, enters credentials again during checkout.

---

## 🛠️ Customization

* **Polling Interval**: Adjust `time.sleep(random.uniform(2.5, 4.0))` in the script.
* **Back-off Window**: Tweak the throttle delay (`10–15s`) when Target flags bot-like behavior.
* **User-Agents**: Extend the `user_agents` list for more variation.

---

## 📦 Packaging & CLI

Next steps:

* Convert to a CLI with `argparse` for multiple URLs
* Package as an installable module with `setup.py`
* Add proxy rotation support (e.g., residential pool)

---

## 🤝 Contributing

Pull requests welcome! Please open an issue to discuss your ideas.


