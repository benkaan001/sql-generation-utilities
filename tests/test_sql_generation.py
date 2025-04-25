import pytest
import os
import sys
from typing import List, Tuple

# Ensure the script modules can be imported
script_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, os.path.abspath(script_dir))

# Import functions from the scripts under test
try:
    # Use the updated function name if you renamed it in the source file
    from generate_bteq_skeletons import parse_table_list as parse_bteq_list, BTEQ_SKELETON
    from generate_databricks_optimize_config import (
        parse_databricks_table_list,
        generate_insert_statements,
        CONFIG_TABLE_NAME
    )
except ImportError as e:
    pytest.skip(f"Skipping tests due to import error: {e}", allow_module_level=True)

# --- Fixtures for sample input data ---

@pytest.fixture
def sample_bteq_input_content():
    """Provides sample content for the BTEQ table list file."""
    # Includes comments and various invalid lines
    return """
    FINANCE_DW.TGL_ACCOUNT_DIM
    ,FINANCE_DW.TGL_JOURNAL_ENTRY_FACT # With comment
    SALES_MART.TCUSTOMER_MASTER

    # This is a full line comment
    INVALID_LINE_NO_DOT
    ,HR_RAW.TEMPL_PROFILE_CURRENT
    .EMPTY_SCHEMA.TABLE # Invalid: Starts with dot, not just schema
    SCHEMA.EMPTY_TABLE. # Invalid: Ends with dot
    ANOTHER_SCHEMA.ANOTHER_TABLE # Valid line after invalid ones
    """

@pytest.fixture
def sample_bteq_input_file(tmp_path, sample_bteq_input_content):
    """Creates a temporary BTEQ input file."""
    file_path = tmp_path / "bteq_list.txt"
    file_path.write_text(sample_bteq_input_content)
    return file_path

@pytest.fixture
def sample_databricks_input_content():
    """Provides sample content for the Databricks table list file."""
    return """
    finance_gl_bronze.t_sap_journal_entries_raw
    sales_orders_silver.t_order_header_cleaned
    marketing_campaign_gold.t_campaign_roi_analysis

    invalid_line_no_dot
    inventory_mgmt_bronze.t_wms_stock_levels_raw
    """

@pytest.fixture
def sample_databricks_input_file(tmp_path, sample_databricks_input_content):
    """Creates a temporary Databricks input file."""
    file_path = tmp_path / "databricks_list.txt"
    file_path.write_text(sample_databricks_input_content)
    return file_path

# --- Tests for generate_bteq_skeletons.py ---

def test_bteq_parse_table_list_valid(sample_bteq_input_file):
    """Verify parsing of valid lines, ignoring comments and invalid lines."""
    # Updated expected list based on refined parsing logic
    expected = [
        ("FINANCE_DW", "TGL_ACCOUNT_DIM"),
        ("FINANCE_DW", "TGL_JOURNAL_ENTRY_FACT"), # Comment is stripped
        ("SALES_MART", "TCUSTOMER_MASTER"),
        ("HR_RAW", "TEMPL_PROFILE_CURRENT"),
        ("ANOTHER_SCHEMA", "ANOTHER_TABLE"), # Added valid line from fixture
    ]
    actual = parse_bteq_list(str(sample_bteq_input_file))
    assert actual == expected

def test_bteq_parse_table_list_file_not_found():
    """Test parsing non-existent file for BTEQ list."""
    assert parse_bteq_list("non_existent_bteq.txt") == []

def test_bteq_skeleton_constant():
    """Basic check on the BTEQ_SKELETON constant."""
    assert isinstance(BTEQ_SKELETON, str)
    assert len(BTEQ_SKELETON) > 100 # Ensure it's not empty
    assert "{schema}" in BTEQ_SKELETON
    assert "{table_name}" in BTEQ_SKELETON

# --- Tests for generate_databricks_optimize_config.py ---

def test_databricks_parse_table_list_valid(sample_databricks_input_file):
    """Verify parsing of valid Databricks table list lines."""
    expected = [
        ("finance_gl_bronze", "t_sap_journal_entries_raw"),
        ("sales_orders_silver", "t_order_header_cleaned"),
        ("marketing_campaign_gold", "t_campaign_roi_analysis"),
        ("inventory_mgmt_bronze", "t_wms_stock_levels_raw"),
    ]
    # Note: Invalid lines are skipped
    actual = parse_databricks_table_list(str(sample_databricks_input_file))
    assert actual == expected

def test_databricks_parse_table_list_file_not_found():
    """Test parsing non-existent file for Databricks list."""
    assert parse_databricks_table_list("non_existent_dbx.txt") == []

def test_generate_insert_statements():
    """Verify the generated INSERT statements match the template."""
    test_tables: List[Tuple[str, str]] = [
        ("schema1", "table_a"),
        ("schema2", "table_b"),
    ]
    statements = generate_insert_statements(test_tables)

    assert len(statements) == 2
    # Check essential parts of the first statement
    assert f"INSERT INTO {CONFIG_TABLE_NAME}" in statements[0]
    assert "'table_a'" in statements[0] # Check table name insertion
    assert "'schema1'" in statements[0] # Check schema name insertion
    assert "VALUES (" in statements[0]
    assert "'daily'" in statements[0] # Check a default value
    assert ");" in statements[0]

    # Check essential parts of the second statement
    assert f"INSERT INTO {CONFIG_TABLE_NAME}" in statements[1]
    assert "'table_b'" in statements[1]
    assert "'schema2'" in statements[1]
    assert ");" in statements[1]

def test_generate_insert_statements_empty_list():
    """Test generating statements with an empty input list."""
    statements = generate_insert_statements([])
    assert statements == []

