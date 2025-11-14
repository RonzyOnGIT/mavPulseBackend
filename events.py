# events.py
# This script is responsible for calling the scraper functions
# and populating the Supabase `events` table with cleaned data.

from scraper import getUpcomingEvents, getTrendingEvents
from supabase_client import supabase
from datetime import datetime
import re

# This will hold all events before inserting
events_by_source = {
    "upcoming": [],
    "trending": [],
}


def parse_date_string(date_str):
    """
    Try to parse various date formats from UTA events.
    Returns ISO format string or None if parsing fails.
    
    Examples:
    - "Thu, Nov 13"
    - "Thu, Nov 13 7pm to 11pm CST"
    - "Thu, Nov 13 9am - Fri, Nov 14 12am CST"
    - "Monday, November 18, 2024 at 6:00pm"
    """
    if not date_str:
        return None
    
    # Get current year for dates that don't include it
    current_year = datetime.now().year
    
    # Clean up the date string - extract just the first date part
    # Remove time ranges and extra info
    date_str = date_str.strip()
    
    # Handle range dates like "Thu, Nov 13 9am - Fri, Nov 14 12am CST"
    # Just take the first date
    if ' - ' in date_str or ' to ' in date_str:
        date_str = re.split(r'\s+-\s+|\s+to\s+', date_str)[0].strip()
    
    # Remove time parts like "7pm to 11pm CST" or "10am to 5pm CST"
    date_str = re.split(r'\s+\d+:\d+[ap]m|\s+\d+[ap]m', date_str)[0].strip()
    
    # Remove trailing "CST", "EST", etc.
    date_str = re.sub(r'\s+(CST|EST|PST|MST)$', '', date_str).strip()
    
    # Try various formats
    formats = [
        ("%a, %b %d", True),           # Thu, Nov 13 (needs year)
        ("%A, %B %d", True),           # Thursday, November 13 (needs year)
        ("%a, %b %d, %Y", False),      # Thu, Nov 13, 2024
        ("%A, %B %d, %Y", False),      # Thursday, November 13, 2024
        ("%B %d, %Y", False),          # November 18, 2024
        ("%m/%d/%Y", False),           # 11/18/2024
        ("%Y-%m-%d", False),           # 2024-11-18
    ]
    
    for fmt, needs_year in formats:
        try:
            if needs_year:
                # Add current year to the date string
                dt = datetime.strptime(f"{date_str}, {current_year}", f"{fmt}, %Y")
            else:
                dt = datetime.strptime(date_str, fmt)
            return dt.isoformat()
        except ValueError:
            continue
    
    # If all parsing fails, return None
    print(f"Warning: Could not parse date '{date_str}'")
    return None


def normalize_events(raw_events, source):
    """
    Take raw events from the scraper and normalize them into
    a consistent shape ready for insertion into Supabase.

    Expected raw shape (from scraper):
      {
        "title": "...",
        "date": "...",
        "imgSrc": "..."
      }

    Supabase `events` table columns:
      - title (text)
      - description (text) -> we'll store the image URL & source here
      - date (timestamptz) -> we'll pass ISO format string
      - course_id (uuid, nullable) -> we don't have this, so set to None
    """
    cleaned = []

    for e in raw_events:
        if not e:
            continue

        title = (e.get("title") or "").strip()
        date_str = (e.get("date") or "").strip()
        img_src = (e.get("imgSrc") or "").strip()

        # Skip anything missing required fields
        if not title or not date_str:
            print(f"Skipping event missing title or date: {e}")
            continue

        # Parse the date into ISO format
        parsed_date = parse_date_string(date_str)
        if not parsed_date:
            print(f"Skipping event with unparseable date: {title} - {date_str}")
            continue

        # Build description: include image URL (if any) + source tag
        description_parts = []
        if img_src:
            description_parts.append(f"Image: {img_src}")
        description_parts.append(f"Source: {source}")
        description = " | ".join(description_parts)

        cleaned.append(
            {
                "title": title,
                "description": description,
                "date": parsed_date,
                "course_id": None,
            }
        )

    return cleaned


def dedupe(events):
    """
    Remove duplicates based on (title, date).
    """
    seen = set()
    unique = []

    for ev in events:
        key = (ev["title"], ev["date"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(ev)

    return unique


def main():
    print("=" * 60)
    print("STARTING EVENT SCRAPING AND INSERTION")
    print("=" * 60)
    
    print("\n[1/5] Fetching upcoming events from scraper...")
    raw_upcoming = getUpcomingEvents()
    events_by_source["upcoming"] = normalize_events(raw_upcoming, "upcoming")
    print(f"✓ Got {len(events_by_source['upcoming'])} cleaned upcoming events")

    print("\n[2/5] Fetching trending events from scraper...")
    raw_trending = getTrendingEvents()
    events_by_source["trending"] = normalize_events(raw_trending, "trending")
    print(f"✓ Got {len(events_by_source['trending'])} cleaned trending events")

    # Combine & dedupe before inserting
    print("\n[3/5] Combining and deduplicating events...")
    all_events = events_by_source["upcoming"] + events_by_source["trending"]
    print(f"  Total before dedupe: {len(all_events)}")
    all_events = dedupe(all_events)
    print(f"  Total after dedupe:  {len(all_events)}")

    if not all_events:
        print("\n⚠ No events to insert!")
        return

    print("\n[4/5] Inserting events into Supabase...")
    inserted = 0
    failed = 0

    for i, ev in enumerate(all_events, 1):
        try:
            result = supabase.table("events").insert(ev).execute()
            inserted += 1
            print(f"  [{i}/{len(all_events)}] ✓ Inserted: {ev['title'][:50]}...")
        except Exception as e:
            failed += 1
            print(f"  [{i}/{len(all_events)}] ✗ Failed: {ev.get('title', 'Unknown')[:50]}...")
            print(f"      Error: {str(e)}")

    print("\n[5/5] SUMMARY")
    print("=" * 60)
    print(f"Total events processed: {len(all_events)}")
    print(f"Successfully inserted:  {inserted}")
    print(f"Failed insertions:      {failed}")
    print("=" * 60)


if __name__ == "__main__":
    main()
