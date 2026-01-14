def read_sales_data(filename):
    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if not line or line.startswith("TransactionID"):
                    continue
                cleaned_lines.append(line)

            return cleaned_lines

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unable to read file with supported encodings.")
    return []


def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts
        pname = pname.replace(",", "")

        try:
            qty = int(qty.replace(",", ""))
            price = float(price.replace(",", ""))
        except ValueError:
            continue

        transactions.append({
            'TransactionID': tid,
            'Date': date,
            'ProductID': pid,
            'ProductName': pname,
            'Quantity': qty,
            'UnitPrice': price,
            'CustomerID': cid,
            'Region': region
        })

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid = 0

    for t in transactions:
        if (
            t['Quantity'] <= 0 or
            t['UnitPrice'] <= 0 or
            not t['TransactionID'].startswith("T") or
            not t['ProductID'].startswith("P") or
            not t['CustomerID'].startswith("C") or
            not t['Region']
        ):
            invalid += 1
            continue
        valid.append(t)

    filtered = []
    for t in valid:
        amount = t['Quantity'] * t['UnitPrice']
        if region and t['Region'] != region:
            continue
        if min_amount and amount < min_amount:
            continue
        if max_amount and amount > max_amount:
            continue
        filtered.append(t)

    summary = {
        'total_input': len(transactions),
        'invalid': invalid,
        'final_count': len(filtered)
    }

    return filtered, invalid, summary
