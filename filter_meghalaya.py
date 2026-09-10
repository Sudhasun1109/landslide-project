import pandas as pd

# Read extracted CSV
df = pd.read_csv("landslide_inventory.csv", header=None)

print("CSV loaded successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# Find the actual header row
header_row = None

for i in range(len(df)):
    values = df.iloc[i].fillna("").astype(str).tolist()
    row_text = " ".join(values)

    if any(value.strip().lower() == "state" for value in values):
        header_row = i
        break

if header_row is None:
    print("\nERROR: Could not find State header.")
    print("\nFirst 10 rows:")
    print(df.head(10).to_string())
    exit()

print("Header found at row:", header_row)

# Set header
headers = df.iloc[header_row].fillna("").astype(str).tolist()

# Clean headers
headers = [
    h.replace("\n", " ")
     .replace("\r", " ")
     .strip()
    for h in headers
]

df.columns = headers

# Remove title/header rows
df = df.iloc[header_row + 1:].copy()

# Remove empty rows
df = df.dropna(how="all")

# Remove columns with empty names
valid_columns = [col for col in df.columns if col.strip() != ""]
df = df[valid_columns]

print("\nDetected columns:")
print(df.columns.tolist())

# Find State column
state_column = None

for col in df.columns:
    if col.strip().lower() == "state":
        state_column = col
        break

if state_column is None:
    print("\nERROR: State column not found.")
    print(df.columns.tolist())
    exit()

# Clean State values
df[state_column] = (
    df[state_column]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Find Meghalaya
meghalaya = df[
    df[state_column].str.lower() == "meghalaya"
].copy()

# Save full cleaned inventory
df.to_csv(
    "landslide_inventory_clean.csv",
    index=False
)

# Save Meghalaya data
meghalaya.to_csv(
    "meghalaya_landslide.csv",
    index=False
)

print("\n================================")
print("SUCCESS!")
print("================================")

print("Total inventory records:", len(df))
print("Meghalaya records:", len(meghalaya))

print("\nFiles created:")
print("1. landslide_inventory_clean.csv")
print("2. meghalaya_landslide.csv")

print("\nMeghalaya sample:")
print(meghalaya.head(10).to_string(index=False))