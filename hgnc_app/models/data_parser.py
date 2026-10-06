
import csv
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)


def read_file(filepath: str) -> List[Dict[str, Any]]:
    """
    Read the HGNC TSV dataset and extract specific fields into a structured list of dictionaries.

    Parameters
    ----------
    filepath : str
        Path to the input TSV file.

    Returns
    -------
    list of dict
        Parsed records, one per line in the file.

    Raises
    ------
    IOError
        If the file cannot be opened or read.
    ValueError
        If parsing fails for all lines.
    """
    logger.info(f"Reading data file: {filepath}")

    output_list = []

    try:
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for i, entry in enumerate(reader):
                try:
                    parsed = parse_line(entry)
                    if parsed:
                        output_list.append(parsed)
                except Exception:
                    logger.warning(f"Skipping malformed line {i+2}")

        if not output_list:
            raise ValueError("No valid data parsed from file")

        logger.info(f"Successfully loaded {len(output_list)} records")
        return output_list

    except Exception:
        logger.exception("Error reading input file")
        raise


def parse_line(row: Dict[str, str]) -> Dict[str, Any]:
    """
    Parse a single row dictionary from the HGNC dataset.
    Returns None if critical data (like symbol or hgnc_id) is missing.

    Parameters
    ----------
    row : dict
        A dictionary representing a row from the input file, typically from csv.DictReader.

    Returns
    -------
    dict or None
        Parsed data as a dictionary, or None if the line is empty or invalid.

    Raises
    ------
    ValueError
        If the line structure is invalid.
    """
    if not row.get("hgnc_id") or not row.get("symbol"):
        return None

    return {
        "hgnc_id": row.get("hgnc_id", ""),
        "gene_symbol": row.get("symbol", ""),
        "gene_name": row.get("name", ""),
        "prev_symbol": row.get("prev_symbol", ""),
        "prev_name": row.get("prev_name", ""),
        "alias_symbol": row.get("alias_symbol", ""),
        "mane_select": row.get("mane_select", "")
    }


def find_gene(query: str, data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Find a gene query (HGNC-approved gene symbol or an HGNC ID) within a parsed hgnc dataset.

    Parameters
    ----------
    query : str
        The search term (e.g., "BRCA2" or "HGNC:1101").
    data : list of dict
        Parsed dataset returned from `read_file`.

    Returns
    -------
    dict or None
        Matching gene record if found, otherwise None.

    Notes
    -----
    Search is case-insensitive and matches exact gene symbols or HGNC IDs.
    """
    clean_query = query.strip().upper()
    logger.debug(f"Searching for gene: {clean_query}")

    for entry in data:
        symbol = str(entry.get("gene_symbol", "")).strip().upper()
        hgnc_id = str(entry.get("hgnc_id", "")).strip().upper()
        if symbol == clean_query or hgnc_id == clean_query:
            logger.info(f"Match found for gene: {clean_query}")
            return entry

    logger.info(f"No match found for gene: {clean_query}")
    return None