# CardFlow: the story

*[VISA] = shown in the Visa data (`ml_readiness/` notebooks), [EXT] = GUS / NBP / Gemius, [SIM] = simulation assumption.
The Visa data are synthetic, so the figures illustrate the method.*

## 1. People pay by card in shops, but not online

Poles tap their Visa card every day at the grocery store, yet when they shop online the card is rarely the first
choice: BLIK dominates Polish e-commerce **[EXT]**. The Visa data show the same gap from the inside: **36% of active
cards never made a single online card payment in 18 months** **[VISA]**, and in categories such as clothing or books
card payments capture only a fraction of what GUS reports as online sales **[VISA + EXT]**.

## 2. Why: paying online by card means typing the card number

The Visa data point to one clear reason. **45% of online card payments are a typed card number** instead of a saved
card, and this share is **growing** **[VISA]**. The most digital customers suffer most: people who pay by phone in the
shop type their 16 digits and CVV **on a phone** in half of their online payments **[VISA]**. And this friction decides
the future: when a customer's first online payment is one-click, **45% keep paying online by card; after a typed first
payment only 31% do** **[VISA]**. Today **7 out of 10 first online payments of a new card are typed** **[VISA]**.

## 3. Solution: Visa QR Pay

Every Visa card gets a QR code. At checkout the customer scans it and approves the payment on the phone: no card
number, no CVV. Because most typing happens on phones **[VISA]**, the QR must live not only on the plastic card but also
in the banking app.

## 4. Who pilots it: data rules, the ML model, and new cards

A launch needs a clear first audience. We choose it from the data, with three complementary tools:

- **A simple data rule finds today's typers.** 190k cards (22% of active cards) make **80% of all typed online
  payments**; the heaviest fifth of them makes almost two thirds of that **[VISA]**. They get QR in their banking app
  first: the effect is immediate and measurable within weeks.
- **New cards get QR from day one.** About 27k cards are issued every month, and a card's chance of going online is
  highest in its first 90 days **[VISA]**. Printing QR on the card is the cheapest way to scale and to make sure the
  habit starts without typing.
- **The ML model finds who is about to start.** Among cards that have never paid online, our readiness model
  (LightGBM, trained and validated on Visa data) points to the one in five cards that holds more than half of the
  future online customers. It was tested on three later periods it never saw (AUC 0.74-0.76; the top 10% start
  3.5x more often than average) **[VISA]**. These cards get QR at the moment of their first online payment, when the
  habit is formed. The model also explains *why*: new cards, phone payments in shops and a digital lifestyle predict
  the start, not how much people spend.

The rule gives the biggest immediate volume, new cards give the cheapest scale, and the model makes the second wave
precise. In each audience the bank keeps a random ~10% without QR as a control group, so the pilot proves what QR itself
changes.

## 5. What it could be worth: the simulation

The data tell us *who* and *how much they pay online today*; they cannot tell the future of a product that does not exist
yet. That is the role of the business-case simulation: a scenario model of adoption, transaction volume, BLIK
cannibalisation and ROI (conservative / base / optimistic) **[SIM]**. To keep it grounded, its key inputs come from the
data **[VISA]** (`ml_readiness/results/target_audiences.json`): audience sizes as shares of active cards, online and typed
payments per card, expected first-time online payers, new cards per month, and the retention effect of a one-click first
payment (+4 pp conservative, +14 pp optimistic). Fees, costs and adoption speed remain assumptions, and the pilot will
replace them with measured values.

## 6. In one sentence

**The Visa data show that typing the card number is what keeps the card out of e-commerce; QR Pay removes it; data rules
and an ML model decide who gets it first; the simulation sizes the prize; the pilot with control groups proves it.**
