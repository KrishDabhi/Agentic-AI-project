import csv
import random
import os

# Step 1: Define ESG-covered industries and their sectors
ESG_INDUSTRY_TO_SECTOR = {
    "Software—Infrastructure": "Technology",
    "Software—Application": "Technology",
    "Semiconductors": "Technology",
    "Auto Manufacturers": "Consumer Discretionary",
    "Banks—Diversified": "Financial Services",
    "Drug Manufacturers—General": "Healthcare",
    "Internet Retail": "Consumer Discretionary",
    "Health Care Plans": "Healthcare",
    "Home Improvement Retail": "Consumer Discretionary",
    "Entertainment": "Communication Services",
    "Oil & Gas Integrated": "Energy",
    "Telecom Services": "Communication Services",
    "Utilities—Regulated Electric": "Utilities",
    # Special case: generic "Healthcare" industry
    "Healthcare": "Healthcare",
}

ESG_INDUSTRIES = set(ESG_INDUSTRY_TO_SECTOR.keys())

# Step 2: Real company data (your original + extras)
REAL_COMPANIES = [
    # (symbol, name, industry)
    ("MSFT", "Microsoft Corporation", "Software—Infrastructure"),
    ("CRM", "Salesforce Inc.", "Software—Infrastructure"),
    ("ADBE", "Adobe Inc.", "Software—Application"),
    ("INTU", "Intuit Inc.", "Software—Application"),
    ("NVDA", "NVIDIA Corporation", "Semiconductors"),
    ("INTC", "Intel Corporation", "Semiconductors"),
    ("AMD", "Advanced Micro Devices Inc.", "Semiconductors"),
    ("AVGO", "Broadcom Inc.", "Semiconductors"),
    ("TXN", "Texas Instruments Incorporated", "Semiconductors"),
    ("QCOM", "Qualcomm Incorporated", "Semiconductors"),
    ("TSLA", "Tesla Inc.", "Auto Manufacturers"),
    ("GM", "General Motors Company", "Auto Manufacturers"),
    ("F", "Ford Motor Company", "Auto Manufacturers"),
    ("JPM", "JPMorgan Chase & Co.", "Banks—Diversified"),
    ("BAC", "Bank of America Corp.", "Banks—Diversified"),
    ("GS", "The Goldman Sachs Group Inc.", "Banks—Diversified"),
    ("C", "Citigroup Inc.", "Banks—Diversified"),
    ("JNJ", "Johnson & Johnson", "Drug Manufacturers—General"),
    ("PFE", "Pfizer Inc.", "Drug Manufacturers—General"),
    ("MRK", "Merck & Co. Inc.", "Drug Manufacturers—General"),
    ("ABBV", "AbbVie Inc.", "Drug Manufacturers—General"),
    ("LLY", "Eli Lilly and Company", "Drug Manufacturers—General"),
    ("BMY", "Bristol Myers Squibb Co.", "Drug Manufacturers—General"),
    ("AMZN", "Amazon.com Inc.", "Internet Retail"),
    ("UNH", "UnitedHealth Group Inc.", "Health Care Plans"),
    ("CVS", "CVS Health Corporation", "Health Care Plans"),
    ("HD", "Home Depot Inc.", "Home Improvement Retail"),
    ("LOW", "Lowe's Companies Inc.", "Home Improvement Retail"),
    ("DIS", "Walt Disney Co.", "Entertainment"),
    ("NFLX", "Netflix Inc.", "Entertainment"),
    ("CMCSA", "Comcast Corporation", "Telecom Services"),
    ("VZ", "Verizon Communications Inc.", "Telecom Services"),
    ("T", "AT&T Inc.", "Telecom Services"),
    ("XOM", "Exxon Mobil Corporation", "Oil & Gas Integrated"),
    ("CVX", "Chevron Corporation", "Oil & Gas Integrated"),
    ("NEE", "NextEra Energy Inc.", "Utilities—Regulated Electric"),
    ("DUK", "Duke Energy Corporation", "Utilities—Regulated Electric"),
    ("SO", "Southern Company", "Utilities—Regulated Electric"),
    ("TMO", "Thermo Fisher Scientific Inc.", "Healthcare"),
    ("DHR", "Danaher Corporation", "Healthcare"),
    ("ISRG", "Intuitive Surgical Inc.", "Healthcare"),
    ("MDT", "Medtronic plc", "Healthcare"),
    ("AMGN", "Amgen Inc.", "Healthcare"),
]

# Convert to full records with sector
companies = []
used_symbols = set()

for symbol, name, industry in REAL_COMPANIES:
    if industry in ESG_INDUSTRIES:
        sector = ESG_INDUSTRY_TO_SECTOR[industry]
        companies.append((symbol, name, sector, industry))
        used_symbols.add(symbol)

# Step 3: Generate synthetic companies to reach 1000
roots = ["Nexus", "Apex", "Vertex", "Horizon", "Pinnacle", "Quantum", "Stellar", "Orion", "Aurora", "Vanta"]
suffixes = ["Inc.", "Corporation", "Group", "Holdings", "Systems", "Solutions", "Dynamics", "Industries", "Technologies", "Enterprises"]

while len(companies) < 1000:
    industry = random.choice(list(ESG_INDUSTRIES))
    sector = ESG_INDUSTRY_TO_SECTOR[industry]
    name = f"{random.choice(roots)} {random.choice(suffixes)}"
    
    # Generate unique symbol (3-5 uppercase letters + number if needed)
    attempts = 0
    while True:
        base = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        if attempts == 0:
            sym = base
        else:
            sym = base + str(attempts)
        if sym not in used_symbols:
            break
        attempts += 1
        if attempts > 1000:  # fallback
            sym = f"SYN{len(companies)}"
            break

    used_symbols.add(sym)
    companies.append((sym, name, sector, industry))

# Step 4: Remove any accidental full-row duplicates (safety net)
unique_companies = list(dict.fromkeys(companies))  # preserves order, removes dup rows

# Trim or extend to exactly 1000 (shouldn't be needed, but safe)
unique_companies = unique_companies[:1000]
while len(unique_companies) < 1000:
    # Extremely unlikely, but just in case
    industry = random.choice(list(ESG_INDUSTRIES))
    sector = ESG_INDUSTRY_TO_SECTOR[industry]
    name = f"Backup {len(unique_companies)}"
    sym = f"EXTRA{len(unique_companies)}"
    unique_companies.append((sym, name, sector, industry))

# Step 5: Save to CSV
output_file = "company.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["symbol", "name", "sector", "industry"])
    writer.writerows(unique_companies)

print(f"Successfully generated '{output_file}' with {len(unique_companies)} unique companies.")
print(f"File saved at: {os.path.abspath(output_file)}")