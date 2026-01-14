# utils/data_processor.py

def calculate_total_revenue(transactions):
    return sum(t['Quantity'] * t['UnitPrice'] for t in transactions)


def region_wise_sales(transactions):
    region_stats = {}
    total_revenue = calculate_total_revenue(transactions)

    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1

    for region in region_stats:
        region_stats[region]['percentage'] = round(
            (region_stats[region]['total_sales'] / total_revenue) * 100, 2
        )

    return dict(
        sorted(
            region_stats.items(),
            key=lambda x: x[1]['total_sales'],
            reverse=True
        )
    )


def top_selling_products(transactions, n=5):
    product_stats = {}

    for t in transactions:
        product = t['ProductName']
        revenue = t['Quantity'] * t['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_stats[product]['quantity'] += t['Quantity']
        product_stats[product]['revenue'] += revenue

    products = [
        (p, d['quantity'], d['revenue'])
        for p, d in product_stats.items()
    ]

    products.sort(key=lambda x: x[1], reverse=True)
    return products[:n]


def customer_analysis(transactions):
    customers = {}

    for t in transactions:
        cid = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']

        if cid not in customers:
            customers[cid] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products': set()
            }

        customers[cid]['total_spent'] += amount
        customers[cid]['purchase_count'] += 1
        customers[cid]['products'].add(t['ProductName'])

    result = {}
    for cid, data in customers.items():
        result[cid] = {
            'total_spent': data['total_spent'],
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(
                data['total_spent'] / data['purchase_count'], 2
            ),
            'products_bought': list(data['products'])
        }

    return dict(
        sorted(
            result.items(),
            key=lambda x: x[1]['total_spent'],
            reverse=True
        )
    )


def daily_sales_trend(transactions):
    daily = {}

    for t in transactions:
        date = t['Date']

        if date not in daily:
            daily[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers': set()
            }

        daily[date]['revenue'] += t['Quantity'] * t['UnitPrice']
        daily[date]['transaction_count'] += 1
        daily[date]['customers'].add(t['CustomerID'])

    return {
        d: {
            'revenue': v['revenue'],
            'transaction_count': v['transaction_count'],
            'unique_customers': len(v['customers'])
        }
        for d, v in sorted(daily.items())
    }


def find_peak_sales_day(transactions):
    daily = daily_sales_trend(transactions)
    peak = max(daily.items(), key=lambda x: x[1]['revenue'])
    return peak[0], peak[1]['revenue'], peak[1]['transaction_count']


def low_performing_products(transactions, threshold=10):
    product_stats = {}

    for t in transactions:
        product = t['ProductName']

        if product not in product_stats:
            product_stats[product] = {
                'quantity': 0,
                'revenue': 0.0
            }

        product_stats[product]['quantity'] += t['Quantity']
        product_stats[product]['revenue'] += t['Quantity'] * t['UnitPrice']

    low_products = [
        (p, d['quantity'], d['revenue'])
        for p, d in product_stats.items()
        if d['quantity'] < threshold
    ]

    return sorted(low_products, key=lambda x: x[1])
