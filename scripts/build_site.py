# -*- coding: utf-8 -*-
"""Generates Lightfeet Apps root landing pages, PlusMinus support/marketing/FAQ/privacy
pages (EN, FI, SV, DE, ES, FR), and the unified root sitemap.xml for lightfeetapps.com.

Note: WakeUp pages under /wakeup/ are maintained directly in this repository and
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
    ("index", "sv"): "PlusMinus Support",
    ("index", "de"): "PlusMinus Support",
    ("index", "es"): "Soporte de PlusMinus",
    ("index", "fr"): "Assistance PlusMinus",
    ("privacy", "en"): "PlusMinus Privacy",
    ("privacy", "fi"): "PlusMinus - Tietosuoja",
    ("privacy", "sv"): "PlusMinus Integritet",
    ("privacy", "de"): "PlusMinus Datenschutz",
    ("privacy", "es"): "Privacidad de PlusMinus",
    ("privacy", "fr"): "Confidentialité PlusMinus",
}
WAKEUP_LANGS = ["", "fi", "sv", "de", "es", "fr"]
SITE_LANGS = [
    {"code": "en", "name": "English", "dir": ""},
    {"code": "fi", "name": "Suomi", "dir": "fi"},
    {"code": "sv", "name": "Svenska", "dir": "sv"},
    {"code": "de", "name": "Deutsch", "dir": "de"},
    {"code": "es", "name": "Español", "dir": "es"},
    {"code": "fr", "name": "Français", "dir": "fr"},
]


def lang_nav_links(page_name: str, current_lang: str) -> str:
    """Build language switcher HTML for 6-language sections (Root and PlusMinus)."""
    parts = []
    for lang in SITE_LANGS:
        code = lang["code"]
        is_active = code == current_lang
        if current_lang == "en":
            href = page_name if code == "en" else f"{lang['dir']}/{page_name}"
        elif code == "en":
            href = f"../{page_name}"
        elif is_active:
            href = page_name
        else:
            href = f"../{lang['dir']}/{page_name}"
        cls = ' class="active"' if is_active else ""
        parts.append(f'<a href="{href}"{cls}>{lang["name"]}</a>')
    return "\n            &middot;\n            ".join(parts)


def hreflang_links(section_prefix: str, page_name: str = "") -> str:
    """Build x-default + 6-language alternate hreflang link tags."""
    base = f"{BASE_URL}/{section_prefix}"
    lines = [f'    <link rel="alternate" hreflang="x-default" href="{base}{page_name}">']
    for lang in SITE_LANGS:
        lang_dir = f"{lang['dir']}/" if lang["dir"] else ""
        lines.append(
            f'    <link rel="alternate" hreflang="{lang["code"]}" href="{base}{lang_dir}{page_name}">'
        )
    return "\n".join(lines)


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
    "sv": {
        "title": "Lightfeet Apps",
        "desc": "Fokuserade, omsorgsfullt skapade appar för iPhone och iPad från Lightfeet Apps: WakeUp och PlusMinus.",
        "canonical": f"{BASE_URL}/sv/",
        "heading": "Lightfeet Apps",
        "tagline": "Fokuserade, omsorgsfullt skapade appar för iPhone och iPad.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Flexibelt alarm för ändrade planer. Hoppa över, justera en gång eller pausa återkommande alarm utan att ändra ditt vanliga schema.",
                "primary_href": "../wakeup/sv/marketing.html",
                "primary_label": "Om WakeUp",
                "links": [
                    ("../wakeup/sv/faq.html", "FAQ"),
                    ("../wakeup/sv/", "Support"),
                    ("../wakeup/sv/privacy.html", "Integritetspolicy"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Lugn månadsbudget direkt på enheten. Se med en blick vad du tryggt kan spendera just nu — utan att logga varje köp.",
                "primary_href": "../plusminus/sv/marketing.html",
                "primary_label": "Om PlusMinus",
                "links": [
                    ("../plusminus/sv/faq.html", "FAQ"),
                    ("../plusminus/sv/", "Support"),
                    ("../plusminus/sv/privacy.html", "Integritetspolicy"),
                ],
            },
        ],
        "contact_label": "Kontakt:",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Språkval",
    },
    "de": {
        "title": "Lightfeet Apps",
        "desc": "Fokussierte, sorgfältig gestaltete Apps für iPhone und iPad von Lightfeet Apps: WakeUp und PlusMinus.",
        "canonical": f"{BASE_URL}/de/",
        "heading": "Lightfeet Apps",
        "tagline": "Fokussierte, sorgfältig gestaltete Apps für iPhone und iPad.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Flexibler Wecker für wechselnde Pläne. Nächsten Wecker auslassen, einmalig anpassen oder pausieren, ohne deine normale Routine zu verändern.",
                "primary_href": "../wakeup/de/marketing.html",
                "primary_label": "Über WakeUp",
                "links": [
                    ("../wakeup/de/faq.html", "FAQ"),
                    ("../wakeup/de/", "Support"),
                    ("../wakeup/de/privacy.html", "Datenschutzerklärung"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Ruhiges Monatsbudget lokal auf deinem Gerät. Sieh auf einen Blick, was du jetzt frei ausgeben kannst – ohne jeden Einkauf einzutragen.",
                "primary_href": "../plusminus/de/marketing.html",
                "primary_label": "Über PlusMinus",
                "links": [
                    ("../plusminus/de/faq.html", "FAQ"),
                    ("../plusminus/de/", "Support"),
                    ("../plusminus/de/privacy.html", "Datenschutzerklärung"),
                ],
            },
        ],
        "contact_label": "Kontakt:",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Sprachauswahl",
    },
    "es": {
        "title": "Lightfeet Apps",
        "desc": "Apps centradas y cuidadas al detalle para iPhone y iPad de Lightfeet Apps: WakeUp y PlusMinus.",
        "canonical": f"{BASE_URL}/es/",
        "heading": "Lightfeet Apps",
        "tagline": "Apps centradas y cuidadas al detalle para iPhone y iPad.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Despertador flexible para planes que cambian. Omite, ajusta una vez o pausa alarmas recurrentes sin cambiar tu horario habitual.",
                "primary_href": "../wakeup/es/marketing.html",
                "primary_label": "Acerca de WakeUp",
                "links": [
                    ("../wakeup/es/faq.html", "Preguntas frecuentes"),
                    ("../wakeup/es/", "Soporte"),
                    ("../wakeup/es/privacy.html", "Política de privacidad"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Presupuesto mensual sereno que funciona en tu dispositivo. Ve de un vistazo lo que puedes gastar ahora con tranquilidad — sin registrar cada compra.",
                "primary_href": "../plusminus/es/marketing.html",
                "primary_label": "Acerca de PlusMinus",
                "links": [
                    ("../plusminus/es/faq.html", "Preguntas frecuentes"),
                    ("../plusminus/es/", "Soporte"),
                    ("../plusminus/es/privacy.html", "Política de privacidad"),
                ],
            },
        ],
        "contact_label": "Contacto:",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Selección de idioma",
    },
    "fr": {
        "title": "Lightfeet Apps",
        "desc": "Des apps ciblées et soigneusement conçues pour iPhone et iPad par Lightfeet Apps : WakeUp et PlusMinus.",
        "canonical": f"{BASE_URL}/fr/",
        "heading": "Lightfeet Apps",
        "tagline": "Des apps ciblées et soigneusement conçues pour iPhone et iPad.",
        "apps": [
            {
                "name": "WakeUp",
                "summary": "Réveil flexible pour les imprévus. Ignorez, ajustez une fois ou mettez en pause des alarmes récurrentes sans modifier votre routine habituelle.",
                "primary_href": "../wakeup/fr/marketing.html",
                "primary_label": "À propos de WakeUp",
                "links": [
                    ("../wakeup/fr/faq.html", "FAQ"),
                    ("../wakeup/fr/", "Assistance"),
                    ("../wakeup/fr/privacy.html", "Politique de confidentialité"),
                ],
            },
            {
                "name": "PlusMinus",
                "summary": "Budget mensuel serein et local avant tout. Voyez en un coup d’œil ce que vous pouvez dépenser maintenant — sans noter chaque achat.",
                "primary_href": "../plusminus/fr/marketing.html",
                "primary_label": "À propos de PlusMinus",
                "links": [
                    ("../plusminus/fr/faq.html", "FAQ"),
                    ("../plusminus/fr/", "Assistance"),
                    ("../plusminus/fr/privacy.html", "Politique de confidentialité"),
                ],
            },
        ],
        "contact_label": "Contact :",
        "copyright": "&copy; 2026 Lightfeet Apps",
        "nav_aria": "Choix de la langue",
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
            "faq_card_body": "Before sending an email, please check our Frequently Asked Questions (FAQ). You will find clear answers covering Safe to Spend, the difference between Live and Plan, Plan analysis, food budget proration, double-deduction protection, backups, and privacy.",
            "faq_card_action": "Browse Frequently Asked Questions (FAQ)",
            "card_title": "Troubleshooting & Good to know",
            "tips": [
                (
                    "Safe to Spend looks higher or lower than expected:",
                    "Make sure <strong>Current money</strong> reflects your real balance right now, and review any unpaid or overdue expenses in <strong>Live</strong>. Scheduled future income (recurring or one-time) arriving before your next primary payday is automatically factored into Safe to Spend using the tightest cash-flow point (without letting you spend money before it arrives), while overdue and due-today income waits until you mark it received. Tap the info button beside Safe to Spend for the exact <strong>Spending calculation</strong>, or review all rules in <strong>Settings &rarr; Understanding PlusMinus &rarr; How Calculations Work</strong>."
                ),
                (
                    "Avoiding double-deductions when marking expenses paid:",
                    "When you tap <strong>Mark Paid</strong>, PlusMinus asks whether to <strong>Subtract from Current Money</strong> or keep your balance unchanged because <strong>Current Money already reflects this</strong>. If you update your balance manually first, quick reconciliation chips let you mark settled expenses without subtracting them twice, and <strong>Undo</strong> lets you reverse a mistake immediately."
                ),
                (
                    "Backups and moving to another device:",
                    "PlusMinus stores all budget data locally on your device. To move your budget or keep a copy, open <strong>Settings &rarr; Data &amp; Privacy &rarr; Backup &amp; Restore</strong> and tap <strong>Create Backup</strong> to save a <code>.plusminusbackup</code> file via Files. Restoring a backup replaces all current budget data and restores the balance as it was when the backup was created, while keeping your app language and appearance unchanged."
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
            "desc": "Frequently asked questions and guides for PlusMinus on iPhone and iPad: Safe to Spend calculation, Live vs. Plan, Plan analysis, daily food budget proration, double-deduction protection, custom-month expenses, rounding, backups, privacy, and supported languages.",
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
                    "intro": "<strong>Live</strong> answers one practical question: <em>How much money can I safely spend right now until my next primary payday?</em> It starts from a clear formula and automatically handles scheduled upcoming income:",
                    "bullets": [
                        "<strong>Current money:</strong> Your manually maintained checking or cash balance right now, shown with a relative last-updated timestamp.",
                        "<strong>Minus unpaid expenses:</strong> Unpaid recurring expenses and one-time expenses due before your next primary payday, plus any overdue unpaid expenses from the immediately preceding pay period.",
                        "<strong>Minus remaining food estimate:</strong> Your estimated remaining food budget for the active cash-flow horizon.",
                        "<strong>Tightest cash-flow point for upcoming income:</strong> When scheduled future income (recurring or one-time) arrives before your next primary payday, PlusMinus checks your balance before each upcoming income date and through the end of the cycle, picking the tightest point so later expenses don't cause false shortages while you never spend money before it arrives. Tap the info button beside Safe to Spend to open <strong>Spending calculation</strong>, which always matches that limiting horizon line by line (showing <strong>Income added to this calculation</strong>, <strong>Reserved for expenses before [date]</strong>, <strong>Food estimate</strong>, and any <strong>Later unpaid expenses</strong>), while the hero overline clearly reads <code>SAFE TO SPEND &middot; CONSIDERING UPCOMING INCOME</code> whenever upcoming income is factored in."
                    ],
                    "note": "<strong>Tip:</strong> You can review the calculation rules at any time inside the app under <strong>Settings &rarr; Understanding PlusMinus &rarr; How Calculations Work</strong>."
                },
                {
                    "question": "What is the difference between Live and Plan?",
                    "intro": "PlusMinus separates day-to-day spending awareness from your long-term monthly baseline across two distinct tabs:",
                    "bullets": [
                        "<strong>Live:</strong> Covers right now until your next primary payday. It starts from your real <strong>Current money</strong>, evaluates unpaid expenses, remaining food, and any future scheduled incomes across the tightest cash-flow point, and tells you your current <strong>Safe to Spend</strong> alongside expandable <strong>Upcoming income</strong> and <strong>Unpaid expenses</strong> lists.",
                        "<strong>Plan:</strong> Shows your steady-state <strong>Planned Monthly Remainder</strong> (normalized monthly income minus normalized monthly expenses minus your monthly food budget), completely independent of today's bank balance or payday cycle length. It also includes <strong>Where your income goes</strong> and <strong>Plan analysis</strong>, comparing your monthly allocation across categories and your food budget as amounts and shares of monthly income."
                    ],
                    "note": "<strong>Why both views?</strong> A yearly insurance expense or shorter February pay period affects how much cash you can spend right now in <strong>Live</strong>, while <strong>Plan</strong> tells you whether your normal income covers your regular expenses over time."
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
                    "question": "How does PlusMinus prevent deducting the same expense twice?",
                    "intro": "Because you update your balance manually without a bank connection, PlusMinus includes built-in safeguards so paid expenses never reduce Safe to Spend twice:",
                    "bullets": [
                        "<strong>Two-button confirmation on Mark Paid:</strong> When marking an expense paid, PlusMinus asks whether to <strong>Subtract from Current Money</strong> or keep your balance as-is because <strong>Current Money already reflects this</strong> (with smart emphasis if you updated your balance within the last 5 minutes).",
                        "<strong>Quick reconciliation chips:</strong> After a manual balance update, quick chips let you mark recently due expenses as settled without subtracting them from your balance again.",
                        "<strong>Safe Undo:</strong> If you tap the wrong option, tap <strong>Undo</strong> right away to restore the expense and any automatic balance change cleanly."
                    ]
                },
                {
                    "question": "How does upcoming income affect Safe to Spend?",
                    "intro": "PlusMinus works cleanly whether you have one main paycheck, 2&ndash;3 staggered recurring incomes, or a scheduled future one-time payment:",
                    "bullets": [
                        "<strong>Future scheduled income (automatic cash-flow bottleneck):</strong> Active recurring and one-time income scheduled strictly after today (and after the current cycle's nominal primary payday when weekend shifting applies) and before your next primary payday is automatically factored into <strong>Safe to Spend</strong> via the tightest checkpoint &mdash; preventing false shortages from later expenses while never letting you spend money before it arrives.",
                        "<strong>Clear labels and exact breakdown:</strong> When upcoming income raises Safe to Spend above cash on hand alone, the hero overline updates to <code>SAFE TO SPEND &middot; CONSIDERING UPCOMING INCOME</code> (with a <code>Full period through &hellip;</code> footnote below when the limiting point ends earlier). Tap the info button for <strong>Spending calculation</strong> to inspect <strong>Income added to this calculation</strong> (distinct from the overview's total <strong>Upcoming income</strong>) and any <strong>Later unpaid expenses</strong> covered by later income.",
                        "<strong>Overdue and due-today income:</strong> Overdue and due-today incomes (both recurring and one-time) are never projected ahead of receipt &mdash; they appear as reminder rows and count only once marked <strong>Received</strong> (or reflected in <strong>Current money</strong>). You can also mark a missed income as <strong>Income cancelled</strong> without altering your balance.",
                        "<strong>No double-counting when received:</strong> Marking an included upcoming income <strong>Received</strong> and adding it to <strong>Current money</strong> moves it cleanly into your balance without double-counting."
                    ]
                },
                {
                    "question": "How do Custom Months, Yearly, Weekly, Biweekly, One-Time items, and Plan analysis work?",
                    "intro": "PlusMinus handles regular expenses, irregular schedules, and category breakdowns accurately across <strong>Plan</strong> and <strong>Live</strong>:",
                    "bullets": [
                        "<strong>Plan normalization:</strong> Weekly items normalize via <code>&times; 52 &divide; 12</code>, every 2 weeks via <code>&times; 26 &divide; 12</code>, <strong>Custom Months</strong> (such as January &amp; October or Quarterly presets) via <code>&times; selected months &divide; 12</code>, and yearly items via <code>&divide; 12</code>.",
                        "<strong>Live full deductions:</strong> Yearly and custom-month expenses are deducted in full during the actual pay period when they fall due, so you see their real cash impact before payday.",
                        "<strong>One-Time items:</strong> One-time income and one-time expenses (for example a tax refund or car repair) have an exact date and can be added in <strong>Plan</strong> or via the <code>+</code> menu in <strong>Live</strong>. They are excluded from your steady-state <strong>Plan</strong> baseline: one-time expenses deduct in full when due in <strong>Live</strong>, while future scheduled one-time income before next payday enters the <strong>Safe to Spend</strong> cash-flow check without spending it early.",
                        "<strong>17 categories, Plan analysis &amp; optional due days:</strong> Expenses can be grouped into 17 optional categories (Housing, Utilities, Subscriptions, Insurance, Loans, Credit Cards &amp; Consumer Credit, Transport, Hobbies, Sports &amp; Fitness, Investing, Health &amp; Wellbeing, Children &amp; Family, Pets, Education, Saving, Giving, Other). On <strong>Plan</strong>, <strong>Where your income goes</strong> and <strong>Plan analysis</strong> compare active recurring expense categories (plus Uncategorized and Food Budget) by monthly amount and share of monthly income. Recurring expenses can also omit a specific due day (<strong>No specific day</strong>) if needed."
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
                    "question": "What are Coming Next Period, paying expenses early, and older unsettled expenses?",
                    "intro": "PlusMinus makes it easy to stay ahead of upcoming cycles and keep older periods tidy:",
                    "bullets": [
                        "<strong>Coming Next Period &amp; early payment:</strong> Expand <strong>Coming Next Period</strong> in <strong>Live</strong> to preview expenses due after your next primary payday. If you already paid a next-period expense early, mark it paid there with the same balance consistency check.",
                        "<strong>Older unsettled expenses (Mark older settled):</strong> Unpaid expenses from before the previous cycle (up to 24 months old) are excluded from deducting against your current <strong>Safe to Spend</strong> and surfaced in a non-destructive catch-up banner with <strong>Mark older settled</strong>."
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
                        "<strong>Stored on your device:</strong> Balances, incomes, expenses, payment history, and preferences stay locally on your iPhone or iPad.",
                        "<strong>No accounts or bank links:</strong> PlusMinus requires no account and never asks for bank credentials or Open Banking access.",
                        "<strong>Zero tracking or ads:</strong> There are no analytics SDKs, no advertising identifiers, and no automatic cloud sync in the background."
                    ]
                },
                {
                    "question": "How do Backup & Restore and Reset All Data work?",
                    "intro": "You stay in full control of your local budget data at all times:",
                    "bullets": [
                        "<strong>Create Backup:</strong> Open <strong>Settings &rarr; Data &amp; Privacy &rarr; Backup &amp; Restore</strong> and tap <strong>Create Backup</strong> to export a readable JSON archive (<code>.plusminusbackup</code>, not password-protected) to iCloud Drive, local storage, or any location in Files.",
                        "<strong>Restore from Backup:</strong> Tap <strong>Restore from Backup</strong> and select a valid <code>.plusminusbackup</code> file (up to 50 MB). Restoring replaces all current budget data and restores the balance from when the backup was created, while keeping your app language and appearance unchanged.",
                        "<strong>Reset All Data:</strong> Under <strong>Settings &rarr; Data &amp; Privacy</strong>, <strong>Reset All Data</strong> uses a two-step confirmation to erase all local budget data and preferences on this device and return to initial setup. Exported backup files and iOS system backups are not deleted."
                    ]
                },
                {
                    "question": "What languages, currencies, themes, and devices are supported?",
                    "intro": "PlusMinus adapts to your preferred language, currency, and appearance:",
                    "bullets": [
                        "<strong>Languages:</strong> Switchable directly inside <strong>Settings &rarr; Preferences &rarr; Language</strong> between <strong>System Default</strong>, <strong>English</strong>, <strong>Suomi</strong> (Finnish), <strong>Svenska</strong> (Swedish), <strong>Deutsch</strong> (German), <strong>Espa&ntilde;ol</strong> (Spanish), and <strong>Fran&ccedil;ais</strong> (French) without restarting the app.",
                        "<strong>Currencies:</strong> Supports <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD,</strong> and <strong>JPY</strong> under <strong>Settings &rarr; Preferences &rarr; Currency</strong>.",
                        "<strong>Appearance:</strong> Choose <strong>System Default</strong>, <strong>Dark</strong>, or <strong>Light</strong> under <strong>Settings &rarr; Preferences &rarr; Appearance</strong>.",
                        "<strong>Supported devices:</strong> Built for iPhone and iPad running <strong>iOS 26 or later</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Calm Monthly Budget & Safe to Spend for iPhone and iPad",
            "desc": "Know what you can safely spend right now without logging every purchase. Local-first budgeting with payday cycle food proration, Plan analysis, and no bank connections.",
            "canonical": f"{BASE_URL}/plusminus/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Know what you can safely spend right now.",
            "subtitle": "Set your recurring income, recurring expenses, payday, and monthly food budget once. Glance at your balance and see what is genuinely free to spend — without logging every coffee.",
            "section1_title": "Clarity in under five seconds",
            "features": [
                ("Live Safe to Spend", "Current money, unpaid expenses, remaining food estimate, and scheduled upcoming incomes evaluated at the tightest cash-flow point &mdash; always explained step by step."),
                ("Steady Monthly Plan", "Separate monthly overview normalizing weekly, biweekly, custom-month, and yearly expenses &mdash; with Plan analysis by category &mdash; without today's cash getting in the way."),
                ("Private & Local-First", "Everything stays on your device. No accounts, no bank logins, no analytics, and no tracking — ever."),
            ],
            "section2_title": "Everything you need, nothing you don't",
            "list_items": [
                "Live Safe to Spend calculated up to your next primary payday &mdash; with automatic recurring and one-time upcoming income cash-flow handling",
                "Transparent Spending calculation breakdown showing exact dates, reserves, and later expenses",
                "Automatic daily food budget proration with instant custom period override",
                "Double-deduction protection when marking expenses paid or updating balances",
                "Weekly, biweekly, monthly, custom-month, yearly, and one-time items",
                "Plan analysis comparing where your monthly income goes across 17 categories and food",
                "Weekend payday shifting to Friday and short-month date clamping",
                "Coming Next Period preview with early payment and older expense catch-up",
                "Manual .plusminusbackup export and restore via Files",
                "Available in 6 languages (English, Finnish, Swedish, German, Spanish, French) with 10 currencies and Light/Dark Mode",
            ],
            "closing_title": "Built for iPhone and iPad",
            "closing_body": "PlusMinus is designed for iPhone and iPad running iOS 26 or later.",
            "faq_btn": "FAQ",
            "privacy_btn": "Privacy Policy",
            "support_btn": "Support",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Language selection",
            "featureList": [
                "Live Safe to Spend calculation until next primary payday with multi-income and one-time cash-flow bottleneck",
                "Normalized Target Monthly Budget plan and Plan analysis across 17 expense categories",
                "Automatic daily food budget proration with custom override",
                "Two-button double-deduction prevention when marking expenses paid",
                "Custom-month, yearly, weekly, biweekly, and one-time schedules",
                "100% local-first storage with manual backup and restore via Files",
            ],
        },
        "privacy": {
            "title": "PlusMinus Privacy Policy",
            "desc": "Read the PlusMinus privacy policy: local-first budgeting on your device with no accounts, analytics, bank connections, or tracking.",
            "heading": "Privacy Policy for PlusMinus",
            "last_updated": "Last updated: November 25, 2026",
            "sections": [
                (
                    "Data on Your Device",
                    [
                        "PlusMinus is a local-first budgeting app. Your budget is not sent to the developer.",
                        "Balances, income, expenses, payment history, and budget settings are stored locally on your device. Language, appearance, and dismissed reminders are saved as local preferences.",
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
            "faq_card_body": "Ennen sähköpostin lähettämistä suosittelemme tutustumaan usein kysyttyihin kysymyksiin. Löydät sieltä selkeät ohjeet aiheista Käytettävissä nyt -laskenta, Tilanne- ja Kuukausi-näkymien erot, suunnitelman analyysi, ruokabudjetin suhteutus, kaksoisvähennysten esto, varmuuskopiot ja tietosuoja.",
            "faq_card_action": "Selaa usein kysyttyjä kysymyksiä (UKK)",
            "card_title": "Vianmääritys ja hyvä tietää",
            "tips": [
                (
                    "Käytettävissä nyt -summa näyttää odotettua suuremmalta tai pienemmältä:",
                    "Varmista, että <strong>Raha nyt</strong> vastaa tämänhetkistä saldoasi, ja tarkista maksamattomat tai myöhässä olevat menot <strong>Tilanne</strong>-näkymästä. Ennen seuraavaa ensisijaista palkkapäivää tulevat ajastetut tulot (säännölliset ja kertaluontoiset) huomioidaan automaattisesti tiukimman kassavirtakohdan mukaan (ilman että rahaa voi kuluttaa etukäteen), kun taas myöhässä olevat ja tänään erääntyvät tulot odottavat saaduksi kuittaamista. Napauta Käytettävissä nyt -summan vieressä olevaa infopainiketta nähdäksesi tarkan <strong>Käyttövaran laskelman</strong>, tai lue kaikki säännöt kohdasta <strong>Asetukset &rarr; Tietoa laskennasta &rarr; Miten laskenta toimii</strong>."
                ),
                (
                    "Kaksoisvähennysten estäminen menoja kuitattaessa:",
                    "Kun napautat menossa <strong>Maksettu</strong>, PlusMinus kysyy, haluatko <strong>Vähentää summan saldosta</strong> vai pitää saldon ennallaan, koska <strong>Saldo sisältää tämän jo</strong>. Jos päivität saldosi ensin käsin, voit kuitata menot pikavalinnoilla muuttamatta saldoa uudelleen, ja <strong>Kumoa</strong>-painikkeella perut valinnan heti."
                ),
                (
                    "Varmuuskopiointi ja siirtäminen toiselle laitteelle:",
                    "PlusMinus tallentaa budjettitiedot paikallisesti laitteellesi. Voit tallentaa kopion tai siirtää tiedot avaamalla <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Varmuuskopiointi ja palautus</strong> ja valitsemalla <strong>Luo varmuuskopio</strong> (<code>.plusminusbackup</code>-tiedosto Tiedostot-apin kautta). Palauttaminen korvaa nykyiset budjettitiedot ja palauttaa saldon varmuuskopion luontihetken tilaan muuttamatta sovelluksen kieltä tai ulkoasua."
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
            "desc": "Usein kysyttyjä kysymyksiä ja ohjeita PlusMinus-sovellukseen iPhonella ja iPadilla: Käytettävissä nyt -laskenta, Tilanne ja Kuukausi, suunnitelman analyysi, ruokabudjetin suhteutus, kaksoisvähennysten esto, pyöristykset, varmuuskopiot, tietosuoja ja tuetut kielet.",
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
                    "intro": "<strong>Tilanne</strong>-näkymä vastaa yhteen arjen tärkeimpään kysymykseen: <em>Paljonko voin turvallisesti käyttää juuri nyt ennen seuraavaa ensisijaista palkkapäivää?</em> Laskelma lähtee selkeästä kaavasta ja mukautuu automaattisesti myös tuleviin tuloihin:",
                    "bullets": [
                        "<strong>Raha nyt:</strong> Käsin päivittämäsi tilin tai käteisen saldo tällä hetkellä, näkyvissä olevan päivitysajankohdan kanssa.",
                        "<strong>Miinus maksamattomat menot:</strong> Kaikki ennen seuraavaa ensisijaista palkkapäivää erääntyvät maksamattomat toistuvat menot ja kertaluontoiset menot sekä edelliseltä jaksolta maksamatta jääneet menot.",
                        "<strong>Miinus arvioitu jäljellä oleva ruoka-arvio:</strong> Aktiivisen tarkastelujakson jäljellä oleville päiville suhteutettu ruokabudjetti.",
                        "<strong>Tiukin kassavirtakohta tulevilla tuloilla:</strong> Jos ennen seuraavaa ensisijaista palkkapäivää saapuu ajastettuja tulevia tuloja (säännöllisiä tai kertaluontoisia), PlusMinus tarkistaa tilanteen ennen kutakin tulopäivää ja jakson lopussa ja valitsee tiukimman kohdan. Näin myöhemmät menot eivät aiheuta turhaa vajetta, mutta rahaa ei koskaan pääse kuluttamaan etukäteen. Infopainikkeesta avautuva <strong>Käyttövaran laskelma</strong> täsmää aina valitun tarkastelukohdan riveihin (<strong>Laskelmaan lisättävät tulot</strong>, <strong>Menoihin varattu ennen [päivämäärää]</strong>, <strong>Ruoka-arvio</strong> ja mahdolliset <strong>Myöhemmät maksamattomat menot</strong>), ja otsake kertoo selvästi <code>KÄYTETTÄVISSÄ &middot; TULEVAT TULOT HUOMIOITU</code> aina, kun tulevat tulot vaikuttavat laskelmaan."
                    ],
                    "note": "<strong>Vinkki:</strong> Voit tarkistaa laskentasäännöt milloin tahansa sovelluksesta kohdasta <strong>Asetukset &rarr; Tietoa laskennasta &rarr; Miten laskenta toimii</strong>."
                },
                {
                    "question": "Mitä eroa on Tilanne- ja Kuukausi-näkymillä?",
                    "intro": "PlusMinus erottaa arjen käyttövaran ja pitkän aikavälin kuukausitasapainon kahdeksi selkeäksi välilehdeksi:",
                    "bullets": [
                        "<strong>Tilanne:</strong> Näyttää tilanteen juuri nyt seuraavaan ensisijaiseen palkkapäivään saakka. Se lähtee todellisesta <strong>Raha nyt</strong> -saldosta, tarkastelee tällä jaksolla erääntyvät maksamattomat menot, jäljellä olevan ruoka-arvion ja tulevat ajastetut tulot tiukimman kassavirtakohdan mukaan ja kertoo paljonko on <strong>Käytettävissä nyt</strong> laajennettavien <strong>Tulevat tulot</strong>- ja <strong>Maksamattomat menot</strong> -osioiden rinnalla.",
                        "<strong>Kuukausi:</strong> Näyttää tasatun <strong>Kuukausibudjetin ylijäämän</strong> (tasatut kuukausitulot miinus tasatut kuukausimenot miinus kuukauden ruokabudjetti) täysin riippumattomana tämän päivän pankkisaldosta. Lisäksi näet kohdasta <strong>Mihin tulosi menevät</strong> ja <strong>Suunnitelman analyysi</strong>, miten kuukausitulosi jakautuvat eri menokategorioihin ja ruokabudjettiin."
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
                    "question": "Miten PlusMinus estää saman menon vähentämisen kahteen kertaan?",
                    "intro": "Koska päivität saldosi itse ilman pankkiyhteyttä, PlusMinusissa on sisäänrakennettu suojaus kaksoisvähennyksiä vastaan:",
                    "bullets": [
                        "<strong>Kahden vaihtoehdon vahvistus:</strong> Kun merkitset menon maksetuksi (<strong>Maksettu</strong>), sovellus kysyy, vähennetäänkö summa saldosta (<strong>Vähennä saldosta</strong>) vai näkyykö se jo saldossa (<strong>Saldo sisältää tämän jo</strong>). Jos olet päivittänyt saldosi viimeisen 5 minuutin aikana, sovellus korostaa valmiiksi jälkimmäistä vaihtoehtoa.",
                        "<strong>Pikakuittaus saldopäivityksen jälkeen:</strong> Kun päivität saldosi käsin, näkyviin tulevilla pikavalinnoilla voit kuitata erääntyneitä menoja maksetuiksi muuttamatta saldoa uudelleen.",
                        "<strong>Helppo peruminen:</strong> Jos valitset vahingossa väärän vaihtoehdon, napauta heti <strong>Kumoa</strong> palauttaaksesi menon ja saldomuutoksen."
                    ]
                },
                {
                    "question": "Miten tulevat tulot vaikuttavat Käytettävissä nyt -summaan?",
                    "intro": "PlusMinus toimii luotettavasti riippumatta siitä, saatko yhden pääpalkan, 2&ndash;3 eri päivinä saapuvaa säännöllistä tuloa tai myöhemmin tällä jaksolla tulevan kertaluontoisen tulon:",
                    "bullets": [
                        "<strong>Tulevat ajastetut tulot (automaattinen kassavirtapullonkaula):</strong> Aktiiviset säännölliset ja kertaluontoiset tulot, joiden maksupäivä on aidosti tulevaisuudessa (tämän päivän sekä viikonloppusiirron mahdollisen nimellisen palkkapäivän jälkeen) ennen seuraavaa ensisijaista palkkapäivää, huomioidaan automaattisesti tiukimman kassavirtakohdan kautta. Näin jakson loppupuolen menot eivät aiheuta turhaa miinusta, mutta tulevaa tuloa ei voi koskaan kuluttaa etukäteen.",
                        "<strong>Selkeä otsake ja täsmäävä erittely:</strong> Kun tulevat tulot nostavat summaa pelkkään käteispohjaan verrattuna, päänäytön otsake tarkentuu muotoon <code>KÄYTETTÄVISSÄ &middot; TULEVAT TULOT HUOMIOITU</code> (ja alla näkyy tarvittaessa <code>Koko jakso [päivämäärä] asti</code>). Infopainikkeesta avautuva <strong>Käyttövaran laskelma</strong> erottelee kohdan <strong>Laskelmaan lisättävät tulot</strong> päänäkymän <strong>Tulevat tulot</strong> -yhteenvedosta ja näyttää tarvittaessa kohdan <strong>Myöhemmät maksamattomat menot</strong>.",
                        "<strong>Myöhässä olevat ja tänään erääntyvät tulot:</strong> Myöhässä olevia tai tänään odotettuja tuloja (sekä säännöllisiä että kertaluontoisia) ei koskaan lasketa ennakkoon — ne näkyvät muistutuslistalla ja vaikuttavat vasta, kun kuittaat ne <strong>Saatu</strong>-napilla (tai päivität saldon). Saamatta jääneen tulon voi myös merkitä <strong>Tulo peruuntui</strong> -valinnalla ilman saldomuutosta.",
                        "<strong>Ei tuplalaskentaa kuittaamisen yhteydessä:</strong> Kun kuittaat mukana olleen tulevan tulon saaduksi ja lisäät sen saldoon, summa siirtyy siististi <strong>Raha nyt</strong> -saldoon ilman kaksinkertaista laskentaa."
                    ]
                },
                {
                    "question": "Miten valitut kuukaudet, vuosittaiset, viikoittaiset, kertaluontoiset erät ja suunnitelman analyysi toimivat?",
                    "intro": "PlusMinus käsittelee säännölliset, harvemmin toistuvat ja kertaluontoiset erät sekä kategoriajakauman tarkasti:",
                    "bullets": [
                        "<strong>Kuukausitasaus (Kuukausi-välilehti):</strong> Viikoittaiset erät tasataan kertoimella <code>&times; 52 &divide; 12</code>, joka 2. viikko toistuvat <code>&times; 26 &divide; 12</code>, <strong>Valitut kuukaudet</strong> (esim. tammi- ja lokakuu tai neljännesvuosi) kertoimella <code>&times; valitut kuukaudet &divide; 12</code> ja vuosittaiset <code>&divide; 12</code>.",
                        "<strong>Täysi vähennys Tilanne-näkymässä:</strong> Vuosittaiset ja valittujen kuukausien menot vähennetään täysimääräisinä juuri sen palkkajakson käyttövarasta, jonka aikana ne erääntyvät.",
                        "<strong>Kertaluontoiset tulot ja menot:</strong> Kertaluontoiset erät (esim. veronpalautus tai yksittäinen isompi hankinta) merkitään tarkalla päivämäärällä joko <strong>Kuukausi</strong>-näkymässä tai <strong>Tilanne</strong>-näkymän <code>+</code>-valikosta. Ne eivät kuulu tasattuun kuukausisuunnitelmaan: kertaluontoiset menot vähennetään täysimääräisinä <strong>Tilanne</strong>-näkymässä erääntyessään, ja tulevat kertaluontoiset tulot ennen seuraavaa palkkapäivää huomioidaan <strong>Käytettävissä nyt</strong> -kassavirtatarkistuksessa ilman etukäteiskulutusta.",
                        "<strong>17 kategoriaa, Suunnitelman analyysi ja valinnainen eräpäivä:</strong> Menoille voi valita kategorian 17 vaihtoehdosta (Asuminen, Sähkö &amp; vesi, Tilaukset, Vakuutukset, Lainat, Luottokortit ja kulutusluotot, Liikenne, Harrastukset, Urheilu ja kuntoilu, Sijoittaminen, Terveys ja hyvinvointi, Lapset ja perhe, Lemmikit, Koulutus, Säästäminen, Antaminen, Muu). <strong>Kuukausi</strong>-välilehden <strong>Mihin tulosi menevät</strong> ja <strong>Suunnitelman analyysi</strong> vertailevat aktiivisten toistuvien menojen kategorioita (sekä luokittelemattomia menoja ja ruokabudjettia) kuukausisummien ja tulo-osuuksien mukaan. Toistuville menoille voi myös jättää tarkan eräpäivän asettamatta (<strong>Ei tarkkaa päivää</strong>)."
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
                    "intro": "PlusMinus auttaa hallitsemaan myös tulevia ja vanhempia kuitattuja menoja selkeästi:",
                    "bullets": [
                        "<strong>Seuraavalla jaksolla ja etukäteismaksu:</strong> Avaamalla <strong>Seuraavalla jaksolla</strong> -osion <strong>Tilanne</strong>-näkymässä näet seuraavan palkkapäivän jälkeen erääntyvät menot ja voit kuitata ne maksetuksi etukäteen samalla saldotarkistuksella.",
                        "<strong>Vanhemmat kuittaamattomat menot:</strong> Edellistä jaksoa vanhemmat maksamattomat menot (enintään 24 kk taaksepäin) jätetään pois nykyisestä Käytettävissä nyt -laskelmasta, ja voit merkitä ne kuitatuiksi erillisestä <strong>Kuittaa vanhemmat</strong> -huomautuksesta."
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
                        "<strong>Tallennetaan laitteellesi:</strong> Saldot, tulot, menot, maksuhistoria ja asetukset pysyvät paikallisesti iPhonellasi tai iPadillasi.",
                        "<strong>Ei tilejä eikä pankkitunnuksia:</strong> Sovellus ei vaadi käyttäjätiliä eikä kysy pankkitunnuksia tai pankkiyhteyksiä.",
                        "<strong>Ei seurantaa tai mainoksia:</strong> Sovelluksessa ei ole mainoksia, analytiikka-SDK:ita eikä automaattista pilvisynkronointia taustalla."
                    ]
                },
                {
                    "question": "Miten Varmuuskopiointi ja palautus sekä Nollaa kaikki tiedot toimivat?",
                    "intro": "Hallitset kaikkia omia budjettitietojasi täysin itse:",
                    "bullets": [
                        "<strong>Luo varmuuskopio:</strong> Avaa <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Varmuuskopiointi ja palautus</strong> ja napauta <strong>Luo varmuuskopio</strong> tallentaaksesi luettavissa olevan JSON-tiedoston (<code>.plusminusbackup</code>, ei salasanasuojattu) iCloud Driveen, laitteelle tai muuhun Tiedostot-apin sijaintiin.",
                        "<strong>Palauta varmuuskopiosta:</strong> Valitse <strong>Palauta varmuuskopiosta</strong> ja avaa kelvollinen <code>.plusminusbackup</code>-tiedosto (enintään 50 Mt). Palautus korvaa kaikki nykyiset budjettitiedot ja palauttaa saldon varmuuskopion luontihetken tilaan. Sovelluksen kieli ja ulkoasu pysyvät ennallaan.",
                        "<strong>Nollaa kaikki tiedot:</strong> Kohdassa <strong>Asetukset &rarr; Tiedot ja yksityisyys &rarr; Nollaa kaikki tiedot</strong> voit poistaa kaikki laitteelle tallennetut tiedot ja asetukset kaksivaiheisen vahvistuksen jälkeen. Vietyjä varmuuskopioita tai laitteen järjestelmävarmuuskopioita ei poisteta."
                    ]
                },
                {
                    "question": "Mitä kieliä, valuuttoja, teemoja ja laitteita tuetaan?",
                    "intro": "PlusMinus mukautuu kieleesi, valuuttaasi ja laitteesi ulkoasuun:",
                    "bullets": [
                        "<strong>Kielet:</strong> Voit vaihtaa kielen suoraan kohdasta <strong>Asetukset &rarr; Kieli</strong> (<strong>Järjestelmän oletus</strong>, <strong>English</strong>, <strong>Suomi</strong>, <strong>Svenska</strong>, <strong>Deutsch</strong>, <strong>Espa&ntilde;ol</strong> tai <strong>Fran&ccedil;ais</strong>) ilman sovelluksen uudelleenkäynnistystä.",
                        "<strong>Valuutat:</strong> Tuettuina ovat <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> ja <strong>JPY</strong> kohdassa <strong>Asetukset &rarr; Valuutta</strong>.",
                        "<strong>Ulkoasu:</strong> Valitse <strong>Järjestelmän oletus</strong>, <strong>Tumma</strong> tai <strong>Vaalea</strong> kohdasta <strong>Asetukset &rarr; Ulkoasu</strong>.",
                        "<strong>Tuetut laitteet:</strong> Suunniteltu iPhonelle ja iPadille, joissa on <strong>iOS 26 tai uudempi</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Rauhallinen kuukausibudjetti ja käyttövara iPhonelle ja iPadille",
            "desc": "Näe yhdellä silmäyksellä, paljonko voit turvallisesti käyttää juuri nyt — ilman jokaisen ostoksen kirjaamista. Paikallinen budjettisovellus, jossa on suunnitelman analyysi ja ei pankkiyhteyksiä.",
            "canonical": f"{BASE_URL}/plusminus/fi/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Tiedä heti, paljonko voit turvallisesti käyttää.",
            "subtitle": "Määritä toistuvat tulot, menot, palkkapäivä ja kuukauden ruokabudjetti kerran. Kurkkaa saldosi ja näe heti todellinen käyttövarasi — ilman jokaisen kahvin kirjaamista.",
            "section1_title": "Selkeyttä alle viidessä sekunnissa",
            "features": [
                ("Käytettävissä juuri nyt", "Raha nyt, maksamattomat menot, ruoka-arvio ja tulevat ajastetut tulot tiukimman kassavirtakohdan mukaan &mdash; aina askel askeleelta eriteltynä."),
                ("Tasainen kuukausisuunnitelma", "Erillinen kuukausinäkymä, joka tasaa viikoittaiset, valittujen kuukausien ja vuosittaiset menot sekä näyttää kategoria-analyysin ilman että päivän saldo sotkee kokonaiskuvaa."),
                ("Yksityinen ja paikallinen", "Kaikki tiedot pysyvät laitteellasi. Ei käyttäjätilejä, ei pankkiyhteyksiä, ei analytiikkaa eikä seurantaa."),
            ],
            "section2_title": "Kaikki oleellinen, ei mitään ylimääräistä",
            "list_items": [
                "Käytettävissä nyt -laskenta seuraavaan ensisijaiseen palkkapäivään &mdash; myös useammalla tulolla ja tulevilla kertaluontoisilla tuloilla",
                "Selkeä Käyttövaran laskelma -erittely tarkkoine päivämäärineen, varauksineen ja myöhempine menoineen",
                "Automaattinen päiväkohtainen ruoka-arvio sekä oma kiinteä arvio tarvittaessa",
                "Kaksoisvähennysten esto menoja maksetuksi kuitatessa ja saldoa päivittäessä",
                "Viikoittaiset, joka 2. viikko, kuukausittaiset, valittujen kuukausien, vuosittaiset ja kertaluontoiset erät",
                "Suunnitelman analyysi 17 menokategorian ja ruokabudjetin kuukausijakaumasta",
                "Viikonloppuun osuvan palkkapäivän siirto perjantaille ja lyhyiden kuukausien huomiointi",
                "Seuraavalla jaksolla -ennakko, etukäteismaksu ja vanhempien menojen kuittaus",
                "Manuaalinen varmuuskopiointi ja palautus Tiedostot-apin kautta (.plusminusbackup)",
                "Saatavilla kuudella kielellä (suomi, englanti, ruotsi, saksa, espanja, ranska), 10 valuuttaa sekä tumma ja vaalea tila",
            ],
            "closing_title": "Suunniteltu iPhonelle ja iPadille",
            "closing_body": "PlusMinus toimii iPhonella ja iPadilla, joissa on iOS 26 tai uudempi.",
            "faq_btn": "UKK",
            "privacy_btn": "Tietosuojaseloste",
            "support_btn": "Tuki",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Kielivalinta",
            "featureList": [
                "Käytettävissä nyt -laskenta seuraavaan ensisijaiseen palkkapäivään sekä toistuvien ja kertaluontoisten tulojen kassavirtatuki",
                "Tasattu kuukausibudjetti ja suunnitelman analyysi 17 kategoriassa",
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
            "last_updated": "Viimeksi päivitetty: 25. marraskuuta 2026",
            "sections": [
                (
                    "Tiedot laitteellasi",
                    [
                        "PlusMinus on paikallisesti toimiva budjetointisovellus. Budjettitietojasi ei lähetetä sovelluksen kehittäjälle.",
                        "Saldot, tulot, menot, maksuhistoria ja budjettiasetukset tallennetaan paikallisesti laitteellesi. Kieli, ulkoasu ja tiedot suljetuista muistutuksista tallennetaan paikallisina asetuksina.",
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
    "sv": {
        "home_href": "../../sv/index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "PlusMinus Support",
            "desc": "Få hjälp med PlusMinus, den lugna lokala budgetappen för iPhone och iPad, eller kontakta PlusMinus-supporten.",
            "heading": "PlusMinus Support",
            "thank_you": "Tack för att du använder PlusMinus.",
            "faq_card_title": "Kolla FAQ först för snabba svar",
            "faq_card_body": "Innan du skickar e-post, ta gärna en titt på våra vanliga frågor (FAQ). Där hittar du tydliga svar om Kvar att spendera, skillnaden mellan Läget och Plan, plananalys, proportionering av matbudget, skydd mot dubbelavdrag, säkerhetskopior och integritet.",
            "faq_card_action": "Läs vanliga frågor (FAQ)",
            "card_title": "Felsökning och bra att veta",
            "tips": [
                (
                    "Kvar att spendera ser högre eller lägre ut än väntat:",
                    "Kontrollera att <strong>Pengar nu</strong> stämmer med ditt verkliga saldo just nu, och se över obetalda eller förfallna utgifter i <strong>Läget</strong>. Planerade framtida inkomster (återkommande eller engångs) före din nästa huvudsakliga lönedag räknas automatiskt in i Kvar att spendera utifrån den snävaste kassaflödespunkten (utan att du kan spendera pengar innan de kommer in), medan förfallna och dagens inkomster väntar tills du markerar dem som mottagna. Tryck på infoknappen bredvid Kvar att spendera för exakt <strong>Beräkning</strong>, eller se alla regler under <strong>Inställningar &rarr; Förstå PlusMinus &rarr; Så fungerar beräkningarna</strong>."
                ),
                (
                    "Undvika dubbelavdrag när utgifter markeras som betalda:",
                    "När du markerar en utgift som <strong>Betald</strong> frågar PlusMinus om summan ska dras av (<strong>Dra av från Pengar nu</strong>) eller lämnas oförändrad eftersom <strong>Detta är redan inräknat i Pengar nu</strong>. Om du uppdaterar saldot manuellt först kan du snabbt kvittera förfallna utgifter utan att dra av dem två gånger, och med <strong>Ångra</strong> kan du direkt ta tillbaka ett misstag."
                ),
                (
                    "Säkerhetskopior och byte av enhet:",
                    "PlusMinus lagrar alla budgetdata lokalt på din enhet. För att flytta din budget eller spara en kopia öppnar du <strong>Inställningar &rarr; Data och integritet &rarr; Säkerhetskopiering och återställning</strong> och trycker på <strong>Skapa säkerhetskopia</strong> för att spara en <code>.plusminusbackup</code>-fil via Filer. Återställning ersätter alla nuvarande budgetdata och återställer saldot till hur det såg ut när säkerhetskopian skapades, utan att ändra appens språk eller utseende."
                ),
            ],
            "contact_intro": "Om du inte hittade svaret i FAQ, stöter på ett problem eller vill lämna feedback, kontakta:",
            "email_label": "E-post:",
            "report_tip": "När du rapporterar ett fel hjälper det om du anger enhetsmodell (iPhone eller iPad), iOS-version och en kort beskrivning av problemet.",
            "about_link": "Om PlusMinus",
            "faq_link": "FAQ",
            "privacy_link": "Integritetspolicy",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Språkval",
        },
        "faq": {
            "title": "PlusMinus FAQ – Vanliga frågor",
            "desc": "Vanliga frågor och guider för PlusMinus på iPhone och iPad: Kvar att spendera, Läget och Plan, plananalys, matbudget, skydd mot dubbelavdrag, valda månader, avrundning, säkerhetskopior, integritet och språk.",
            "back_label": "&larr; PlusMinus Support",
            "about_link": "Om PlusMinus",
            "privacy_link": "Integritetspolicy",
            "heading": "Vanliga frågor",
            "subtitle": "Hjälp, beräkningsregler och guider för PlusMinus.",
            "toc_title": "På den här sidan",
            "toc_tip": 'Hittar du inte det du söker? <a href="index.html">Kontakta PlusMinus Support &rarr;</a>',
            "back_to_top": "&uarr; Tillbaka till toppen",
            "nav_aria": "Språkval",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "Hur beräknas Kvar att spendera?",
                    "intro": "<strong>Läget</strong> svarar på en konkret vardagsfråga: <em>Hur mycket pengar kan jag tryggt spendera just nu fram till min nästa huvudsakliga lönedag?</em> Beräkningen utgår från en tydlig formel och hanterar automatiskt planerade kommande inkomster:",
                    "bullets": [
                        "<strong>Pengar nu:</strong> Ditt manuellt uppdaterade konto- eller kontantsaldo just nu, med relativ tidsstämpel för senaste uppdatering.",
                        "<strong>Minus obetalda utgifter:</strong> Obetalda återkommande utgifter och engångsutgifter som förfaller före din nästa huvudsakliga lönedag, samt obetalda förfallna utgifter från närmast föregående löneperiod.",
                        "<strong>Minus uppskattad kvarvarande matbudget:</strong> Din beräknade återstående matbudget för den aktiva kassaflödeshorisonten.",
                        "<strong>Snävaste kassaflödespunkten vid kommande inkomster:</strong> När planerade framtida inkomster (återkommande eller engångs) kommer in före din nästa huvudsakliga lönedag kontrollerar PlusMinus saldot före varje kommande inkomstdatum och vid periodens slut och väljer den snävaste punkten. På så sätt orsakar senare utgifter inga falska underskott, samtidigt som du aldrig kan spendera pengar innan de kommit in. Infoknappen bredvid Kvar att spendera öppnar <strong>Beräkning</strong>, som alltid matchar den begränsande horisonten rad för rad (med <strong>Inkomster som läggs till i beräkningen</strong>, <strong>Reserverat för utgifter före [datum]</strong>, <strong>Matuppskattning</strong> och eventuella <strong>Senare obetalda utgifter</strong>), och rubriken visar tydligt <code>KVAR ATT SPENDERA &middot; MED HÄNSYN TILL KOMMANDE INKOMSTER</code> när kommande inkomster påverkar summan."
                    ],
                    "note": "<strong>Tips:</strong> Du kan när som helst granska beräkningsreglerna i appen under <strong>Inställningar &rarr; Förstå PlusMinus &rarr; Så fungerar beräkningarna</strong>."
                },
                {
                    "question": "Vad är skillnaden mellan Läget och Plan?",
                    "intro": "PlusMinus skiljer vardagens spelrum från din långsiktiga månadsbalans i två tydliga flikar:",
                    "bullets": [
                        "<strong>Läget:</strong> Gäller från just nu fram till din nästa huvudsakliga lönedag. Den utgår från ditt verkliga saldo i <strong>Pengar nu</strong>, tar hänsyn till obetalda utgifter, kvarvarande matbudget och eventuella framtida planerade inkomster utifrån den snävaste kassaflödespunkten, och visar vad som finns <strong>Kvar att spendera</strong> tillsammans med utfällbara listor för <strong>Kommande inkomst</strong> och <strong>Obetalda utgifter</strong>.",
                        "<strong>Plan:</strong> Visar ditt normaliserade <strong>Planerade månadsöverskott</strong> (normaliserad månadsinkomst minus normaliserade månadsutgifter minus månatlig matbudget), helt oberoende av dagens kontosaldo eller löneperiodens längd. Här finns även <strong>Vad din inkomst går till</strong> och <strong>Plananalys</strong>, som visar månadens fördelning per kategori och matbudget i belopp och andel av månadsinkomsten."
                    ],
                    "note": "<strong>Varför två vyer?</strong> En årlig försäkringsutgift eller en kortare löneperiod påverkar hur mycket kontanter du kan använda just nu i <strong>Läget</strong>, medan <strong>Plan</strong> visar om dina normala inkomster täcker dina löpande utgifter över tid."
                },
                {
                    "question": "Hur fungerar matbudgeten och kan jag ändra den för den här perioden?",
                    "intro": "I stället för att registrera varje matkvitto modellerar PlusMinus matkostnader som en enda månadsuppskattning som automatiskt trappas ned fram till lönedagen:",
                    "bullets": [
                        "<strong>Automatisk daglig beräkning:</strong> PlusMinus beräknar <code>Månatlig matbudget &times; (återstående dagar till nästa lönedag &divide; totalt antal dagar i den aktuella löneperioden)</code>, avrundat uppåt till en hel valutaenhet. Idag ingår och lönedagen räknas inte med.",
                        "<strong>Egen uppskattning för den här perioden:</strong> Tryck på <strong>Matuppskattning</strong> i <strong>Läget</strong> för att ange ett fast belopp för innevarande period (inklusive noll) om du till exempel redan handlat mat i förväg eller ska resa bort. Din månatliga matbudget i <strong>Plan</strong> förblir oförändrad.",
                        "<strong>Återställa automatisk beräkning:</strong> Öppna <strong>Matuppskattning</strong> och tryck på <strong>Återställ automatisk beräkning</strong> när som helst, eller låt den återställas automatiskt på nästa huvudsakliga lönedag."
                    ],
                    "note": "<strong>Obs!</strong> Datum för andra inkomster återställer aldrig din matbudget — bara din <strong>Huvudsakliga lönedag</strong> styr löneperioden och återställer matuppskattningen."
                },
                {
                    "question": "Hur förhindrar PlusMinus att samma utgift dras av två gånger?",
                    "intro": "Eftersom du uppdaterar ditt saldo manuellt utan bankkoppling har PlusMinus inbyggda spärrar som hindrar dubbelavdrag:",
                    "bullets": [
                        "<strong>Tvåvalsbekräftelse vid Betald:</strong> När du markerar en utgift som <strong>Betald</strong> frågar PlusMinus om beloppet ska dras av (<strong>Dra av från Pengar nu</strong>) eller om saldot ska lämnas oförändrat eftersom <strong>Detta är redan inräknat i Pengar nu</strong> (med smart rekommendation om du uppdaterade saldot inom de senaste 5 minuterna).",
                        "<strong>Snabbkvittering efter saldouppdatering:</strong> Efter en manuell saldouppdatering låter snabbval dig markera nyligen förfallna utgifter som betalda utan att dra av dem en gång till.",
                        "<strong>Enkel ångrafunktion:</strong> Om du råkar välja fel kan du direkt trycka på <strong>Ångra</strong> för att återställa både utgiften och saldot."
                    ]
                },
                {
                    "question": "Hur påverkar kommande inkomster Kvar att spendera?",
                    "intro": "PlusMinus fungerar lika smidigt vare sig du har en huvudlön, 2&ndash;3 återkommande inkomster på olika dagar eller en planerad framtida engångsinkomst:",
                    "bullets": [
                        "<strong>Framtida planerade inkomster (automatisk kassaflödesflaskhals):</strong> Aktiva återkommande inkomster och engångsinkomster med datum strikt efter idag (och efter periodens nominella lönedag vid helgjustering) och före nästa huvudsakliga lönedag räknas automatiskt in i <strong>Kvar att spendera</strong> via den snävaste kontrollpunkten &mdash; så senare utgifter inte skapar falska underskott samtidigt som du aldrig spenderar pengar i förväg.",
                        "<strong>Tydliga rubriker och exakt uppställning:</strong> När kommande inkomster höjer beloppet jämfört med enbart kontosaldot visas <code>KVAR ATT SPENDERA &middot; MED HÄNSYN TILL KOMMANDE INKOMSTER</code> (med raden <code>Hela perioden till &hellip;</code> under om den begränsande punkten infaller tidigare). Öppna <strong>Beräkning</strong> via infoknappen för att se <strong>Inkomster som läggs till i beräkningen</strong> (skilt från översiktens <strong>Kommande inkomst</strong>) och eventuella <strong>Senare obetalda utgifter</strong>.",
                        "<strong>Förfallna och dagens inkomster:</strong> Förfallna eller dagens inkomster (både återkommande och engångs) räknas aldrig in i förväg &mdash; de visas som påminnelser och räknas först när du markerar dem som <strong>Mottagen</strong> (eller uppdaterar <strong>Pengar nu</strong>). En utebliven inkomst kan markeras som <strong>Inkomst inställd</strong> utan att ändra saldot.",
                        "<strong>Ingen dubbelräkning vid mottagande:</strong> När du markerar en medräknad kommande inkomst som <strong>Mottagen</strong> och lägger till den i <strong>Pengar nu</strong> flyttas den sömlöst in i saldot utan dubbelräkning."
                    ]
                },
                {
                    "question": "Hur fungerar Valda månader, Årligen, Veckovis, Varannan vecka, Engångs och Plananalys?",
                    "intro": "PlusMinus hanterar regelbundna utgifter, oregelbundna intervall och kategorifördelning noggrant i <strong>Plan</strong> och <strong>Läget</strong>:",
                    "bullets": [
                        "<strong>Månadsnormalisering i Plan:</strong> Veckovisa poster normaliseras med <code>&times; 52 &divide; 12</code>, varannan vecka med <code>&times; 26 &divide; 12</code>, <strong>Valda månader</strong> (t.ex. januari &amp; oktober eller kvartalsvis) med <code>&times; valda månader &divide; 12</code>, och årliga med <code>&divide; 12</code>.",
                        "<strong>Fullt avdrag i Läget:</strong> Årliga utgifter och utgifter för valda månader dras av i sin helhet under just den löneperiod då de förfaller.",
                        "<strong>Engångsposter:</strong> Engångsinkomster och engångsutgifter (t.ex. skatteåterbäring eller bilreparation) har ett exakt datum och kan läggas till i <strong>Plan</strong> eller via <code>+</code>-menyn i <strong>Läget</strong>. De ingår inte i den månatliga basen i <strong>Plan</strong>: engångsutgifter dras av i sin helhet i <strong>Läget</strong> när de förfaller, och framtida engångsinkomster före nästa lönedag ingår i kassaflödeskontrollen för <strong>Kvar att spendera</strong> utan att spenderas i förväg.",
                        "<strong>17 kategorier, Plananalys och valfritt förfallodatum:</strong> Utgifter kan ordnas i 17 valfria kategorier (Boende, El och vatten, Prenumerationer, Försäkringar, Lån, Kreditkort och konsumentkrediter, Transport, Hobbyer, Sport och träning, Investering, Hälsa och välbefinnande, Barn och familj, Husdjur, Utbildning, Sparande, Gåvor, Övrigt). I <strong>Plan</strong> visar <strong>Vad din inkomst går till</strong> och <strong>Plananalys</strong> aktiva återkommande utgiftskategorier (samt Okategoriserat och Matbudget) efter månadsbelopp och andel av inkomsten. Regelbundna utgifter kan vid behov sakna ett exakt förfallodatum (<strong>Ingen specifik dag</strong>)."
                    ]
                },
                {
                    "question": "Hur fungerar Huvudsaklig lönedag och helgjustering?",
                    "intro": "Din <strong>Huvudsakliga lönedag</strong> under <strong>Inställningar &rarr; Budgetperiod</strong> styr lönecykler och återställning av matuppskattningen:",
                    "bullets": [
                        "<strong>Dag 1&ndash;31 med anpassning för korta månader:</strong> Välj din huvudsakliga lönedag mellan dag 1 och 31. Under kortare månader (som februari eller 30-dagarsmånader) anpassas datumet automatiskt till månadens sista dag.",
                        "<strong>Helgjustering till fredag:</strong> Aktivera <strong>Lön på fredag om lönedagen infaller på en helg</strong> om din lön betalas ut föregående fredag när lönedagen faller på lördag eller söndag.",
                        "<strong>Förhandsgranskning av perioder:</strong> I väljaren för <strong>Huvudsaklig lönedag</strong> ser du kommande faktiska lönedagar innan du sparar."
                    ]
                },
                {
                    "question": "Vad är Kommer nästa period, tidig betalning och Markera äldre som avklarade?",
                    "intro": "PlusMinus gör det enkelt att ligga steget före kommande perioder och hålla äldre perioder prydliga:",
                    "bullets": [
                        "<strong>Kommer nästa period och tidig betalning:</strong> Expandera <strong>Kommer nästa period</strong> i <strong>Läget</strong> för att se utgifter som förfaller efter din nästa huvudsakliga lönedag. Har du redan betalat en sådan utgift i förväg kan du markera den som betald där med samma saldokontroll.",
                        "<strong>Äldre obetalda utgifter (Markera äldre som avklarade):</strong> Obetalda utgifter från tidigare än föregående period (upp till 24 månader tillbaka) dras inte av från ditt nuvarande <strong>Kvar att spendera</strong> utan samlas i en tydlig banner med knappen <strong>Markera äldre som avklarade</strong>."
                    ]
                },
                {
                    "question": "Hur avrundas beloppen?",
                    "intro": "Alla synliga siffror är utformade så att uträkningen stämmer exakt:",
                    "bullets": [
                        "<strong>Öre-/centprecision och exakta summor:</strong> Varje delpost avrundas till närmaste öre/cent (halva ören/cent avrundas bort från noll) före summering eller subtraktion, så varje synlig rad summerar exakt till totalsumman.",
                        "<strong>Avrundning av matuppskattningen:</strong> Den automatiska dagliga matuppskattningen i <strong>Läget</strong> avrundas uppåt till en hel valutaenhet, medan egna fasta belopp behåller decimaler.",
                        "<strong>Ren decimalvisning:</strong> Belopp med decimaler visar två decimaler, medan hela belopp döljer avslutande nollor."
                    ]
                },
                {
                    "question": "Ansluter PlusMinus till min bank, samlar det in analysdata eller synkar det till molnet?",
                    "intro": "Nej. PlusMinus är byggt helt och hållet för lokal lagring utan spårning:",
                    "bullets": [
                        "<strong>Lagras på din enhet:</strong> Saldon, inkomster, utgifter, betalningshistorik och inställningar stannar lokalt på din iPhone eller iPad.",
                        "<strong>Inga konton eller bankkopplingar:</strong> PlusMinus kräver inget konto och ber aldrig om bankinloggningar eller Open Banking-åtkomst.",
                        "<strong>Ingen spårning eller reklam:</strong> Appen innehåller inga analys-SDK:er, inga reklamidentifierare och ingen automatisk molnsynkronisering i bakgrunden."
                    ]
                },
                {
                    "question": "Hur fungerar Säkerhetskopiering och återställning samt Nollställ alla data?",
                    "intro": "Du har alltid full kontroll över dina lokala budgetdata:",
                    "bullets": [
                        "<strong>Skapa säkerhetskopia:</strong> Öppna <strong>Inställningar &rarr; Data och integritet &rarr; Säkerhetskopiering och återställning</strong> och tryck på <strong>Skapa säkerhetskopia</strong> för att exportera en läsbar JSON-fil (<code>.plusminusbackup</code>, inte lösenordsskyddad) till iCloud Drive, lokal lagring eller valfri plats i Filer.",
                        "<strong>Återställ från säkerhetskopia:</strong> Tryck på <strong>Återställ från säkerhetskopia</strong> och välj en giltig <code>.plusminusbackup</code>-fil (upp till 50 MB). Återställning ersätter alla nuvarande budgetdata och återställer saldot från när säkerhetskopian skapades, utan att ändra appens språk eller utseende.",
                        "<strong>Nollställ alla data:</strong> Under <strong>Inställningar &rarr; Data och integritet</strong> raderar <strong>Nollställ alla data</strong> med tvåstegsbekräftelse alla lokala budgetdata och inställningar på den här enheten och återgår till startläget. Exporterade säkerhetskopior och enhetens systemsäkerhetskopior raderas inte."
                    ]
                },
                {
                    "question": "Vilka språk, valutor, teman och enheter stöds?",
                    "intro": "PlusMinus anpassar sig efter ditt önskade språk, din valuta och ditt utseende:",
                    "bullets": [
                        "<strong>Språk:</strong> Kan bytas direkt under <strong>Inställningar &rarr; Preferenser &rarr; Språk</strong> mellan <strong>Systemstandard</strong>, <strong>English</strong>, <strong>Suomi</strong>, <strong>Svenska</strong>, <strong>Deutsch</strong>, <strong>Espa&ntilde;ol</strong> och <strong>Fran&ccedil;ais</strong> utan att starta om appen.",
                        "<strong>Valutor:</strong> Stöder <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> och <strong>JPY</strong> under <strong>Inställningar &rarr; Preferenser &rarr; Valuta</strong>.",
                        "<strong>Utseende:</strong> Välj <strong>Systemstandard</strong>, <strong>Mörkt</strong> eller <strong>Ljust</strong> under <strong>Inställningar &rarr; Preferenser &rarr; Utseende</strong>.",
                        "<strong>Enheter som stöds:</strong> Utvecklad för iPhone och iPad med <strong>iOS 26 eller senare</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Lugn månadsbudget och Kvar att spendera för iPhone och iPad",
            "desc": "Se vad du tryggt kan spendera just nu utan att logga varje köp. Lokal budgetapp med plananalys, automatisk matbudget och utan bankkoppling.",
            "canonical": f"{BASE_URL}/plusminus/sv/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Vet alltid vad du tryggt kan spendera just nu.",
            "subtitle": "Ställ in återkommande inkomster, utgifter, lönedag och månatlig matbudget en gång. Släng ett öga på saldot och se vad som faktiskt är fritt att spendera — utan att logga varje kaffe.",
            "section1_title": "Klarhet på under fem sekunder",
            "features": [
                ("Kvar att spendera i realtid", "Pengar nu, obetalda utgifter, kvarvarande matuppskattning och kommande planerade inkomster utvärderade vid den snävaste kassaflödespunkten &mdash; alltid steg för steg."),
                ("Stabil månadsplan", "Separat månadsöversikt som normaliserar utgifter för varje vecka, varannan vecka, valda månader och årligen &mdash; med plananalys per kategori &mdash; utan att dagens saldo stör bilden."),
                ("Privat och lokal först", "Allt stannar på din enhet. Inga konton, inga bankinloggningar, ingen analys och ingen spårning — någonsin."),
            ],
            "section2_title": "Allt du behöver, inget onödigt",
            "list_items": [
                "Kvar att spendera beräknat fram till nästa huvudsakliga lönedag &mdash; med automatiskt stöd för återkommande och engångsinkomster",
                "Tydlig Beräkning-vy med exakta datum, reserveringar och senare utgifter",
                "Automatisk daglig matuppskattning med egen anpassad perioduppskattning vid behov",
                "Skydd mot dubbelavdrag när utgifter markeras som betalda eller saldot uppdateras",
                "Posttyper för varje vecka, varannan vecka, månadsvis, valda månader, årligen och engångsposter",
                "Plananalys över hur din månadsinkomst fördelas på 17 kategorier och matbudget",
                "Helgjustering av lönedag till fredag och anpassning för korta månader",
                "Förhandsvisning för Kommer nästa period med tidig betalning och hantering av äldre utgifter",
                "Manuell export och återställning via Filer (.plusminusbackup)",
                "Tillgänglig på 6 språk (svenska, engelska, finska, tyska, spanska, franska) med 10 valutor samt mörkt och ljust läge",
            ],
            "closing_title": "Byggd för iPhone och iPad",
            "closing_body": "PlusMinus är designad för iPhone och iPad med iOS 26 eller senare.",
            "faq_btn": "FAQ",
            "privacy_btn": "Integritetspolicy",
            "support_btn": "Support",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Språkval",
            "featureList": [
                "Beräkning av Kvar att spendera till nästa huvudsakliga lönedag med stöd för flera och engångsinkomster",
                "Normaliserad månadsbudget och plananalys i 17 utgiftskategorier",
                "Automatisk daglig matuppskattning med egen periodöverskrivning",
                "Tvåvalsbekräftelse mot dubbelavdrag när utgifter betalas",
                "Stöd för valda månader, årligen, veckovis, varannan vecka och engångsposter",
                "100 % lokal lagring med manuell säkerhetskopiering och återställning via Filer",
            ],
        },
        "privacy": {
            "title": "Integritetspolicy för PlusMinus",
            "desc": "Läs PlusMinus integritetspolicy: lokal budgetering på din enhet utan konton, analys, bankkopplingar eller spårning.",
            "heading": "Integritetspolicy för PlusMinus",
            "last_updated": "Senast uppdaterad: 25 november 2026",
            "sections": [
                (
                    "Data på din enhet",
                    [
                        "PlusMinus är en budgetapp som lagrar allt lokalt i första hand. Din budget skickas inte till utvecklaren.",
                        "Saldon, inkomster, utgifter, betalningshistorik och budgetinställningar lagras på din enhet. Språk, utseende och avfärdade påminnelser sparas som lokala inställningar.",
                    ],
                ),
                (
                    "Spårning och datainsamling",
                    [
                        "PlusMinus har inga konton, ingen reklam, ingen analys, inga bankkopplingar eller någon automatisk molnsynkronisering. Appen samlar inte in personuppgifter och spårar dig inte mellan appar eller webbplatser.",
                    ],
                ),
                (
                    "Säkerhetskopior och filer",
                    [
                        "När du skapar en säkerhetskopia exporteras din budget och betalningshistorik till den plats du väljer i Filer. Säkerhetskopiefiler är läsbara och inte lösenordsskyddade. Om du väljer iCloud Drive eller en annan leverantör lagrar den leverantören filen enligt sina egna villkor och sin integritetspolicy.",
                        "Enhetens systemsäkerhetskopior kan även innehålla appdata beroende på dina inställningar för säkerhetskopiering hos Apple. PlusMinus styr inte över dessa säkerhetskopior.",
                    ],
                ),
                (
                    "Radera dina data",
                    [
                        "Använd <strong>Nollställ alla data</strong> i <strong>Inställningar &rarr; Data och integritet</strong> för att radera den budget och de inställningar som PlusMinus lagrar på den här enheten. Exporterade filer och systemsäkerhetskopior raderas inte; hantera dem separat i Filer eller i enhetens säkerhetskopieringsinställningar.",
                    ],
                ),
                (
                    "Barns integritet",
                    [
                        "PlusMinus samlar inte in personlig information från barn eller andra användare.",
                    ],
                ),
                (
                    "Ändringar i denna integritetspolicy",
                    [
                        "Denna integritetspolicy kan uppdateras om PlusMinus funktionalitet eller datahantering ändras. Eventuella uppdateringar publiceras på denna sida.",
                    ],
                ),
            ],
            "contact_heading": "Kontakt",
            "contact_intro": "Om du har frågor om denna integritetspolicy, vänligen kontakta:",
            "about_link": "Om PlusMinus",
            "faq_link": "FAQ",
            "support_link": "PlusMinus Support",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Språkval",
        },
    },
    "de": {
        "home_href": "../../de/index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "PlusMinus Support",
            "desc": "Erhalte Hilfe zu PlusMinus, der ruhigen lokalen Budget-App für iPhone und iPad, oder kontaktiere den PlusMinus Support.",
            "heading": "PlusMinus Support",
            "thank_you": "Vielen Dank, dass du PlusMinus nutzt.",
            "faq_card_title": "Schau zuerst in die FAQ für schnelle Antworten",
            "faq_card_body": "Bevor du eine E-Mail schreibst, wirf bitte einen Blick in unsere häufig gestellten Fragen (FAQ). Dort findest du klare Antworten zu Frei verfügbar, dem Unterschied zwischen Aktuell und Plan, der Plananalyse, der Essensbudget-Berechnung, dem Schutz vor doppeltem Abzug, Backups und Datenschutz.",
            "faq_card_action": "Häufig gestellte Fragen (FAQ) ansehen",
            "card_title": "Fehlerbehebung &amp; Gut zu wissen",
            "tips": [
                (
                    "„Frei verfügbar“ wirkt höher oder niedriger als erwartet:",
                    "Stelle sicher, dass <strong>Aktuelles Geld</strong> deinem echten Kontostand entspricht, und prüfe offene oder überfällige Ausgaben unter <strong>Aktuell</strong>. Geplante zukünftige Einnahmen (wiederkehrend oder einmalig) vor deinem nächsten Hauptzahltag werden automatisch anhand des engsten Cashflow-Punkts in „Frei verfügbar“ einbezogen (ohne dass du Geld vor Eingang ausgeben kannst), während fällige und überfällige Einnahmen warten, bis du sie als erhalten markierst. Tippe auf die Info-Taste neben „Frei verfügbar“ für die genaue <strong>Berechnung</strong> oder lies alle Regeln unter <strong>Einstellungen &rarr; PlusMinus verstehen &rarr; So funktionieren die Berechnungen</strong>."
                ),
                (
                    "Doppelten Abzug beim Bezahlen von Ausgaben vermeiden:",
                    "Wenn du eine Ausgabe als <strong>Bezahlt</strong> markierst, fragt PlusMinus, ob der Betrag vom <strong>aktuellen Geld abgezogen</strong> werden soll oder dein Kontostand unverändert bleibt, weil er <strong>bereits im aktuellen Geld berücksichtigt</strong> ist. Wenn du zuerst deinen Kontostand manuell aktualisierst, helfen dir Schnell-Chips dabei, fällige Ausgaben ohne doppelten Abzug abzuhaken, und mit <strong>Widerrufen</strong> machst du ein Versehen sofort rückgängig."
                ),
                (
                    "Backups und Umzug auf ein anderes Gerät:",
                    "PlusMinus speichert alle Budgetdaten lokal auf deinem Gerät. Um dein Budget zu sichern oder umzuziehen, öffne <strong>Einstellungen &rarr; Daten &amp; Datenschutz &rarr; Backup &amp; Wiederherstellung</strong> und tippe auf <strong>Backup erstellen</strong>, um eine <code>.plusminusbackup</code>-Datei über „Dateien“ zu speichern. Beim Wiederherstellen werden alle aktuellen Budgetdaten ersetzt und der Kontostand auf den Stand bei Backup-Erstellung zurückgesetzt, während App-Sprache und Erscheinungsbild unverändert bleiben."
                ),
            ],
            "contact_intro": "Wenn du in den FAQ keine Antwort gefunden hast, auf ein Problem stößt oder Feedback teilen möchtest, kontaktiere bitte:",
            "email_label": "E-Mail:",
            "report_tip": "Wenn du ein Problem meldest, ist es hilfreich, dein Gerätemodell (iPhone oder iPad), die iOS-Version und eine kurze Beschreibung anzugeben.",
            "about_link": "Über PlusMinus",
            "faq_link": "FAQ",
            "privacy_link": "Datenschutzerklärung",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Sprachauswahl",
        },
        "faq": {
            "title": "PlusMinus FAQ – Häufig gestellte Fragen",
            "desc": "Häufig gestellte Fragen und Anleitungen für PlusMinus auf iPhone und iPad: Frei verfügbar, Aktuell vs. Plan, Plananalyse, Essensbudget, doppelter Abzug, bestimmte Monate, Rundung, Backups, Datenschutz und Sprachen.",
            "back_label": "&larr; PlusMinus Support",
            "about_link": "Über PlusMinus",
            "privacy_link": "Datenschutzerklärung",
            "heading": "Häufig gestellte Fragen",
            "subtitle": "Hilfe, Berechnungsregeln und Anleitungen für PlusMinus.",
            "toc_title": "Auf dieser Seite",
            "toc_tip": 'Nicht gefunden, wonach du suchst? <a href="index.html">PlusMinus Support kontaktieren &rarr;</a>',
            "back_to_top": "&uarr; Zurück nach oben",
            "nav_aria": "Sprachauswahl",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "Wie wird „Frei verfügbar“ berechnet?",
                    "intro": "<strong>Aktuell</strong> beantwortet eine praktische Frage: <em>Wie viel Geld kann ich bis zu meinem nächsten Hauptzahltag bedenkenlos ausgeben?</em> Die Berechnung folgt einer klaren Formel und berücksichtigt automatisch geplante kommende Einnahmen:",
                    "bullets": [
                        "<strong>Aktuelles Geld:</strong> Dein manuell gepflegter Giro- oder Bargeldbestand im Moment, inklusive relativer Aktualisierungszeit.",
                        "<strong>Minus offene Ausgaben:</strong> Offene wiederkehrende und einmalige Ausgaben, die vor deinem nächsten Hauptzahltag fällig sind, sowie unbezahlte überfällige Ausgaben aus dem unmittelbar vorherigen Zeitraum.",
                        "<strong>Minus geschätztes verbleibendes Essensbudget:</strong> Dein geschätztes Restbudget für Essen im aktiven Cashflow-Horizont.",
                        "<strong>Engster Cashflow-Punkt bei kommenden Einnahmen:</strong> Wenn geplante zukünftige Einnahmen (wiederkehrend oder einmalig) vor deinem nächsten Hauptzahltag eingehen, prüft PlusMinus deinen Kontostand vor jedem kommenden Einnahmetermin sowie am Ende des Zeitraums und wählt den engsten Punkt. So lösen spätere Ausgaben keinen falschen Fehlbetrag aus, und du gibst nie Geld vor Eingang aus. Über die Info-Taste neben „Frei verfügbar“ öffnest du die <strong>Berechnung</strong> (mit <strong>Hier addierte Einnahmen</strong>, <strong>Für Ausgaben vor dem [Datum] zurückgelegt</strong>, <strong>Essensschätzung</strong> und ggf. <strong>Spätere offene Ausgaben</strong>), und die Überschrift zeigt deutlich <code>FREI VERFÜGBAR &middot; KOMMENDES EINKOMMEN BERÜCKSICHTIGT</code>."
                    ],
                    "note": "<strong>Tipp:</strong> Du kannst die Berechnungsregeln jederzeit in der App unter <strong>Einstellungen &rarr; PlusMinus verstehen &rarr; So funktionieren die Berechnungen</strong> nachlesen."
                },
                {
                    "question": "Was ist der Unterschied zwischen Aktuell und Plan?",
                    "intro": "PlusMinus trennt deinen alltäglichen Spielraum sauber von deiner langfristigen Monatsbasis in zwei Tabs:",
                    "bullets": [
                        "<strong>Aktuell:</strong> Deckt den Zeitraum von jetzt bis zu deinem nächsten Hauptzahltag ab. Es startet bei deinem echten <strong>aktuellen Geld</strong>, prüft offene Ausgaben, das verbleibende Essensbudget sowie zukünftige geplante Einnahmen am engsten Cashflow-Punkt und nennt dir deinen Betrag <strong>Frei verfügbar</strong> samt ausklappbaren Listen für <strong>Kommendes Einkommen</strong> und <strong>Offene Ausgaben</strong>.",
                        "<strong>Plan:</strong> Zeigt deinen normalisierten <strong>Geplanten Monatsrest</strong> (normalisiertes Monatseinkommen minus normalisierte Monatsausgaben minus monatliches Essensbudget), völlig unabhängig vom heutigen Kontostand oder der Länge des aktuellen Zahlungszeitraums. Zudem zeigen <strong>Wohin deine Einnahmen fließen</strong> und die <strong>Plananalyse</strong> deine monatliche Aufteilung nach Ausgabenkategorien und Essensbudget als Beträge und Anteile am Monatseinkommen."
                    ],
                    "note": "<strong>Warum beide Ansichten?</strong> Eine jährliche Versicherungsausgabe oder ein kürzerer Februar-Zeitraum beeinflusst, wie viel Bargeld dir jetzt in <strong>Aktuell</strong> zur Verfügung steht, während <strong>Plan</strong> dir zeigt, ob dein normales Einkommen deine regulären Ausgaben dauerhaft deckt."
                },
                {
                    "question": "Wie funktioniert das Essensbudget, und kann ich es für diesen Zeitraum anpassen?",
                    "intro": "Statt jeden Supermarktbong einzutragen, behandelt PlusMinus Essen als ein einziges monatliches Budget, das bis zum Zahltag automatisch abnimmt:",
                    "bullets": [
                        "<strong>Automatische tägliche Anteilung:</strong> PlusMinus rechnet <code>Monatliches Essensbudget &times; (verbleibende Tage bis zum nächsten Zahltag &divide; Gesamttage im aktuellen Zahlungszeitraum)</code>, aufgerundet auf eine ganze Währungseinheit. Der heutige Tag zählt mit, der Zahltag nicht.",
                        "<strong>Eigene Schätzung für diesen Zeitraum:</strong> Tippe in <strong>Aktuell</strong> auf <strong>Essensschätzung</strong>, um für den aktuellen Zeitraum einen festen Betrag (auch null) festzulegen, wenn du zum Beispiel schon groß eingekauft hast oder verreist bist. Dein monatliches Essensbudget in <strong>Plan</strong> bleibt unverändert.",
                        "<strong>Automatische Berechnung wiederherstellen:</strong> Öffne die <strong>Essensschätzung</strong> und tippe jederzeit auf <strong>Automatische Berechnung wiederherstellen</strong>, oder warte auf die automatische Zurücksetzung am nächsten Hauptzahltag."
                    ],
                    "note": "<strong>Hinweis:</strong> Termine weiterer Einnahmen setzen dein Essensbudget niemals zurück – nur dein <strong>Hauptzahltag</strong> verankert den Zeitraum und setzt die Essensschätzung zurück."
                },
                {
                    "question": "Wie verhindert PlusMinus, dass dieselbe Ausgabe zweimal abgezogen wird?",
                    "intro": "Da du deinen Kontostand manuell ohne Bankverbindung pflegst, schützt PlusMinus dich gezielt vor doppeltem Abzug:",
                    "bullets": [
                        "<strong>Zwei-Optionen-Abfrage beim Bezahlen:</strong> Wenn du eine Ausgabe als <strong>Bezahlt</strong> markierst, fragt PlusMinus, ob der Betrag vom <strong>aktuellen Geld abgezogen</strong> werden soll oder dein Kontostand unverändert bleibt, weil er <strong>bereits im aktuellen Geld berücksichtigt</strong> ist (mit automatischer Empfehlung, wenn du deinen Kontostand innerhalb der letzten 5 Minuten aktualisiert hast).",
                        "<strong>Schnellabgleich per Chip:</strong> Nach einer manuellen Kontostandsaktualisierung kannst du kürzlich fällige Ausgaben direkt per Chip als erledigt markieren, ohne sie erneut vom Kontostand abzuziehen.",
                        "<strong>Sicheres Widerrufen:</strong> Wenn du die falsche Option antippst, nutze sofort <strong>Widerrufen</strong>, um Ausgabe und Kontostandsänderung sauber zurückzusetzen."
                    ]
                },
                {
                    "question": "Wie wirken sich kommende Einnahmen auf „Frei verfügbar“ aus?",
                    "intro": "PlusMinus funktioniert zuverlässig mit einem Hauptgehalt, 2&ndash;3 wiederkehrenden Einnahmen an verschiedenen Tagen oder einer geplanten zukünftigen Einmaleinnahme:",
                    "bullets": [
                        "<strong>Zukünftige geplante Einnahmen (automatischer Cashflow-Engpass):</strong> Aktive wiederkehrende und einmalige Einnahmen mit Fälligkeit strikt nach heute (und bei Wochenendverschiebung nach dem nominellen Hauptzahltag des Zeitraums) sowie vor dem nächsten Hauptzahltag werden automatisch anhand des engsten Prüfpunkts einbezogen &mdash; spätere Ausgaben lösen keinen Fehlbetrag aus und du gibst nie Geld vor Eingang aus.",
                        "<strong>Klare Beschriftung und exakte Aufschlüsselung:</strong> Sobald kommendes Einkommen den Betrag über den reinen Kassenbestand hebt, wechselt die Überschrift zu <code>FREI VERFÜGBAR &middot; KOMMENDES EINKOMMEN BERÜCKSICHTIGT</code> (mit dem Hinweis <code>Gesamter Zeitraum bis &hellip;</code> darunter, falls der Engpass früher endet). Tippe auf die Info-Taste für die <strong>Berechnung</strong>, um <strong>Hier addierte Einnahmen</strong> (getrennt vom <strong>Kommenden Einkommen</strong> der Übersicht) und ggf. <strong>Spätere offene Ausgaben</strong> einzusehen.",
                        "<strong>Überfällige und heute fällige Einnahmen:</strong> Überfällige oder heute erwartete Einnahmen (wiederkehrend wie einmalig) werden nie im Voraus eingerechnet &mdash; sie erscheinen als Erinnerung und zählen erst, wenn du sie als <strong>Erhalten</strong> markierst (oder ins <strong>aktuelle Geld</strong> übernimmst). Ausgefallene Einnahmen lassen sich ohne Kontostandsänderung als <strong>Einnahme ausgefallen</strong> markieren.",
                        "<strong>Keine Doppelzählung bei Erhalt:</strong> Wenn du eine einbezogene kommende Einnahme als <strong>Erhalten</strong> markierst und zum <strong>aktuellen Geld</strong> addierst, geht sie sauber ohne Doppelzählung in deinen Kontostand über."
                    ]
                },
                {
                    "question": "Wie funktionieren Bestimmte Monate, Jährlich, Wöchentlich, Alle 2 Wochen, Einmalig und die Plananalyse?",
                    "intro": "PlusMinus bildet regelmäßige Ausgaben, unregelmäßige Rhythmen und Kategorien in <strong>Plan</strong> und <strong>Aktuell</strong> präzise ab:",
                    "bullets": [
                        "<strong>Monatliche Normalisierung in Plan:</strong> Wöchentliche Posten werden mit <code>&times; 52 &divide; 12</code> normalisiert, zweiwöchentliche mit <code>&times; 26 &divide; 12</code>, <strong>Bestimmte Monate</strong> (z. B. Januar &amp; Oktober oder Quartalsvorlagen) mit <code>&times; ausgewählte Monate &divide; 12</code> und jährliche mit <code>&divide; 12</code>.",
                        "<strong>Voller Abzug in Aktuell:</strong> Jährliche Ausgaben und Ausgaben für bestimmte Monate werden exakt in dem Zahlungszeitraum voll abgezogen, in dem sie fällig werden.",
                        "<strong>Einmalige Posten:</strong> Einmalige Einnahmen und Ausgaben (z. B. eine Steuerrückzahlung oder Autoreparatur) erhalten ein genaues Datum und lassen sich in <strong>Plan</strong> oder über das <code>+</code>-Menü in <strong>Aktuell</strong> anlegen. Sie bleiben aus dem festen Monatsplan in <strong>Plan</strong> außen vor: einmalige Ausgaben werden bei Fälligkeit in <strong>Aktuell</strong> voll abgezogen, und geplante zukünftige Einmaleinnahmen vor dem nächsten Zahltag fließen in die Cashflow-Prüfung von <strong>Frei verfügbar</strong> ein, ohne vorab ausgegeben zu werden.",
                        "<strong>17 Kategorien, Plananalyse &amp; optionaler Fälligkeitstag:</strong> Ausgaben lassen sich in 17 optionale Kategorien einordnen (Wohnen, Nebenkosten, Abos, Versicherungen, Darlehen, Kreditkarten &amp; Konsumkredite, Mobilität, Hobbys, Sport &amp; Fitness, Investieren, Gesundheit &amp; Wohlbefinden, Kinder &amp; Familie, Haustiere, Bildung, Sparen, Spenden, Sonstiges). In <strong>Plan</strong> zeigen <strong>Wohin deine Einnahmen fließen</strong> und die <strong>Plananalyse</strong> aktive wiederkehrende Ausgabenkategorien (sowie Ohne Kategorie und Essensbudget) nach Monatsbetrag und Einkommensanteil. Bei wiederkehrenden Ausgaben kann bei Bedarf auch <strong>Kein bestimmter Tag</strong> gewählt werden."
                    ]
                },
                {
                    "question": "Wie funktionieren Hauptzahltag und die Verschiebung aufs Wochenende?",
                    "intro": "Dein <strong>Hauptzahltag</strong> unter <strong>Einstellungen &rarr; Budgetzeitraum</strong> verankert deine Zahlungszeiträume und die Zurücksetzung des Essensbudgets:",
                    "bullets": [
                        "<strong>Tage 1&ndash;31 mit Monatslängen-Anpassung:</strong> Wähle deinen Hauptzahltag von Tag 1 bis 31. In kürzeren Monaten (z. B. Februar oder Monate mit 30 Tagen) wird das Datum automatisch auf den letzten Tag des Monats gekürzt.",
                        "<strong>Wochenendverschiebung auf Freitag:</strong> Aktiviere <strong>Am Freitag auszahlen, wenn der Zahltag auf ein Wochenende fällt</strong>, wenn dein Gehalt bei einem Samstag oder Sonntag bereits am vorherigen Freitag eingeht.",
                        "<strong>Vorschau der nächsten Zahltage:</strong> Direkt in der Auswahl für den <strong>Hauptzahltag</strong> siehst du die nächsten effektiven Zahltage vor dem Speichern."
                    ]
                },
                {
                    "question": "Was sind Im nächsten Zeitraum, vorzeitiges Bezahlen und Ältere als erledigt markieren?",
                    "intro": "PlusMinus hilft dir, vorauszuschauen und vergangene Zeiträume aufgeräumt zu halten:",
                    "bullets": [
                        "<strong>Im nächsten Zeitraum &amp; vorzeitiges Bezahlen:</strong> Klappe in <strong>Aktuell</strong> den Bereich <strong>Im nächsten Zeitraum</strong> auf, um Ausgaben nach deinem nächsten Hauptzahltag anzusehen. Wenn du eine davon schon vorab bezahlt hast, hake sie dort mit demselben Kontostandsabgleich ab.",
                        "<strong>Ältere offene Ausgaben (Ältere als erledigt markieren):</strong> Unbezahlte Ausgaben von vor dem vorherigen Zeitraum (bis zu 24 Monate zurück) verringern nicht dein aktuelles <strong>Frei verfügbar</strong>, sondern erscheinen in einem Hinweisbanner mit der Aktion <strong>Ältere als erledigt markieren</strong>."
                    ]
                },
                {
                    "question": "Wie werden Beträge gerundet?",
                    "intro": "Jede angezeigte Zahl ist so aufgebaut, dass die Rechnung exakt aufgeht:",
                    "bullets": [
                        "<strong>Cent-Genauigkeit &amp; exakte Summen:</strong> Geldposten werden vor dem Addieren oder Subtrahieren auf den nächsten Cent gerundet (genaue halbe Cents werden von null weg gerundet), sodass jede angezeigte Zeile exakt zum Gesamtwert addiert wird.",
                        "<strong>Rundung der Essensschätzung:</strong> Die automatische tägliche Essensschätzung in <strong>Aktuell</strong> rundet auf eine ganze Währungseinheit auf, während selbst gewählte feste Schätzungen Cents beibehalten.",
                        "<strong>Saubere Dezimalanzeige:</strong> Beträge mit Cents zeigen zwei Nachkommastellen, glatte Beträge blenden Nachkommanullen aus."
                    ]
                },
                {
                    "question": "Verbindet sich PlusMinus mit meiner Bank, erfasst es Analysen oder synchronisiert es in die Cloud?",
                    "intro": "Nein. PlusMinus wurde konsequent als lokale App ohne Tracking entwickelt:",
                    "bullets": [
                        "<strong>Speicherung auf deinem Gerät:</strong> Kontostände, Einnahmen, Ausgaben, Zahlungsverlauf und Einstellungen bleiben lokal auf deinem iPhone oder iPad.",
                        "<strong>Keine Konten oder Bankverbindungen:</strong> PlusMinus erfordert keinen Account und fragt niemals nach Bankzugängen oder Open-Banking-Zugriff.",
                        "<strong>Kein Tracking und keine Werbung:</strong> Es gibt keine Analyse-SDKs, keine Werbe-IDs und keine automatische Cloud-Synchronisierung im Hintergrund."
                    ]
                },
                {
                    "question": "Wie funktionieren Backup &amp; Wiederherstellung sowie Alle Daten zurücksetzen?",
                    "intro": "Du behältst jederzeit die volle Kontrolle über deine lokalen Budgetdaten:",
                    "bullets": [
                        "<strong>Backup erstellen:</strong> Öffne <strong>Einstellungen &rarr; Daten &amp; Datenschutz &rarr; Backup &amp; Wiederherstellung</strong> und tippe auf <strong>Backup erstellen</strong>, um eine lesbare JSON-Datei (<code>.plusminusbackup</code>, nicht passwortgeschützt) in iCloud Drive, lokal oder an einem beliebigen Ort in „Dateien“ zu speichern.",
                        "<strong>Aus Backup wiederherstellen:</strong> Tippe auf <strong>Aus Backup wiederherstellen</strong> und wähle eine gültige <code>.plusminusbackup</code>-Datei (bis zu 50 MB). Dabei werden alle aktuellen Budgetdaten ersetzt und der Kontostand vom Erstellungszeitpunkt des Backups wiederhergestellt; App-Sprache und Erscheinungsbild bleiben unverändert.",
                        "<strong>Alle Daten zurücksetzen:</strong> Unter <strong>Einstellungen &rarr; Daten &amp; Datenschutz</strong> löscht <strong>Alle Daten zurücksetzen</strong> nach doppelter Bestätigung alle lokalen Budgetdaten und Einstellungen auf diesem Gerät und kehrt zur Ersteinrichtung zurück. Exportierte Backupdateien und System-Backups von iOS werden nicht gelöscht."
                    ]
                },
                {
                    "question": "Welche Sprachen, Währungen, Erscheinungsbilder und Geräte werden unterstützt?",
                    "intro": "PlusMinus passt sich an deine bevorzugte Sprache, Währung und Optik an:",
                    "bullets": [
                        "<strong>Sprachen:</strong> Direkt unter <strong>Einstellungen &rarr; Präferenzen &rarr; Sprache</strong> umschaltbar zwischen <strong>Systemstandard</strong>, <strong>English</strong>, <strong>Suomi</strong>, <strong>Svenska</strong>, <strong>Deutsch</strong>, <strong>Espa&ntilde;ol</strong> und <strong>Fran&ccedil;ais</strong> – ohne App-Neustart.",
                        "<strong>Währungen:</strong> Unterstützt <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> und <strong>JPY</strong> unter <strong>Einstellungen &rarr; Präferenzen &rarr; Währung</strong>.",
                        "<strong>Erscheinungsbild:</strong> Wähle <strong>Systemstandard</strong>, <strong>Dunkel</strong> oder <strong>Hell</strong> unter <strong>Einstellungen &rarr; Präferenzen &rarr; Erscheinungsbild</strong>.",
                        "<strong>Unterstützte Geräte:</strong> Entwickelt für iPhone und iPad mit <strong>iOS 26 oder neuer</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Ruhiges Monatsbudget & Frei verfügbar für iPhone und iPad",
            "desc": "Sieh sofort, was du aktuell sicher ausgeben kannst, ohne jeden Einkauf einzutragen. Lokale Budget-App mit Plananalyse, Essensbudget-Anteilung und ohne Bankverbindung.",
            "canonical": f"{BASE_URL}/plusminus/de/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Wisse sofort, was du sicher ausgeben kannst.",
            "subtitle": "Lege wiederkehrende Einnahmen, Ausgaben, deinen Zahltag und dein monatliches Essensbudget einmal fest. Ein Blick auf deinen Kontostand zeigt dir, was wirklich frei verfügbar ist – ohne jeden Kaffee zu notieren.",
            "section1_title": "Klarheit in unter fünf Sekunden",
            "features": [
                ("Frei verfügbar in Echtzeit", "Aktuelles Geld, offene Ausgaben, geschätztes Restbudget für Essen und geplante kommende Einkommen am engsten Cashflow-Punkt bewertet &mdash; Schritt für Schritt nachvollziehbar."),
                ("Ruhiger Monatsplan", "Getrennte Monatsübersicht, die wöchentliche, zweiwöchentliche, jährliche und für bestimmte Monate geplante Ausgaben glättet &mdash; inklusive Plananalyse nach Kategorien &mdash; ohne dass der heutige Kontostand stört."),
                ("Privat &amp; lokal zuerst", "Alles bleibt auf deinem Gerät. Keine Konten, keine Bank-Logins, keine Analysen und kein Tracking – niemals."),
            ],
            "section2_title": "Alles was du brauchst, nichts Überflüssiges",
            "list_items": [
                "„Frei verfügbar“-Berechnung bis zum nächsten Hauptzahltag &mdash; inklusive automatischer Prüfung wiederkehrender und einmaliger kommender Einnahmen",
                "Transparente Berechnungsansicht mit genauen Daten, Rücklagen und späteren Ausgaben",
                "Automatische tägliche Essensbudget-Anteilung mit eigener Schätzung für den Zeitraum",
                "Schutz vor doppeltem Abzug beim Abhaken von Ausgaben und Aktualisieren des Kontostands",
                "Rhythmen für wöchentlich, alle 2 Wochen, monatlich, bestimmte Monate, jährlich und einmalig",
                "Plananalyse über die monatliche Verteilung auf 17 Ausgabenkategorien und das Essensbudget",
                "Zahltagsverschiebung auf Freitag bei Wochenenden und Anpassung für kurze Monate",
                "Vorschau „Im nächsten Zeitraum“ mit vorzeitigem Bezahlen und Nachholen älterer Ausgaben",
                "Manueller Export und Wiederherstellung über „Dateien“ (.plusminusbackup)",
                "Verfügbar in 6 Sprachen (Deutsch, Englisch, Finnisch, Schwedisch, Spanisch, Französisch) mit 10 Währungen sowie Dunkel- und Hellmodus",
            ],
            "closing_title": "Für iPhone und iPad entwickelt",
            "closing_body": "PlusMinus ist für iPhone und iPad mit iOS 26 oder neuer konzipiert.",
            "faq_btn": "FAQ",
            "privacy_btn": "Datenschutzerklärung",
            "support_btn": "Support",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Sprachauswahl",
            "featureList": [
                "Echtzeit-Berechnung von „Frei verfügbar“ bis zum nächsten Hauptzahltag mit Cashflow-Prüfung für mehrere und einmalige Einnahmen",
                "Normalisierter Monatsbudget-Plan und Plananalyse über 17 Ausgabenkategorien",
                "Automatische tägliche Essensbudget-Anteilung mit eigener Zeitraum-Anpassung",
                "Zwei-Optionen-Schutz vor doppeltem Abzug beim Bezahlen von Ausgaben",
                "Zeitpläne für bestimmte Monate, jährlich, wöchentlich, alle 2 Wochen und einmalig",
                "100 % lokale Speicherung mit manuellem Backup und Wiederherstellung über Dateien",
            ],
        },
        "privacy": {
            "title": "Datenschutzerklärung für PlusMinus",
            "desc": "Lies die Datenschutzerklärung von PlusMinus: lokale Budgetierung auf deinem Gerät ohne Konten, Analysen, Bankverbindungen oder Tracking.",
            "heading": "Datenschutzerklärung für PlusMinus",
            "last_updated": "Zuletzt aktualisiert: 25. November 2026",
            "sections": [
                (
                    "Daten auf deinem Gerät",
                    [
                        "PlusMinus ist eine lokal funktionierende Budget-App. Dein Budget wird nicht an Entwickler:innen gesendet.",
                        "Kontostände, Einnahmen, Ausgaben, Zahlungsverlauf und Budgeteinstellungen werden auf deinem Gerät gesichert. Sprache, Erscheinungsbild und ausgeblendete Erinnerungen werden als lokale Einstellungen gesichert.",
                    ],
                ),
                (
                    "Tracking und Datenerhebung",
                    [
                        "PlusMinus hat keine Konten, Werbung, Analysen, Bankverbindungen oder automatische Cloud-Synchronisierung. Die App erhebt keine personenbezogenen Daten und verfolgt dich nicht über Apps oder Websites hinweg.",
                    ],
                ),
                (
                    "Backups und Dateien",
                    [
                        "Beim Erstellen eines Backups werden dein Budget und dein Zahlungsverlauf an den von dir in „Dateien“ ausgewählten Speicherort exportiert. Backupdateien sind lesbar und nicht passwortgeschützt. Wenn du iCloud Drive oder einen anderen Anbieter wählst, sichert dieser Anbieter die Datei gemäß seinen eigenen Nutzungsbedingungen und seiner Datenschutzerklärung.",
                        "System-Backups deines Geräts können je nach deinen Apple-Backup-Einstellungen auch App-Daten enthalten. PlusMinus hat keine Kontrolle über diese Backups.",
                    ],
                ),
                (
                    "Löschen deiner Daten",
                    [
                        "Verwende <strong>Alle Daten zurücksetzen</strong> in <strong>Einstellungen &rarr; Daten &amp; Datenschutz</strong>, um das von PlusMinus auf diesem Gerät gesicherte Budget und die Einstellungen zu löschen. Exportierte Dateien und System-Backups werden nicht gelöscht; verwalte diese separat in „Dateien“ oder in den Backup-Einstellungen deines Geräts.",
                    ],
                ),
                (
                    "Datenschutz für Kinder",
                    [
                        "PlusMinus erhebt keine personenbezogenen Daten von Kindern oder anderen Nutzer:innen.",
                    ],
                ),
                (
                    "Änderungen dieser Datenschutzerklärung",
                    [
                        "Diese Datenschutzerklärung kann aktualisiert werden, wenn sich die Funktionen oder Datenpraktiken von PlusMinus ändern. Alle Aktualisierungen werden auf dieser Seite veröffentlicht.",
                    ],
                ),
            ],
            "contact_heading": "Kontakt",
            "contact_intro": "Wenn du Fragen zu dieser Datenschutzerklärung hast, kontaktiere bitte:",
            "about_link": "Über PlusMinus",
            "faq_link": "FAQ",
            "support_link": "PlusMinus Support",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Sprachauswahl",
        },
    },
    "es": {
        "home_href": "../../es/index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "Soporte de PlusMinus",
            "desc": "Obtén ayuda con PlusMinus, la app de presupuestos local y serena para iPhone y iPad, o ponte en contacto con el soporte de PlusMinus.",
            "heading": "Soporte de PlusMinus",
            "thank_you": "Gracias por usar PlusMinus.",
            "faq_card_title": "Consulta primero las preguntas frecuentes (FAQ)",
            "faq_card_body": "Antes de enviar un correo electrónico, revisa nuestras preguntas frecuentes. Encontrarás respuestas claras sobre Disponible para gastar, la diferencia entre Actual y Plan, el análisis del plan, el prorrateo del presupuesto de comida, la protección frente a deducciones dobles, las copias de seguridad y la privacidad.",
            "faq_card_action": "Ver preguntas frecuentes (FAQ)",
            "card_title": "Solución de problemas e información útil",
            "tips": [
                (
                    "El importe Disponible para gastar parece más alto o más bajo de lo esperado:",
                    "Asegúrate de que <strong>Dinero actual</strong> refleja tu saldo real en este momento y revisa los gastos pendientes o vencidos en <strong>Actual</strong>. Los ingresos futuros programados (recurrentes o puntuales) antes de tu próximo día de cobro principal se incluyen automáticamente en Disponible según el punto más ajustado del flujo de caja (sin dejarte gastar dinero antes de recibirlo), mientras que los ingresos vencidos y previstos para hoy esperan hasta que los marques como recibidos. Toca el botón de información junto a Disponible para ver el <strong>Cálculo del disponible</strong> exacto, o consulta todas las reglas en <strong>Ajustes &rarr; Funcionamiento de PlusMinus &rarr; Cómo funcionan los cálculos</strong>."
                ),
                (
                    "Evitar deducciones dobles al marcar gastos como pagados:",
                    "Cuando tocas <strong>Marcar como pagado</strong>, PlusMinus te pregunta si debe <strong>Restar del dinero actual</strong> o mantener el saldo sin cambios porque <strong>El dinero actual ya lo refleja</strong>. Si primero actualizas tu saldo manualmente, los chips de conciliación rápida te permiten marcar gastos vencidos sin volver a restarlos, y <strong>Deshacer</strong> revierte cualquier error al instante."
                ),
                (
                    "Copias de seguridad y cambio a otro dispositivo:",
                    "PlusMinus almacena todos los datos del presupuesto de forma local en tu dispositivo. Para mover tu presupuesto o guardar una copia, abre <strong>Ajustes &rarr; Datos y privacidad &rarr; Copia de seguridad y restauración</strong> y toca <strong>Crear copia de seguridad</strong> para guardar un archivo <code>.plusminusbackup</code> mediante Archivos. Al restaurar se reemplazan todos los datos actuales del presupuesto y se restablece el saldo tal como estaba cuando se creó la copia de seguridad, manteniendo sin cambios el idioma y el aspecto de la app."
                ),
            ],
            "contact_intro": "Si no encontraste respuesta en las preguntas frecuentes, tienes un problema o quieres enviarnos comentarios, escribe a:",
            "email_label": "Correo electrónico:",
            "report_tip": "Al informar de un problema, resulta útil indicar el modelo de dispositivo (iPhone o iPad), la versión de iOS y una breve descripción del fallo.",
            "about_link": "Acerca de PlusMinus",
            "faq_link": "Preguntas frecuentes",
            "privacy_link": "Política de privacidad",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Selección de idioma",
        },
        "faq": {
            "title": "PlusMinus FAQ – Preguntas frecuentes",
            "desc": "Preguntas frecuentes y guías de PlusMinus para iPhone y iPad: Disponible para gastar, Actual vs. Plan, análisis del plan, presupuesto de comida, prevención de cobro doble, meses seleccionados, redondeo, copias de seguridad, privacidad e idiomas.",
            "back_label": "&larr; Soporte de PlusMinus",
            "about_link": "Acerca de PlusMinus",
            "privacy_link": "Política de privacidad",
            "heading": "Preguntas frecuentes",
            "subtitle": "Ayuda, reglas de cálculo y guías para PlusMinus.",
            "toc_title": "En esta página",
            "toc_tip": '¿No encuentras lo que buscas? <a href="index.html">Contactar con el soporte de PlusMinus &rarr;</a>',
            "back_to_top": "&uarr; Volver arriba",
            "nav_aria": "Selección de idioma",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "¿Cómo se calcula Disponible para gastar?",
                    "intro": "<strong>Actual</strong> responde a una pregunta práctica: <em>¿Cuánto dinero puedo gastar con tranquilidad ahora mismo hasta mi próximo día de cobro principal?</em> Parte de una fórmula clara y contempla automáticamente los ingresos futuros programados:",
                    "bullets": [
                        "<strong>Dinero actual:</strong> Tu saldo bancario o en efectivo actualizado manualmente ahora mismo, junto con la fecha relativa de su última actualización.",
                        "<strong>Menos gastos pendientes:</strong> Los gastos recurrentes pendientes y los gastos puntuales que vencen antes de tu próximo día de cobro principal, además de los gastos pendientes vencidos del ciclo de cobro inmediatamente anterior.",
                        "<strong>Menos estimación de comida restante:</strong> Tu presupuesto de comida restante estimado para el horizonte de flujo de caja activo.",
                        "<strong>Punto más ajustado del flujo de caja con ingresos próximos:</strong> Cuando hay ingresos futuros programados (recurrentes o puntuales) antes de tu próximo día de cobro principal, PlusMinus evalúa tu saldo antes de cada próximo ingreso y al final del ciclo, eligiendo el punto más ajustado para que los gastos posteriores no generen déficits falsos sin permitirte gastar dinero antes de recibirlo. Toca el botón de información junto a Disponible para abrir <strong>Cálculo del disponible</strong> (con <strong>Ingresos añadidos a este cálculo</strong>, <strong>Reservado para gastos anteriores al [fecha]</strong>, <strong>Estimación de comida</strong> y los posibles <strong>Gastos pendientes posteriores</strong>), y el encabezado muestra claramente <code>DISPONIBLE &middot; CONSIDERANDO LOS PRÓXIMOS INGRESOS</code>."
                    ],
                    "note": "<strong>Consejo:</strong> Puedes revisar las reglas de cálculo en cualquier momento dentro de la app en <strong>Ajustes &rarr; Funcionamiento de PlusMinus &rarr; Cómo funcionan los cálculos</strong>."
                },
                {
                    "question": "¿Cuál es la diferencia entre Actual y Plan?",
                    "intro": "PlusMinus separa el margen del día a día de tu referencia mensual estable en dos pestañas distintas:",
                    "bullets": [
                        "<strong>Actual:</strong> Abarca desde ahora mismo hasta tu próximo día de cobro principal. Parte de tu <strong>Dinero actual</strong> real, evalúa los gastos pendientes, la comida restante y cualquier ingreso futuro programado según el punto más ajustado del flujo de caja, y muestra tu importe <strong>Disponible para gastar</strong> junto con listas desplegables de <strong>Ingresos próximos</strong> y <strong>Gastos pendientes</strong>.",
                        "<strong>Plan:</strong> Muestra tu <strong>Excedente mensual previsto</strong> normalizado (ingresos mensuales normalizados menos gastos mensuales normalizados menos tu presupuesto mensual de comida), totalmente independiente del saldo bancario de hoy o de la duración del ciclo. Además incluye <strong>A dónde van tus ingresos</strong> y <strong>Análisis del plan</strong>, comparando tus categorías de gastos y tu presupuesto de comida en importes mensuales y porcentaje sobre los ingresos."
                    ],
                    "note": "<strong>¿Por qué dos vistas?</strong> Un seguro anual o un febrero más corto afecta al efectivo disponible hoy en <strong>Actual</strong>, mientras que <strong>Plan</strong> te confirma si tus ingresos habituales cubren tus gastos periódicos a largo plazo."
                },
                {
                    "question": "¿Cómo funciona el presupuesto de comida y puedo ajustarlo para este período?",
                    "intro": "En lugar de registrar cada ticket del supermercado, PlusMinus modela la comida como una única estimación mensual que disminuye automáticamente conforme se acerca el cobro:",
                    "bullets": [
                        "<strong>Prorrateo diario automático:</strong> PlusMinus calcula <code>Presupuesto mensual de comida &times; (días restantes hasta el próximo día de cobro &divide; días totales del ciclo de cobro actual)</code>, redondeado al alza a una unidad monetaria entera. Se incluye el día de hoy y se excluye el día de cobro.",
                        "<strong>Estimación personalizada para este período:</strong> En <strong>Actual</strong>, toca <strong>Estimación de comida</strong> para fijar un importe fijo para el período en curso (incluido cero) si ya hiciste una compra grande o estás de viaje. Tu presupuesto mensual de comida en <strong>Plan</strong> no cambia.",
                        "<strong>Restaurar el cálculo automático:</strong> Abre la hoja de <strong>Estimación de comida</strong> y toca <strong>Restaurar el cálculo automático</strong> en cualquier momento, o deja que se restablezca automáticamente en tu próximo día de cobro principal."
                    ],
                    "note": "<strong>Nota:</strong> Las fechas de ingresos secundarios nunca restablecen el presupuesto de comida — solo tu <strong>Día de cobro principal</strong> ancla el ciclo y restablece la estimación."
                },
                {
                    "question": "¿Cómo evita PlusMinus restar el mismo gasto dos veces?",
                    "intro": "Como actualizas tu saldo manualmente sin conexión bancaria, PlusMinus incorpora controles para que un gasto pagado nunca se descuente dos veces:",
                    "bullets": [
                        "<strong>Confirmación de dos opciones al marcar como pagado:</strong> Al tocar <strong>Marcar como pagado</strong>, PlusMinus pregunta si quieres <strong>Restar del dinero actual</strong> o dejar el saldo igual porque <strong>El dinero actual ya lo refleja</strong> (destacando esta opción si actualizaste tu saldo en los últimos 5 minutos).",
                        "<strong>Chips de conciliación rápida:</strong> Tras una actualización manual del saldo, los chips rápidos te permiten marcar como saldados los gastos vencidos recientemente sin volver a restarlos del saldo.",
                        "<strong>Deshacer seguro:</strong> Si te equivocas de opción, toca <strong>Deshacer</strong> al instante para restaurar tanto el gasto como cualquier cambio automático de saldo."
                    ]
                },
                {
                    "question": "¿Cómo afectan los ingresos próximos a Disponible para gastar?",
                    "intro": "PlusMinus funciona con total precisión tanto si tienes una nómina principal como si recibes 2&ndash;3 ingresos recurrentes en distintos días o un ingreso puntual futuro programado:",
                    "bullets": [
                        "<strong>Ingresos futuros programados (cuello de botella automático):</strong> Los ingresos activos recurrentes y puntuales programados estrictamente después de hoy (y después del día de cobro nominal del ciclo actual cuando se aplica el adelanto por fin de semana) y antes del próximo día de cobro principal se incluyen automáticamente en <strong>Disponible para gastar</strong> mediante el punto más ajustado &mdash; evitando déficits falsos por gastos posteriores sin gastar dinero por adelantado.",
                        "<strong>Etiquetas claras y desglose exacto:</strong> Cuando los ingresos próximos elevan la cifra respecto al efectivo disponible, el título se actualiza a <code>DISPONIBLE &middot; CONSIDERANDO LOS PRÓXIMOS INGRESOS</code> (con la línea <code>Período completo hasta el &hellip;</code> debajo si el punto limitante llega antes). Toca el botón de información para abrir <strong>Cálculo del disponible</strong> y revisar <strong>Ingresos añadidos a este cálculo</strong> (distinto del total <strong>Ingresos próximos</strong> del resumen) y los posibles <strong>Gastos pendientes posteriores</strong>.",
                        "<strong>Ingresos vencidos y de hoy:</strong> Los ingresos vencidos o previstos para hoy (tanto recurrentes como puntuales) nunca se proyectan por adelantado &mdash; aparecen como recordatorios y cuentan solo cuando los marcas como <strong>Recibido</strong> (o los reflejas en <strong>Dinero actual</strong>). Un ingreso no recibido puede marcarse como <strong>Ingreso cancelado</strong> sin cambiar el saldo.",
                        "<strong>Sin doble cómputo al recibirlos:</strong> Al marcar un ingreso próximo incluido como <strong>Recibido</strong> y sumarlo a <strong>Dinero actual</strong>, pasa limpiamente a tu saldo sin contarse dos veces."
                    ]
                },
                {
                    "question": "¿Cómo funcionan Meses seleccionados, Anual, Semanal, Cada 2 semanas, Puntual y Análisis del plan?",
                    "intro": "PlusMinus gestiona con exactitud gastos periódicos, frecuencias menos habituales y análisis por categorías entre <strong>Plan</strong> y <strong>Actual</strong>:",
                    "bullets": [
                        "<strong>Normalización en Plan:</strong> Los conceptos semanales se normalizan mediante <code>&times; 52 &divide; 12</code>, los quincenales mediante <code>&times; 26 &divide; 12</code>, <strong>Meses seleccionados</strong> (como enero y octubre o trimestrales) mediante <code>&times; meses seleccionados &divide; 12</code> y los anuales mediante <code>&divide; 12</code>.",
                        "<strong>Deducción íntegra en Actual:</strong> Los gastos anuales y de meses seleccionados se descuentan íntegramente durante el ciclo de cobro real en el que vencen, para mostrar su impacto real en efectivo.",
                        "<strong>Elementos puntuales:</strong> Los ingresos y gastos de tipo <strong>Puntual</strong> (por ejemplo una devolución fiscal o una reparación del coche) llevan una fecha exacta y pueden añadirse en <strong>Plan</strong> o desde el menú <code>+</code> en <strong>Actual</strong>. Quedan excluidos de la referencia mensual de <strong>Plan</strong>: los gastos puntuales se descuentan íntegramente al vencer en <strong>Actual</strong>, y los ingresos puntuales futuros antes del próximo día de cobro participan en la comprobación de flujo de caja de <strong>Disponible para gastar</strong> sin gastarse por adelantado.",
                        "<strong>17 categorías, Análisis del plan y día opcional:</strong> Los gastos pueden organizarse en 17 categorías opcionales (Vivienda, Suministros, Suscripciones, Seguros, Préstamos, Tarjetas de crédito y crédito al consumo, Transporte, Aficiones, Deportes y fitness, Inversión, Salud y bienestar, Hijos y familia, Mascotas, Educación, Ahorro, Donaciones, Otros). En <strong>Plan</strong>, <strong>A dónde van tus ingresos</strong> y <strong>Análisis del plan</strong> comparan los gastos recurrentes activos por categoría (más Sin categoría y Presupuesto de comida) según importe mensual y porcentaje sobre ingresos. En gastos recurrentes también es posible elegir <strong>Sin día específico</strong>."
                    ]
                },
                {
                    "question": "¿Cómo funcionan el Día de cobro principal y el ajuste por fin de semana?",
                    "intro": "Tu <strong>Día de cobro principal</strong> en <strong>Ajustes &rarr; Ciclo del presupuesto</strong> marca el inicio y reinicio de tus ciclos y del presupuesto de comida:",
                    "bullets": [
                        "<strong>Días 1&ndash;31 con ajuste en meses cortos:</strong> Elige tu día principal de cobro del 1 al 31. En meses más cortos (como febrero o meses de 30 días), PlusMinus ajusta la fecha automáticamente al último día del mes.",
                        "<strong>Adelanto al viernes en fin de semana:</strong> Activa <strong>Pasar el día de cobro al viernes si cae en fin de semana</strong> si cobras el viernes anterior cuando tu día de cobro cae en sábado o domingo.",
                        "<strong>Vista previa del ciclo:</strong> En el selector de <strong>Día de cobro principal</strong> puedes consultar los próximos días efectivos de cobro antes de guardar."
                    ]
                },
                {
                    "question": "¿Qué son Próximo período, el pago anticipado y Marcar anteriores como saldadas?",
                    "intro": "PlusMinus te ayuda a anticiparte al siguiente ciclo y mantener limpios los períodos anteriores:",
                    "bullets": [
                        "<strong>Próximo período y pago anticipado:</strong> Despliega <strong>Próximo período</strong> en <strong>Actual</strong> para previsualizar los gastos que vencen después de tu próximo día de cobro principal. Si ya pagaste uno por adelantado, márcalo ahí mismo con la misma comprobación de saldo.",
                        "<strong>Gastos antiguos sin saldar (Marcar anteriores como saldadas):</strong> Los gastos impagados anteriores al ciclo previo (hasta 24 meses atrás) no se descuentan de tu <strong>Disponible para gastar</strong> actual y se muestran en un aviso específico con el botón <strong>Marcar anteriores como saldadas</strong>."
                    ]
                },
                {
                    "question": "¿Cómo se redondean los importes?",
                    "intro": "Cada cifra visible está pensada para que las cuentas cuadren con total exactitud:",
                    "bullets": [
                        "<strong>Precisión de céntimo y totales exactos:</strong> Los importes se redondean al céntimo más cercano (con empates de medio céntimo alejándose de cero) antes de sumar o restar, de modo que cada línea visible suma exactamente el total mostrado.",
                        "<strong>Redondeo de la estimación de comida:</strong> La estimación diaria automática de comida en <strong>Actual</strong> se redondea al alza a una unidad monetaria entera, mientras que las estimaciones fijas personalizadas conservan los céntimos.",
                        "<strong>Presentación limpia de decimales:</strong> Los importes con céntimos muestran dos decimales y los importes enteros omiten los ceros finales."
                    ]
                },
                {
                    "question": "¿PlusMinus se conecta a mi banco, recopila analíticas o sincroniza en la nube?",
                    "intro": "No. PlusMinus está diseñada íntegramente como una app local y sin rastreo:",
                    "bullets": [
                        "<strong>Guardado en tu dispositivo:</strong> Saldos, ingresos, gastos, historial de pagos y preferencias permanecen localmente en tu iPhone o iPad.",
                        "<strong>Sin cuentas ni enlaces bancarios:</strong> PlusMinus no requiere ninguna cuenta y nunca solicita credenciales bancarias ni acceso Open Banking.",
                        "<strong>Cero rastreo ni anuncios:</strong> No hay SDK de analítica, identificadores publicitarios ni sincronización automática en la nube en segundo plano."
                    ]
                },
                {
                    "question": "¿Cómo funcionan Copia de seguridad y restauración y Restablecer todos los datos?",
                    "intro": "Mantienes el control total sobre los datos locales de tu presupuesto en todo momento:",
                    "bullets": [
                        "<strong>Crear copia de seguridad:</strong> Abre <strong>Ajustes &rarr; Datos y privacidad &rarr; Copia de seguridad y restauración</strong> y toca <strong>Crear copia de seguridad</strong> para exportar un archivo JSON legible (<code>.plusminusbackup</code>, sin contraseña) a iCloud Drive, almacenamiento local o cualquier ubicación de Archivos.",
                        "<strong>Restaurar desde copia de seguridad:</strong> Toca <strong>Restaurar desde copia de seguridad</strong> y selecciona un archivo <code>.plusminusbackup</code> válido (hasta 50 MB). Al restaurar se reemplazan todos los datos actuales del presupuesto y se restablece el saldo desde el momento de la copia, manteniendo sin cambios el idioma y el aspecto de la app.",
                        "<strong>Restablecer todos los datos:</strong> En <strong>Ajustes &rarr; Datos y privacidad</strong>, <strong>Restablecer todos los datos</strong> utiliza una confirmación en dos pasos para borrar todo el presupuesto y preferencias locales en este dispositivo y volver a la configuración inicial. Las copias exportadas y las copias del sistema iOS no se eliminan."
                    ]
                },
                {
                    "question": "¿Qué idiomas, monedas, aspectos y dispositivos son compatibles?",
                    "intro": "PlusMinus se adapta a tu idioma, moneda y aspecto preferidos:",
                    "bullets": [
                        "<strong>Idiomas:</strong> Cambia directamente en <strong>Ajustes &rarr; Preferencias &rarr; Idioma</strong> entre <strong>Predeterminado del sistema</strong>, <strong>English</strong>, <strong>Suomi</strong>, <strong>Svenska</strong>, <strong>Deutsch</strong>, <strong>Espa&ntilde;ol</strong> y <strong>Fran&ccedil;ais</strong> sin reiniciar la app.",
                        "<strong>Monedas:</strong> Compatible con <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> y <strong>JPY</strong> en <strong>Ajustes &rarr; Preferencias &rarr; Moneda</strong>.",
                        "<strong>Aspecto:</strong> Elige <strong>Predeterminado del sistema</strong>, <strong>Oscuro</strong> o <strong>Claro</strong> en <strong>Ajustes &rarr; Preferencias &rarr; Aspecto</strong>.",
                        "<strong>Dispositivos compatibles:</strong> Diseñada para iPhone y iPad con <strong>iOS 26 o posterior</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Presupuesto mensual sereno y Disponible para gastar para iPhone y iPad",
            "desc": "Ve de un vistazo lo que puedes gastar ahora con tranquilidad sin registrar cada compra. Presupuesto local con análisis del plan, prorrateo diario de comida y sin conexiones bancarias.",
            "canonical": f"{BASE_URL}/plusminus/es/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Sabe al instante cuánto puedes gastar con tranquilidad.",
            "subtitle": "Configura una sola vez tus ingresos recurrentes, gastos, día de cobro y presupuesto mensual de comida. Mira tu saldo y comprueba lo que realmente tienes disponible — sin anotar cada café.",
            "section1_title": "Claridad en menos de cinco segundos",
            "features": [
                ("Disponible en tiempo real", "Dinero actual, gastos pendientes, estimación de comida restante e ingresos próximos programados evaluados en el punto más ajustado del flujo de caja &mdash; siempre explicado paso a paso."),
                ("Plan mensual estable", "Resumen mensual independiente que normaliza gastos semanales, quincenales, anuales y de meses seleccionados &mdash; con análisis del plan por categorías &mdash; sin que el saldo de hoy enturbie la foto."),
                ("Privado y local ante todo", "Todo permanece en tu dispositivo. Sin cuentas, sin accesos bancarios, sin analíticas y sin rastreo — nunca."),
            ],
            "section2_title": "Todo lo necesario, nada superfluo",
            "list_items": [
                "Cálculo de Disponible para gastar hasta tu próximo día de cobro principal &mdash; con gestión automática de ingresos recurrentes y puntuales",
                "Desglose transparente en Cálculo del disponible con fechas exactas, reservas y gastos posteriores",
                "Prorrateo diario automático de comida con ajuste instantáneo para el período actual",
                "Protección contra deducciones dobles al marcar gastos como pagados o actualizar el saldo",
                "Frecuencias semanales, cada 2 semanas, mensuales, de meses seleccionados, anuales y puntuales",
                "Análisis del plan para ver a dónde van tus ingresos en 17 categorías de gastos y comida",
                "Adelanto al viernes cuando el día de cobro cae en fin de semana y ajuste en meses cortos",
                "Vista previa de Próximo período con pago anticipado y regularización de gastos anteriores",
                "Exportación y restauración manual mediante Archivos (.plusminusbackup)",
                "Disponible en 6 idiomas (español, inglés, finés, sueco, alemán, francés) con 10 monedas y modo oscuro/claro",
            ],
            "closing_title": "Diseñada para iPhone y iPad",
            "closing_body": "PlusMinus está diseñada para iPhone y iPad con iOS 26 o posterior.",
            "faq_btn": "Preguntas frecuentes",
            "privacy_btn": "Política de privacidad",
            "support_btn": "Soporte",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Selección de idioma",
            "featureList": [
                "Cálculo en tiempo real de Disponible para gastar hasta el próximo día de cobro principal con soporte de múltiples ingresos e ingresos puntuales",
                "Plan mensual normalizado y Análisis del plan en 17 categorías de gastos",
                "Prorrateo diario automático de comida con ajuste personalizado del período",
                "Confirmación en dos opciones para evitar deducciones dobles al pagar gastos",
                "Frecuencias de meses seleccionados, anual, semanal, cada 2 semanas y puntual",
                "Almacenamiento 100 % local con copia de seguridad y restauración manual en Archivos",
            ],
        },
        "privacy": {
            "title": "Política de privacidad de PlusMinus",
            "desc": "Lee la política de privacidad de PlusMinus: presupuesto local en tu dispositivo sin cuentas, analíticas, conexiones bancarias ni rastreo.",
            "heading": "Política de privacidad de PlusMinus",
            "last_updated": "Última actualización: 25 de noviembre de 2026",
            "sections": [
                (
                    "Datos en tu dispositivo",
                    [
                        "PlusMinus es una app de presupuestos centrada en el almacenamiento local. Tu presupuesto no se envía a quien desarrolla la app.",
                        "Los saldos, los ingresos, los gastos, el historial de pagos y los ajustes del presupuesto se almacenan en tu dispositivo. El idioma, el aspecto y los recordatorios descartados se guardan como preferencias locales.",
                    ],
                ),
                (
                    "Seguimiento y recopilación de datos",
                    [
                        "PlusMinus no tiene cuentas, publicidad, análisis, conexiones bancarias ni sincronización automática en la nube. La app no recopila datos personales ni te rastrea en otras apps o sitios web.",
                    ],
                ),
                (
                    "Copias de seguridad y archivos",
                    [
                        "Al crear una copia de seguridad, se exportan tu presupuesto y tu historial de pagos a la ubicación que elijas en Archivos. Los archivos de copia de seguridad son legibles y no están protegidos con contraseña. Si eliges iCloud Drive u otro proveedor, dicho proveedor almacena el archivo según sus propios términos y política de privacidad.",
                        "Las copias de seguridad del sistema de tu dispositivo también pueden incluir datos de la app, según tus ajustes de copia de seguridad de Apple. PlusMinus no controla esas copias de seguridad.",
                    ],
                ),
                (
                    "Eliminación de tus datos",
                    [
                        "Usa <strong>Restablecer todos los datos</strong> en <strong>Ajustes &rarr; Datos y privacidad</strong> para borrar el presupuesto y las preferencias almacenados por PlusMinus en este dispositivo. Los archivos exportados y las copias de seguridad del sistema no se eliminan; gestiónalos por separado en Archivos o en los ajustes de copias de seguridad del dispositivo.",
                    ],
                ),
                (
                    "Privacidad de los menores",
                    [
                        "PlusMinus no recopila información personal de menores ni de ningún otro usuario.",
                    ],
                ),
                (
                    "Cambios en esta política de privacidad",
                    [
                        "Esta política de privacidad puede actualizarse si cambian las funciones o las prácticas de datos de PlusMinus. Cualquier actualización se publicará en esta página.",
                    ],
                ),
            ],
            "contact_heading": "Contacto",
            "contact_intro": "Si tienes preguntas sobre esta política de privacidad, ponte en contacto con:",
            "about_link": "Acerca de PlusMinus",
            "faq_link": "Preguntas frecuentes",
            "support_link": "Soporte de PlusMinus",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Selección de idioma",
        },
    },
    "fr": {
        "home_href": "../../fr/index.html",
        "home_label": "Lightfeet Apps",
        "index": {
            "title": "Assistance PlusMinus",
            "desc": "Obtenez de l’aide pour PlusMinus, l’app de budget serein et local avant tout sur iPhone et iPad, ou contactez l’assistance PlusMinus.",
            "heading": "Assistance PlusMinus",
            "thank_you": "Merci d’utiliser PlusMinus.",
            "faq_card_title": "Consultez d’abord la FAQ pour des réponses rapides",
            "faq_card_body": "Avant d’envoyer un e-mail, parcourez notre Foire aux questions (FAQ). Vous y trouverez des réponses claires sur Disponible à dépenser, la différence entre Actuel et Plan, l’analyse du plan, le prorata du budget alimentation, la protection contre la double déduction, les sauvegardes et la confidentialité.",
            "faq_card_action": "Consulter la Foire aux questions (FAQ)",
            "card_title": "Dépannage et informations utiles",
            "tips": [
                (
                    "Le montant Disponible à dépenser semble plus élevé ou plus bas que prévu :",
                    "Vérifiez que <strong>Argent actuel</strong> correspond bien à votre solde réel du moment et passez en revue les dépenses impayées ou en retard dans <strong>Actuel</strong>. Les revenus futurs prévus (récurrents ou ponctuels) avant votre prochain jour de paie principal sont automatiquement pris en compte selon le point de trésorerie le plus serré (sans vous permettre de dépenser l’argent avant de le recevoir), tandis que les revenus arrivés à échéance ou attendus aujourd’hui attendent d’être marqués comme reçus. Touchez le bouton d’information à côté de Disponible à dépenser pour ouvrir le <strong>Calcul du disponible</strong> exact, ou consultez toutes les règles dans <strong>Réglages &rarr; Comprendre PlusMinus &rarr; Fonctionnement des calculs</strong>."
                ),
                (
                    "Éviter les doubles déductions lorsque vous marquez une dépense payée :",
                    "Lorsque vous marquez une dépense comme <strong>Payée</strong>, PlusMinus vous demande s’il faut <strong>Soustraire de l’argent actuel</strong> ou laisser le solde inchangé parce que <strong>L’argent actuel en tient déjà compte</strong>. Si vous mettez d’abord votre solde à jour manuellement, des raccourcis de rapprochement permettent de valider les dépenses échues sans les soustraire une seconde fois, et <strong>Annuler</strong> corrige aussitôt une erreur."
                ),
                (
                    "Sauvegardes et changement d’appareil :",
                    "PlusMinus conserve toutes vos données budgétaires localement sur votre appareil. Pour transférer votre budget ou garder une copie, ouvrez <strong>Réglages &rarr; Données et confidentialité &rarr; Sauvegarde et restauration</strong> et touchez <strong>Créer une sauvegarde</strong> pour enregistrer un fichier <code>.plusminusbackup</code> via Fichiers. La restauration remplace toutes les données budgétaires actuelles et rétablit le solde tel qu’il était lors de la création de la sauvegarde, sans modifier la langue ni l’apparence de l’app."
                ),
            ],
            "contact_intro": "Si vous n’avez pas trouvé de réponse dans la FAQ, rencontrez un problème ou souhaitez partager votre avis, contactez :",
            "email_label": "E-mail :",
            "report_tip": "Lors du signalement d’un problème, il est utile d’indiquer le modèle de votre appareil (iPhone ou iPad), la version d’iOS et une brève description du souci.",
            "about_link": "À propos de PlusMinus",
            "faq_link": "FAQ",
            "privacy_link": "Politique de confidentialité",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Choix de la langue",
        },
        "faq": {
            "title": "PlusMinus FAQ – Foire aux questions",
            "desc": "Questions fréquentes et guides pour PlusMinus sur iPhone et iPad : Disponible à dépenser, Actuel et Plan, analyse du plan, budget alimentation, double déduction, mois sélectionnés, arrondis, sauvegardes, confidentialité et langues.",
            "back_label": "&larr; Assistance PlusMinus",
            "about_link": "À propos de PlusMinus",
            "privacy_link": "Politique de confidentialité",
            "heading": "Foire aux questions",
            "subtitle": "Aide, règles de calcul et guides pour PlusMinus.",
            "toc_title": "Sur cette page",
            "toc_tip": 'Vous ne trouvez pas ce que vous cherchez ? <a href="index.html">Contacter l’assistance PlusMinus &rarr;</a>',
            "back_to_top": "&uarr; Haut de page",
            "nav_aria": "Choix de la langue",
            "copyright": "PlusMinus &copy; 2026",
            "items": [
                {
                    "question": "Comment est calculé le montant Disponible à dépenser ?",
                    "intro": "<strong>Actuel</strong> répond à une question pratique : <em>De combien puis-je disposer sereinement dès maintenant jusqu’à mon prochain jour de paie principal ?</em> Le calcul part d’une formule limpide et gère automatiquement les revenus futurs prévus :",
                    "bullets": [
                        "<strong>Argent actuel :</strong> Le solde de votre compte ou de vos espèces mis à jour manuellement à cet instant, avec un horodatage relatif de la dernière mise à jour.",
                        "<strong>Moins les dépenses impayées :</strong> Les dépenses récurrentes impayées et les dépenses ponctuelles arrivant à échéance avant votre prochain jour de paie principal, ainsi que les dépenses impayées en retard du cycle de paie immédiatement précédent.",
                        "<strong>Moins l’estimation alimentation restante :</strong> Votre budget alimentation restant estimé sur l’horizon de trésorerie actif.",
                        "<strong>Point de trésorerie le plus serré avec des revenus à venir :</strong> Lorsqu’un revenu futur prévu (récurrent ou ponctuel) arrive avant votre prochain jour de paie principal, PlusMinus évalue votre solde avant chaque prochaine date de revenu ainsi qu’à la fin du cycle et retient le point le plus serré : les dépenses ultérieures ne créent pas de faux déficit, tout en vous empêchant de dépenser l’argent avant de le recevoir. Touchez le bouton d’information à côté de Disponible à dépenser pour ouvrir le <strong>Calcul du disponible</strong> (affichant <strong>Revenus ajoutés à ce calcul</strong>, <strong>Réservé aux dépenses avant le [date]</strong>, <strong>Estimation alimentation</strong> et les éventuelles <strong>Dépenses impayées ultérieures</strong>), et l’intitulé indique clairement <code>DISPONIBLE &middot; REVENUS À VENIR PRIS EN COMPTE</code>."
                    ],
                    "note": "<strong>Astuce :</strong> Vous pouvez consulter à tout moment le détail des règles dans l’app sous <strong>Réglages &rarr; Comprendre PlusMinus &rarr; Fonctionnement des calculs</strong>."
                },
                {
                    "question": "Quelle est la différence entre Actuel et Plan ?",
                    "intro": "PlusMinus sépare clairement votre marge de manœuvre immédiate de votre référence mensuelle régulière dans deux onglets distincts :",
                    "bullets": [
                        "<strong>Actuel :</strong> Couvre la période de maintenant jusqu’à votre prochain jour de paie principal. Cet onglet part de votre vrai solde <strong>Argent actuel</strong>, examine les dépenses impayées, l’alimentation restante et les éventuels revenus futurs prévus au point de trésorerie le plus serré pour afficher votre <strong>Disponible à dépenser</strong> avec les listes dépliables <strong>Revenus à venir</strong> et <strong>Dépenses impayées</strong>.",
                        "<strong>Plan :</strong> Affiche votre <strong>Reste mensuel prévu</strong> normalisé (revenus mensuels normalisés moins dépenses mensuelles normalisées moins votre budget alimentation mensuel), totalement indépendant du solde du jour ou de la durée du cycle de paie. Il propose également <strong>Où vont vos revenus</strong> et l’<strong>Analyse du plan</strong> pour comparer la répartition mensuelle par catégorie de dépenses et le budget alimentation en montants et en part des revenus mensuels."
                    ],
                    "note": "<strong>Pourquoi deux vues ?</strong> Une dépense d’assurance annuelle ou un mois de février plus court influe directement sur le cash disponible aujourd’hui dans <strong>Actuel</strong>, tandis que <strong>Plan</strong> vérifie si vos revenus habituels couvrent vos dépenses régulières dans la durée."
                },
                {
                    "question": "Comment fonctionne le budget alimentation et puis-je le modifier pour ce cycle ?",
                    "intro": "Plutôt que de saisir chaque ticket de caisse, PlusMinus modélise l’alimentation comme une estimation mensuelle unique qui décroît automatiquement à mesure que la paie approche :",
                    "bullets": [
                        "<strong>Prorata quotidien automatique :</strong> PlusMinus calcule <code>Budget alimentation mensuel &times; (jours restants jusqu’au prochain jour de paie &divide; nombre total de jours du cycle de paie en cours)</code>, arrondi à l’unité monétaire supérieure. Aujourd’hui est inclus et le jour de paie est exclu.",
                        "<strong>Estimation personnalisée pour cette période :</strong> Dans <strong>Actuel</strong>, touchez <strong>Estimation alimentation</strong> pour fixer un montant fixe pour le cycle en cours (y compris zéro) si vous avez déjà fait le plein de courses ou si vous voyagez. Votre budget mensuel dans <strong>Plan</strong> ne change pas.",
                        "<strong>Rétablir le calcul automatique :</strong> Ouvrez la fiche <strong>Estimation alimentation</strong> et touchez <strong>Rétablir le calcul automatique</strong> à tout moment, ou laissez la réinitialisation s’opérer automatiquement à la prochaine paie principale."
                    ],
                    "note": "<strong>Remarque :</strong> Les dates de revenus secondaires ne réinitialisent jamais votre budget alimentation — seul votre <strong>Jour de paie principal</strong> délimite le cycle et réinitialise l’estimation."
                },
                {
                    "question": "Comment PlusMinus évite-t-il de déduire deux fois la même dépense ?",
                    "intro": "Comme vous mettez à jour votre solde manuellement sans connexion bancaire, PlusMinus intègre plusieurs garde-fous contre les doubles déductions :",
                    "bullets": [
                        "<strong>Confirmation à deux choix sur Payée :</strong> Lorsque vous marquez une dépense comme <strong>Payée</strong>, PlusMinus demande s’il faut <strong>Soustraire de l’argent actuel</strong> ou garder le solde tel quel parce que <strong>L’argent actuel en tient déjà compte</strong> (avec mise en avant intelligente si vous avez mis à jour votre solde dans les 5 dernières minutes).",
                        "<strong>Raccourcis de rapprochement rapide :</strong> Après une mise à jour manuelle du solde, des pastilles rapides permettent de valider les dépenses récemment échues sans les soustraire de nouveau de votre solde.",
                        "<strong>Annulation sûre :</strong> En cas d’erreur, touchez aussitôt <strong>Annuler</strong> pour rétablir proprement la dépense et tout ajustement automatique du solde."
                    ]
                },
                {
                    "question": "Quel est l’impact des revenus à venir sur Disponible à dépenser ?",
                    "intro": "PlusMinus fonctionne avec la même clarté que vous ayez un seul salaire principal, 2&ndash;3 revenus récurrents versés à des dates différentes ou un revenu ponctuel prévu :",
                    "bullets": [
                        "<strong>Revenus futurs prévus (goulot de trésorerie automatique) :</strong> Les revenus récurrents et ponctuels actifs prévus strictement après aujourd’hui (et après le jour de paie nominal du cycle en cours en cas d’avance au vendredi) et avant le prochain jour de paie principal sont pris en compte automatiquement via le point de contrôle le plus serré &mdash; évitant de faux déficits dus aux dépenses ultérieures sans jamais dépenser d’argent à l’avance.",
                        "<strong>Libellés clairs et détail exact :</strong> Lorsque des revenus à venir relèvent le disponible par rapport à la seule trésorerie en main, le titre passe à <code>DISPONIBLE &middot; REVENUS À VENIR PRIS EN COMPTE</code> (avec la mention <code>Période complète jusqu’au &hellip;</code> dessous si le point contraignant arrive plus tôt). Touchez le bouton d’information pour ouvrir le <strong>Calcul du disponible</strong> et consulter <strong>Revenus ajoutés à ce calcul</strong> (distinct du total <strong>Revenus à venir</strong> de l’aperçu) ainsi que les éventuelles <strong>Dépenses impayées ultérieures</strong>.",
                        "<strong>Revenus en retard et prévus aujourd’hui :</strong> Les revenus en retard ou attendus aujourd’hui (récurrents comme ponctuels) ne sont jamais anticipés &mdash; ils figurent en rappel et comptent uniquement une fois marqués comme <strong>Reçu</strong> (ou intégrés dans <strong>Argent actuel</strong>). Un revenu annulé peut être marqué comme <strong>Revenu annulé</strong> sans modifier votre solde.",
                        "<strong>Aucun double comptage à la réception :</strong> Lorsque vous marquez un revenu à venir inclus comme <strong>Reçu</strong> et l’ajoutez à <strong>Argent actuel</strong>, il rejoint votre solde sans être compté deux fois."
                    ]
                },
                {
                    "question": "Comment fonctionnent Mois sélectionnés, Annuel, Hebdomadaire, Toutes les 2 semaines, Ponctuel et Analyse du plan ?",
                    "intro": "PlusMinus gère avec précision les dépenses régulières, les fréquences ponctuelles ou espacées et la répartition par catégorie entre <strong>Plan</strong> et <strong>Actuel</strong> :",
                    "bullets": [
                        "<strong>Normalisation dans Plan :</strong> Les éléments hebdomadaires sont normalisés via <code>&times; 52 &divide; 12</code>, toutes les 2 semaines via <code>&times; 26 &divide; 12</code>, <strong>Mois sélectionnés</strong> (comme janvier &amp; octobre ou trimestriels) via <code>&times; mois sélectionnés &divide; 12</code>, et les éléments annuels via <code>&divide; 12</code>.",
                        "<strong>Déduction intégrale dans Actuel :</strong> Les dépenses annuelles et des mois sélectionnés sont déduites en entier durant le cycle de paie où elles arrivent à échéance, pour refléter leur impact réel.",
                        "<strong>Éléments ponctuels :</strong> Les revenus et dépenses de type <strong>Ponctuel</strong> (par exemple un remboursement fiscal ou une réparation auto) ont une date précise et peuvent être ajoutés dans <strong>Plan</strong> ou via le menu <code>+</code> dans <strong>Actuel</strong>. Ils restent exclus de la base mensuelle de <strong>Plan</strong> : les dépenses ponctuelles sont déduites intégralement à échéance dans <strong>Actuel</strong>, et les revenus ponctuels futurs avant le prochain jour de paie participent au contrôle de trésorerie de <strong>Disponible à dépenser</strong> sans être dépensés d’avance.",
                        "<strong>17 catégories, Analyse du plan et jour d’échéance facultatif :</strong> Les dépenses peuvent être classées parmi 17 catégories facultatives (Logement, Eau et énergie, Abonnements, Assurance, Prêts, Cartes de crédit et crédit à la consommation, Transport, Loisirs, Sport et fitness, Investissement, Santé et bien-être, Enfants et famille, Animaux, Éducation, Épargne, Dons, Autre). Dans <strong>Plan</strong>, <strong>Où vont vos revenus</strong> et <strong>Analyse du plan</strong> comparent les dépenses récurrentes actives par catégorie (plus Sans catégorie et Budget alimentation) par montant mensuel et part des revenus. Pour les dépenses récurrentes, il est aussi possible de choisir <strong>Aucun jour précis</strong>."
                    ]
                },
                {
                    "question": "Comment fonctionnent le Jour de paie principal et le décalage du week-end ?",
                    "intro": "Votre <strong>Jour de paie principal</strong> dans <strong>Réglages &rarr; Cycle budgétaire</strong> rythme vos cycles de paie et la réinitialisation de l’estimation alimentation :",
                    "bullets": [
                        "<strong>Jours 1&ndash;31 avec adaptation aux mois courts :</strong> Choisissez votre jour de paie principal entre 1 et 31. Lors des mois plus courts (comme février ou les mois de 30 jours), PlusMinus cale automatiquement la date sur le dernier jour du mois.",
                        "<strong>Décalage au vendredi en cas de week-end :</strong> Activez <strong>Avancer au vendredi si la paie tombe un week-end</strong> si votre employeur vous verse le salaire le vendredi précédent lorsque le jour de paie tombe un samedi ou un dimanche.",
                        "<strong>Aperçu du cycle :</strong> Dans le sélecteur de <strong>Jour de paie principal</strong>, vous pouvez prévisualiser les prochaines dates de paie effectives avant d’enregistrer."
                    ]
                },
                {
                    "question": "Que sont À venir pour la prochaine période, le paiement anticipé et Marquer les anciennes comme réglées ?",
                    "intro": "PlusMinus vous aide à anticiper les cycles suivants tout en gardant les anciens cycles bien ordonnés :",
                    "bullets": [
                        "<strong>À venir pour la prochaine période et paiement anticipé :</strong> Dépliez <strong>À venir pour la prochaine période</strong> dans <strong>Actuel</strong> pour voir les dépenses échues après votre prochain jour de paie principal. Si vous avez déjà payé l’une d’elles à l’avance, marquez-la payée ici avec la même vérification du solde.",
                        "<strong>Anciennes dépenses non réglées (Marquer les anciennes comme réglées) :</strong> Les dépenses impayées antérieures au cycle précédent (jusqu’à 24 mois en arrière) ne sont pas déduites de votre <strong>Disponible à dépenser</strong> actuel et apparaissent dans un bandeau dédié avec l’action <strong>Marquer les anciennes comme réglées</strong>."
                    ]
                },
                {
                    "question": "Comment les montants sont-ils arrondis ?",
                    "intro": "Chaque chiffre affiché est conçu pour que l’arithmétique reste parfaitement exacte :",
                    "bullets": [
                        "<strong>Précision au centime et totaux exacts :</strong> Les composantes monétaires sont arrondies au centime le plus proche (demi-centime arrondi en s’éloignant de zéro) avant l’addition ou la soustraction, afin que chaque ligne affichée donne exactement le total indiqué.",
                        "<strong>Arrondi de l’estimation alimentation :</strong> L’estimation quotidienne automatique dans <strong>Actuel</strong> est arrondie à l’unité monétaire supérieure, tandis que les montants fixes saisis manuellement conservent les centimes.",
                        "<strong>Affichage sobre des décimales :</strong> Les montants comportant des centimes affichent deux décimales, tandis que les montants entiers omettent les zéros superflus."
                    ]
                },
                {
                    "question": "PlusMinus se connecte-t-elle à ma banque, collecte-t-elle des statistiques ou synchronise-t-elle dans le cloud ?",
                    "intro": "Non. PlusMinus est conçue exclusivement comme une app locale et sans suivi :",
                    "bullets": [
                        "<strong>Stocké sur votre appareil :</strong> Soldes, revenus, dépenses, historique des paiements et réglages restent localement sur votre iPhone ou iPad.",
                        "<strong>Aucun compte ni connexion bancaire :</strong> PlusMinus ne demande aucun compte et n’exige jamais vos identifiants bancaires ni un accès Open Banking.",
                        "<strong>Zéro pistage ni publicité :</strong> L’app n’intègre aucun SDK analytique, aucun identifiant publicitaire et aucune synchronisation cloud automatique en arrière-plan."
                    ]
                },
                {
                    "question": "Comment fonctionnent Sauvegarde et restauration ainsi que Réinitialiser toutes les données ?",
                    "intro": "Vous gardez à tout moment le contrôle total de vos données budgétaires locales :",
                    "bullets": [
                        "<strong>Créer une sauvegarde :</strong> Ouvrez <strong>Réglages &rarr; Données et confidentialité &rarr; Sauvegarde et restauration</strong> et touchez <strong>Créer une sauvegarde</strong> pour exporter une archive JSON lisible (<code>.plusminusbackup</code>, non protégée par mot de passe) vers iCloud Drive, le stockage local ou n’importe quel dossier de Fichiers.",
                        "<strong>Restaurer à partir d’une sauvegarde :</strong> Touchez <strong>Restaurer à partir d’une sauvegarde</strong> et sélectionnez un fichier <code>.plusminusbackup</code> valide (jusqu’à 50 Mo). La restauration remplace toutes les données budgétaires actuelles et rétablit le solde tel qu’il était lors de la sauvegarde, tout en conservant la langue et l’apparence actuelles de l’app.",
                        "<strong>Réinitialiser toutes les données :</strong> Sous <strong>Réglages &rarr; Données et confidentialité</strong>, <strong>Réinitialiser toutes les données</strong> efface après double confirmation toutes les données budgétaires et préférences locales sur cet appareil et revient à la configuration initiale. Les sauvegardes exportées et les sauvegardes système iOS ne sont pas supprimées."
                    ]
                },
                {
                    "question": "Quels sont les langues, devises, thèmes et appareils pris en charge ?",
                    "intro": "PlusMinus s’adapte à votre langue, à votre devise et à votre thème préférés :",
                    "bullets": [
                        "<strong>Langues :</strong> Modifiable directement dans <strong>Réglages &rarr; Préférences &rarr; Langue</strong> entre <strong>Par défaut du système</strong>, <strong>English</strong>, <strong>Suomi</strong>, <strong>Svenska</strong>, <strong>Deutsch</strong>, <strong>Espa&ntilde;ol</strong> et <strong>Fran&ccedil;ais</strong> sans redémarrer l’app.",
                        "<strong>Devises :</strong> Prend en charge <strong>EUR, USD, GBP, SEK, NOK, DKK, CHF, CAD, AUD</strong> et <strong>JPY</strong> dans <strong>Réglages &rarr; Préférences &rarr; Devise</strong>.",
                        "<strong>Apparence :</strong> Choisissez <strong>Par défaut du système</strong>, <strong>Sombre</strong> ou <strong>Clair</strong> dans <strong>Réglages &rarr; Préférences &rarr; Apparence</strong>.",
                        "<strong>Appareils compatibles :</strong> Conçue pour iPhone et iPad sous <strong>iOS 26 ou ultérieur</strong>."
                    ]
                },
            ],
        },
        "marketing": {
            "title": "PlusMinus – Budget mensuel serein et Disponible à dépenser sur iPhone et iPad",
            "desc": "Voyez en un coup d’œil ce que vous pouvez dépenser sereinement dès maintenant sans noter chaque achat. Budget local avec analyse du plan, prorata alimentaire et sans connexion bancaire.",
            "canonical": f"{BASE_URL}/plusminus/fr/marketing.html",
            "hero_title": "PlusMinus",
            "tagline": "Sachez instantanément ce que vous pouvez dépenser sereinement.",
            "subtitle": "Configurez une fois vos revenus récurrents, dépenses, jour de paie et budget alimentation mensuel. Jetez un œil à votre solde et voyez ce qui est vraiment disponible — sans noter chaque café.",
            "section1_title": "La clarté en moins de cinq secondes",
            "features": [
                ("Disponible en temps réel", "Argent actuel, dépenses impayées, estimation alimentation restante et revenus à venir prévus évalués au point de trésorerie le plus serré &mdash; toujours détaillé étape par étape."),
                ("Plan mensuel régulier", "Vue mensuelle distincte qui lisse dépenses hebdomadaires, bimensuelles, annuelles et de mois sélectionnés &mdash; avec analyse du plan par catégorie &mdash; sans que le solde du jour brouille la vision."),
                ("Privée et locale avant tout", "Tout reste sur votre appareil. Aucun compte, aucun identifiant bancaire, aucune analyse et aucun suivi — jamais."),
            ],
            "section2_title": "Tout ce qu’il faut, rien de superflu",
            "list_items": [
                "Calcul du Disponible à dépenser jusqu’au prochain jour de paie principal &mdash; avec gestion automatique des revenus récurrents et ponctuels à venir",
                "Fiche Calcul du disponible transparente avec dates exactes, réserves et dépenses ultérieures",
                "Prorata quotidien automatique du budget alimentation avec personnalisation immédiate pour le cycle en cours",
                "Protection contre les doubles déductions au paiement des dépenses et à la mise à jour du solde",
                "Fréquences hebdomadaire, toutes les 2 semaines, mensuelle, mois sélectionnés, annuelle et ponctuelle",
                "Analyse du plan montrant la répartition mensuelle sur 17 catégories de dépenses et l’alimentation",
                "Avance au vendredi lorsque le jour de paie tombe un week-end et adaptation aux mois courts",
                "Aperçu À venir pour la prochaine période avec paiement anticipé et régularisation des anciennes dépenses",
                "Export et restauration manuels via Fichiers (.plusminusbackup)",
                "Disponible en 6 langues (français, anglais, finnois, suédois, allemand, espagnol) avec 10 devises et mode sombre/clair",
            ],
            "closing_title": "Conçue pour iPhone et iPad",
            "closing_body": "PlusMinus est conçue pour iPhone et iPad sous iOS 26 ou version ultérieure.",
            "faq_btn": "FAQ",
            "privacy_btn": "Politique de confidentialité",
            "support_btn": "Assistance",
            "copyright": "&copy; 2026 PlusMinus",
            "nav_aria": "Choix de la langue",
            "featureList": [
                "Calcul en temps réel du Disponible à dépenser jusqu’au prochain jour de paie principal avec gestion des revenus récurrents et ponctuels",
                "Budget mensuel prévisionnel normalisé et Analyse du plan sur 17 catégories de dépenses",
                "Prorata quotidien automatique du budget alimentation avec surcharge manuelle par cycle",
                "Confirmation à deux choix anti-double déduction lors du paiement des dépenses",
                "Fréquences mois sélectionnés, annuelle, hebdomadaire, toutes les 2 semaines et ponctuelle",
                "Stockage 100 % local avec sauvegarde et restauration manuelles via Fichiers",
            ],
        },
        "privacy": {
            "title": "Politique de confidentialité de PlusMinus",
            "desc": "Consultez la politique de confidentialité de PlusMinus : budget local sur votre appareil sans compte, statistique, connexion bancaire ni suivi.",
            "heading": "Politique de confidentialité de PlusMinus",
            "last_updated": "Dernière mise à jour : 25 novembre 2026",
            "sections": [
                (
                    "Données sur votre appareil",
                    [
                        "PlusMinus est une app de gestion budgétaire locale avant tout. Votre budget n’est pas envoyé au développeur.",
                        "Les soldes, les revenus, les dépenses, l’historique des paiements et les réglages du budget sont stockés sur votre appareil. La langue, l’apparence et les rappels ignorés sont enregistrés comme préférences locales.",
                    ],
                ),
                (
                    "Suivi et collecte de données",
                    [
                        "PlusMinus ne comporte ni compte, ni publicité, ni outil d’analyse, ni connexion bancaire, ni synchronisation cloud automatique. L’app ne collecte pas de données personnelles et ne vous suit pas sur d’autres apps ou sites web.",
                    ],
                ),
                (
                    "Sauvegardes et Fichiers",
                    [
                        "La création d’une sauvegarde exporte votre budget et votre historique des paiements vers l’emplacement de votre choix dans Fichiers. Les fichiers de sauvegarde sont lisibles et non protégés par mot de passe. Si vous choisissez iCloud Drive ou un autre fournisseur, celui-ci stocke le fichier selon ses propres conditions et sa politique de confidentialité.",
                        "Les sauvegardes système de votre appareil peuvent également inclure des données de l’app, selon vos réglages de sauvegarde Apple. PlusMinus ne contrôle pas ces sauvegardes.",
                    ],
                ),
                (
                    "Suppression de vos données",
                    [
                        "Utilisez <strong>Réinitialiser toutes les données</strong> dans <strong>Réglages &rarr; Données et confidentialité</strong> pour effacer le budget et les préférences stockés par PlusMinus sur cet appareil. Les fichiers exportés et les sauvegardes système ne sont pas supprimés ; gérez-les séparément dans Fichiers ou dans les réglages de sauvegarde de votre appareil.",
                    ],
                ),
                (
                    "Confidentialité des enfants",
                    [
                        "PlusMinus ne collecte aucune information personnelle auprès des enfants ni d’aucun autre utilisateur.",
                    ],
                ),
                (
                    "Modifications de cette politique de confidentialité",
                    [
                        "Cette politique de confidentialité peut être mise à jour si les fonctionnalités ou les pratiques de PlusMinus évoluent. Toute mise à jour sera publiée sur cette page.",
                    ],
                ),
            ],
            "contact_heading": "Contact",
            "contact_intro": "Pour toute question concernant cette politique de confidentialité, veuillez contacter :",
            "about_link": "À propos de PlusMinus",
            "faq_link": "FAQ",
            "support_link": "Assistance PlusMinus",
            "copyright": "PlusMinus &copy; 2026",
            "nav_aria": "Choix de la langue",
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
{hreflang_links("")}
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
    prefix = "" if lang_code == "en" else f"{lang_code}/"
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
{hreflang_links("plusminus/")}
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
    prefix = "" if lang_code == "en" else f"{lang_code}/"
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
{hreflang_links("plusminus/", "faq.html")}
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
            "inLanguage": [lang["code"] for lang in SITE_LANGS],
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
{hreflang_links("plusminus/", "marketing.html")}

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
    prefix = "" if lang_code == "en" else f"{lang_code}/"
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
{hreflang_links("plusminus/", "privacy.html")}
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

    # Root landing pages (6)
    for lang in SITE_LANGS:
        prefix = f"{lang['dir']}/" if lang["dir"] else ""
        urls.append((f"{BASE_URL}/{prefix}", "2026-11-25"))

    # WakeUp pages under /wakeup/ (24)
    for page in ["", "faq.html", "marketing.html", "privacy.html"]:
        for lang in WAKEUP_LANGS:
            prefix = f"{lang}/" if lang else ""
            urls.append((f"{BASE_URL}/wakeup/{prefix}{page}", "2026-11-23"))

    # PlusMinus pages under /plusminus/ (24)
    for page in ["", "faq.html", "marketing.html", "privacy.html"]:
        for lang in SITE_LANGS:
            prefix = f"{lang['dir']}/" if lang["dir"] else ""
            urls.append((f"{BASE_URL}/plusminus/{prefix}{page}", "2026-11-25"))

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
    # 1. Root landing pages (EN, FI, SV, DE, ES, FR)
    for lang in SITE_LANGS:
        rel_path = "index.html" if not lang["dir"] else os.path.join(lang["dir"], "index.html")
        write_output(rel_path, build_root_index(lang["code"]))

    # 2. PlusMinus pages (EN, FI, SV, DE, ES, FR)
    for lang in SITE_LANGS:
        code = lang["code"]
        subdir = "plusminus" if not lang["dir"] else os.path.join("plusminus", lang["dir"])
        write_output(os.path.join(subdir, "index.html"), build_pm_index(code))
        write_output(os.path.join(subdir, "faq.html"), build_pm_faq(code))
        write_output(os.path.join(subdir, "marketing.html"), build_pm_marketing(code))
        write_output(os.path.join(subdir, "privacy.html"), build_pm_privacy(code))

    # 3. Unified sitemap.xml
    write_output("sitemap.xml", build_sitemap())
    print("Generated 6 root pages, 24 PlusMinus pages, and sitemap.xml successfully.")


if __name__ == "__main__":
    main()
