# sales-analytics-system
## Project Overview
The **Sales Analytics System** is a Python based data analytics application designed to process, clean, analyze, and enrich sales transaction data.  
The system handles real world data quality issues, integrates with an external product API, performs analytical computations and generates structured reports for business insights.

This project demonstrates core Python programming concepts including file handling, data validation, modular design, API integration, and report generation.

---

## Project Structure
sales-analytics-system/
├── main.py
├── utils/
│ ├── init.py
│ ├── file_handler.py
│ ├── data_processor.py
│ └── api_handler.py
├── data/
│ ├── sales_data.txt
│ └── enriched_sales_data.txt
├── output/
│ └── sales_report.txt
├── requirements.txt
└── README.md
---

## Features

### 1. Data File Handling & Cleaning
- Reads pipe delimited sales data
- Handles encoding issues (utf-8, latin-1, cp1252)
- Cleans formatting issues (commas in numbers, product names)
- Filters invalid records based on validation rules

### 2. Data Analysis
- Total revenue calculation
- Region wise sales analysis
- Top selling products
- Customer purchase analysis
- Daily sales trend analysis
- Peak sales day identification
- Low performing product identification

### 3. API Integration
- Fetches product data from the DummyJSON API
- Maps API product details to sales data
- Enriches transactions with category, brand and rating
- Handles unmatched products gracefully

### 4. Output Generation
- Saves enriched sales data to a file
- Generates a formatted sales analytics report

---

## How to Run the Project

### Prerequisites
- Python 3.10 or higher
- Internet connection (for API calls)

### Step 1: Install Dependencies

pip install -r requirements.txt

### Step 2: Run the Application
From the project root directory:
py main.py

### Step 3: Follow Console Prompts
View available regions and transaction amount range
Choose whether to apply filters
Let the system complete processing automatically

Output Files
After successful execution, the following files are generated:
Enriched Sales Data
data/enriched_sales_data.txt

Sales Analytics Report
output/sales_report.txt

Notes
API enrichment may result in zero matches if product IDs do not overlap with API product IDs. This scenario is handled gracefully without errors.
The project follows modular design principles for better readability and maintainability.

Technologies Used
Python
Requests library
File I/O
REST API integration

Author
Sai Sneha Matta
Python Programming Assignment – Sales Analytics System
