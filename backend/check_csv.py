import requests

res = requests.post(
    "http://localhost:6333/collections/rag_prod/points/scroll",
    json={"limit": 50, "with_payload": True}
)

points = res.json()["result"]["points"]

found = False
for p in points:
    if p["payload"].get("file_type") == ".csv":
        found = True
        print("CSV FOUND")
        print("Source:", p["payload"]["source"])
        print("Text preview:", p["payload"]["text"][:300])
        break

if not found:
    print("❌ NO CSV DATA INGESTED")
