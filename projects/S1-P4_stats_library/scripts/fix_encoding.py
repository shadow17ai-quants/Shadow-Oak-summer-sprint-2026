import re

path = r"D:\The Underhood\SEMESTERS\Sprint_Summer2026\Shadow-Oak-summer-sprint-2026\projects\S1-P4_stats_library\scripts\dashboard.py"

with open(path, "rb") as f:
    raw = f.read()

text = raw.decode("utf-8", errors="replace")

# Repair known mojibake chains regardless of how many times they got re-encoded
repairs = {
    "\ufffd": "",
}
for bad, good in repairs.items():
    text = text.replace(bad, good)

# Nuke ANY mojibake em-dash variant by targeting the stable anchor around it
text = re.sub(
    r'st\.markdown\(f"### \{choice\.upper\(\)\}.*?\{ticker\}"\)',
    'st.markdown(f"### {choice.upper()} - {ticker}")',
    text
)

# Nuke ANY mojibake rupee-sign variant by targeting the stable anchor around it
text = re.sub(
    r'st\.caption\(f"Last close: .*?\{last_price:,\.2f\}',
    'st.caption(f"Last close: Rs {last_price:,.2f}',
    text
)

with open(path, "w", encoding="utf-8", newline="\n") as f:
    f.write(text)

print("Fixed via Python - anchors replaced cleanly.")

# Verify
with open(path, "rb") as f:
    check = f.read()
if b"\xc3\x83" in check or b"\xc3\xa2" in check:
    print("STILL DIRTY - mojibake bytes remain elsewhere in file.")
else:
    print("File is clean.")
