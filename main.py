# Copyright (c) 2025 Pawel Mania. All rights reserved.

import unicodecsv as csv
import sys
import polib

# simple .po to .csv with or without duplicates
def po2csv(po_file, with_duplicates = True):
    po = polib.pofile(po_file)
    new_file = po_file.replace('.po', '.csv')
    if not with_duplicates:
        new_file = 'no_dupes_' + new_file

    dupes = []
    unique_ones = []
    with open(new_file, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['comment','msgctxt', 'Raw', 'English'])
        for entry in po:
            if with_duplicates:
                writer.writerow([entry.comment,entry.msgctxt, entry.msgid, entry.msgstr])
            else:
                if entry.msgid not in unique_ones:
                    writer.writerow([entry.comment,entry.msgctxt, entry.msgid, entry.msgstr])
                    unique_ones.append(entry.msgid)
                else:
                    dupes.append(entry.msgid)

    if not with_duplicates:
        print("Skipped: " + str(len(dupes)))
        with open("dupes.txt", "w") as file:
            for duped in dupes:
                file.write(duped + "\n")

# simple .csv to .po with column index for multi language rows
def csv2po(csv_file, csv_column):
    po = polib.POFile()
    skip_first = True
    new_file = csv_file.replace('.csv', '.po')
    with open(csv_file, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if skip_first:
                new_file = row[csv_column] + new_file
                skip_first = False
            else:
                entry = polib.POEntry(
                    msgctxt=row[0],
                    msgid=row[1],
                    msgstr=row[csv_column]
                )
                po.append(entry)
    po.save(new_file)

# filling empty msgid in your existing .po file
def fill2po(csv_file, csv_column, po_file):
    po = polib.pofile(po_file)

    msgid_to_entry = {}
    for entry in po:
        if entry.msgid.strip() not in msgid_to_entry:
            msgid_to_entry[entry.msgid.strip()] = [entry]
        else:
            msgid_to_entry[entry.msgid.strip()].append(entry)

    msgctxt_to_entry = {}
    for entry in po:
        if entry.msgctxt.strip() not in msgctxt_to_entry:
            msgctxt_to_entry[entry.msgctxt.strip()] = [entry]
        else:
            msgctxt_to_entry[entry.msgctxt.strip()].append(entry)

    updated_count = 0
    not_found_count = 0
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader):
            msgctxt = row[0]
            msgid   = row[1]
            msgstr  = row[csv_column]

            if not msgid:
                continue

            key_msgctxt = msgctxt.strip()
            key_msgid = msgid.strip()
            if key_msgctxt in msgctxt_to_entry:
                for entry in msgctxt_to_entry[key_msgctxt]:
                    if entry.msgstr.strip() == "":
                        entry.msgstr = msgstr
                        updated_count += 1
                        print(f"Filled [{row_num}]: {msgid[:60]}... → {msgstr[:60]}...")
            elif key_msgid in msgid_to_entry:
                for entry in msgid_to_entry[key_msgid]:
                    if entry.msgstr.strip() == "":
                        entry.msgstr = msgstr
                        updated_count += 1
                        print(f"Filled [{row_num}]: {msgid[:60]}... → {msgstr[:60]}...")
            else:
                not_found_count += 1
                print(f"Not Found [{row_num}]: msgctxt='{msgctxt}', msgid='{msgid}'")

    po.save(po_file)
    print(f"\nDone. {updated_count} rows filled. {not_found_count} not found.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: {} <po2csv|csv2po|fill2po> <po_file|csv_file|csv_file> <with_duplicates|csv_column|csv_column> <...|...|po_file>'.format(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == 'po2csv':
        # simple .po to .csv with or without duplicates
        # "po2csv" "po_file" "with_duplicates"
        po2csv(sys.argv[2], sys.argv[3] == 'True')
    if sys.argv[1] == 'fill2po':
        # filling empty msgid in your existing .po file
        # "fill2po" "csv_file" "csv_column" "po_file"
        fill2po(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    elif sys.argv[1] == 'csv2po':
        # simple .csv to .po with column index for multi language rows
        # "csv2po" "csv_file" "csv_column"
        csv2po(sys.argv[2], int(sys.argv[3]))

