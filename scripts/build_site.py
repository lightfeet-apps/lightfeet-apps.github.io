# -*- coding: utf-8 -*-
"""Generates Lightfeet Apps root landing pages, PlusMinus support/marketing/FAQ/privacy
pages (EN & FI), and the unified root sitemap.xml for lightfeetapps.com.

Note: WakeUp pages under /wakeup/ are mirrored separately from wakeup-support and
are not overwritten by this script.
"""

import html
import json
import os
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://lightfeetapps.com"
CONTACT_EMAIL = "contact@lightfeetapps.com"
PLUSMINUS_EMAIL = "plusminus@lightfeetapps.com"
PLUSMINUS_EMAIL_SUBJECTS = {
    ("index", "en"): "PlusMinus Support",
    ("index", "fi"): "PlusMinus-tuki",
    ("privacy", "en"): "PlusMinus Privacy",
    ("privacy", "fi"): "PlusMinus - Tietosuoja",
}
WAKEUP_LANGS = ["", "fi", "sv", "de", "es", "fr"]
PLUSMINUS_LANGS = [
    {"code": "en", "name": "English", "dir": ""},
    {"code": "fi", "name": "Suomi", "dir": "fi"},
]


def lang_nav_links(page_name: str, current_lang: str, depth_from_en: int = 0) -> str:
    """Build language switcher HTML for 2-language sections (Root EN/FI and PlusMinus EN/FI)."""
    parts = []
    for lang in PLUSMINUS_LANGS:
        code = lang["code"]
        is_active = code == current_lang
        if current_lang == "en":
            href = page_name if code == "en" else f"fi/{page_name}"
        else:
            href = f"../{page_name}" if code == "en" else page_name
        cls = ' class="active"' if is_active else ""
        parts.append(f'<a href="{href}"{cls}>{lang["name"]}</a>')
    return "\n            &middot;\n            ".join(parts)


ROOT_DATA = {
    "en": {
        "title": "Lightfeet Apps",
        "desc": "Focused, thoughtfully crafted apps for iPhone and iPad by Lightfeet Apps: WakeUp and PlusMinus.",
        "canonical": f"{BASE_URL}/",
        "heading": "Lightfeet Apps",
        "tagline": "Focused, thoughtfully crafted apps for iPhone and iPad.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Flexible alarm clock for changing plans. Skip, adjust once, or pause repeating alarms without changing your regular schedule.",
                "primary_href": "wakeup/marketing.html",
                "primary_label": "About WakeUp",
                "links": [
                    ("wakeup/faq.html", "FAQ"),
                    ("wakeup/", "Support"),
                    ("wakeup/privacy.html", "Privacy Policy"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Calm, local-first monthly budget and live safe-to-spend clarity. Know what you can safely spend right now without logging every purchase.",
                "primary_href": "plusminus/marketing.html",
                "primary_label": "About PlusMinus",
                "links": [
                    ("plusminus/faq.html", "FAQ"),
                    ("plusminus/", "Support"),
                    ("plusminus/privacy.html", "Privacy Policy"),
                ],
            },
        ],
        "contact_label": "Contact:",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Language selection",
    },
    "fi": {
        "title": "Lightfeet Apps",
        "desc": "Huolellisesti viimeisteltyjä sovelluksia iPhonelle ja iPadille Lightfeet Appsilta: WakeUp ja PlusMinus.",
        "canonical": f"{BASE_URL}/fi/",
        "heading": "Lightfeet Apps",
        "tagline": "Huolellisesti viimeisteltyjä sovelluksia iPhonelle ja iPadille.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Joustava herätyskello muuttuviin suunnitelmiin. Ohita, säädä kerran tai tauota toistuvia herätyksiä muuttamatta normaalia aikatauluasi.",
                "primary_href": "../wakeup/fi/marketing.html",
                "primary_label": "Tietoa WakeUpista",
                "links": [
                    ("../wakeup/fi/faq.html", "UKK"),
                    ("../wakeup/fi/", "Tuki"),
                    ("../wakeup/fi/privacy.html", "Tietosuojaseloste"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Rauhallinen, paikallisesti toimiva kuukausibudjetti. Näe yhdellä silmäyksellä, paljonko voit turvallisesti käyttää juuri nyt — ilman jokaisen ostoksen kirjaamista.",
                "primary_href": "../plusminus/fi/marketing.html",
                "primary_label": "Tietoa PlusMinusista",
                "links": [
                    ("../plusminus/fi/faq.html", "UKK"),
                    ("../plusminus/fi/", "Tuki"),
                    ("../plusminus/fi/privacy.html", "Tietosuojaseloste"),
                ],
            },
        ],
        "contact_label": "Yhteystiedot:",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Kielivalinta",
    },
}


PLUSMINUS_DATA = {
    "en": {
        "home_href": "../index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "PlusMinus Support",
            "desc": "Get help with PlusMinus, the calm local-first budget app for iPhone and iPad, or contact PlusMinus support.",
            "heading": "PlusMinus Support",
            "thank_you": "Thank you for using PlusMinus.",
            "faq_card_title": "Check the FAQ first for quick answers",
            "faq_card_body": "Before sending an email, please check our Frequently Asked Questions (FAQ). You will find clear answers covering Safe to Spend, the difference between Live and Plan, food budget proration, double-deduction protection, backups, and privacy.",
            "faq_card_action": "Browse Frequently Asked Questions (FAQ)",
            "card_title": "Troubleshooting & Good to know",
            "tips": [
                (
                    "Safe to Spend looks higher or lower than expected:",
                    "Make sure <strong>Current Available Money</strong> reflects your real balance right now, and review any unpaid or overdue bills in <strong>Live</strong>. Expected income arriving before your next payday is shown as a quiet reminder and is not included in Safe to Spend until you mark it received. You can also inspect the full calculation rules in <strong>Settings &rarr; How Calculations Work</strong>."
                ),
                (
                    "Avoiding double-deductions when marking bills paid:",
                    "When you tap <strong>Mark Paid</strong>, PlusMinus asks whether to <strong>Subtract from Current Money</strong> or keep your balance unchanged because <strong>Current Money already reflects this</strong>. If you update your balance manually first, quick reconciliation chips let you mark settled bills without subtracting them twice, and <strong>Undo</strong> lets you reverse a mistake immediately."
                ),
                (
                    "Backups and moving to another device:",
                    "PlusMinus stores all budget data locally on your device. To move your budget or keep a copy, open <strong>Settings &rarr; Data &amp; Privacy &rarr; Backup &amp; Restore</strong> and tap <strong>Create Backup</strong> to save a <code>.plusminusbackup</code> file via Files. Restoring a backup replaces all current budget data and restores the balance as it was when the backup was created, while keeping your app language unchanged."
                ),
            ],
            "contact_intro": "If you couldn't find an answer in the FAQ, experience an issue, or would like to share feedback, please contact:",
            "email_label": "Email:",
            "report_tip": "When reporting a problem, it may be helpful to include your device model (iPhone or iPad), iOS version, and a short description of the issue.",
            "about_link": "About PlusMinus",
            "faq_link": "FAQ",
            "privacy_link": "Privacy Policy",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Language selection",
        },
        "faq": {
            "title": "PlusMinus FAQ – Frequently Asked Questions",
            "desc": "Frequently asked questions and guides for PlusMinus on iPhone and iPad: Safe to Spend calculation, Live vs. Plan, daily food budget proration, double-deduction protection, custom-month bills, rounding, backups, privacy, and supported languages.",
            "back_label": "&larr; PlusMinus Support",
            "about_link": "About PlusMinus",
            "privacy_link": "Privacy Policy",
            "heading": "Frequently Asked Questions",
            "subtitle": "Help, calculation rules, and guides for PlusMinus.",
            "toc_title": "On this page",
            "toc_tip": 'Can\'t find what you\'re looking for? <a href="index.html">Contact PlusMinus Support &rarr;</a>',
            "back_to_top": "&uarr; Back to top",
            "nav_aria": "Language selection",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "How is Safe to Spend calculated?",
                    "intro": "<strong>Live</strong> answers one practical question: <em>How much money can I safely spend right now until my next primary payday?</em> It uses a transparent 3-line formula:",
                    "bullets": [
                        "<strong>Current Available Money:</strong> Your manually maintained checking or cash balance right now, shown with a relative last-updated timestamp.",
                        "<strong>Minus unpaid bills:</strong> Unpaid recurring bills and one-time bills due before your next primary payday, plus any overdue unpaid bills from the immediately preceding pay period.",
                        "<strong>Minus remaining food estimate:</strong> Your estimated remaining food budget for the rest of the current payday cycle."
                    ],
                    "note": "<strong>Tip:</strong> You can review the calculation breakdown at any time inside the app under <strong>Settings &rarr; Understanding PlusMinus &rarr; How Calculations Work</strong>."
                },
                {
                    "question": "What is the difference between Live and Plan?",
                    "intro": "PlusMinus separates day-to-day spending awareness from your long-term monthly baseline across two distinct tabs:",
                    "bullets": [
                        "<strong>Live:</strong> Covers right now until your next primary payday. It starts from your real <strong>Current Available Money</strong>, deducts bills due in this pay period and remaining food, and tells you your current <strong>Safe to Spend</strong>.",
                        "<strong>Plan:</strong> Shows your steady-state <strong>Planned Monthly Remainder</strong> (normalized monthly income minus normalized monthly bills minus your monthly food budget), completely independent of today's bank balance or payday cycle length."
                    ],
                    "note": "<strong>Why both views?</strong> A yearly insurance bill or shorter February pay period affects how much cash you can spend right now in <strong>Live</strong>, while <strong>Plan</strong> tells you whether your normal income covers your regular expenses over time."
                },
                {
                    "question": "How does the Food Budget work, and can I override it for the current period?",
                    "intro": "Instead of tracking every grocery receipt, PlusMinus models food as a single monthly estimate that automatically scales down as payday approaches:",
                    "bullets": [
                        "<strong>Automatic daily proration:</strong> PlusMinus calculates <code>Monthly Food Budget &times; (days remaining until next payday &divide; total days in the current payday cycle)</code>, rounded up to a whole currency unit. Today is included and payday is excluded.",
                        "<strong>Custom period override:</strong> In <strong>Live</strong>, tap <strong>Food estimate</strong> to set a fixed amount for the current period (including zero) if you already bought groceries in bulk or are traveling. Your monthly food budget in <strong>Plan</strong> stays unchanged.",
                        "<strong>Restoring automatic calculation:</strong> Open the <strong>Food estimate</strong> sheet and tap <strong>Restore automatic calculation</strong> at any time, or let it reset automatically on your next primary payday."
                    ],
                    "note": "<strong>Note:</strong> Secondary income dates never reset your food budget — only your <strong>Primary Payday</strong> anchors and resets the food estimate."
                },
                {
                    "question": "How does PlusMinus prevent deducting the same bill twice?",
                    "intro": "Because you update your balance manually without a bank connection, PlusMinus includes built-in safeguards so paid bills never reduce Safe to Spend twice:",
                    "bullets": [
                        "<strong>Two-button confirmation on Mark Paid:</strong> When marking a bill paid, PlusMinus asks whether to <strong>Subtract from Current Money</strong> or keep your balance as-is because <strong>Current Money already reflects this</strong> (with smart emphasis if you updated your balance within the last 5 minutes).",
                        "<strong>Quick reconciliation chips:</strong> After a manual balance update, quick chips let you mark recently due bills as settled without subtracting them from your balance again.",
                        "<strong>Safe Undo:</strong> If you tap the wrong option, tap <strong>Undo</strong> right away to restore the bill and any automatic balance change cleanly."
                    ]
                },
                {
                    "question": "Why isn't upcoming income added to Safe to Spend automatically?",
                    "intro": "PlusMinus keeps <strong>Safe to Spend</strong> strictly grounded in money you actually have on hand right now:",
                    "bullets": [
                        "<strong>Quiet reminder chip:</strong> If another recurring or one-time income is expected before your next primary payday, it appears quietly in <strong>Live</strong> as an upcoming income reminder so you know it is on the way.",
                        "<strong>Never inflated prematurely:</strong> Future unreceived income is never added to <strong>Safe to Spend</strong> until you actually receive it and update <strong>Current Available Money</strong> (or mark the income received and add it to your balance)."
                    ]
                },
                {
                    "question": "How do Custom Months, Yearly, Weekly, Biweekly, and One-Time items work?",
                    "intro": "PlusMinus handles both regular bills and irregular schedules accurately across <strong>Plan</strong> and <strong>Live</strong>:",
                    "bullets": [
                        "<strong>Plan normalization:</strong> Weekly items normalize via <code>&times; 52 &divide; 12</code>, every 2 weeks via <code>&times; 26 &divide; 12</code>, <strong>Custom Months</strong> (such as January &amp; October or Quarterly presets) via <code>&times; selected months &divide; 12</code>, and yearly items via <code>&divide; 12</code>.",
                        "<strong>Live full deductions:</strong> Yearly and custom-month bills are deducted in full during the actual pay period when they fall due, so you see their real cash impact before payday.",
                        "<strong>One-Time items:</strong> One-time income and one-time bills (for example a tax refund or car repair) have an exact date and are excluded from your steady-state <strong>Plan</strong> baseline, appearing only when due in <strong>Live</strong>.",
                        "<strong>Categories &amp; optional due days:</strong> Recurring bills can be organized with optional categories (Housing, Utilities, Subscriptions, Insurance, Loan &amp; Debt, Transport, Other), and recurring items can omit a specific due day if needed."
                    ]
                },
                {
                    "question": "How do Primary Payday and weekend payday shifting work?",
                    "intro": "Your <strong>Primary Payday</strong> in <strong>Settings &rarr; Budget Cycle</strong> anchors your pay cycles and food estimate resets:",
                    "bullets": [
                        "<strong>Days 1–31 with short-month handling:</strong> Choose your main payday from day 1 to 31. In shorter months (such as February or 30-day months), PlusMinus automatically clamps the date to the last day of that month.",
                        "<strong>Weekend shifting:</strong> Turn on <strong>Pay on Friday if payday falls on a weekend</strong> if your employer pays on the preceding Friday whenever the payday falls on Saturday or Sunday.",
                        "<strong>Cycle preview:</strong> In the <strong>Primary Payday</strong> picker, you can preview upcoming effective payday dates before saving."
                    ]
                },
                {
                    "question": "What are Coming Next Period, paying bills early, and older unsettled bills?",
                    "intro": "PlusMinus makes it easy to stay ahead of upcoming cycles and keep older periods tidy:",
                    "bullets": [
                        "<strong>Coming Next Period &amp; early payment:</strong> Expand <strong>Coming Next Period</strong> in <strong>Live</strong> to preview bills due after your next primary payday. If you already paid a next-period bill early, mark it paid there with the same balance consistency check.",
                        "<strong>Older unsettled bills (Mark older settled):</strong> Unpaid bills from before the previous cycle (up to 24 months old) are excluded from deducting against your current <strong>Safe to Spend</strong> and surfaced in a non-destructive catch-up banner with <strong>Mark older settled</strong>."
                    ]
                },
                {
                    "question": "How are amounts rounded?",
                    "intro": "Every visible figure is designed so the arithmetic adds up clearly:",
                    "bullets": [
                        "<strong>Cent precision &amp; exact totals:</strong> Monetary components are rounded to the nearest cent (with half-cent ties rounding away from zero) before summing or subtracting, so every displayed line adds up to the exact total shown.",
                        "<strong>Food estimate rounding:</strong> The automatic daily food estimate in <strong>Live</strong> rounds up to a whole currency unit, whereas custom fixed food estimates keep cents.",
                        "<strong>Clean decimal display:</strong> Amounts with cents display two decimal places, while whole amounts omit trailing decimals."
                    ]
                },
                {
                    "question": "Does PlusMinus connect to my bank, collect analytics, or sync automatically to the cloud?",
                    "intro": "No. PlusMinus is built strictly as a local-first, zero-tracking app:",
                    "bullets": [
                        "<strong>Stored on your device:</strong> Balances, incomes, bills, payment history, and preferences stay locally on your iPhone or iPad.",
                        "<strong>No accounts or bank links:</strong> PlusMinus requires no account and never asks for bank credentials or Open Banking access.",
                        "<strong>Zero tracking or ads:</strong> There are no analytics SDKs, no advertising identifiers, and no automatic cloud sync in the background."
                    ]
                },
                {
                    "question": "How do Backup & Restore and Reset All Data work?",
                    "intro": "You stay in full control of your local budget data at all times:",
                    "bullets": [
                        "<strong>Create Backup:</strong> Open <strong>Settings &rarr; Data &amp; Privacy &rarr; Backup &amp; Restore</strong> and tap <strong>Create Backup</strong> to export a readable JSON archive (<code>.plusminusbackup</code>, not password-protected) to iCloud Drive, local storage, or any location in Files.",
                        "<strong>Restore from Backup:</strong> Tap <strong>Restore from Backup</strong> and select a valid <code>.plusminusbackup</code> file (up to 50 MB). Restoring replaces all current budget data and restores the balance from when the backup was created, while keeping your app language unchanged.",
                        "<strong>Reset All Data:</strong> Under <strong>Settings &rarr; Data &amp; Privacy</strong>, <strong>Reset All Data</strong> uses a two-step confirmation to erase all local budget data and preferences on this device and return to initial setup. Exported backup files and iOS system backups are not deleted."
                    ]
                },
                {
                    "question": "What languages, currencies, themes, and devices are supported?",
                    "intro": "PlusMinus adapts to your preferred language, currency, and appearance:",
                    "bullets": [
                        "<strong>Languages:</strong> Switchable directly inside <strong>Settings &rarr; Preferences &rarr; Language</strong> between <strong>System Default</strong>, <strong>English</strong>, and <strong>Suomi</strong> (Finnish) without restarting the app.",
                        "<strong>Currencies:</strong> Supports <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD,</strong> and <strong>JPY</strong> under <strong>Settings &rarr; Preferences &rarr; Currency</strong>.",
                        "<strong>Appearance:</strong> Choose <strong>System Default</strong>, <strong>Dark</strong>, or <strong>Light</strong> under <strong>Settings &rarr; Preferences &rarr; Appearance</strong>.",
                        "<strong>Supported devices:</strong> Built for iPhone and iPad running <strong>iOS 26 or later</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Calm Monthly Budget & Safe to Spend for iPhone and iPad",
            "desc": "Know what you can safely spend right now without logging every purchase. Local-first budgeting with payday cycle food proration and no bank connections.",
            "canonical": f"{BASE_URL}/plusminus/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Know what you can safely spend right now.",
            "subtitle": "Set your recurring income, recurring bills, payday, and monthly food budget once. Glance at your balance and see what is genuinely free to spend — without logging every coffee.",
            "section1_title": "Clarity in under five seconds",
            "features": [
                ("Live Safe to Spend", "Current Available Money minus unpaid bills before payday minus your remaining food estimate — clearly broken down on three lines."),
                ("Steady Monthly Plan", "Separate monthly overview normalizing weekly, biweekly, custom-month, and yearly bills without today's cash getting in the way."),
                ("Private & Local-First", "Everything stays on your device. No accounts, no bank logins, no analytics, and no tracking — ever."),
            ],
            "section2_title": "Everything you need, nothing you don't",
            "list_items": [
                "Live Safe to Spend calculated up to your next primary payday",
                "Automatic daily food budget proration with instant custom period override",
                "Double-deduction protection when marking bills paid or updating balances",
                "Weekly, biweekly, monthly, yearly, custom-month, and one-time items",
                "Weekend payday shifting to Friday and short-month date clamping",
                "Coming Next Period preview with early payment and older bill catch-up",
                "Manual .plusminusbackup export and restore via Files",
                "Available in English and Finnish with 10 currencies and Light/Dark Mode",
            ],
            "closing_title": "Built for iPhone and iPad",
            "closing_body": "PlusMinus is designed for iPhone and iPad running iOS 26 or later.",
            "faq_btn": "FAQ",
            "privacy_btn": "Privacy Policy",
            "support_btn": "Support",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Language selection",
            "featureList": [
                "Live Safe to Spend calculation until next primary payday",
                "Normalized Target Monthly Budget plan",
                "Automatic daily food budget proration with custom override",
                "Two-button double-deduction prevention when marking bills paid",
                "Custom-month, yearly, weekly, biweekly, and one-time schedules",
                "100% local-first storage with manual backup and restore via Files",
            ],
        },
        "privacy": {
            "title": "PlusMinus Privacy Policy",
            "desc": "Read the PlusMinus privacy policy: local-first budgeting on your device with no accounts, analytics, bank connections, or tracking.",
            "heading": "Privacy Policy for PlusMinus",
            "last_updated": "Last updated: November 23, 2026",
            "sections": [
                (
                    "Data on Your Device",
                    [
                        "PlusMinus is a local-first budgeting app. Your budget is not sent to the developer.",
                        "Balances, income, bills, payment history, and budget settings are stored locally on your device. Language, appearance, and dismissed reminders are saved as local preferences.",
                    ],
                ),
                (
                    "Tracking and Data Collection",
                    [
                        "PlusMinus has no accounts, advertising, analytics, bank connections, or automatic cloud sync. The app does not collect personal data or track you across apps or websites.",
                    ],
                ),
                (
                    "Backups and Files",
                    [
                        "Creating a backup exports your budget and payment history to the location you choose in Files. Backup files are readable and are not password protected. If you choose iCloud Drive or another provider, that provider stores the file under its own terms and privacy policy.",
                        "Your device's system backups may also include app data, depending on your Apple backup settings. PlusMinus does not control those backups.",
                    ],
                ),
                (
                    "Deleting Your Data",
                    [
                        "Use <strong>Reset All Data</strong> in <strong>Settings &rarr; Data &amp; Privacy</strong> to erase the budget and preferences stored by PlusMinus on this device. Exported files and system backups are not deleted; manage those separately in Files or your device's backup settings.",
                    ],
                ),
                (
                    "Children's Privacy",
                    [
                        "PlusMinus does not collect personal information from children or any other users.",
                    ],
                ),
                (
                    "Changes to This Privacy Policy",
                    [
                        "This Privacy Policy may be updated if the functionality or data practices of PlusMinus change. Any updates will be published on this page.",
                    ],
                ),
            ],
            "contact_heading": "Contact",
            "contact_intro": "If you have questions about this Privacy Policy, please contact:",
            "about_link": "About PlusMinus",
            "faq_link": "FAQ",
            "support_link": "PlusMinus Support",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Language selection",
        },
    },
    "fi": {
        "home_href": "../../fi/index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "PlusMinus-tuki",
            "desc": "Hanki apua PlusMinus-budjettisovellukseen iPhonella ja iPadilla tai ota yhteyttä PlusMinus-tukeen.",
            "heading": "PlusMinus-tuki",
            "thank_you": "Kiitos, että käytät PlusMinusta.",
            "faq_card_title": "Katso ensin usein kysytyt kysymykset (UKK)",
            "faq_card_body": "Ennen sähköpostin lähettämistä suosittelemme tutustumaan usein kysyttyihin kysymyksiin. Löydät sieltä selkeät ohjeet aiheista Käytettävissä nyt -laskenta, Tilanne- ja Kuukausi-näkymien erot, ruokabudjetin suhteutus, kaksoisvähennysten esto, varmuuskopiot ja tietosuoja.",
            "faq_card_action": "Selaa usein kysyttyjä kysymyksiä (UKK)",
            "card_title": "Vianmääritys ja hyvä tietää",
            "tips": [
                (
                    "Käytettävissä nyt -summa näyttää odotettua suuremmalta tai pienemmältä:",
                    "Varmista, että <strong>Käytettävissä oleva raha nyt</strong> vastaa tämänhetkistä saldoasi, ja tarkista maksamattomat tai myöhässä olevat laskut <strong>Tilanne</strong>-näkymästä. Ennen seuraavaa palkkapäivää tulevat tulot näkyvät muistutuksena eivätkä kasvata käytettävissä olevaa summaa ennen kuin ne merkitään saaduiksi. Voit myös tarkistaa laskentasäännöt kohdasta <strong>Asetukset &rarr; Miten laskenta toimii</strong>."
                ),
                (
                    "Kaksoisvähennysten estäminen laskuja kuitattaessa:",
                    "Kun napautat laskussa <strong>Maksettu</strong>, PlusMinus kysyy, haluatko <strong>Vähentää summan saldosta</strong> vai pitää saldon ennallaan, koska <strong>Saldo sisältää tämän jo</strong>. Jos päivität saldosi ensin käsin, voit kuitata laskut pikavalinnoilla muuttamatta saldoa uudelleen, ja <strong>Kumoa</strong>-painikkeella perut valinnan heti."
                ),
                (
                    "Varmuuskopiointi ja siirtäminen toiselle laitteelle:",
                    "PlusMinus tallentaa budjettitiedot paikallisesti laitteellesi. Voit tallentaa kopion tai siirtää tiedot avaamalla <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Varmuuskopiointi ja palautus</strong> ja valitsemalla <strong>Luo varmuuskopio</strong> (<code>.plusminusbackup</code>-tiedosto Tiedostot-apin kautta). Palauttaminen korvaa nykyiset budjettitiedot ja palauttaa saldon varmuuskopion luontihetken tilaan muuttamatta sovelluksen kieltä."
                ),
            ],
            "contact_intro": "Jos et löytänyt vastausta UKK-osiosta, kohtaat ongelman tai haluat antaa palautetta, ota yhteyttä:",
            "email_label": "Sähköposti:",
            "report_tip": "Ongelmatilanteesta ilmoittaessa on hyödyllistä mainita laitemalli (iPhone tai iPad), iOS-versio ja lyhyt kuvaus ongelmasta.",
            "about_link": "Tietoa PlusMinusista",
            "faq_link": "UKK",
            "privacy_link": "Tietosuojaseloste",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Kielivalinta",
        },
        "faq": {
            "title": "PlusMinus UKK – Usein kysytyt kysymykset",
            "desc": "Usein kysyttyjä kysymyksiä ja ohjeita PlusMinus-sovellukseen iPhonella ja iPadilla: Käytettävissä nyt -laskenta, Tilanne ja Kuukausi, ruokabudjetin suhteutus, kaksoisvähennysten esto, pyöristykset, varmuuskopiot, tietosuoja ja tuetut kielet.",
            "back_label": "&larr; PlusMinus-tuki",
            "about_link": "Tietoa PlusMinusista",
            "privacy_link": "Tietosuojaseloste",
            "heading": "Usein kysytyt kysymykset",
            "subtitle": "Ohjeita, laskentasääntöjä ja vinkkejä PlusMinusin käyttöön.",
            "toc_title": "Aiheet tällä sivulla",
            "toc_tip": 'Etkö löytänyt vastausta kysymykseesi? <a href="index.html">Ota yhteyttä PlusMinus-tukeen &rarr;</a>',
            "back_to_top": "&uarr; Takaisin alkuun",
            "nav_aria": "Kielivalinta",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "Miten Käytettävissä nyt -summa lasketaan?",
                    "intro": "<strong>Tilanne</strong>-näkymä vastaa yhteen arjen tärkeimpään kysymykseen: <em>Paljonko voin turvallisesti käyttää juuri nyt ennen seuraavaa ensisijaista palkkapäivää?</em> Laskelma perustuu selkeään kolmen rivin kaavaan:",
                    "bullets": [
                        "<strong>Käytettävissä oleva raha nyt:</strong> Käsin päivittämäsi tilin tai käteisen saldo tällä hetkellä, näkyvissä olevan päivitysajankohdan kanssa.",
                        "<strong>Miinus maksamattomat laskut:</strong> Kaikki ennen seuraavaa ensisijaista palkkapäivää erääntyvät maksamattomat toistuvat laskut ja kertaluontoiset menot sekä edelliseltä jaksolta maksamatta jääneet laskut.",
                        "<strong>Miinus arvioitu jäljellä oleva ruoka-arvio:</strong> Palkkajakson jäljellä oleville päiville suhteutettu ruokabudjetti."
                    ],
                    "note": "<strong>Vinkki:</strong> Voit tarkistaa koko laskentakaavan milloin tahansa sovelluksesta kohdasta <strong>Asetukset &rarr; Tietoa laskennasta &rarr; Miten laskenta toimii</strong>."
                },
                {
                    "question": "Mitä eroa on Tilanne- ja Kuukausi-näkymillä?",
                    "intro": "PlusMinus erottaa arjen käyttövaran ja pitkän aikavälin kuukausitasapainon kahdeksi selkeäksi välilehdeksi:",
                    "bullets": [
                        "<strong>Tilanne:</strong> Näyttää tilanteen juuri nyt seuraavaan ensisijaiseen palkkapäivään saakka. Se lähtee todellisesta <strong>Raha nyt</strong> -saldosta, vähentää tällä jaksolla erääntyvät laskut ja jäljellä olevan ruoka-arvion ja kertoo paljonko on <strong>Käytettävissä nyt</strong>.",
                        "<strong>Kuukausi:</strong> Näyttää tasatun <strong>Kuukausibudjetin ylijäämän</strong> (tasatut kuukausitulot miinus tasatut kuukausilaskut miinus kuukauden ruokabudjetti) täysin riippumattomana tämän päivän pankkisaldosta."
                    ],
                    "note": "<strong>Miksi kaksi näkymää?</strong> Esimerkiksi kerran vuodessa erääntyvä vakuutus tai lyhyempi palkkajakso vaikuttaa suoraan siihen, paljonko rahaa on käytettävissä nyt <strong>Tilanne</strong>-näkymässä, kun taas <strong>Kuukausi</strong> kertoo, riittävätkö normaalitulosi kattamaan säännölliset kulusi."
                },
                {
                    "question": "Miten ruokabudjetti toimii, ja voinko asettaa sille oman arvion?",
                    "intro": "Yksittäisten kauppaostosten tai kuittien kirjaamisen sijaan PlusMinus mallintaa ruokakulut yhtenä kuukausiarviona, joka pienenee automaattisesti palkkapäivän lähestyessä:",
                    "bullets": [
                        "<strong>Automaattinen päiväkohtainen suhteutus:</strong> PlusMinus laskee kaavalla <code>Kuukauden ruokabudjetti &times; (päiviä jäljellä seuraavaan palkkapäivään &divide; palkkajakson kokonaispäivät)</code> ja pyöristää tuloksen ylöspäin kokonaisiin rahayksiköihin. Tämä päivä lasketaan mukaan, palkkapäivää ei.",
                        "<strong>Oma arvio tälle jaksolle:</strong> Napauta <strong>Tilanne</strong>-näkymässä <strong>Ruoka-arvio</strong>-kohtaa ja aseta tälle jaksolle kiinteä summa (tarvittaessa nolla), jos olet esimerkiksi tehnyt ruokaostokset etukäteen tai olet matkalla. <strong>Kuukausi</strong>-näkymän kuukausibudjetti ei muutu.",
                        "<strong>Automaattisen laskennan palauttaminen:</strong> Voit palauttaa automaattisen laskennan milloin tahansa valinnasta <strong>Palauta automaattinen laskenta</strong>. Se palautuu käyttöön myös automaattisesti seuraavana ensisijaisena palkkapäivänä."
                    ],
                    "note": "<strong>Huomio:</strong> Muiden tulojen maksupäivät eivät koskaan nollaa ruokabudjettia — vain <strong>Ensisijainen palkkapäivä</strong> määrittää palkkajakson ja nollaa ruoka-arvion."
                },
                {
                    "question": "Miten PlusMinus estää saman laskun vähentämisen kahteen kertaan?",
                    "intro": "Koska päivität saldosi itse ilman pankkiyhteyttä, PlusMinusissa on sisäänrakennettu suojaus kaksoisvähennyksiä vastaan:",
                    "bullets": [
                        "<strong>Kahden vaihtoehdon vahvistus:</strong> Kun merkitset laskun maksetuksi (<strong>Maksettu</strong>), sovellus kysyy, vähennetäänkö summa saldosta (<strong>Vähennä saldosta</strong>) vai näkyykö se jo saldossa (<strong>Saldo sisältää tämän jo</strong>). Jos olet päivittänyt saldosi viimeisen 5 minuutin aikana, sovellus korostaa valmiiksi jälkimmäistä vaihtoehtoa.",
                        "<strong>Pikakuittaus saldopäivityksen jälkeen:</strong> Kun päivität saldosi käsin, näkyviin tulevilla pikavalinnoilla voit kuitata erääntyneitä laskuja maksetuiksi muuttamatta saldoa uudelleen.",
                        "<strong>Helppo peruminen:</strong> Jos valitset vahingossa väärän vaihtoehdon, napauta heti <strong>Kumoa</strong> palauttaaksesi laskun ja saldomuutoksen."
                    ]
                },
                {
                    "question": "Miksi tulevaa tuloa ei lisätä automaattisesti Käytettävissä nyt -summaan?",
                    "intro": "PlusMinus pitää <strong>Käytettävissä nyt</strong> -summan tiukasti kiinni todellisessa, tällä hetkellä käytössäsi olevassa rahassa:",
                    "bullets": [
                        "<strong>Hiljainen muistutus:</strong> Jos ennen seuraavaa ensisijaista palkkapäivää on tulossa toinen tulo (kuten etuus, palkka tai kertaluontoinen tulo), se näkyy <strong>Tilanne</strong>-näkymässä muistutuksena.",
                        "<strong>Ei ennenaikaisia oletuksia:</strong> Tulevaa tuloa ei lasketa käytettävissä olevaan rahaan ennen kuin olet oikeasti saanut sen ja päivittänyt saldosi (tai kuitannut tulon saaduksi ja lisännyt sen saldoon)."
                    ]
                },
                {
                    "question": "Miten valitut kuukaudet, vuosittaiset, viikoittaiset ja kertaluontoiset erät toimivat?",
                    "intro": "PlusMinus käsittelee sekä säännölliset että harvemmin toistuvat tai kertaluontoiset erät tarkasti:",
                    "bullets": [
                        "<strong>Kuukausitasaus (Kuukausi-välilehti):</strong> Viikoittaiset erät tasataan kertoimella <code>&times; 52 &divide; 12</code>, joka 2. viikko toistuvat <code>&times; 26 &divide; 12</code>, <strong>Valitut kuukaudet</strong> (esim. tammi- ja lokakuu tai neljännesvuosi) kertoimella <code>&times; valitut kuukaudet &divide; 12</code> ja vuosittaiset <code>&divide; 12</code>.",
                        "<strong>Täysi vähennys Tilanne-näkymässä:</strong> Vuosittaiset ja valittujen kuukausien laskut vähennetään täysimääräisinä juuri sen palkkajakson käyttövarasta, jonka aikana ne erääntyvät.",
                        "<strong>Kertaluontoiset tulot ja menot:</strong> Kertaluontoiset erät (esim. veronpalautus tai yksittäinen isompi hankinta) merkitään tarkalla päivämäärällä. Ne eivät kuulu tasattuun kuukausisuunnitelmaan, vaan näkyvät vain kyseisen jakson <strong>Tilanne</strong>-näkymässä.",
                        "<strong>Kategoriat ja valinnainen eräpäivä:</strong> Toistuville laskuille voi valita kategorian (Asuminen, Sähkö &amp; vesi, Tilaukset, Vakuutukset, Lainat, Liikenne, Muu), ja säännöllisille erille voi tarvittaessa jättää tarkan eräpäivän asettamatta."
                    ]
                },
                {
                    "question": "Miten Ensisijainen palkkapäivä ja viikonloppujen siirto toimivat?",
                    "intro": "Kohdasta <strong>Asetukset &rarr; Budjettijakso</strong> asetettava <strong>Ensisijainen palkkapäivä</strong> määrittää palkkajakson ja ruoka-arvion nollauksen:",
                    "bullets": [
                        "<strong>Päivät 1–31 ja lyhyet kuukaudet:</strong> Valitse ensisijainen palkkapäivä väliltä 1–31. Lyhyemmissä kuukausissa (kuten helmikuussa tai 30-päiväisissä kuukausissa) päivä siirtyy automaattisesti kuukauden viimeiseen päivään.",
                        "<strong>Siirto perjantaille viikonlopusta:</strong> Ota käyttöön <strong>Palkkapäivä on perjantai, jos se osuu viikonloppuun</strong>, jos palkkasi maksetaan edeltävänä perjantaina palkkapäivän osuessa lauantaille tai sunnuntaille.",
                        "<strong>Seuraavien palkkapäivien esikatselu:</strong> Näet valitsimesta suoraan tulevat todelliset palkkapäivät ennen tallennusta."
                    ]
                },
                {
                    "question": "Mitä tarkoittavat Seuraavalla jaksolla, etukäteen maksaminen ja Kuittaa vanhemmat?",
                    "intro": "PlusMinus auttaa hallitsemaan myös tulevia ja vanhempia kuitattuja laskuja selkeästi:",
                    "bullets": [
                        "<strong>Seuraavalla jaksolla ja etukäteismaksu:</strong> Avaamalla <strong>Seuraavalla jaksolla</strong> -osion <strong>Tilanne</strong>-näkymässä näet seuraavan palkkapäivän jälkeen erääntyvät laskut ja voit kuitata ne maksetuksi etukäteen samalla saldotarkistuksella.",
                        "<strong>Vanhemmat kuittaamattomat laskut:</strong> Edellistä jaksoa vanhemmat maksamattomat laskut (enintään 24 kk taaksepäin) jätetään pois nykyisestä Käytettävissä nyt -laskelmasta, ja voit merkitä ne kuitatuiksi erillisestä <strong>Kuittaa vanhemmat</strong> -huomautuksesta."
                    ]
                },
                {
                    "question": "Miten summat pyöristetään?",
                    "intro": "Kaikki näkyvät luvut pyöristetään niin, että laskutoimitukset täsmäävät tarkasti:",
                    "bullets": [
                        "<strong>Senttitarkkuus ja täsmäävät rivit:</strong> Summat pyöristetään lähimpään senttiin (tasan puolen sentin erot poispäin nollasta) ennen yhteen- tai vähennyslaskua, joten näkyvät rivit täsmäävät aina tarkalleen loppusummaan.",
                        "<strong>Ruoka-arvion pyöristys:</strong> Tilanne-näkymän automaattinen ruoka-arvio pyöristetään ylöspäin kokonaisiin rahayksiköihin, kun taas itse asetetuissa arvioissa säilytetään sentit.",
                        "<strong>Siisti esitystapa:</strong> Sentilliset summat näytetään kahdella desimaalilla ja tasasummat ilman desimaaleja."
                    ]
                },
                {
                    "question": "Yhdistyykö PlusMinus pankkiin, kerääkö se analytiikkaa tai synkronoiko se pilveen?",
                    "intro": "Ei. PlusMinus on alusta asti suunniteltu paikallisesti laitteella toimivaksi sovellukseksi:",
                    "bullets": [
                        "<strong>Tallennetaan laitteellesi:</strong> Saldot, tulot, laskut, maksuhistoria ja asetukset pysyvät paikallisesti iPhonellasi tai iPadillasi.",
                        "<strong>Ei tilejä eikä pankkitunnuksia:</strong> Sovellus ei vaadi käyttäjätiliä eikä kysy pankkitunnuksia tai pankkiyhteyksiä.",
                        "<strong>Ei seurantaa tai mainoksia:</strong> Sovelluksessa ei ole mainoksia, analytiikka-SDK:ita eikä automaattista pilvisynkronointia taustalla."
                    ]
                },
                {
                    "question": "Miten Varmuuskopiointi ja palautus sekä Nollaa kaikki tiedot toimivat?",
                    "intro": "Hallitset kaikkia omia budjettitietojasi täysin itse:",
                    "bullets": [
                        "<strong>Luo varmuuskopio:</strong> Avaa <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Varmuuskopiointi ja palautus</strong> ja napauta <strong>Luo varmuuskopio</strong> tallentaaksesi luettavissa olevan JSON-tiedoston (<code>.plusminusbackup</code>, ei salasanasuojattu) iCloud Driveen, laitteelle tai muuhun Tiedostot-apin sijaintiin.",
                        "<strong>Palauta varmuuskopiosta:</strong> Valitse <strong>Palauta varmuuskopiosta</strong> ja avaa kelvollinen <code>.plusminusbackup</code>-tiedosto (enintään 50 Mt). Palautus korvaa kaikki nykyiset budjettitiedot ja palauttaa saldon varmuuskopion luontihetken tilaan. Sovelluksen kieli pysyy ennallaan.",
                        "<strong>Nollaa kaikki tiedot:</strong> Kohdassa <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Nollaa kaikki tiedot</strong> voit poistaa kaikki laitteelle tallennetut tiedot ja asetukset kaksivaiheisen vahvistuksen jälkeen. Vietyjä varmuuskopioita tai laitteen järjestelmävarmuuskopioita ei poisteta."
                    ]
                },
                {
                    "question": "Mitä kieliä, valuuttoja, teemoja ja laitteita tuetaan?",
                    "intro": "PlusMinus mukautuu kieleesi, valuuttaasi ja laitteesi ulkoasuun:",
                    "bullets": [
                        "<strong>Kielet:</strong> Voit vaihtaa kielen suoraan kohdasta <strong>Asetukset &rarr; Kieli</strong> (<strong>Järjestelmän oletus</strong>, <strong>English</strong> tai <strong>Suomi</strong>) ilman sovelluksen uudelleenkäynnistystä.",
                        "<strong>Valuutat:</strong> Tuettuina ovat <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> ja <strong>JPY</strong> kohdassa <strong>Asetukset &rarr; Valuutta</strong>.",
                        "<strong>Ulkoasu:</strong> Valitse <strong>Järjestelmän oletus</strong>, <strong>Tumma</strong> tai <strong>Vaalea</strong> kohdasta <strong>Asetukset &rarr; Ulkoasu</strong>.",
                        "<strong>Tuetut laitteet:</strong> Suunniteltu iPhonelle ja iPadille, joissa on <strong>iOS 26 tai uudempi</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Rauhallinen kuukausibudjetti ja käyttövara iPhonelle ja iPadille",
            "desc": "Näe yhdellä silmäyksellä, paljonko voit turvallisesti käyttää juuri nyt — ilman jokaisen ostoksen kirjaamista. Paikallinen budjettisovellus ilman pankkiyhteyksiä.",
            "canonical": f"{BASE_URL}/plusminus/fi/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Tiedä heti, paljonko voit turvallisesti käyttää.",
            "subtitle": "Määritä toistuvat tulot, laskut, palkkapäivä ja kuukauden ruokabudjetti kerran. Kurkkaa saldosi ja näe heti todellinen käyttövarasi — ilman jokaisen kahvin kirjaamista.",
            "section1_title": "Selkeyttä alle viidessä sekunnissa",
            "features": [
                ("Käytettävissä juuri nyt", "Käytettävissä oleva raha miinus ennen palkkapäivää erääntyvät laskut miinus jäljellä oleva ruoka-arvio — selkeänä kolmen rivin laskelmana."),
                ("Tasainen kuukausisuunnitelma", "Erillinen kuukausinäkymä, joka tasaa viikoittaiset, valittujen kuukausien ja vuosittaiset laskut ilman että päivän saldo sotkee kokonaiskuvaa."),
                ("Yksityinen ja paikallinen", "Kaikki tiedot pysyvät laitteellasi. Ei käyttäjätilejä, ei pankkiyhteyksiä, ei analytiikkaa eikä seurantaa."),
            ],
            "section2_title": "Kaikki oleellinen, ei mitään ylimääräistä",
            "list_items": [
                "Käytettävissä nyt -laskenta seuraavaan ensisijaiseen palkkapäivään",
                "Automaattinen päiväkohtainen ruoka-arvio sekä oma kiinteä arvio tarvittaessa",
                "Kaksoisvähennysten esto laskuja maksetuksi kuitatessa ja saldoa päivittäessä",
                "Viikoittaiset, joka 2. viikko, kuukausittaiset, valittujen kuukausien, vuosittaiset ja kertaluontoiset erät",
                "Viikonloppuun osuvan palkkapäivän siirto perjantaille ja lyhyiden kuukausien huomiointi",
                "Seuraavalla jaksolla -ennakko, etukäteismaksu ja vanhempien laskujen kuittaus",
                "Manuaalinen varmuuskopiointi ja palautus Tiedostot-apin kautta (.plusminusbackup)",
                "Saatavilla suomeksi ja englanniksi, 10 valuuttaa sekä tumma ja vaalea tila",
            ],
            "closing_title": "Suunniteltu iPhonelle ja iPadille",
            "closing_body": "PlusMinus toimii iPhonella ja iPadilla, joissa on iOS 26 tai uudempi.",
            "faq_btn": "UKK",
            "privacy_btn": "Tietosuojaseloste",
            "support_btn": "Tuki",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Kielivalinta",
            "featureList": [
                "Käytettävissä nyt -laskenta seuraavaan ensisijaiseen palkkapäivään",
                "Tasattu kuukausibudjetti (Kuukausi-näkymä)",
                "Automaattinen päiväkohtainen ruoka-arvio ja oma jaksoarvio",
                "Kaksoisvähennysten esto kahden vaihtoehdon vahvistuksella",
                "Valitut kuukaudet, vuosittaiset, viikoittaiset ja kertaluontoiset erät",
                "Paikallinen tallennus sekä manuaalinen varmuuskopiointi ja palautus Tiedostot-apin kautta",
            ],
        },
        "privacy": {
            "title": "PlusMinusin tietosuojaseloste",
            "desc": "Lue PlusMinusin tietosuojaseloste: paikallisesti laitteella toimiva budjettisovellus ilman tilejä, analytiikkaa, pankkiyhteyksiä tai seurantaa.",
            "heading": "PlusMinusin tietosuojaseloste",
            "last_updated": "Viimeksi päivitetty: 23. marraskuuta 2026",
            "sections": [
                (
                    "Tiedot laitteellasi",
                    [
                        "PlusMinus on paikallisesti toimiva budjetointisovellus. Budjettitietojasi ei lähetetä sovelluksen kehittäjälle.",
                        "Saldo, tulot, laskut, maksuhistoria ja budjettiasetukset tallennetaan paikallisesti laitteellesi. Kieli, ulkoasu ja ohitetut muistutukset tallennetaan paikallisina asetuksina.",
                    ],
                ),
                (
                    "Seuranta ja tietojen kerääminen",
                    [
                        "PlusMinus ei käytä käyttäjätilejä, mainontaa, analytiikkaa, pankkiyhteyksiä tai automaattista pilvisynkronointia. Sovellus ei kerää henkilötietoja eikä seuraa sinua sovellusten tai verkkosivustojen välillä.",
                    ],
                ),
                (
                    "Varmuuskopiot ja tiedostot",
                    [
                        "Kun luot varmuuskopion, budjettisi ja maksuhistoriasi viedään Tiedostot-apissa valitsemaasi sijaintiin. Varmuuskopiotiedostot ovat luettavissa, eikä niitä ole suojattu salasanalla. Jos valitset iCloud Driven tai muun palveluntarjoajan, se säilyttää tiedoston omien ehtojensa ja tietosuojakäytäntönsä mukaisesti.",
                        "Myös laitteesi järjestelmän varmuuskopiot voivat sisältää sovelluksen tietoja Applen varmuuskopiointiasetustesi mukaan. PlusMinus ei hallitse näitä varmuuskopioita.",
                    ],
                ),
                (
                    "Tietojen poistaminen",
                    [
                        "Voit poistaa PlusMinusin tälle laitteelle tallentamat budjettitiedot ja asetukset valitsemalla <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Nollaa kaikki tiedot</strong>. Vietyjä tiedostoja tai järjestelmän varmuuskopioita ei poisteta; hallitse niitä erikseen Tiedostot-apissa tai laitteesi varmuuskopiointiasetuksissa.",
                    ],
                ),
                (
                    "Lasten yksityisyys",
                    [
                        "PlusMinus ei kerää henkilötietoja lapsilta tai muiltakaan käyttäjiltä.",
                    ],
                ),
                (
                    "Muutokset tähän tietosuojaselosteeseen",
                    [
                        "Tätä tietosuojaselostetta voidaan päivittää, jos PlusMinusin toiminnallisuus tai tietokäytännöt muuttuvat. Päivitykset julkaistaan tällä sivulla.",
                    ],
                ),
            ],
            "contact_heading": "Yhteystiedot",
            "contact_intro": "Jos sinulla on kysyttävää tästä tietosuojaselosteesta, ota yhteyttä:",
            "about_link": "Tietoa PlusMinusista",
            "faq_link": "UKK",
            "support_link": "PlusMinus-tuki",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Kielivalinta",
        },
    },
}


def build_root_index(lang_code: str) -> str:
    d = ROOT_DATA[lang_code]
    lang_links = lang_nav_links("index.html", lang_code)

    cards_html = []
    for app in d["apps"]:
        secondary = "\n                    &middot;\n                    ".join(
            f'<a href="{href}">{label}</a>' for href, label in app["links"]
        )
        cards_html.append(
            f"""            <article class="app-card">
                <h2>{app["name"]}</h2>
                <p>{app["summary"]}</p>
                <div class="app-actions">
                    <a class="button" href="{app["primary_href"]}">{app["primary_label"]}</a>
                </div>
                <p class="app-links">
                    {secondary}
                </p>
            </article>"""
        )
    cards_block = "\n\n".join(cards_html)

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{d["title"]}</title>
    <meta name="description" content="{html.escape(d["desc"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{d["canonical"]}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/">
    <link rel="alternate" hreflang="fi" href="{BASE_URL}/fi/">
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f6f7f9;
            color: #1d1d1f;
            line-height: 1.6;
        }}

        .container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 80px 24px 60px;
        }}

        .hero {{
            text-align: center;
            padding: 20px 0 48px;
        }}

        h1 {{
            font-size: 48px;
            margin: 0 0 12px;
            letter-spacing: -1.2px;
        }}

        .tagline {{
            font-size: 21px;
            color: #444;
            max-width: 620px;
            margin: 0 auto;
            line-height: 1.45;
        }}

        .apps-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }}

        .app-card {{
            background: #ffffff;
            border-radius: 22px;
            padding: 32px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            display: flex;
            flex-direction: column;
        }}

        .app-card h2 {{
            margin: 0 0 12px;
            font-size: 28px;
            color: #111;
        }}

        .app-card > p {{
            margin: 0 0 22px;
            font-size: 16px;
            color: #444;
            flex-grow: 1;
        }}

        .app-actions {{
            margin-bottom: 16px;
        }}

        .button {{
            display: inline-block;
            padding: 12px 18px;
            border-radius: 12px;
            text-decoration: none;
            background: #007aff;
            color: #ffffff;
            font-weight: 600;
            font-size: 15px;
        }}

        .button:hover {{
            background: #0066d6;
        }}

        .app-links {{
            margin: 0;
            font-size: 14px;
            color: #666;
        }}

        .app-links a {{
            color: #007aff;
            text-decoration: none;
        }}

        .app-links a:hover {{
            text-decoration: underline;
        }}

        footer {{
            text-align: center;
            margin-top: 56px;
            font-size: 14px;
            color: #666;
        }}

        .contact-line {{
            margin: 0 0 18px;
        }}

        .contact-line a {{
            color: #007aff;
        }}

        .lang-nav {{
            margin-bottom: 12px;
            font-size: 13px;
        }}

        .lang-nav a {{
            color: #666;
            text-decoration: none;
            padding: 2px 4px;
        }}

        .lang-nav a:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        .lang-nav a.active {{
            font-weight: 600;
            color: #111;
        }}

        .copyright {{
            margin: 0;
            color: #888;
            font-size: 13px;
        }}

        @media (max-width: 640px) {{
            .container {{
                padding: 48px 16px 40px;
            }}

            h1 {{
                font-size: 38px;
            }}

            .tagline {{
                font-size: 18px;
            }}

            .apps-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

    <main class="container">

        <section class="hero">
            <h1>{d["heading"]}</h1>
            <p class="tagline">{d["tagline"]}</p>
        </section>

        <section class="apps-grid" aria-label="Apps">
{cards_block}
        </section>

        <footer>
            <p class="contact-line">
                {d["contact_label"]}
                <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>
            </p>
            <nav class="lang-nav" aria-label="{d["nav_aria"]}">
            {lang_links}
            </nav>
            <p class="copyright">{d["copyright"]}</p>
        </footer>

    </main>

</body>
</html>
"""


def build_pm_index(lang_code: str) -> str:
    pm = PLUSMINUS_DATA[lang_code]
    d = pm["index"]
    prefix = "" if lang_code == "en" else "fi/"
    canonical = f"{BASE_URL}/plusminus/{prefix}"
    lang_links = lang_nav_links("index.html", lang_code)

    tips_html = []
    for title, body in d["tips"]:
        tips_html.append(
            f"""        <p>
            <strong>{title}</strong>
            {body}
        </p>"""
        )
    tips_block = "\n\n".join(tips_html)

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{d["title"]}</title>
    <meta name="description" content="{html.escape(d["desc"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/plusminus/">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/plusminus/">
    <link rel="alternate" hreflang="fi" href="{BASE_URL}/plusminus/fi/">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #222;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 8px;
        }}

        .card {{
            background: #f6f7f9;
            border-radius: 16px;
            padding: 24px;
            margin: 28px 0;
        }}

        .card h2 {{
            margin: 0 0 12px;
            font-size: 19px;
            color: #111;
        }}

        .card p {{
            margin: 0 0 14px;
            font-size: 15px;
            line-height: 1.5;
            color: #444;
        }}

        .card p:last-child {{
            margin-bottom: 0;
        }}

        .faq-card {{
            background: #ffffff;
            border: 1.5px solid #007aff;
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.06);
        }}

        .faq-card h2 {{
            color: #007aff;
        }}

        .faq-card-link {{
            display: inline-block;
            font-weight: 600;
            color: #007aff;
            text-decoration: none;
        }}

        .faq-card-link:hover {{
            text-decoration: underline;
        }}

        code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 13px;
            background: #e9ecf0;
            padding: 1px 5px;
            border-radius: 4px;
        }}

        a {{
            color: #007aff;
        }}

        footer {{
            margin-top: 50px;
            font-size: 14px;
            color: #666;
        }}

        .links-nav {{
            margin: 40px 0 20px;
        }}

        .lang-nav {{
            margin-bottom: 12px;
            font-size: 13px;
        }}

        .lang-nav a {{
            color: #666;
            text-decoration: none;
            padding: 2px 4px;
        }}

        .lang-nav a:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        .lang-nav a.active {{
            font-weight: 600;
            color: #111;
        }}

        .copyright {{
            margin: 0;
            color: #888;
            font-size: 13px;
        }}
    </style>
</head>
<body>

    <h1>{d["heading"]}</h1>

    <p>
        {d["thank_you"]}
    </p>

    <div class="card faq-card">
        <h2>{d["faq_card_title"]}</h2>
        <p>
            {d["faq_card_body"]}
        </p>
        <p>
            <a href="faq.html" class="faq-card-link">{d["faq_card_action"]} &rarr;</a>
        </p>
    </div>

    <div class="card">
        <h2>{d["card_title"]}</h2>

{tips_block}
    </div>

    <p>
        {d["contact_intro"]}
    </p>

    <p>
        <strong>{d["email_label"]}</strong>
        <a href="mailto:{PLUSMINUS_EMAIL}?subject={quote(PLUSMINUS_EMAIL_SUBJECTS[('index', lang_code)])}">
            {PLUSMINUS_EMAIL}
        </a>
    </p>

    <p>
        {d["report_tip"]}
    </p>

    <p class="links-nav">
        <a href="marketing.html">{d["about_link"]}</a>
        &middot;
        <a href="faq.html">{d["faq_link"]}</a>
        &middot;
        <a href="privacy.html">{d["privacy_link"]}</a>
        &middot;
        <a href="{pm["home_href"]}">{pm["home_label"]}</a>
    </p>

    <footer>
        <nav class="lang-nav" aria-label="{d["nav_aria"]}">
            {lang_links}
        </nav>
        <p class="copyright">{d["copyright"]}</p>
    </footer>

</body>
</html>
"""


def build_pm_faq(lang_code: str) -> str:
    pm = PLUSMINUS_DATA[lang_code]
    d = pm["faq"]
    prefix = "" if lang_code == "en" else "fi/"
    canonical = f"{BASE_URL}/plusminus/{prefix}faq.html"
    lang_links = lang_nav_links("faq.html", lang_code)

    toc_items = []
    faq_blocks = []
    for idx, item in enumerate(d["items"], 1):
        toc_items.append(f'            <li><a href="#faq-{idx}">{item["question"]}</a></li>')

        bullets_html = "\n".join(f'            <li>{b}</li>' for b in item["bullets"])
        note_html = ""
        if item.get("note"):
            note_html = f"""
        <div class="note">
            {item["note"]}
        </div>"""

        faq_blocks.append(
            f"""    <div class="faq-item" id="faq-{idx}">
        <h2>{item["question"]}</h2>
        <p>{item["intro"]}</p>
        <ul>
{bullets_html}
        </ul>{note_html}
        <a href="#top" class="back-to-top">{d["back_to_top"]}</a>
    </div>"""
        )

    toc_list = "\n".join(toc_items)
    items_block = "\n\n".join(faq_blocks)

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{d["title"]}</title>
    <meta name="description" content="{html.escape(d["desc"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/plusminus/faq.html">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/plusminus/faq.html">
    <link rel="alternate" hreflang="fi" href="{BASE_URL}/plusminus/fi/faq.html">
    <style>
        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #222;
        }}

        h1 {{
            font-size: 32px;
            margin-bottom: 8px;
        }}

        .subtitle {{
            font-size: 18px;
            color: #666;
            margin-top: 0;
            margin-bottom: 32px;
        }}

        .toc {{
            background: #ffffff;
            border: 1px solid #e5e5ea;
            border-radius: 16px;
            padding: 22px 28px;
            margin-bottom: 36px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }}

        .toc-title {{
            margin: 0 0 14px;
            font-size: 13px;
            font-weight: 600;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .toc ol {{
            margin: 0;
            padding-left: 20px;
        }}

        .toc li {{
            margin-bottom: 8px;
            font-size: 15px;
            line-height: 1.45;
        }}

        .toc li:last-child {{
            margin-bottom: 0;
        }}

        .toc a {{
            color: #007aff;
            text-decoration: none;
        }}

        .toc a:hover {{
            text-decoration: underline;
        }}

        .top-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 28px;
            font-size: 14px;
        }}

        .top-nav a {{
            color: #007aff;
            text-decoration: none;
        }}

        .top-nav a:hover {{
            text-decoration: underline;
        }}

        .top-nav .back-link {{
            font-weight: 600;
        }}

        .top-nav-links {{
            color: #888;
        }}

        .toc-contact-tip {{
            margin: 18px 0 0;
            padding-top: 14px;
            border-top: 1px solid #e5e5ea;
            font-size: 14px;
            color: #555;
            line-height: 1.45;
        }}

        .toc-contact-tip a {{
            font-weight: 600;
            color: #007aff;
            text-decoration: none;
        }}

        .toc-contact-tip a:hover {{
            text-decoration: underline;
        }}

        .faq-item {{
            background: #f6f7f9;
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 24px;
            scroll-margin-top: 24px;
        }}

        .faq-item h2 {{
            margin: 0 0 16px;
            font-size: 20px;
            color: #111;
        }}

        .faq-item p {{
            margin: 0 0 12px;
            font-size: 16px;
            line-height: 1.6;
        }}

        ol, ul {{
            padding-left: 20px;
            margin: 0 0 16px;
        }}

        ol li, ul li {{
            margin-bottom: 8px;
            font-size: 16px;
            line-height: 1.5;
        }}

        code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 14px;
            background: #e9ecf0;
            padding: 1px 5px;
            border-radius: 4px;
        }}

        .note {{
            background: #fff;
            border-left: 4px solid #007aff;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #444;
            margin-top: 16px;
        }}

        .back-to-top {{
            display: inline-block;
            margin-top: 14px;
            font-size: 13px;
            color: #8e8e93;
            text-decoration: none;
            font-weight: 500;
        }}

        .back-to-top:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        a {{
            color: #007aff;
        }}

        footer {{
            margin-top: 50px;
            font-size: 14px;
            color: #666;
        }}

        .links-nav {{
            margin: 40px 0 20px;
        }}

        .lang-nav {{
            margin-bottom: 12px;
            font-size: 13px;
        }}

        .lang-nav a {{
            color: #666;
            text-decoration: none;
            padding: 2px 4px;
        }}

        .lang-nav a:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        .lang-nav a.active {{
            font-weight: 600;
            color: #111;
        }}

        .copyright {{
            margin: 0;
            color: #888;
            font-size: 13px;
        }}
    </style>
</head>
<body id="top">

    <nav class="top-nav" aria-label="Site navigation">
        <a href="index.html" class="back-link">{d["back_label"]}</a>
        <span class="top-nav-links">
            <a href="marketing.html">{d["about_link"]}</a>
            &middot;
            <a href="privacy.html">{d["privacy_link"]}</a>
            &middot;
            <a href="{pm["home_href"]}">{pm["home_label"]}</a>
        </span>
    </nav>

    <h1>{d["heading"]}</h1>
    <p class="subtitle">{d["subtitle"]}</p>

    <nav class="toc" aria-label="{d["toc_title"]}">
        <h2 class="toc-title">{d["toc_title"]}</h2>
        <ol>
{toc_list}
        </ol>
        <p class="toc-contact-tip">
            {d["toc_tip"]}
        </p>
    </nav>

{items_block}

    <p class="links-nav">
        <a href="marketing.html">{d["about_link"]}</a>
        &middot;
        <a href="privacy.html">{d["privacy_link"]}</a>
        &middot;
        <a href="index.html">{pm["privacy"]["support_link"]}</a>
        &middot;
        <a href="{pm["home_href"]}">{pm["home_label"]}</a>
    </p>

    <footer>
        <nav class="lang-nav" aria-label="{d["nav_aria"]}">
            {lang_links}
        </nav>
        <p class="copyright">{d["copyright"]}</p>
    </footer>

</body>
</html>
"""


def build_pm_marketing(lang_code: str) -> str:
    pm = PLUSMINUS_DATA[lang_code]
    d = pm["marketing"]
    lang_links = lang_nav_links("marketing.html", lang_code)

    ld_json = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "MobileApplication",
            "name": "PlusMinus",
            "url": d["canonical"],
            "description": d["desc"],
            "applicationCategory": "FinanceApplication",
            "operatingSystem": "iOS",
            "inLanguage": ["en", "fi"],
            "featureList": d["featureList"],
        },
        indent=8,
        ensure_ascii=False,
    )

    feature_cards = "\n\n".join(
        f"""                <article class="feature">
                    <h3>{title}</h3>
                    <p>{body}</p>
                </article>"""
        for title, body in d["features"]
    )

    list_items = "\n".join(f"                <li>{item}</li>" for item in d["list_items"])

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{d["title"]}</title>

    <meta name="description" content="{html.escape(d["desc"])}">
    <meta name="robots" content="index, follow">

    <link rel="canonical" href="{d["canonical"]}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/plusminus/marketing.html">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/plusminus/marketing.html">
    <link rel="alternate" hreflang="fi" href="{BASE_URL}/plusminus/fi/marketing.html">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="PlusMinus">
    <meta property="og:title" content="{html.escape(d["title"])}">
    <meta property="og:description" content="{html.escape(d["desc"])}">
    <meta property="og:url" content="{d["canonical"]}">
    <meta property="og:locale" content="{lang_code}">

    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{html.escape(d["title"])}">
    <meta name="twitter:description" content="{html.escape(d["desc"])}">

    <script type="application/ld+json">
    {ld_json}
    </script>
    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f6f7f9;
            color: #1d1d1f;
        }}

        .container {{
            max-width: 860px;
            margin: 0 auto;
            padding: 80px 24px;
        }}

        .hero {{
            text-align: center;
            padding: 40px 0 70px;
        }}

        h1 {{
            font-size: 56px;
            margin: 0 0 16px;
            letter-spacing: -1.5px;
        }}

        .tagline {{
            font-size: 26px;
            color: #444;
            max-width: 680px;
            margin: 0 auto;
            line-height: 1.4;
        }}

        .subtitle {{
            font-size: 19px;
            color: #777;
            max-width: 680px;
            margin: 20px auto 0;
            line-height: 1.6;
        }}

        .section {{
            background: white;
            border-radius: 22px;
            padding: 36px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        }}

        h2 {{
            margin-top: 0;
            font-size: 28px;
        }}

        h3 {{
            margin: 0 0 10px;
            font-size: 21px;
        }}

        p {{
            font-size: 18px;
            line-height: 1.6;
            color: #444;
        }}

        .feature-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
        }}

        .feature {{
            padding: 22px;
            border-radius: 16px;
            background: #f6f7f9;
        }}

        .feature p {{
            margin: 0;
            font-size: 16px;
        }}

        .compact-list {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px 32px;
            padding-left: 22px;
            margin-bottom: 0;
        }}

        .compact-list li {{
            font-size: 17px;
            line-height: 1.5;
        }}

        .links {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 24px;
        }}

        .button {{
            display: inline-block;
            padding: 13px 18px;
            border-radius: 12px;
            text-decoration: none;
            background: #007aff;
            color: white;
            font-weight: 600;
        }}

        .secondary {{
            background: #e8e8ed;
            color: #1d1d1f;
        }}

        .closing {{
            text-align: center;
        }}

        .closing p {{
            max-width: 620px;
            margin: 0 auto;
        }}

        .closing .links {{
            justify-content: center;
        }}

        footer {{
            text-align: center;
            padding: 40px 0 10px;
            color: #777;
            font-size: 14px;
        }}

        .lang-nav {{
            margin-bottom: 12px;
            font-size: 13px;
        }}

        .lang-nav a {{
            color: #666;
            text-decoration: none;
            padding: 2px 4px;
        }}

        .lang-nav a:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        .lang-nav a.active {{
            font-weight: 600;
            color: #111;
        }}

        .home-nav {{
            margin-bottom: 14px;
            font-size: 13px;
        }}

        .home-nav a {{
            color: #007aff;
            text-decoration: none;
        }}

        .home-nav a:hover {{
            text-decoration: underline;
        }}

        .copyright {{
            margin: 0;
            color: #888;
            font-size: 13px;
        }}

        @media (max-width: 600px) {{
            .container {{
                padding: 40px 16px;
            }}

            h1 {{
                font-size: 42px;
            }}

            .tagline {{
                font-size: 22px;
            }}

            .section {{
                padding: 26px;
            }}

            .feature-grid,
            .compact-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>

    <main class="container">

        <section class="hero">
            <h1>{d["hero_title"]}</h1>

            <p class="tagline">
                {d["tagline"]}
            </p>

            <p class="subtitle">
                {d["subtitle"]}
            </p>
        </section>

        <section class="section">
            <h2>{d["section1_title"]}</h2>

            <div class="feature-grid">
{feature_cards}
            </div>
        </section>

        <section class="section">
            <h2>{d["section2_title"]}</h2>

            <ul class="compact-list">
{list_items}
            </ul>
        </section>

        <section class="section closing">
            <h2>{d["closing_title"]}</h2>

            <p>
                {d["closing_body"]}
            </p>

            <div class="links">
                <a class="button secondary" href="faq.html">
                    {d["faq_btn"]}
                </a>

                <a class="button secondary" href="privacy.html">
                    {d["privacy_btn"]}
                </a>

                <a class="button secondary" href="index.html">
                    {d["support_btn"]}
                </a>
            </div>
        </section>

        <footer>
            <p class="home-nav">
                <a href="{pm["home_href"]}">{pm["home_label"]}</a>
            </p>
            <nav class="lang-nav" aria-label="{d["nav_aria"]}">
            {lang_links}
            </nav>
            <p class="copyright">{d["copyright"]}</p>
        </footer>

    </main>

</body>
</html>
"""


def build_pm_privacy(lang_code: str) -> str:
    pm = PLUSMINUS_DATA[lang_code]
    d = pm["privacy"]
    prefix = "" if lang_code == "en" else "fi/"
    canonical = f"{BASE_URL}/plusminus/{prefix}privacy.html"
    lang_links = lang_nav_links("privacy.html", lang_code)

    sections_html = []
    for title, paras in d["sections"]:
        p_blocks = "\n\n".join(f"    <p>\n        {p}\n    </p>" for p in paras)
        sections_html.append(f"    <h2>{title}</h2>\n\n{p_blocks}")
    sections_block = "\n\n".join(sections_html)

    return f"""<!DOCTYPE html>
<html lang="{lang_code}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{d["title"]}</title>
    <meta name="description" content="{html.escape(d["desc"])}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="x-default" href="{BASE_URL}/plusminus/privacy.html">
    <link rel="alternate" hreflang="en" href="{BASE_URL}/plusminus/privacy.html">
    <link rel="alternate" hreflang="fi" href="{BASE_URL}/plusminus/fi/privacy.html">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 0 20px;
            line-height: 1.6;
            color: #222;
        }}

        h1 {{
            font-size: 32px;
        }}

        h2 {{
            margin-top: 32px;
        }}

        a {{
            color: #007aff;
        }}

        footer {{
            margin-top: 50px;
            font-size: 14px;
            color: #666;
        }}

        .lang-nav {{
            margin-bottom: 12px;
            font-size: 13px;
        }}

        .lang-nav a {{
            color: #666;
            text-decoration: none;
            padding: 2px 4px;
        }}

        .lang-nav a:hover {{
            color: #007aff;
            text-decoration: underline;
        }}

        .lang-nav a.active {{
            font-weight: 600;
            color: #111;
        }}

        .copyright {{
            margin: 0;
            color: #888;
            font-size: 13px;
        }}
    </style>
</head>
<body>

    <h1>{d["heading"]}</h1>

    <p>
        <strong>{d["last_updated"]}</strong>
    </p>

{sections_block}

    <h2>{d["contact_heading"]}</h2>

    <p>
        {d["contact_intro"]}
    </p>

    <p>
        <a href="mailto:{PLUSMINUS_EMAIL}?subject={quote(PLUSMINUS_EMAIL_SUBJECTS[('privacy', lang_code)])}">
            {PLUSMINUS_EMAIL}
        </a>
    </p>

    <p>
        <a href="marketing.html">{d["about_link"]}</a>
        &middot;
        <a href="faq.html">{d["faq_link"]}</a>
        &middot;
        <a href="index.html">{d["support_link"]}</a>
        &middot;
        <a href="{pm["home_href"]}">{pm["home_label"]}</a>
    </p>

    <footer>
        <nav class="lang-nav" aria-label="{d["nav_aria"]}">
            {lang_links}
        </nav>
        <p class="copyright">{d["copyright"]}</p>
    </footer>

</body>
</html>
"""


def build_sitemap() -> str:
    urls = []

    # Root landing pages (2)
    for lang in ["", "fi"]:
        prefix = f"{lang}/" if lang else ""
        urls.append((f"{BASE_URL}/{prefix}", "2026-11-23"))

    # WakeUp pages under /wakeup/ (24)
    for page in ["", "faq.html", "marketing.html", "privacy.html"]:
        for lang in WAKEUP_LANGS:
            prefix = f"{lang}/" if lang else ""
            urls.append((f"{BASE_URL}/wakeup/{prefix}{page}", "2026-11-23"))

    # PlusMinus pages under /plusminus/ (8)
    for page in ["", "faq.html", "marketing.html", "privacy.html"]:
        for lang in ["", "fi"]:
            prefix = f"{lang}/" if lang else ""
            urls.append((f"{BASE_URL}/plusminus/{prefix}{page}", "2026-11-23"))

    entries = "\n".join(
        f"""    <url>
        <loc>{xml_escape(loc)}</loc>
        <lastmod>{lastmod}</lastmod>
    </url>"""
        for loc, lastmod in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""


def write_output(rel_path: str, content: str) -> None:
    full_path = os.path.join(REPO_ROOT, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    # 1. Root landing pages (EN & FI)
    write_output("index.html", build_root_index("en"))
    write_output("fi/index.html", build_root_index("fi"))

    # 2. PlusMinus pages (EN & FI)
    for lang in PLUSMINUS_LANGS:
        code = lang["code"]
        subdir = "plusminus" if not lang["dir"] else os.path.join("plusminus", lang["dir"])
        write_output(os.path.join(subdir, "index.html"), build_pm_index(code))
        write_output(os.path.join(subdir, "faq.html"), build_pm_faq(code))
        write_output(os.path.join(subdir, "marketing.html"), build_pm_marketing(code))
        write_output(os.path.join(subdir, "privacy.html"), build_pm_privacy(code))

    # 3. Unified sitemap.xml
    write_output("sitemap.xml", build_sitemap())
    print("Generated 2 root pages, 8 PlusMinus pages, and sitemap.xml successfully.")


if __name__ == "__main__":
    main()
