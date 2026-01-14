# main.py

from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

import os


def main():
    try:
        print("=" * 40)
        print("      SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Filter options
        print("\n[3/10] Filter Options Available:")
        temp_valid, _, _ = validate_and_filter(transactions)

        regions = sorted({t['Region'] for t in temp_valid})
        amounts = [t['Quantity'] * t['UnitPrice'] for t in temp_valid]

        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region = min_amount = max_amount = None
        if choice == 'y':
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()
            min_amount = float(min_amt) if min_amt else None
            max_amount = float(max_amt) if max_amt else None

        # 4. Validate
        print("\n[4/10] Validating transactions...")
        valid_txns, invalid_count, summary = validate_and_filter(
            transactions, region, min_amount, max_amount
        )
        print(f"✓ Valid: {len(valid_txns)} | Invalid: {invalid_count}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_txns)
        region_wise_sales(valid_txns)
        top_selling_products(valid_txns)
        customer_analysis(valid_txns)
        daily_sales_trend(valid_txns)
        find_peak_sales_day(valid_txns)
        low_performing_products(valid_txns)
        print("✓ Analysis complete")

        # 6. API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrichment
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched = enrich_sales_data(valid_txns, product_mapping)

        success = sum(1 for t in enriched if t['API_Match'])
        rate = (success / len(enriched)) * 100 if enriched else 0
        print(f"✓ Enriched {success}/{len(enriched)} transactions ({rate:.1f}%)")

        # 8. Save enriched data
        print("\n[8/10] Saving enriched data...")
        os.makedirs("data", exist_ok=True)
        save_enriched_data(enriched, "data/enriched_sales_data.txt")

        # 9. Done
        print("\n[9/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\nERROR:", e)


if __name__ == "__main__":
    main()

