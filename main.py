import gspread
import json

gc = gspread.service_account("service_account.json")
spreadsheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1F7cGThvbwbHU0HrNR69mK4zSh5Q4jq7AoaKkwuVTR4k/edit"
)

worksheets = spreadsheet.worksheets()
for ws in worksheets[1:]:
    records = ws.get_all_records()
    print(f"# channel: {ws.title}")
    for _, time, name, text, data in ws.get_all_values():
        data = json.loads(data)
        if data.get("subtype") == "channel_join":
            continue
        print(f"({time}) {name}: {text}")
    print()
