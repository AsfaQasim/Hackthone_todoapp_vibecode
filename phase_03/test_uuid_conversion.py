import uuid

# Test UUID conversion
canonical_uuid = "776e40cf-6874-43a2-bb12-b43f117df73c"
hex_uuid = uuid.UUID(canonical_uuid).hex

print(f"Canonical UUID: {canonical_uuid}")
print(f"Hex UUID: {hex_uuid}")

# Check if this matches what's in the database
db_uuid = "776e40cf687443a2bb12b43f117df73c"
print(f"DB UUID: {db_uuid}")
print(f"Do they match? {hex_uuid == db_uuid}")