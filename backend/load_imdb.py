import os
import gzip
import pymysql
from pathlib import Path

conn = pymysql.connect(
    host="silvertrack.mysql.database.azure.com",
    port=3306,
    user="silvertrack",
    password="SilverTrack2026!",
    database="silvertrack",
    autocommit=True,
    charset='utf8mb4'
)
cur = conn.cursor()

DOWNLOADS = Path.home() / "Downloads"
LIMIT = 10000

print("Reading title.basics — collecting recent titles...")
titles = []
with gzip.open(DOWNLOADS / "title.basics.tsv.gz", 'rt', encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 9:
            continue
        tconst, titleType, primaryTitle, _, isAdult, startYear, _, _, genres = parts[:9]
        if isAdult == '1':
            continue
        if titleType not in ('movie', 'tvSeries', 'tvMiniSeries'):
            continue
        if startYear == '\\N':
            continue
        try:
            year = int(startYear)
        except:
            continue
        genres = None if genres == '\\N' else genres
        titles.append((tconst, titleType, primaryTitle, year, genres))

# Sort by most recent year first, take top 10000
titles.sort(key=lambda x: x[3], reverse=True)
titles = titles[:LIMIT]
print(f"  Found {len(titles)} recent titles, inserting into Azure...")

for t in titles:
    try:
        cur.execute(
            "INSERT IGNORE INTO title_basics (tconst, titleType, primaryTitle, startYear, genres) VALUES (%s,%s,%s,%s,%s)",
            t
        )
    except:
        continue
print(f"  ✅ Loaded {len(titles)} titles (most recent first)")

# Get the tconsts we loaded for filtering other tables
loaded_tconsts = set(t[0] for t in titles)

print("Loading title.ratings...")
count = 0
with gzip.open(DOWNLOADS / "title.ratings.tsv.gz", 'rt', encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 3:
            continue
        tconst, avgRating, numVotes = parts[:3]
        if tconst not in loaded_tconsts:
            continue
        try:
            cur.execute(
                "INSERT IGNORE INTO title_ratings (tconst, averageRating, numVotes) VALUES (%s,%s,%s)",
                (tconst, float(avgRating), int(numVotes))
            )
            count += 1
        except:
            continue
print(f"  ✅ Loaded {count} ratings")

print("Loading name.basics...")
count = 0
with gzip.open(DOWNLOADS / "name.basics.tsv.gz", 'rt', encoding='utf-8') as f:
    next(f)
    for line in f:
        if count >= LIMIT:
            break
        parts = line.strip().split('\t')
        if len(parts) < 5:
            continue
        nconst, primaryName, birthYear, _, primaryProfession = parts[:5]
        birthYear = None if birthYear == '\\N' else int(birthYear)
        primaryProfession = None if primaryProfession == '\\N' else primaryProfession
        try:
            cur.execute(
                "INSERT IGNORE INTO name_basics (nconst, primaryName, birthYear, primaryProfession) VALUES (%s,%s,%s,%s)",
                (nconst, primaryName, birthYear, primaryProfession)
            )
            count += 1
        except:
            continue
print(f"  ✅ Loaded {count} people")

print("Loading title.crew...")
count = 0
with gzip.open(DOWNLOADS / "title.crew.tsv.gz", 'rt', encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 3:
            continue
        tconst, directors, writers = parts[:3]
        if tconst not in loaded_tconsts:
            continue
        directors = None if directors == '\\N' else directors
        writers = None if writers == '\\N' else writers
        try:
            cur.execute(
                "INSERT IGNORE INTO title_crew (tconst, directors, writers) VALUES (%s,%s,%s)",
                (tconst, directors, writers)
            )
            count += 1
        except:
            continue
print(f"  ✅ Loaded {count} crew records")

print("Loading title.episode...")
count = 0
with gzip.open(DOWNLOADS / "title.episode.tsv.gz", 'rt', encoding='utf-8') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 4:
            continue
        tconst, parentTconst, seasonNumber, episodeNumber = parts[:4]
        if parentTconst not in loaded_tconsts:
            continue
        seasonNumber = None if seasonNumber == '\\N' else int(seasonNumber)
        episodeNumber = None if episodeNumber == '\\N' else int(episodeNumber)
        try:
            cur.execute(
                "INSERT IGNORE INTO title_episode (tconst, parentTconst, seasonNumber, episodeNumber) VALUES (%s,%s,%s,%s)",
                (tconst, parentTconst, seasonNumber, episodeNumber)
            )
            count += 1
        except:
            continue
print(f"  ✅ Loaded {count} episodes")

print("\n🎬 All done! Your Azure database now has 10,000 most recent IMDB titles!")
cur.close()
conn.close()
