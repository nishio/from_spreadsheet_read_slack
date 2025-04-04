import gspread
import json

gc = gspread.service_account("service_account.json")
spreadsheet = gc.open_by_url(
    "https://docs.google.com/spreadsheets/d/1q0lpXJ_wNQ8mYZ2nlYT1eXfHFGGLmK8wJoKz-Bd_m58/edit"
)
ignore_channels = ["2_開発_いどばた_github", "2_開発_広聴ai_github"]
worksheets = spreadsheet.worksheets()
for ws in worksheets[1:]:
    records = ws.get_all_records()
    print(f"# channel: {ws.title}")
    if ws.title != "2_開発_広聴ai":
        continue
    for _, time, name, text, data in ws.get_all_values():
        data = json.loads(data)
        if data.get("subtype") == "channel_join":
            continue
        print(f"({time}) {name}: {text}")
    print()
