import os
import json
import sqlite3
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

# Get credentials from environment
credentials_json = os.environ['GOOGLE_CREDENTIALS']
file_id = os.environ['FILE_ID']

# Parse credentials
credentials_info = json.loads(credentials_json)
credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

# Build Drive API client
service = build('drive', 'v3', credentials=credentials)

# Download the file
request = service.files().get_media(fileId=file_id)
file_handle = io.BytesIO()
downloader = MediaIoBaseDownload(file_handle, request)

done = False
while not done:
    status, done = downloader.next_chunk()

# Save to temporary file
with open('koreader.db', 'wb') as f:
    f.write(file_handle.getvalue())

# Connect to SQLite database
conn = sqlite3.connect('koreader.db')
cursor = conn.cursor()

# Query reading progress for each book (latest reading session)
cursor.execute("""
    SELECT
        d.id_book,
        b.title,
        b.authors,
        ROUND((CAST(d.page AS FLOAT) / d.total_pages) * 100, 2) AS percentage_completed
    FROM page_stat_data d
    JOIN book b ON b.id = d.id_book
    WHERE d.start_time = (
        SELECT MAX(d1.start_time)
        FROM page_stat_data d1
        WHERE d1.id_book = d.id_book
    )
    ORDER BY percentage_completed ASC
""")

books = cursor.fetchall()

# Process and create JSON output
reading_data = {
    "updated_at": datetime.now().isoformat(),
    "books": [
        {
            "id": row[0],
            "title": row[1],
            "authors": row[2],
            "percentage_completed": row[3]
        }
        for row in books
    ]
}

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Write JSON file
with open('data/reading-progress.json', 'w') as f:
    json.dump(reading_data, f, indent=2)

conn.close()
