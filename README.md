# SQL Generation Utilities

[![CI Pipeline](https://github.com/benkaan001/sql-generation-utilities/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/benkaan001/sql-generation-utilities/actions/workflows/ci.yml)

This repository contains Python scripts designed to automate the generation of SQL code based on input lists or predefined templates. These tools aim to improve consistency and efficiency in development workflows involving repetitive SQL tasks.

These scripts are adapted from real-world automation tasks, using anonymized sample data.

## Scripts Included

1. **BTEQ Skeleton Generator (`generate_bteq_skeletons.py`)**
2. **Databricks Optimize Config Generator (`generate_databricks_optimize_config.py`)**

## 1. BTEQ Skeleton Generator (`src/generate_bteq_skeletons.py`)

### Purpose

This script automates the creation of skeleton `.sql` files intended for use with Teradata BTEQ (Basic Teradata Query utility). It reads a list of target tables and generates a separate `.sql` file for each, pre-populated with a standard structure including comment blocks for common BTEQ steps (e.g., dropping/creating work tables, collecting statistics, inserting data).

This was originally created to help enforce consistency and ensure developers included necessary steps when creating complex BTEQ deployment scripts.

### Functionality

* Reads a list of `SCHEMA.TABLE` names from an input text file.
* Handles variations in input format (e.g., leading commas, whitespace, comments starting with `#`).
* For each valid table entry, it creates a `.sql` file named after the table (e.g., `TCUSTOMER_MASTER.sql`).
* Populates each file with a predefined BTEQ skeleton template, inserting the specific schema and table name where appropriate.

### Usage

```
python src/generate_bteq_skeletons.py --input <path_to_table_list.txt> --output-dir <path_to_output_directory>

```

**Arguments:**

* `--input` (Required): Path to the input text file containing the list of tables (one `SCHEMA.TABLE` per line).
* `--output-dir` (Required): Path to the directory where the generated `.sql` skeleton files will be saved. The directory will be created if it doesn't exist.

**Example:**

```
python src/generate_bteq_skeletons.py --input sample_data/sample_bteq_table_list.txt --output-dir sample_output/bteq_scripts/

```

This command reads table names from `sample_data/sample_bteq_table_list.txt` and creates corresponding `.sql` files inside the `sample_output/bteq_scripts/` directory.

### Input File Format (`sample_data/sample_bteq_table_list.txt`)

A plain text file with one table per line in `SCHEMA.TABLE` format. Leading commas, whitespace, and lines starting with `#` (or parts of lines after `#`) are ignored.

```
FINANCE_DW.TGL_ACCOUNT_DIM
,FINANCE_DW.TGL_JOURNAL_ENTRY_FACT # With comment
SALES_MART.TCUSTOMER_MASTER
# This is a full line comment
,HR_RAW.TEMPL_PROFILE_CURRENT
ANOTHER_SCHEMA.ANOTHER_TABLE

```

## 2. Databricks Optimize Config Generator (`src/generate_databricks_optimize_config.py`)

### Purpose

This script automates the generation of SQL `INSERT` statements used to configure Databricks table optimization tasks. It reads a list of source tables and creates corresponding `INSERT` statements for a configuration table (e.g., one that schedules or tracks `OPTIMIZE` and `ZORDER` operations).

This was originally used to ensure that all necessary tables created during a deployment were registered for optimization in the production environment.

### Functionality

* Reads a list of `schema.table` names from an input text file.
* Parses the schema and table name from each line.
* Uses a predefined SQL `INSERT` template to generate configuration entries for each table.
* Writes all generated `INSERT` statements into a single output `.sql` file.

### Usage

```
python src/generate_databricks_optimize_config.py --input <path_to_table_list.txt> --output-sql <path_to_output.sql>

```

**Arguments:**

* `--input` (Required): Path to the input text file containing the list of Databricks tables (one `schema.table` per line).
* `--output-sql` (Required): Path for the single output `.sql` file where all generated `INSERT` statements will be saved.

**Example:**

```
python src/generate_databricks_optimize_config.py --input sample_data/sample_databricks_table_list.txt --output-sql sample_output/databricks_optimize_inserts.sql

```

This command reads table names from `sample_data/sample_databricks_table_list.txt` and writes the corresponding `INSERT` statements into `sample_output/databricks_optimize_inserts.sql`.

### Input File Format (`sample_data/sample_databricks_table_list.txt`)

A plain text file with one table per line in `schema.table` format.

```
finance_gl_bronze.t_sap_journal_entries_raw
finance_gl_silver.t_journal_entries_cleaned
sales_orders_bronze.t_crm_orders_raw
...

```

### Output SQL Format (`sample_output/databricks_optimize_inserts.sql`)

The output file contains standard SQL `INSERT` statements based on the template defined in the script, targeting a generic configuration table (`config_db.optimization_tasks` in the sample).

```
-- Generated Databricks Optimization Configuration SQL
-- Generated by: Python Automation Script

INSERT INTO config_db.optimization_tasks (
    tbl_name,
    tbl_schema,
    ignore_partition,
    zorder_col,
    run_freq,
    rec_strt_ts,
    rec_end_ts,
    rec_flg,
    run_parallel_flg,
    non_partition_tables
) VALUES (
    't_sap_journal_entries_raw', -- tbl_name
    'finance_gl_bronze',       -- tbl_schema
    'Y',                   -- ignore_partition (defaulted)
    '',                    -- zorder_col (defaulted)
    'daily',               -- run_freq (defaulted)
    current_timestamp(),   -- rec_strt_ts
    '9999-12-31T00:00:00.000+0000', -- rec_end_ts
    'Y',                   -- rec_flg (defaulted)
    'Y',                   -- run_parallel_flg (defaulted)
    'group1'               -- non_partition_tables / grouping column (defaulted)
);

-- (Additional INSERT statements follow)


```

## General Setup

1. **Clone the repository:**
   ```
   git clone <your-repository-url>
   cd sql-generation-utilities

   ```
2. **Create a virtual environment (recommended):**
   ```
   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # On Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt

   ```

## Testing

Unit tests are included to verify the core logic of the scripts, such as parsing input files and generating the expected SQL statement structures.

To run the tests locally:

1. Ensure you have installed the dependencies (`pip install -r requirements.txt`).
2. Navigate to the root directory of the repository.
3. Run `pytest`:
   ```
   pytest

   ```

   All tests should pass.

A Continuous Integration (CI) workflow is set up using GitHub Actions (`.github/workflows/ci.yml`). This workflow automatically runs the linter (`flake8`) and the unit tests (`pytest`) on pushes and pull requests to the main branch, ensuring code quality and correctness.

## Sample Data

* `sample_data/sample_bteq_table_list.txt`: Sample input for `generate_bteq_skeletons.py`.
* `sample_data/sample_databricks_table_list.txt`: Sample input for `generate_databricks_optimize_config.py`.
* `sample_output/`: Contains example output files generated by running the scripts with the sample inputs (Note: This directory might be gitignored; check `.gitignore`).

## Confidentiality Note

This repository uses anonymized/fictitious data. The structure and logic are representative of a real-world automation task.
