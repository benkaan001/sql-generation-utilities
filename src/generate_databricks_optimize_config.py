import os
import argparse
import sys
from typing import List, Tuple

# --- Configuration ---
# Generic placeholder for the target configuration table
CONFIG_TABLE_NAME = "config_db.optimization_tasks"

# Template for the INSERT statement
INSERT_TEMPLATE = """
INSERT INTO {config_table} (
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
    '{table_name}',        -- tbl_name
    '{schema_name}',       -- tbl_schema
    'Y',                   -- ignore_partition (defaulted)
    '',                    -- zorder_col (defaulted)
    'daily',               -- run_freq (defaulted)
    current_timestamp(),   -- rec_strt_ts
    '9999-12-31T00:00:00.000+0000', -- rec_end_ts (using UTC offset +0000 for generic example)
    'Y',                   -- rec_flg (defaulted)
    'Y',                   -- run_parallel_flg (defaulted)
    'group1'               -- non_partition_tables / grouping column (defaulted)
);
"""

def parse_databricks_table_list(file_path: str) -> List[Tuple[str, str]]:
    """
    Reads the input file and parses schema.table names for Databricks.

    Args:
        file_path: Path to the input text file.

    Returns:
        A list of tuples, where each tuple is (schema_name, table_name).
        Returns an empty list if the file cannot be read or is empty.
    """
    tables = []
    if not os.path.exists(file_path):
        print(f"Error: Input file not found at {file_path}", file=sys.stderr)
        return []

    try:
        with open(file_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                cleaned_line = line.strip()
                if not cleaned_line:
                    continue # Skip empty lines

                if '.' not in cleaned_line:
                    print(f"Warning: Skipping invalid line {line_num} (missing '.'): {line.strip()}", file=sys.stderr)
                    continue

                parts = cleaned_line.split('.', 1)
                if len(parts) == 2 and parts[0] and parts[1]:
                    schema, table_name = parts
                    tables.append((schema.strip(), table_name.strip()))
                else:
                     print(f"Warning: Skipping invalid line {line_num} (format error): {line.strip()}", file=sys.stderr)

    except IOError as e:
        print(f"Error: Could not read file {file_path}. Details: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"An unexpected error occurred while reading {file_path}: {e}", file=sys.stderr)
        return []

    return tables

def generate_insert_statements(table_list: List[Tuple[str, str]]) -> List[str]:
    """
    Generates a list of SQL INSERT statements based on the table list.

    Args:
        table_list: A list of (schema, table_name) tuples.

    Returns:
        A list of formatted SQL INSERT statements.
    """
    insert_statements = []
    for schema, table in table_list:
        sql = INSERT_TEMPLATE.format(
            config_table=CONFIG_TABLE_NAME,
            schema_name=schema,
            table_name=table
        )
        insert_statements.append(sql.strip()) # Add trimmed SQL statement
    return insert_statements

def write_output_sql(statements: List[str], output_path: str) -> bool:
    """
    Writes the generated SQL statements to the output file.

    Args:
        statements: A list of SQL INSERT statements.
        output_path: Path for the output SQL file.

    Returns:
        True if writing was successful, False otherwise.
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        with open(output_path, 'w') as f:
            f.write("-- Generated Databricks Optimization Configuration SQL\n")
            f.write("-- Generated by: Python Automation Script\n\n")
            for stmt in statements:
                f.write(stmt + "\n\n") # Write each statement followed by a blank line
        return True
    except IOError as e:
        print(f"Error: Could not write output file {output_path}. Details: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while writing {output_path}: {e}", file=sys.stderr)
        return False

def main():
    """
    Main function to parse arguments and generate Databricks optimization config SQL.
    """
    parser = argparse.ArgumentParser(description="Generate Databricks optimization INSERT statements from a list of tables.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input text file listing tables (format: schema.table).")
    parser.add_argument("-o", "--output-sql", required=True, help="Path for the output SQL file containing INSERT statements.")

    args = parser.parse_args()

    # Parse the input list
    table_list = parse_databricks_table_list(args.input)
    if not table_list:
        print("No valid tables found in the input file. Exiting.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(table_list)} tables. Generating INSERT statements...")

    # Generate INSERT statements
    insert_statements = generate_insert_statements(table_list)

    # Write output file
    if write_output_sql(insert_statements, args.output_sql):
        print(f"Successfully created configuration SQL file: {args.output_sql}")
    else:
        print("Failed to create output SQL file.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
