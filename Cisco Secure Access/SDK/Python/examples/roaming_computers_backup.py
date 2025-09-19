from secure_access.api import roaming_computers_api
from secure_access.api_client import ApiClient
from access_token import generate_access_token
from secure_access.configuration import Configuration
import json, argparse, logging, sys, re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Union

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


class RoamingComputersBackup:
    def __init__(self, page_size=100, name=None, status=None, swg_status=None, 
                 last_sync_before=None, last_sync_after=None):
        """
        Initialize the RoamingComputersBackup class
        
        :param page_size: Number of records per page (default: 100, max: 100)
        :param name: Filter by roaming computer name
        :param status: Filter by DNS-layer security status
        :param swg_status: Filter by Internet security (SWG) status
        :param last_sync_before: Filter by last sync before this datetime
        :param last_sync_after: Filter by last sync after this datetime
        """
        self.access_token = generate_access_token()
        self.configuration = Configuration(
            access_token=self.access_token,
        )
        self.api_client = ApiClient(configuration=self.configuration)
        self.roaming_computers_list = []
        self.backup_file_name = "roaming_computers_backup.json"
        self.filtered_backup_file_name = "roaming_computers_filtered.json"
        
        # API parameters
        self.page_size = min(page_size, 100)  # API max limit is 100
        self.name = name
        self.status = status
        self.swg_status = swg_status
        self.last_sync_before = last_sync_before
        self.last_sync_after = last_sync_after

    def list_roaming_computers_page(self, page_number: int) -> List[Dict[str, Any]]:
        """
        Fetch a single page of roaming computers
        
        :param page_number: Page number to fetch (1-based)
        :return: List of roaming computer objects for the page
        """
        api_instance = roaming_computers_api.RoamingComputersApi(api_client=self.api_client)
        
        try:
            logger.debug(f"Fetching page {page_number} with limit {self.page_size}")
            
            response = api_instance.list_roaming_computers_without_preload_content(
                page=page_number,
                limit=self.page_size,
                name=self.name,
                status=self.status,
                swg_status=self.swg_status,
                last_sync_before=self.last_sync_before,
                last_sync_after=self.last_sync_after
            )
            
            if response.status == 200:
                response_data = response.json()
                # Handle both direct list response and paginated response with 'data' field
                if isinstance(response_data, list):
                    return response_data
                elif isinstance(response_data, dict) and 'data' in response_data:
                    return response_data['data']
                elif isinstance(response_data, dict) and 'results' in response_data:
                    return response_data['results']
                else:
                    logger.warning(f"Unexpected response format: {type(response_data)}")
                    return []
            else:
                logger.error(f"Error fetching page {page_number}: HTTP {response.status}")
                return []
                
        except Exception as e:
            logger.error(f"An error occurred while fetching page {page_number}: {e}")
            return []

    def backup_all_roaming_computers(self, apply_simple_filter=False, apply_complex_filter=False,
                                   filter_key=None, filter_value=None, 
                                   filter_expression=None):
        """
        Iterate through all pages and backup all roaming computers
        
        :param apply_simple_filter: Whether to apply simple filter after backup
        :param apply_complex_filter: Whether to apply complex filter after backup
        :param filter_key: Key for simple filter
        :param filter_value: Value for simple filter
        :param filter_expression: Expression for complex filter
        """
        logger.info("Starting backup of all roaming computers...")
        
        page_number = 1
        total_records = 0
        
        while True:
            logger.info(f"Processing page {page_number}...")
            
            page_data = self.list_roaming_computers_page(page_number)
            
            if not page_data:  # Empty array means no more data
                logger.info(f"No more data found at page {page_number}. Stopping iteration.")
                break
            
            self.roaming_computers_list.extend(page_data)
            records_in_page = len(page_data)
            total_records += records_in_page
            
            logger.info(f"Page {page_number}: Retrieved {records_in_page} records")
            
            # If we got fewer records than page_size, we've reached the end
            if records_in_page < self.page_size:
                logger.info("Reached the last page (partial page received)")
                break
                
            page_number += 1
        
        logger.info(f"Backup completed. Total records collected: {total_records}")
        
        if self.roaming_computers_list:
            # Save the original backup first
            self.save_backup_to_file()
            
            # Apply filter if requested
            if apply_simple_filter:
                self.apply_filter_after_backup("simple", filter_key, filter_value, filter_expression)
            elif apply_complex_filter:
                self.apply_filter_after_backup("complex", filter_key, filter_value, filter_expression)
        else:
            logger.warning("No roaming computers found to backup")

    def save_backup_to_file(self, filename=None):
        """
        Save the collected roaming computers data to a JSON file
        
        :param filename: Optional custom filename
        """
        if filename is None:
            filename = self.backup_file_name
            
        try:
            with open(filename, "w") as file:
                json.dump(self.roaming_computers_list, file, indent=4, default=str)
            logger.info(f"Backup saved to {filename} with {len(self.roaming_computers_list)} records")
        except Exception as e:
            logger.error(f"Error saving backup to file: {e}")

    def load_backup_from_file(self, filename=None):
        """
        Load roaming computers data from a JSON file
        
        :param filename: Optional custom filename
        """
        if filename is None:
            filename = self.backup_file_name
            
        try:
            with open(filename, "r") as file:
                self.roaming_computers_list = json.load(file)
            logger.info(f"Loaded {len(self.roaming_computers_list)} records from {filename}")
        except FileNotFoundError:
            logger.error(f"Backup file {filename} not found. Please run backup first.")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error loading backup from file: {e}")
            sys.exit(1)

    def apply_generic_filter(self, filter_key: str, filter_value: str):
        """
        Apply a generic filter to the loaded data based on key-value pair
        
        :param filter_key: The key to filter on (supports dot notation for nested keys)
        :param filter_value: The value to match (string comparison)
        :return: List of filtered records
        """
        if not self.roaming_computers_list:
            logger.warning("No data loaded to filter")
            return []
        
        filtered_data = []
        
        for record in self.roaming_computers_list:
            try:
                # Support dot notation for nested keys (e.g., "status.dns")
                keys = filter_key.split('.')
                value = record
                
                for key in keys:
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = None
                        break
                
                # Convert value to string for comparison
                if value is not None and str(value).lower() == filter_value.lower():
                    filtered_data.append(record)
                    
            except Exception as e:
                logger.debug(f"Error filtering record: {e}")
                continue
        
        logger.info(f"Filter applied: {filter_key}={filter_value}. Found {len(filtered_data)} matching records")
        return filtered_data

    def apply_complex_filter(self, filter_expression: str):
        """
        Apply complex filter with logical operators and time comparisons
        
        Supported operators:
        - Comparison: =, !=, <, >, <=, >=
        - Logical: AND, OR
        - Time: time_diff() function for time differences
        
        Examples:
        - "lastSyncStatus != encrypted"
        - "status = Off AND swgStatus = Off"
        - "time_diff(lastSync) > 30m"
        - "lastSyncStatus != encrypted OR time_diff(lastSync) > 1d"
        
        :param filter_expression: Complex filter expression
        :return: List of filtered records
        """
        if not self.roaming_computers_list:
            logger.warning("No data loaded to filter")
            return []
        
        filtered_data = []
        
        for record in self.roaming_computers_list:
            try:
                if self._evaluate_filter_expression(record, filter_expression):
                    filtered_data.append(record)
            except Exception as e:
                logger.debug(f"Error evaluating filter for record {record.get('originId', 'unknown')}: {e}")
                continue
        
        logger.info(f"Complex filter applied: '{filter_expression}'. Found {len(filtered_data)} matching records")
        return filtered_data

    def _evaluate_filter_expression(self, record: Dict[str, Any], expression: str) -> bool:
        """
        Evaluate a complex filter expression against a single record
        
        :param record: The record to evaluate
        :param expression: The filter expression
        :return: True if record matches the expression
        """
        expression = expression.strip()
        
        if not expression:
            return True
            
        # Handle parentheses by recursively evaluating sub-expressions
        # while '(' in expression:
        #     # Find innermost parentheses
        #     start = expression.rfind('(')
        #     end = expression.find(')', start)
        #     if end == -1:
        #         raise ValueError("Mismatched parentheses in filter expression")
            
        #     sub_expr = expression[start+1:end]
        #     logger.info(f"Evaluating sub-expression: '{sub_expr}'")
        #     sub_result = self._evaluate_filter_expression(record, sub_expr)
        #     expression = expression[:start] + str(sub_result) + expression[end+1:]
        
        # Split by OR first (lower precedence)
        or_parts = self._split_preserving_functions(expression, ' OR ')
        if len(or_parts) > 1:
            logger.debug(f"Evaluating OR expression with parts: {or_parts}")
            result = any(self._evaluate_filter_expression(record, part) for part in or_parts if part.strip())
            logger.debug(f"OR expression result: {result}")
            return result
        
        # Split by AND (higher precedence)
        and_parts = self._split_preserving_functions(expression, ' AND ')
        if len(and_parts) > 1:
            logger.debug(f"Evaluating AND expression with parts: {and_parts}")
            results = []
            for part in and_parts:
                if part.strip():
                    part_result = self._evaluate_filter_expression(record, part)
                    results.append(part_result)
                    logger.debug(f"AND part '{part.strip()}' result: {part_result}")
            result = all(results)
            logger.debug(f"AND expression overall result: {result}")
            return result
        
        # Handle boolean literals
        if expression.lower() == 'true':
            return True
        if expression.lower() == 'false':
            return False
                
        # Handle single comparison
        result = self._evaluate_single_comparison(record, expression)
        logger.debug(f"Single comparison '{expression}' result: {result}")
        return result

    def _split_preserving_functions(self, expression: str, delimiter: str) -> List[str]:
        """
        Split expression by delimiter while preserving function calls
        """
        if delimiter not in expression:
            return [expression]
            
        parts = []
        current_part = ""
        paren_depth = 0
        i = 0
        
        while i < len(expression):
            char = expression[i]
            
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            
            # Check for delimiter only when not inside parentheses
            if paren_depth == 0 and expression[i:i+len(delimiter)] == delimiter:
                if current_part.strip():  # Only add non-empty parts
                    parts.append(current_part.strip())
                current_part = ""
                i += len(delimiter)
                continue
            
            current_part += char
            i += 1
        
        if current_part.strip():  # Only add non-empty parts
            parts.append(current_part.strip())
        
        return parts if parts else [expression]

    def _evaluate_single_comparison(self, record: Dict[str, Any], expression: str) -> bool:
        """
        Evaluate a single comparison expression
        
        :param record: The record to evaluate
        :param expression: Single comparison expression (e.g., "status = Off", "time_diff(lastSync) > 30m")
        :return: True if comparison is true
        """
        expression = expression.strip()
        logger.debug(f"Evaluating expression: '{expression}'")
        
        # Check if it's just a field name without comparison (treat as existence check)
        if not any(op in expression for op in ['!=', '<=', '>=', '=', '<', '>', 'time_diff(']):
            logger.debug(f"Expression '{expression}' appears to be a field name without comparison operator")
            # Treat as existence/truthiness check
            value = self._get_nested_value(record, expression)
            return value is not None and value != "" and value != 0 and value != False
        
        # Handle time_diff function
        time_diff_pattern = r'time_diff\(([^)]+)\)\s*([<>=!]+)\s*(.+)'
        time_match = re.match(time_diff_pattern, expression)
        if time_match:
            field_name = time_match.group(1).strip()
            operator = time_match.group(2).strip()
            time_value = time_match.group(3).strip()
            
            logger.debug(f"Time comparison: field='{field_name}', operator='{operator}', value='{time_value}'")
            return self._evaluate_time_comparison(record, field_name, operator, time_value)
        
        # Handle regular comparisons - check != before = to avoid partial matches
        for op in ['!=', '<=', '>=', '<', '>', '=']:
            if op in expression:
                parts = expression.split(op, 1)
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    
                    # Skip if this creates empty parts
                    if not left or not right:
                        continue
                        
                    # Get value from record
                    record_value = self._get_nested_value(record, left)
                    
                    # Remove quotes from right side if present
                    if (right.startswith('"') and right.endswith('"')) or (right.startswith("'") and right.endswith("'")):
                        right = right[1:-1]
                    
                    logger.debug(f"Field comparison: field='{left}', record_value='{record_value}', operator='{op}', right='{right}'")
                    result = self._compare_values(record_value, op, right)
                    logger.debug(f"Comparison result: {result}")
                    return result
        
        raise ValueError(f"Invalid comparison expression: {expression}")

    def _evaluate_time_comparison(self, record: Dict[str, Any], field_name: str, 
                                operator: str, time_value: str) -> bool:
        """
        Evaluate time-based comparison
        
        :param record: The record to evaluate
        :param field_name: Field name containing the timestamp
        :param operator: Comparison operator
        :param time_value: Time value (e.g., "30m", "1d", "2h")
        :return: True if comparison is true
        """
        timestamp_str = self._get_nested_value(record, field_name)
        logger.debug(f"Time comparison - field_name: '{field_name}', timestamp_str: '{timestamp_str}', operator: '{operator}', time_value: '{time_value}'")
        
        if not timestamp_str:
            logger.debug(f"No timestamp found for field {field_name}")
            return False
        
        try:
            # Parse the timestamp
            timestamp = self._parse_iso_timestamp(timestamp_str)
            current_time = datetime.utcnow()
            
            # Calculate time difference in minutes
            time_diff_minutes = (current_time - timestamp).total_seconds() / 60
            
            # Parse the time value
            target_minutes = self._parse_time_value(time_value)
            
            logger.debug(f"Time comparison - time_diff_minutes: {time_diff_minutes:.2f}, target_minutes: {target_minutes}, operator: '{operator}'")
            
            # Perform comparison
            result = self._compare_values(time_diff_minutes, operator, target_minutes)
            logger.debug(f"Time comparison result: {result}")
            return result
            
        except Exception as e:
            logger.debug(f"Error in time comparison for field {field_name}: {e}")
            return False

    def _parse_iso_timestamp(self, timestamp_str: str) -> datetime:
        """Parse ISO timestamp string"""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"Unable to parse timestamp: {timestamp_str}")

    def _parse_time_value(self, time_value: str) -> float:
        """
        Parse time value string into minutes
        
        Supported formats: 30m, 1h, 2d, 1w
        """
        time_value = time_value.strip().lower()
        
        if time_value.endswith('m'):
            return float(time_value[:-1])
        elif time_value.endswith('h'):
            return float(time_value[:-1]) * 60
        elif time_value.endswith('d'):
            return float(time_value[:-1]) * 60 * 24
        elif time_value.endswith('w'):
            return float(time_value[:-1]) * 60 * 24 * 7
        else:
            # Assume minutes if no unit specified
            return float(time_value)

    def _get_nested_value(self, record: Dict[str, Any], key_path: str) -> Any:
        """
        Get value from nested dictionary using dot notation
        
        :param record: The record dictionary
        :param key_path: Dot-separated key path (e.g., "config.status")
        :return: The value or None if not found
        """
        keys = key_path.split('.')
        value = record
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        
        return value

    def _compare_values(self, left: Any, operator: str, right: Any) -> bool:
        """
        Compare two values using the specified operator
        
        :param left: Left value
        :param operator: Comparison operator
        :param right: Right value
        :return: Comparison result
        """
        if left is None:
            logger.debug(f"Left value is None, returning False")
            return False
        
        logger.debug(f"Comparing: '{left}' ({type(left).__name__}) {operator} '{right}' ({type(right).__name__})")
        
        # Convert values for comparison
        try:
            # Try numeric comparison first
            left_num = float(left)
            right_num = float(right)
            
            logger.debug(f"Using numeric comparison: {left_num} {operator} {right_num}")
            
            if operator == '=':
                return left_num == right_num
            elif operator == '!=':
                return left_num != right_num
            elif operator == '<':
                return left_num < right_num
            elif operator == '>':
                return left_num > right_num
            elif operator == '<=':
                return left_num <= right_num
            elif operator == '>=':
                return left_num >= right_num
                
        except (ValueError, TypeError):
            # Fall back to string comparison
            left_str = str(left).lower()
            right_str = str(right).lower()
            
            logger.debug(f"Using string comparison: '{left_str}' {operator} '{right_str}'")
            
            if operator == '=':
                return left_str == right_str
            elif operator == '!=':
                return left_str != right_str
            elif operator == '<':
                return left_str < right_str
            elif operator == '>':
                return left_str > right_str
            elif operator == '<=':
                return left_str <= right_str
            elif operator == '>=':
                return left_str >= right_str
        
        logger.debug(f"No matching operator found, returning False")
        return False

    def save_filtered_data(self, filtered_data: List[Dict[str, Any]], 
                          filter_description: str):
        """
        Save filtered data to a separate JSON file
        
        :param filtered_data: The filtered data to save
        :param filter_description: Description of the filter applied
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a safe filename from filter description
        safe_description = re.sub(r'[^\w\-_\.]', '_', filter_description)[:50]
        filename = f"roaming_computers_filtered_{safe_description}_{timestamp}.json"
        
        try:
            with open(filename, "w") as file:
                json.dump(filtered_data, file, indent=4, default=str)
            logger.info(f"Filtered data saved to {filename} with {len(filtered_data)} records")
        except Exception as e:
            logger.error(f"Error saving filtered data to file: {e}")

    def list_available_filter_keys(self):
        """
        Analyze the loaded data and show available filter keys
        """
        if not self.roaming_computers_list:
            logger.warning("No data loaded to analyze")
            return
        
        # Get all unique keys from the first few records
        all_keys = set()
        
        def extract_keys(obj, prefix=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    full_key = f"{prefix}.{key}" if prefix else key
                    all_keys.add(full_key)
                    if isinstance(value, dict):
                        extract_keys(value, full_key)
                    elif isinstance(value, list) and value and isinstance(value[0], dict):
                        extract_keys(value[0], f"{full_key}[0]")
        
        # Analyze first 5 records to get a good sample of keys
        sample_size = min(5, len(self.roaming_computers_list))
        for record in self.roaming_computers_list[:sample_size]:
            extract_keys(record)
        
        sorted_keys = sorted(all_keys)
        logger.info(f"Available filter keys ({len(sorted_keys)} found):")
        for key in sorted_keys:
            print(f"  - {key}")

    def apply_filter_after_backup(self, filter_type, filter_key=None, filter_value=None, filter_expression=None):
        """
        Apply filter to the already collected roaming computers data
        
        :param filter_type: Type of filter ("simple" or "complex")
        :param filter_key: Key for simple filter
        :param filter_value: Value for simple filter  
        :param filter_expression: Expression for complex filter
        """
        logger.info(f"Applying {filter_type} filter to collected data...")
        
        if filter_type == "simple":
            if not filter_key or not filter_value:
                logger.error("Simple filter requires both filter_key and filter_value")
                return
            
            filtered_data = self.apply_generic_filter(filter_key, filter_value)
            if filtered_data:
                filter_description = f"{filter_key}={filter_value}"
                self.save_filtered_data(filtered_data, filter_description)
                logger.info(f"Simple filter applied and saved. Found {len(filtered_data)} matching records")
            else:
                logger.warning("No records matched the simple filter criteria")
                
        elif filter_type == "complex":
            if not filter_expression:
                logger.error("Complex filter requires filter_expression")
                return
                
            try:
                filtered_data = self.apply_complex_filter(filter_expression)
                if filtered_data:
                    self.save_filtered_data(filtered_data, filter_expression)
                    logger.info(f"Complex filter applied and saved. Found {len(filtered_data)} matching records")
                else:
                    logger.warning("No records matched the complex filter criteria")
            except Exception as e:
                logger.error(f"Error applying complex filter: {e}")
        else:
            logger.error(f"Unknown filter type: {filter_type}")


def parse_datetime(date_string: str) -> datetime:
    """
    Parse datetime string in various formats
    
    :param date_string: Date string to parse
    :return: datetime object
    """
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_string}")


def main():
    parser = argparse.ArgumentParser(
        description="Utility to backup roaming computers and apply filters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Backup all roaming computers
  python roaming_computers_backup.py --operation backup

  # Backup with specific page size
  python roaming_computers_backup.py --operation backup --page-size 50

  # Backup with API filters
  python roaming_computers_backup.py --operation backup --name "MyComputer" --status active

  # Backup and apply simple filter immediately after
  python roaming_computers_backup.py --operation backup --apply-simple-filter --filter-key status --filter-value Off

  # Backup and apply complex filter immediately after
  python roaming_computers_backup.py --operation backup --apply-complex-filter --filter-expression "lastSyncStatus != encrypted AND time_diff(lastSync) > 30m"

  # Apply simple filter to existing backup
  python roaming_computers_backup.py --operation filter --filter-key status --filter-value active

  # Apply complex filter to existing backup
  python roaming_computers_backup.py --operation complex-filter --filter-expression "lastSyncStatus != encrypted"
  python roaming_computers_backup.py --operation complex-filter --filter-expression "status = Off AND swgStatus = Off"
  python roaming_computers_backup.py --operation complex-filter --filter-expression "time_diff(lastSync) > 30m"
  python roaming_computers_backup.py --operation complex-filter --filter-expression "lastSyncStatus != encrypted OR time_diff(lastSync) > 1d"

  # List available filter keys
  python roaming_computers_backup.py --operation analyze
        """
    )
    
    # Main operation
    parser.add_argument(
        '--operation',
        help="Operation to perform",
        required=True,
        choices=["backup", "filter", "complex-filter", "analyze"],
        type=str
    )
    
    # Backup parameters
    parser.add_argument(
        '--page-size',
        help="Number of records per page (max: 100)",
        required=False,
        type=int,
        default=100
    )
    
    parser.add_argument(
        '--name',
        help="Filter by roaming computer name",
        required=False,
        type=str
    )
    
    parser.add_argument(
        '--status',
        help="Filter by DNS-layer security status",
        required=False,
        type=str
    )
    
    parser.add_argument(
        '--swg-status',
        help="Filter by Internet security (SWG) status",
        required=False,
        type=str
    )
    
    parser.add_argument(
        '--last-sync-before',
        help="Filter by last sync before this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
        required=False,
        type=str
    )
    
    parser.add_argument(
        '--last-sync-after',
        help="Filter by last sync after this date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)",
        required=False,
        type=str
    )
    
    # Simple filter parameters
    parser.add_argument(
        '--filter-key',
        help="Key to filter on (supports dot notation for nested keys)",
        required=False,
        type=str
    )
    
    parser.add_argument(
        '--filter-value',
        help="Value to match for filtering",
        required=False,
        type=str
    )
    
    # Complex filter parameters
    parser.add_argument(
        '--filter-expression',
        help="Complex filter expression with logical operators and time functions",
        required=False,
        type=str
    )
    
    # File parameters
    parser.add_argument(
        '--backup-file',
        help="Custom backup file name",
        required=False,
        type=str
    )
    
    # Filter after backup parameters
    parser.add_argument(
        '--apply-simple-filter',
        help="Apply simple filter immediately after backup",
        action='store_true'
    )
    
    parser.add_argument(
        '--apply-complex-filter',
        help="Apply complex filter immediately after backup",
        action='store_true'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.operation == "filter" and (not args.filter_key or not args.filter_value):
        parser.error("--filter-key and --filter-value are required for filter operation")
    
    if args.operation == "complex-filter" and not args.filter_expression:
        parser.error("--filter-expression is required for complex-filter operation")
    
    # Validate filter after backup arguments
    if args.apply_simple_filter and (not args.filter_key or not args.filter_value):
        parser.error("--filter-key and --filter-value are required when using --apply-simple-filter")
    
    if args.apply_complex_filter and not args.filter_expression:
        parser.error("--filter-expression is required when using --apply-complex-filter")
    
    if args.apply_simple_filter and args.apply_complex_filter:
        parser.error("Cannot apply both simple and complex filters simultaneously. Choose one.")
    
    # Parse datetime arguments
    last_sync_before = None
    last_sync_after = None
    
    if args.last_sync_before:
        try:
            last_sync_before = parse_datetime(args.last_sync_before)
        except ValueError as e:
            logger.error(f"Invalid last-sync-before format: {e}")
            sys.exit(1)
    
    if args.last_sync_after:
        try:
            last_sync_after = parse_datetime(args.last_sync_after)
        except ValueError as e:
            logger.error(f"Invalid last-sync-after format: {e}")
            sys.exit(1)
    
    logger.info("Starting roaming computers backup utility...")
    
    # Initialize the backup class
    backup_tool = RoamingComputersBackup(
        page_size=args.page_size,
        name=args.name,
        status=args.status,
        swg_status=args.swg_status,
        last_sync_before=last_sync_before,
        last_sync_after=last_sync_after
    )
    
    # Set custom backup file if provided
    if args.backup_file:
        backup_tool.backup_file_name = args.backup_file
    
    # Execute the requested operation
    if args.operation == "backup":
        # Determine if filters should be applied immediately after backup
        apply_simple = args.apply_simple_filter
        apply_complex = args.apply_complex_filter
        filter_key = args.filter_key if apply_simple else None
        filter_value = args.filter_value if apply_simple else None
        filter_expression = args.filter_expression if apply_complex else None
        
        backup_tool.backup_all_roaming_computers(
            apply_simple_filter=apply_simple,
            apply_complex_filter=apply_complex,
            filter_key=filter_key,
            filter_value=filter_value,
            filter_expression=filter_expression
        )
        logger.info("Backup operation completed successfully")
        
    elif args.operation == "filter":
        logger.info("Loading existing backup for filtering...")
        backup_tool.load_backup_from_file()
        
        filtered_data = backup_tool.apply_generic_filter(args.filter_key, args.filter_value)
        
        if filtered_data:
            filter_description = f"{args.filter_key}={args.filter_value}"
            backup_tool.save_filtered_data(filtered_data, filter_description)
        else:
            logger.warning("No records matched the filter criteria")
            
    elif args.operation == "complex-filter":
        logger.info("Loading existing backup for complex filtering...")
        backup_tool.load_backup_from_file()
        
        try:
            logger.debug(f"Applying complex filter expression: {args.filter_expression}")
            filtered_data = backup_tool.apply_complex_filter(args.filter_expression)
            
            if filtered_data:
                backup_tool.save_filtered_data(filtered_data, args.filter_expression)
            else:
                logger.warning("No records matched the complex filter criteria")
        except Exception as e:
            logger.error(f"Error applying complex filter: {e}")
            sys.exit(1)
            
    elif args.operation == "analyze":
        logger.info("Loading existing backup for analysis...")
        backup_tool.load_backup_from_file()
        backup_tool.list_available_filter_keys()
    
    logger.info("Operation completed successfully")


if __name__ == "__main__":
    main()
