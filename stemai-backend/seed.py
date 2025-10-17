import json, os, asyncio
from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "stemai")

async def main():
    client = None
    db = client[MONGODB_DB]
    coll = db["concepts"]
    with open("algebra_concepts_with_weights.json") as f:
        data = json.load(f)
    # upsert
    for name, info in data.items():
        doc = {
            "name": name,
            "domain": info.get("domain", "Mathematics"),
            "grade_level": info.get("grade_level"),
            "description": info.get("description"),
            "tags": info.get("tags", []),
            "depends_on": info.get("depends_on", []),
            "leads_to": info.get("leads_to", []),
            "updated_at": __import__("datetime").datetime.utcnow()
        }
        await coll.update_one({"name": name}, {"$set": doc}, upsert=True)
    await coll.create_index("name", unique=True)
    await coll.create_index("domain")
    await coll.create_index("depends_on.topic")
    await coll.create_index("leads_to.topic")
    print(f"Seeded {len(data)} concepts.")

if __name__ == "__main__":
    asyncio.run(main())
