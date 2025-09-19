from secure_access.api import destination_lists_api, destinations_api
from secure_access.api_client import ApiClient
from access_token import generate_access_token
from secure_access.configuration import Configuration
from secure_access.models import (
    DestinationListCreate,
    DestinationListPatch,
    DestinationCreateObject,
)
import json, argparse, logging, sys, csv
from datetime import datetime, timedelta

# Constants for filter help text
FILTER_HELP_TEXT = (
    "Supported filters: created_after=7d, created_before=2024-01-01, "
    "modified_after=1h, access=allow (or access=allow,block,none for multiple), "
    "name_contains=test (or name_contains=test,prod for multiple), "
    "global_only=true, exclude_deleted=true, "
    "min_destinations=5, max_destinations=100"
)

# Constants for destination filter help text
DESTINATION_FILTER_HELP_TEXT = (
    "Supported filters: created_after=7d, created_before=2024-01-01, "
    "type=domain (or type=domain,url,ipv4 for multiple), "
    "destination_contains=youtube (or destination_contains=youtube,google for multiple), "
    "has_comment=true/false"
)


# Common filter examples for reuse
def get_common_filter_examples(operation="list"):
    """Generate common filter examples for list/backup operations"""
    return f"""  # {operation.title()} destination lists created in last 7 days
  python destination_list_manager.py destination-lists {operation} --filter created_after=7d
  
  # Filter by access type and minimum destination count
  python destination_list_manager.py destination-lists {operation} --filter access=allow --filter min_destinations=10
  
  # Filter by multiple access types (comma-separated)
  python destination_list_manager.py destination-lists {operation} --filter access=allow,block,none
  
  # Filter by name containing text and exclude deleted lists
  python destination_list_manager.py destination-lists {operation} --filter name_contains=security --filter exclude_deleted=true
  
  # Filter by multiple name patterns
  python destination_list_manager.py destination-lists {operation} --filter name_contains=test,prod,security
  
  # Filter by multiple time-based criteria
  python destination_list_manager.py destination-lists {operation} --filter created_after=30d --filter modified_after=7d"""


def get_list_specific_examples():
    """Get examples specific to list operation"""
    return """  # List all destination lists with auto-pagination
  python destination_list_manager.py destination-lists list
  
  # List specific page with manual pagination
  python destination_list_manager.py destination-lists list --page 1 --limit 50
  
  # List specific destination lists by IDs
  python destination_list_manager.py destination-lists list --ids 123 456 789"""


def get_backup_specific_examples():
    """Get examples specific to backup operation"""
    return """  # Backup all destination lists
  python destination_list_manager.py destination-lists backup
  
  # Backup specific lists by IDs
  python destination_list_manager.py destination-lists backup --ids 123 456
  
  # Backup lists with destinations included
  python destination_list_manager.py destination-lists backup --filter created_after=30d --include-destinations
  
  # Backup to custom file
  python destination_list_manager.py destination-lists backup --filter name_contains=prod --file prod_backup.json"""


def get_main_command_examples():
    """Get examples for main destination-lists command"""
    return """  # List all destination lists
  python destination_list_manager.py destination-lists list
  
  # Filter destination lists by access type
  python destination_list_manager.py destination-lists list --filter access=allow,block
  
  # Create destination list with CSV import
  python destination_list_manager.py destination-lists create --name "Corporate Domains" --access allow --csv-file destinations.csv
  
  # Update destination list name
  python destination_list_manager.py destination-lists update --id 123 --name "Updated List Name"
  
  # Delete destination list
  python destination_list_manager.py destination-lists delete --id 123
  
  # Backup all destination lists
  python destination_list_manager.py destination-lists backup
  
  # Backup with filters
  python destination_list_manager.py destination-lists backup --filter access=allow --filter created_after=30d"""


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
logger.addHandler(handler)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)


def parse_filters(filter_strings):
    """Parse filter key=value pairs into a dictionary"""
    filters = {}

    if not filter_strings:
        return filters

    for filter_str in filter_strings:
        if "=" not in filter_str:
            logger.warning(
                f"Invalid filter format '{filter_str}'. Expected key=value format."
            )
            continue

        key, value = filter_str.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Parse different value types
        if key in [
            "created_after",
            "created_before",
            "modified_after",
            "modified_before",
        ]:
            # Time-based filters - parse relative time (e.g., "7d", "1h", "30m") or ISO date
            try:
                if value.endswith("d"):
                    days = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(days=days)
                elif value.endswith("h"):
                    hours = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(hours=hours)
                elif value.endswith("m"):
                    minutes = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(minutes=minutes)
                else:
                    # Try to parse as ISO date
                    filters[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Invalid time format for {key}: {value}. Use format like '7d', '2h', '30m' or ISO date."
                )
                continue

        elif key in ["min_destinations", "max_destinations"]:
            # Numeric filters
            try:
                filters[key] = int(value)
            except ValueError:
                logger.warning(f"Invalid numeric value for {key}: {value}")
                continue

        elif key in ["global_only", "exclude_deleted"]:
            # Boolean filters
            filters[key] = value.lower() in ["true", "1", "yes", "on"]

        else:
            # String filters (access, name_contains) - support comma-separated values
            if "," in value:
                # Split comma-separated values for multi-value filters
                filters[key] = [v.strip() for v in value.split(",") if v.strip()]
            else:
                filters[key] = value

    return filters


def parse_destination_filters(filter_strings):
    """Parse destination filter key=value pairs into a dictionary"""
    filters = {}

    if not filter_strings:
        return filters

    for filter_str in filter_strings:
        if "=" not in filter_str:
            logger.warning(
                f"Invalid filter format '{filter_str}'. Expected key=value format."
            )
            continue

        key, value = filter_str.split("=", 1)
        key = key.strip()
        value = value.strip()

        # Parse different value types
        if key in ["created_after", "created_before"]:
            # Time-based filters - parse relative time (e.g., "7d", "1h", "30m") or ISO date
            try:
                if value.endswith("d"):
                    days = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(days=days)
                elif value.endswith("h"):
                    hours = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(hours=hours)
                elif value.endswith("m"):
                    minutes = int(value[:-1])
                    filters[key] = datetime.now() - timedelta(minutes=minutes)
                else:
                    # Try to parse as ISO date
                    filters[key] = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Invalid time format for {key}: {value}. Use format like '7d', '2h', '30m' or ISO date."
                )
                continue

        elif key in ["has_comment"]:
            # Boolean filters
            filters[key] = value.lower() in ["true", "1", "yes", "on"]

        else:
            # String filters (type, destination_contains) - support comma-separated values
            if "," in value:
                # Split comma-separated values for multi-value filters
                filters[key] = [v.strip() for v in value.split(",") if v.strip()]
            else:
                filters[key] = value

    return filters


def apply_destination_list_filters(destination_lists, filters):
    """Apply filters to destination lists data"""
    if not filters:
        return destination_lists

    filtered_lists = []

    for dest_list in destination_lists:
        # Apply each filter
        include_list = True

        # Time-based filters
        if "created_after" in filters:
            try:
                created_at_raw = dest_list.get("createdAt", "")
                created_at = None

                if isinstance(created_at_raw, str) and created_at_raw:
                    # Handle ISO string format
                    created_at = datetime.fromisoformat(
                        created_at_raw.replace("Z", "+00:00")
                    )
                elif isinstance(created_at_raw, (int, float)):
                    # Handle Unix timestamp
                    created_at = datetime.fromtimestamp(created_at_raw)

                if created_at and created_at < filters["created_after"]:
                    include_list = False
            except (ValueError, TypeError, OSError):
                pass

        if "created_before" in filters and include_list:
            try:
                created_at_raw = dest_list.get("createdAt", "")
                created_at = None

                if isinstance(created_at_raw, str) and created_at_raw:
                    # Handle ISO string format
                    created_at = datetime.fromisoformat(
                        created_at_raw.replace("Z", "+00:00")
                    )
                elif isinstance(created_at_raw, (int, float)):
                    # Handle Unix timestamp
                    created_at = datetime.fromtimestamp(created_at_raw)

                if created_at and created_at > filters["created_before"]:
                    include_list = False
            except (ValueError, TypeError, OSError):
                pass

        if "modified_after" in filters and include_list:
            try:
                modified_at_raw = dest_list.get("modifiedAt", "")
                modified_at = None

                if isinstance(modified_at_raw, str) and modified_at_raw:
                    # Handle ISO string format
                    modified_at = datetime.fromisoformat(
                        modified_at_raw.replace("Z", "+00:00")
                    )
                elif isinstance(modified_at_raw, (int, float)):
                    # Handle Unix timestamp
                    modified_at = datetime.fromtimestamp(modified_at_raw)

                if modified_at and modified_at < filters["modified_after"]:
                    include_list = False
            except (ValueError, TypeError, OSError):
                pass

        if "modified_before" in filters and include_list:
            try:
                modified_at_raw = dest_list.get("modifiedAt", "")
                modified_at = None

                if isinstance(modified_at_raw, str) and modified_at_raw:
                    # Handle ISO string format
                    modified_at = datetime.fromisoformat(
                        modified_at_raw.replace("Z", "+00:00")
                    )
                elif isinstance(modified_at_raw, (int, float)):
                    # Handle Unix timestamp
                    modified_at = datetime.fromtimestamp(modified_at_raw)

                if modified_at and modified_at > filters["modified_before"]:
                    include_list = False
            except (ValueError, TypeError, OSError):
                pass

        # Field-based filters
        if "access" in filters and include_list:
            # Handle both single value and list of values
            access_filter = filters["access"]
            dest_access = dest_list.get("access", "").lower()

            if isinstance(access_filter, list):
                # Multiple values - check if any match
                if not any(dest_access == val.lower() for val in access_filter):
                    include_list = False
            else:
                # Single value
                if dest_access != access_filter.lower():
                    include_list = False

        if "name_contains" in filters and include_list:
            # Handle both single value and list of values
            name_filter = filters["name_contains"]
            dest_name = dest_list.get("name", "").lower()

            if isinstance(name_filter, list):
                # Multiple values - check if any match
                if not any(val.lower() in dest_name for val in name_filter):
                    include_list = False
            else:
                # Single value
                if name_filter.lower() not in dest_name:
                    include_list = False

        # Boolean filters
        if "global_only" in filters and include_list:
            if filters["global_only"] and not dest_list.get("isGlobal", False):
                include_list = False

        if "exclude_deleted" in filters and include_list:
            if filters["exclude_deleted"] and dest_list.get("isDeleted", False):
                include_list = False

        # Numeric filters (destination count)
        if "min_destinations" in filters and include_list:
            dest_count = dest_list.get("destinationCount", 0)
            if dest_count < filters["min_destinations"]:
                include_list = False

        if "max_destinations" in filters and include_list:
            dest_count = dest_list.get("destinationCount", 0)
            if dest_count > filters["max_destinations"]:
                include_list = False

        if include_list:
            filtered_lists.append(dest_list)

    return filtered_lists


def apply_destination_filters(destinations, filters):
    """Apply filters to destinations data"""
    if not filters:
        return destinations

    filtered_destinations = []

    for destination in destinations:
        # Apply each filter
        include_destination = True

        # Time-based filters
        if "created_after" in filters:
            try:
                created_at_raw = destination.get("createdAt", "")
                created_at = None

                if isinstance(created_at_raw, str) and created_at_raw:
                    # Handle different datetime formats
                    try:
                        # Try parsing as ISO format first
                        created_at = datetime.fromisoformat(
                            created_at_raw.replace("Z", "+00:00")
                        )
                    except ValueError:
                        # Try parsing as space-separated format "YYYY-MM-DD HH:MM:SS"
                        created_at = datetime.strptime(
                            created_at_raw, "%Y-%m-%d %H:%M:%S"
                        )
                elif isinstance(created_at_raw, (int, float)):
                    # Handle Unix timestamp
                    created_at = datetime.fromtimestamp(created_at_raw)

                if created_at and created_at < filters["created_after"]:
                    include_destination = False
            except (ValueError, TypeError, OSError):
                pass

        if "created_before" in filters and include_destination:
            try:
                created_at_raw = destination.get("createdAt", "")
                created_at = None

                if isinstance(created_at_raw, str) and created_at_raw:
                    try:
                        created_at = datetime.fromisoformat(
                            created_at_raw.replace("Z", "+00:00")
                        )
                    except ValueError:
                        created_at = datetime.strptime(
                            created_at_raw, "%Y-%m-%d %H:%M:%S"
                        )
                elif isinstance(created_at_raw, (int, float)):
                    created_at = datetime.fromtimestamp(created_at_raw)

                if created_at and created_at > filters["created_before"]:
                    include_destination = False
            except (ValueError, TypeError, OSError):
                pass

        # Type-based filters
        if "type" in filters and include_destination:
            type_filter = filters["type"]
            dest_type = destination.get("type", "").lower()

            if isinstance(type_filter, list):
                # Multiple values - check if any match
                if not any(dest_type == val.lower() for val in type_filter):
                    include_destination = False
            else:
                # Single value
                if dest_type != type_filter.lower():
                    include_destination = False

        # Content filters
        if "destination_contains" in filters and include_destination:
            content_filter = filters["destination_contains"]
            dest_content = destination.get("destination", "").lower()

            if isinstance(content_filter, list):
                # Multiple values - check if any match
                if not any(val.lower() in dest_content for val in content_filter):
                    include_destination = False
            else:
                # Single value
                if content_filter.lower() not in dest_content:
                    include_destination = False

        # Boolean filters
        if "has_comment" in filters and include_destination:
            dest_comment = destination.get("comment", "")
            has_comment = bool(dest_comment and dest_comment.strip())
            if filters["has_comment"] != has_comment:
                include_destination = False

        if include_destination:
            filtered_destinations.append(destination)

    return filtered_destinations


def apply_filters_to_destination_lists(
    destination_lists, args, operation_name="operation"
):
    """Apply filters to destination lists if filters are provided"""
    if hasattr(args, "filter") and args.filter:
        filters = parse_filters(args.filter)
        if filters:
            logger.info(f"Applying {operation_name} filters: {filters}")
            original_count = len(destination_lists)
            filtered_lists = apply_destination_list_filters(destination_lists, filters)
            filtered_count = len(filtered_lists)
            logger.info(
                f"Filtering reduced {operation_name} set from {original_count} to {filtered_count} destination lists"
            )
            return filtered_lists
    return destination_lists


def apply_filters_to_destinations(destinations, args, operation_name="operation"):
    """Apply filters to destinations if filters are provided"""
    if hasattr(args, "filter") and args.filter:
        filters = parse_destination_filters(args.filter)
        if filters:
            logger.info(f"Applying {operation_name} filters: {filters}")
            original_count = len(destinations)
            filtered_destinations = apply_destination_filters(destinations, filters)
            filtered_count = len(filtered_destinations)
            logger.info(
                f"Filtering reduced {operation_name} set from {original_count} to {filtered_count} destinations"
            )
            return filtered_destinations
    return destinations


def add_filter_argument(parser, context="results"):
    """Add standardized filter argument to a parser"""
    parser.add_argument(
        "--filter",
        action="append",
        help=f"Filter {context} using key=value pairs. Can be used multiple times. {FILTER_HELP_TEXT}",
    )


def add_destination_filter_argument(parser, context="results"):
    """Add destination filter argument to a parser"""
    parser.add_argument(
        "--filter",
        action="append",
        help=f"Filter {context} using key=value pairs. Can be used multiple times. {DESTINATION_FILTER_HELP_TEXT}",
    )


def get_destination_filter_examples(operation="list"):
    """Generate common destination filter examples"""
    return f"""  # Filter by destination type
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter type=domain
  
  # Filter by multiple types
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter type=domain,url
  
  # Filter destinations containing specific text
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter destination_contains=google
  
  # Filter by multiple content patterns
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter destination_contains=youtube,google
  
  # Filter destinations created in last 7 days
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter created_after=7d
  
  # Filter destinations with comments
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter has_comment=true
  
  # Combine multiple filters
  python destination_list_manager.py destinations {operation} --destination-list-id 123 --filter type=domain --filter created_after=30d"""


def parse_destinations_from_csv(csv_file_path):
    """Parse destinations from CSV file"""
    destinations = []

    try:
        with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            # Validate required columns
            if not reader.fieldnames:
                raise ValueError("CSV file appears to be empty or malformed")

            required_columns = {"destination"}
            missing_columns = required_columns - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(
                    f"CSV file missing required columns: {', '.join(missing_columns)}"
                )

            for row_num, row in enumerate(
                reader, start=2
            ):  # Start at 2 because of header
                # Skip empty rows
                if not any(row.values()):
                    continue

                destination = row.get("destination", "").strip()
                dest_type = row.get("type", "").strip()
                comment = row.get("comment", "").strip()

                if not destination:
                    logger.warning(f"Row {row_num}: Empty destination, skipping")
                    continue

                # Basic validation - just check if type is valid when provided
                if dest_type:
                    valid_types = ["domain", "url", "ipv4"]
                    if dest_type not in valid_types:
                        raise ValueError(
                            f"Row {row_num}: Invalid type '{dest_type}'. Valid types: {', '.join(valid_types)}"
                        )
                dest_obj = {"destination": destination}
                if dest_type:
                    dest_obj["type"] = dest_type
                if comment:
                    dest_obj["comment"] = comment
                destinations.append(dest_obj)
        logger.info(
            f"Successfully parsed {len(destinations)} destinations from CSV file"
        )
        return destinations

    except FileNotFoundError:
        raise ValueError(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {e}")


def show_csv_example():
    """Show example CSV format for destinations"""
    example = """
CSV Format Example:

File: destinations.csv
destination,type,comment
google.com,domain,Search engine
https://api.example.com,url,API endpoint  
192.168.1.1,ipv4,Internal server
facebook.com,,Social media platform (type auto-detected)
https://secure.site.com/api,url,Secure API
10.0.0.1,,Network gateway (type auto-detected)

Required columns:
- destination: The actual destination (domain, URL, or IP address)

Optional columns:
- type: Must be one of: domain, url, ipv4 (if not provided, API determines automatically)
- comment: Description for the destination

Notes:
- CSV files must use comma delimiter
- Empty rows are automatically skipped
- Comments are optional and will be omitted if not provided
- Type is optional - when provided, it enables stricter validation
- When type is not provided, the API automatically determines it based on destination format
- Basic validation is performed on domains, URLs, and IP addresses
    """
    print(example)


class DestinationListManager:
    def __init__(
        self, page=None, limit=None, destination_list_ids=None, destination_ids=None
    ):
        self.access_token = generate_access_token()
        self.configuration = Configuration(
            access_token=self.access_token,
        )
        self.api_client = ApiClient(configuration=self.configuration)
        self.destination_lists = []
        self.destinations = []
        self.destination_list_response = None
        self.destination_response = None
        self.backup_file_name = "destination_lists_backup.json"
        self.destinations_backup_file_name = "destinations_backup.json"
        self.page = page
        self.limit = limit
        self.destination_list_ids = destination_list_ids
        self.destination_ids = destination_ids

    def create_destination_list_request(self, destination_list_data):
        """Create a destination list request object"""
        return DestinationListCreate.from_dict(destination_list_data)

    def create_destination_list(self, destination_list_request):
        """Create a new destination list"""
        api_instance = destination_lists_api.DestinationListsApi(
            api_client=self.api_client
        )
        try:
            self.destination_list_response = (
                api_instance.create_destination_list_without_preload_content(
                    destination_list_create=destination_list_request
                )
            )
            if self.destination_list_response.status == 200:
                logger.info("Destination list created successfully")
            else:
                error_msg = f"Failed to create destination list. Status: {self.destination_list_response.status}"
                try:
                    error_details = self.destination_list_response.json()
                    error_msg += f", Details: {error_details}"
                except:
                    error_msg += f", Response: {self.destination_list_response.data}"
                logger.error(error_msg)
            return self.destination_list_response
        except Exception as e:
            logger.error(
                "An error occurred while creating the destination list: " + str(e)
            )
            return None

    def list_destination_lists(self):
        """List all destination lists with automatic pagination when page/limit not specified"""
        api_instance = destination_lists_api.DestinationListsApi(
            api_client=self.api_client
        )
        try:
            if self.page is not None and self.limit is not None:
                # Manual pagination - return specific page
                self.destination_list_response = (
                    api_instance.get_destination_lists_without_preload_content(
                        page=self.page, limit=self.limit
                    )
                )
                if self.destination_list_response.status == 200:
                    response_data = self.destination_list_response.json()
                    self.destination_lists = response_data.get("data", [])
            elif self.destination_list_ids:
                # Get specific destination lists by IDs
                for dest_list_id in self.destination_list_ids:
                    response = (
                        api_instance.get_destination_list_without_preload_content(
                            dest_list_id
                        )
                    )
                    if response.status == 200:
                        # Extract just the data part, not the whole response
                        response_data = response.json()
                        if "data" in response_data:
                            self.destination_lists.append(response_data["data"])
                        else:
                            self.destination_lists.append(response_data)
                return
            else:
                # Auto-pagination - fetch all pages
                logger.info(
                    "Auto-pagination enabled: fetching all destination lists..."
                )
                self.destination_lists = []
                current_page = 1
                page_limit = 100  # Use maximum allowed limit for efficiency
                total_items = None

                # Continue until we've fetched all data or encounter an error
                while current_page == 1 or (
                    total_items and len(self.destination_lists) < total_items
                ):
                    self.destination_list_response = (
                        api_instance.get_destination_lists_without_preload_content(
                            page=current_page, limit=page_limit
                        )
                    )

                    if self.destination_list_response.status != 200:
                        error_msg = f"Error in fetching destination lists (page {current_page}). Status: {self.destination_list_response.status}"
                        try:
                            error_details = self.destination_list_response.json()
                            error_msg += f", Details: {error_details}"
                        except:
                            error_msg += (
                                f", Response: {self.destination_list_response.data}"
                            )
                        logger.error(error_msg)
                        break

                    response_data = self.destination_list_response.json()
                    page_data = response_data.get("data", [])
                    meta = response_data.get("meta", {})

                    # Set total_items from first response
                    if total_items is None:
                        total_items = meta.get("total", 0)
                        if total_items == 0:
                            logger.info("No destination lists found")
                            break

                    self.destination_lists.extend(page_data)

                    logger.info(
                        f"Fetched page {current_page}: {len(page_data)} destination lists (total so far: {len(self.destination_lists)})"
                    )

                    # Stop if we got fewer items than requested (last page) or no items
                    if len(page_data) < page_limit or len(page_data) == 0:
                        break

                    current_page += 1

                logger.info(
                    f"Auto-pagination complete: Retrieved {len(self.destination_lists)} destination lists across {current_page} pages"
                )

            if (
                self.destination_list_response
                and self.destination_list_response.status != 200
            ):
                error_msg = f"Error in fetching destination lists. Status: {self.destination_list_response.status}"
                try:
                    error_details = self.destination_list_response.json()
                    error_msg += f", Details: {error_details}"
                except:
                    error_msg += f", Response: {self.destination_list_response.data}"
                logger.error(error_msg)
        except Exception as e:
            logger.error("An error occurred while listing destination lists: " + str(e))

    def get_destination_list(self, destination_list_id):
        """Get a specific destination list by ID"""
        api_instance = destination_lists_api.DestinationListsApi(
            api_client=self.api_client
        )
        try:
            self.destination_list_response = (
                api_instance.get_destination_list_without_preload_content(
                    destination_list_id
                )
            )
            if self.destination_list_response.status == 200:
                logger.debug(
                    "Retrieved destination list ID: " + str(destination_list_id)
                )
            return self.destination_list_response
        except Exception as e:
            logger.error("An error occurred while fetching destination list: " + str(e))

    def update_destination_list_request(self, destination_list_data):
        """Create destination list patch request object"""
        return DestinationListPatch.from_dict(destination_list_data)

    def update_destination_list(self, destination_list_id, destination_list_request):
        """Update an existing destination list"""
        api_instance = destination_lists_api.DestinationListsApi(
            api_client=self.api_client
        )
        try:
            self.destination_list_response = (
                api_instance.update_destination_lists_without_preload_content(
                    destination_list_id, destination_list_patch=destination_list_request
                )
            )
            if self.destination_list_response.status == 200:
                logger.info(
                    "Destination list updated successfully for ID: "
                    + str(destination_list_id)
                )
            return self.destination_list_response
        except Exception as e:
            logger.error("An error occurred while updating destination list: " + str(e))

    def delete_destination_list(self, destination_list_id):
        """Delete a destination list"""
        api_instance = destination_lists_api.DestinationListsApi(
            api_client=self.api_client
        )
        try:
            self.destination_list_response = (
                api_instance.delete_destination_list_without_preload_content(
                    destination_list_id
                )
            )
            if self.destination_list_response.status == 200:
                logger.info(
                    "Destination list deleted successfully for ID: "
                    + str(destination_list_id)
                )
            return self.destination_list_response
        except Exception as e:
            logger.error("An error occurred while deleting destination list: " + str(e))

    def create_destination_request(self, destination_data_list):
        """Create destination request objects from a list of destination data"""
        if not isinstance(destination_data_list, list):
            destination_data_list = [destination_data_list]

        return [
            DestinationCreateObject.from_dict(dest_data)
            for dest_data in destination_data_list
        ]

    def create_destination(self, destination_list_id, destination_request_list):
        """Create new destinations in a destination list"""
        api_instance = destinations_api.DestinationsApi(api_client=self.api_client)
        try:
            self.destination_response = (
                api_instance.create_destinations_without_preload_content(
                    destination_list_id=destination_list_id,
                    destination_create_object=destination_request_list,
                )
            )
            if self.destination_response.status == 200:
                logger.info(
                    f"Created {len(destination_request_list)} destinations successfully"
                )
            else:
                error_msg = f"Failed to create destinations. Status: {self.destination_response.status}"
                try:
                    error_details = self.destination_response.json()
                    error_msg += f", Details: {error_details}"
                except:
                    error_msg += f", Response: {self.destination_response.data}"
                logger.error(error_msg)
            return self.destination_response
        except Exception as e:
            logger.error("An error occurred while creating destinations: " + str(e))
            return None

    def list_destinations(self, destination_list_id=None):
        """List destinations from a specific destination list with automatic pagination when page/limit not specified"""
        api_instance = destinations_api.DestinationsApi(api_client=self.api_client)
        try:
            if self.page is not None and self.limit is not None:
                # Manual pagination - return specific page
                api_params = {
                    "destination_list_id": destination_list_id,
                    "page": self.page,
                    "limit": self.limit,
                }
                self.destination_response = (
                    api_instance.get_destinations_without_preload_content(**api_params)
                )

                if self.destination_response.status == 200:
                    response_data = self.destination_response.json()
                    self.destinations = response_data.get("data", [])
            else:
                # Auto-pagination - fetch all pages
                logger.info(
                    f"Auto-pagination enabled: fetching all destinations from destination list ID: {destination_list_id}..."
                )
                self.destinations = []
                current_page = 1
                page_limit = 100  # Use maximum allowed limit for efficiency
                total_items = None

                # Continue until we've fetched all data or encounter an error
                while current_page == 1 or (
                    total_items and len(self.destinations) < total_items
                ):
                    api_params = {
                        "destination_list_id": destination_list_id,
                        "page": current_page,
                        "limit": page_limit,
                    }
                    self.destination_response = (
                        api_instance.get_destinations_without_preload_content(
                            **api_params
                        )
                    )

                    if self.destination_response.status != 200:
                        error_msg = f"Error in fetching destinations (page {current_page}). Status: {self.destination_response.status}"
                        try:
                            error_details = self.destination_response.json()
                            error_msg += f", Details: {error_details}"
                        except:
                            error_msg += f", Response: {self.destination_response.data}"
                        logger.error(error_msg)
                        break

                    response_data = self.destination_response.json()
                    page_data = response_data.get("data", [])
                    meta = response_data.get("meta", {})

                    # Set total_items from first response
                    if total_items is None:
                        total_items = meta.get("total", 0)
                        if total_items == 0:
                            logger.info("No destinations found")
                            break

                    self.destinations.extend(page_data)

                    logger.info(
                        f"Fetched page {current_page}: {len(page_data)} destinations (total so far: {len(self.destinations)})"
                    )

                    # Stop if we got fewer items than requested (last page) or no items
                    if len(page_data) < page_limit or len(page_data) == 0:
                        break

                    current_page += 1

                logger.info(
                    f"Auto-pagination complete: Retrieved {len(self.destinations)} destinations from destination list ID: {destination_list_id} across {current_page} pages"
                )

            if self.destination_response and self.destination_response.status != 200:
                error_msg = f"Error in fetching destinations. Status: {self.destination_response.status}"
                try:
                    error_details = self.destination_response.json()
                    error_msg += f", Details: {error_details}"
                except:
                    error_msg += f", Response: {self.destination_response.data}"
                logger.error(error_msg)
        except Exception as e:
            logger.error(f"An error occurred while listing destinations: {e}")

    def delete_destination(self, destination_list_id, destination_ids):
        """Delete destinations from a destination list"""
        api_instance = destinations_api.DestinationsApi(api_client=self.api_client)
        try:
            # Validate max 500 IDs
            if len(destination_ids) > 500:
                raise ValueError("Maximum 500 destination IDs allowed per request")

            self.destination_response = (
                api_instance.delete_destinations_without_preload_content(
                    destination_list_id=destination_list_id,
                    request_body=destination_ids,
                )
            )
            if self.destination_response.status == 200:
                logger.info(
                    f"Deleted {len(destination_ids)} destinations successfully from list ID: {destination_list_id}"
                )
            return self.destination_response
        except Exception as e:
            logger.error("An error occurred while deleting destinations: " + str(e))

    def backup_destination_lists(self, include_destinations=False):
        """Backup destination lists to JSON file with optional destination details"""
        try:
            data_to_backup = self.destination_lists

            if include_destinations:
                # Enhance destination lists with full destination details
                data_to_backup = self._enhance_lists_with_destinations(
                    self.destination_lists
                )

            # Save data to file
            with open(self.backup_file_name, "w+") as backup_file:
                json.dump(data_to_backup, backup_file, indent=4)

            backup_type = (
                "with full destination details" if include_destinations else ""
            )
            logger.info(
                f"Destination lists {backup_type} backed up to: {self.backup_file_name}"
            )

        except Exception as e:
            logger.error(
                "An error occurred while backing up destination lists: " + str(e)
            )

    def _enhance_lists_with_destinations(self, destination_list_data):
        """Private method to enhance destination lists with full destination details"""
        enhanced_data = []

        for dest_list in destination_list_data:
            # Work with clean data (no HTTP status wrappers)
            enhanced_list = dest_list.copy()
            dest_list_id = enhanced_list.get("id")

            # Get destinations for this destination list
            if dest_list_id:
                logger.info(
                    f"Fetching destinations for destination list ID: {dest_list_id}"
                )
                enhanced_list["destinations"] = self._fetch_destinations_for_list(
                    dest_list_id
                )
            else:
                enhanced_list["destinations"] = []

            enhanced_data.append(enhanced_list)

        return enhanced_data

    def _fetch_destinations_for_list(self, dest_list_id):
        """Private method to fetch ALL destinations for a specific destination list by reusing list_destinations"""
        try:
            # Save current state
            original_page = self.page
            original_limit = self.limit
            original_destinations = self.destinations

            # Temporarily set to None to enable auto-pagination
            self.page = None
            self.limit = None

            # Use existing list_destinations method with auto-pagination
            self.list_destinations(destination_list_id=dest_list_id)

            # Get the results
            fetched_destinations = self.destinations.copy()

            # Restore original state
            self.page = original_page
            self.limit = original_limit
            self.destinations = original_destinations

            logger.info(
                f"Found {len(fetched_destinations)} destinations for list {dest_list_id}"
            )
            return fetched_destinations

        except Exception as e:
            logger.error(f"Error fetching destinations for list {dest_list_id}: {e}")
            # Restore original state in case of error
            self.page = original_page if "original_page" in locals() else self.page
            self.limit = original_limit if "original_limit" in locals() else self.limit
            self.destinations = (
                original_destinations
                if "original_destinations" in locals()
                else self.destinations
            )
            return []

    def backup_destinations(self):
        """Backup destinations to JSON file"""
        try:
            with open(self.destinations_backup_file_name, "w+") as backup_file:
                json.dump(self.destinations, backup_file, indent=4)
            logger.info(
                "Destinations backed up to: " + self.destinations_backup_file_name
            )
        except Exception as e:
            logger.error("An error occurred while backing up destinations: " + str(e))

    def parse_backup_destination_lists(self):
        """Parse destination lists from backup file"""
        try:
            with open(self.backup_file_name, "r+") as backup_file:
                self.destination_lists = json.load(backup_file)
            logger.info(
                "Loaded "
                + str(len(self.destination_lists))
                + " destination lists from backup"
            )
        except Exception as e:
            logger.error(
                "The backup file not found, Please run backup first: " + str(e)
            )
            sys.exit(1)

    def parse_backup_destinations(self):
        """Parse destinations from backup file"""
        try:
            with open(self.destinations_backup_file_name, "r+") as backup_file:
                self.destinations = json.load(backup_file)
            logger.info(
                "Loaded " + str(len(self.destinations)) + " destinations from backup"
            )
        except Exception as e:
            logger.error(
                "The destinations backup file not found, Please run backup first: "
                + str(e)
            )
            sys.exit(1)


def setup_destination_lists_parser(subparsers):
    """Setup destination lists commands and arguments"""
    dest_lists_parser = subparsers.add_parser(
        "destination-lists",
        help="Manage destination lists",
        description="Operations for managing destination lists",
        epilog=f"""Examples:
{get_main_command_examples()}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    dest_lists_subparsers = dest_lists_parser.add_subparsers(
        dest="dest_lists_command", help="Destination lists commands", required=True
    )

    # List destination lists
    list_parser = dest_lists_subparsers.add_parser(
        "list",
        help="List destination lists",
        description="List all destination lists or filter by IDs. Uses automatic pagination to fetch all results when page/limit not specified.",
        epilog=f"""Filter Examples:
{get_list_specific_examples()}
  
{get_common_filter_examples("list")}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    list_parser.add_argument(
        "-p",
        "--page",
        type=int,
        help="Starting page for pagination (enables manual pagination)",
    )
    list_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help="Limit for pagination (enables manual pagination, max 100)",
    )
    list_parser.add_argument(
        "--ids", type=int, nargs="+", help="List of destination list IDs to filter"
    )
    add_filter_argument(list_parser, "results")

    # Create destination list
    create_parser = dest_lists_subparsers.add_parser(
        "create",
        help="Create a new destination list",
        description="Create a new destination list with specified parameters",
    )
    create_parser.add_argument(
        "--name",
        help="Name for the destination list (required unless showing examples)",
    )
    create_parser.add_argument(
        "--description", help="Description for the destination list"
    )
    create_parser.add_argument(
        "--access",
        choices=[
            "allow",
            "block",
            "url_proxy",
            "no_decrypt",
            "warn",
            "none",
            "thirdparty_block",
        ],
        help="Access type for the destination list (required unless showing examples)",
    )

    # Destination input methods (mutually exclusive)
    dest_group = create_parser.add_mutually_exclusive_group()
    dest_group.add_argument(
        "--destinations", help="JSON string of destinations to include"
    )
    dest_group.add_argument("--csv-file", help="CSV file path containing destinations")

    # Helper option
    create_parser.add_argument(
        "--show-csv-example",
        action="store_true",
        help="Show CSV format example and exit",
    )

    # Update destination list
    update_parser = dest_lists_subparsers.add_parser(
        "update",
        help="Update an existing destination list",
        description="Update an existing destination list by ID (only name can be updated)",
    )
    update_parser.add_argument(
        "--id", required=True, type=int, help="Destination list ID to update"
    )
    update_parser.add_argument(
        "--name", required=True, help="New name for the destination list"
    )

    # Delete destination list
    delete_parser = dest_lists_subparsers.add_parser(
        "delete",
        help="Delete a destination list",
        description="Delete a destination list by ID",
    )
    delete_parser.add_argument(
        "--id", required=True, type=int, help="Destination list ID to delete"
    )

    # Backup destination lists
    backup_parser = dest_lists_subparsers.add_parser(
        "backup",
        help="Backup destination lists to file",
        description="Backup destination lists to a JSON file with optional filtering and destination inclusion",
        epilog=f"""Backup Filter Examples:
{get_backup_specific_examples()}
  
{get_common_filter_examples("backup")}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    backup_parser.add_argument(
        "--file", help="Output file name (default: destination_lists_backup.json)"
    )
    backup_parser.add_argument(
        "--ids",
        type=int,
        nargs="+",
        help="List of destination list IDs to backup (if not specified, backs up all or filtered results)",
    )
    add_filter_argument(backup_parser, "which destination lists to backup")
    backup_parser.add_argument(
        "--include-destinations",
        action="store_true",
        help="Include full destination details for each destination in the lists",
    )


def setup_destinations_parser(subparsers):
    """Setup destinations commands and arguments"""
    destinations_parser = subparsers.add_parser(
        "destinations",
        help="Manage destinations",
        description="Operations for managing destinations",
        epilog="""Examples:
  # List all destinations from a destination list with auto-pagination
  python destination_list_manager.py destinations list --destination-list-id 123
  
  # List specific page of destinations with manual pagination
  python destination_list_manager.py destinations list --destination-list-id 123 --page 2 --limit 25
  
  # Filter destinations by type
  python destination_list_manager.py destinations list --destination-list-id 123 --filter type=domain
  
  # Create destinations from CSV file
  python destination_list_manager.py destinations create --destination-list-id 123 --csv-file new_destinations.csv
  
  # Create single destination with JSON
  python destination_list_manager.py destinations create --destination-list-id 123 --data '{"destination":"example.com","comment":"Example site"}'
  
  # Create multiple destinations with JSON
  python destination_list_manager.py destinations create --destination-list-id 123 --data '[{"destination":"site1.com"},{"destination":"192.168.1.100","comment":"Internal server"}]'
  
  # Delete specific destinations by IDs
  python destination_list_manager.py destinations delete --destination-list-id 123 --ids 456 789 101112
  
  # Backup destinations from a list
  python destination_list_manager.py destinations backup --destination-list-id 123 --file destinations_backup.json""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    destinations_subparsers = destinations_parser.add_subparsers(
        dest="destinations_command", help="Destinations commands", required=True
    )

    # List destinations
    list_parser = destinations_subparsers.add_parser(
        "list",
        help="List destinations from a destination list",
        description="List destinations from a specific destination list. Uses automatic pagination to fetch all results when page/limit not specified.",
        epilog=f"""Filter Examples:
  # List all destinations with auto-pagination
  python destination_list_manager.py destinations list --destination-list-id 123
  
  # List specific page with manual pagination
  python destination_list_manager.py destinations list --destination-list-id 123 --page 2 --limit 25
  
{get_destination_filter_examples("list")}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    list_parser.add_argument(
        "--destination-list-id",
        required=True,
        type=int,
        help="Destination list ID to retrieve destinations from",
    )
    list_parser.add_argument(
        "-p",
        "--page",
        type=int,
        help="Starting page for pagination (enables manual pagination)",
    )
    list_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help="Limit for pagination (enables manual pagination, max 100)",
    )
    add_destination_filter_argument(list_parser, "destinations")

    # Create destination
    create_parser = destinations_subparsers.add_parser(
        "create",
        help="Create new destinations",
        description="Create new destinations in a destination list with specified data",
    )
    create_parser.add_argument(
        "--destination-list-id",
        type=int,
        help="Destination list ID to add destinations to (required unless showing examples)",
    )

    # Destination input methods (mutually exclusive)
    dest_group = create_parser.add_mutually_exclusive_group()
    dest_group.add_argument(
        "--data",
        help="JSON string containing destination data (single destination or list)",
    )
    dest_group.add_argument("--csv-file", help="CSV file path containing destinations")

    # Helper option
    create_parser.add_argument(
        "--show-csv-example",
        action="store_true",
        help="Show CSV format example and exit",
    )

    # Delete destination
    delete_parser = destinations_subparsers.add_parser(
        "delete",
        help="Delete destinations",
        description="Delete destinations from a destination list by IDs",
    )
    delete_parser.add_argument(
        "--destination-list-id",
        required=True,
        type=int,
        help="Destination list ID to remove destinations from",
    )
    delete_parser.add_argument(
        "--ids",
        required=True,
        type=int,
        nargs="+",
        help="List of destination IDs to delete (max 500 IDs)",
    )

    # Backup destinations
    backup_parser = destinations_subparsers.add_parser(
        "backup",
        help="Backup destinations from a destination list to file",
        description="Backup destinations from a specific destination list to a JSON file",
        epilog=f"""Backup Filter Examples:
  # Backup all destinations from a list
  python destination_list_manager.py destinations backup --destination-list-id 123
  
  # Backup to custom file
  python destination_list_manager.py destinations backup --destination-list-id 123 --file custom_backup.json
  
{get_destination_filter_examples("backup")}""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    backup_parser.add_argument(
        "--destination-list-id",
        required=True,
        type=int,
        help="Destination list ID to backup destinations from",
    )
    backup_parser.add_argument(
        "--file", help="Output file name (default: destinations_backup.json)"
    )
    add_destination_filter_argument(backup_parser, "destinations to backup")


def handle_destination_lists(args):
    """Handle all destination list operations"""
    # Handle helper options first (before initializing manager to avoid API calls)
    if args.dest_lists_command == "create":
        if hasattr(args, "show_csv_example") and args.show_csv_example:
            show_csv_example()
            return

    # Initialize manager with appropriate parameters
    manager_kwargs = {}

    # Handle pagination for list operations
    if hasattr(args, "page") and args.page is not None:
        manager_kwargs["page"] = args.page
    if hasattr(args, "limit") and args.limit is not None:
        manager_kwargs["limit"] = args.limit

    # Handle ID filters for list operations
    if hasattr(args, "ids") and args.ids:
        manager_kwargs["destination_list_ids"] = args.ids

    manager = DestinationListManager(**manager_kwargs)

    if args.dest_lists_command == "list":
        logger.info("Listing destination lists")
        manager.list_destination_lists()

        # Apply filters if provided
        manager.destination_lists = apply_filters_to_destination_lists(
            manager.destination_lists, args, "list"
        )

        if manager.destination_lists:
            print(json.dumps(manager.destination_lists, indent=2))
        else:
            logger.info("No destination lists found")

    elif args.dest_lists_command == "create":
        # Validate required arguments for actual creation
        if not args.name:
            logger.error("--name is required for creating a destination list")
            sys.exit(1)

        if not args.access:
            logger.error("--access is required for creating a destination list")
            sys.exit(1)

        # Build destinations list from JSON or CSV input
        destinations_list = []

        if args.destinations:
            try:
                destinations_list = json.loads(args.destinations)
                logger.info(f"Loaded {len(destinations_list)} destinations from JSON")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON format for destinations: {e}")
                sys.exit(1)
        elif hasattr(args, "csv_file") and args.csv_file:
            try:
                destinations_list = parse_destinations_from_csv(args.csv_file)
                logger.info(
                    f"Loaded {len(destinations_list)} destinations from CSV file: {args.csv_file}"
                )
            except ValueError as e:
                logger.error(f"CSV parsing error: {e}")
                sys.exit(1)

        destination_list_data = {
            "name": args.name,
            "description": args.description or "",
            "destinations": destinations_list,
            "access": args.access,
            "isGlobal": False,
            "bundleTypeId": 2,
        }

        logger.info(f"Creating destination list: {args.name}")
        request = manager.create_destination_list_request(destination_list_data)
        result = manager.create_destination_list(request)
        if result and result.status == 200:
            print("Destination list created successfully")
            print(json.dumps(result.json(), indent=2))
        else:
            if result:
                logger.error(
                    f"Failed to create destination list. HTTP Status: {result.status}"
                )
            else:
                logger.error(
                    "Failed to create destination list. Check the error details above."
                )
            sys.exit(1)

    elif args.dest_lists_command == "update":
        # Only name can be updated according to DestinationListPatch model
        update_data = {"name": args.name}

        logger.info(f"Updating destination list ID: {args.id} with name: {args.name}")
        request = manager.update_destination_list_request(update_data)
        result = manager.update_destination_list(args.id, request)
        if result and result.status == 200:
            print("Destination list updated successfully")
        else:
            logger.error("Failed to update destination list")
            sys.exit(1)

    elif args.dest_lists_command == "delete":
        logger.info(f"Deleting destination list ID: {args.id}")
        result = manager.delete_destination_list(args.id)
        if result and result.status == 200:
            print("Destination list deleted successfully")
        else:
            logger.error("Failed to delete destination list")
            sys.exit(1)

    elif args.dest_lists_command == "backup":
        # Handle specific IDs for backup - reuse the existing manager
        if hasattr(args, "ids") and args.ids:
            # Update the existing manager with the IDs for backup
            manager.destination_list_ids = args.ids
            logger.info(f"Backing up specific destination lists: {args.ids}")
        else:
            logger.info("Backing up destination lists...")

        # Use the existing manager to get the lists
        manager.list_destination_lists()

        # Apply filters if provided (and not using specific IDs)
        if not (hasattr(args, "ids") and args.ids):
            manager.destination_lists = apply_filters_to_destination_lists(
                manager.destination_lists, args, "backup"
            )

        if manager.destination_lists:
            if args.file:
                manager.backup_file_name = args.file

            # Check if we need to include full destination details
            include_destinations = (
                hasattr(args, "include_destinations") and args.include_destinations
            )
            if include_destinations:
                logger.info("Including full destination details in backup...")

            manager.backup_destination_lists(include_destinations=include_destinations)

            # Show summary
            list_count = len(manager.destination_lists)
            backup_type = "with destinations" if include_destinations else ""

            # Determine filter information for summary
            if hasattr(args, "ids") and args.ids:
                filter_info = f" (filtered by IDs: {args.ids})"
            elif hasattr(args, "filter") and args.filter:
                filter_info = " (filtered)"
            else:
                filter_info = " (all)"

            print(
                f"Backed up {list_count} destination lists{filter_info} {backup_type} to: {manager.backup_file_name}"
            )
        else:
            logger.info("No destination lists to backup")


def handle_destinations(args):
    """Handle all destination operations"""
    # Handle helper options first (before initializing manager to avoid API calls)
    if args.destinations_command == "create":
        if hasattr(args, "show_csv_example") and args.show_csv_example:
            show_csv_example()
            return

    # Initialize manager with appropriate parameters
    manager_kwargs = {}

    # Handle pagination for list operations
    if hasattr(args, "page") and args.page is not None:
        manager_kwargs["page"] = args.page
    if hasattr(args, "limit") and args.limit is not None:
        manager_kwargs["limit"] = args.limit

    manager = DestinationListManager(**manager_kwargs)

    if args.destinations_command == "list":
        logger.info(
            f"Listing destinations from destination list ID: {args.destination_list_id}"
        )

        manager.list_destinations(destination_list_id=args.destination_list_id)

        # Apply filters if provided
        manager.destinations = apply_filters_to_destinations(
            manager.destinations, args, "list"
        )

        if manager.destinations:
            print(json.dumps(manager.destinations, indent=2))
        else:
            logger.info("No destinations found")

    elif args.destinations_command == "create":
        # Validate required arguments for actual creation
        if not args.destination_list_id:
            logger.error("--destination-list-id is required for creating destinations")
            sys.exit(1)

        if not args.data and not args.csv_file:
            logger.error(
                "Either --data or --csv-file is required for creating destinations"
            )
            sys.exit(1)

        # Build destinations list from JSON or CSV input
        destinations_list = []

        if args.data:
            try:
                data = json.loads(args.data)
                # Handle both single destination and list of destinations
                if isinstance(data, list):
                    destinations_list = data
                else:
                    destinations_list = [data]
                logger.info(f"Loaded {len(destinations_list)} destinations from JSON")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON format for destination data: {e}")
                sys.exit(1)
        elif hasattr(args, "csv_file") and args.csv_file:
            try:
                destinations_list = parse_destinations_from_csv(args.csv_file)
                logger.info(
                    f"Loaded {len(destinations_list)} destinations from CSV file: {args.csv_file}"
                )
            except ValueError as e:
                logger.error(f"CSV parsing error: {e}")
                sys.exit(1)

        if not destinations_list:
            logger.error("No destinations provided")
            sys.exit(1)

        # Validate destination list limit (500 for regular, 100 for thirdparty_block)
        if len(destinations_list) > 500:
            logger.error("Maximum 500 destinations allowed per request")
            sys.exit(1)

        logger.info(
            f"Creating {len(destinations_list)} destinations in destination list ID: {args.destination_list_id}"
        )
        request_list = manager.create_destination_request(destinations_list)
        result = manager.create_destination(args.destination_list_id, request_list)
        if result and result.status == 200:
            print(f"Created {len(destinations_list)} destinations successfully")
            print(json.dumps(result.json(), indent=2))
        else:
            if result:
                logger.error(
                    f"Failed to create destinations. HTTP Status: {result.status}"
                )
            else:
                logger.error(
                    "Failed to create destinations. Check the error details above."
                )
            sys.exit(1)

    elif args.destinations_command == "delete":
        # Validate destination IDs count
        if len(args.ids) > 500:
            logger.error("Maximum 500 destination IDs allowed per request")
            sys.exit(1)

        logger.info(
            f"Deleting {len(args.ids)} destinations from destination list ID: {args.destination_list_id}"
        )
        result = manager.delete_destination(args.destination_list_id, args.ids)
        if result and result.status == 200:
            print(f"Deleted {len(args.ids)} destinations successfully")
        else:
            logger.error("Failed to delete destinations")
            sys.exit(1)

    elif args.destinations_command == "backup":
        logger.info(
            f"Backing up destinations from destination list ID: {args.destination_list_id}"
        )
        manager.list_destinations(destination_list_id=args.destination_list_id)

        # Apply filters if provided
        manager.destinations = apply_filters_to_destinations(
            manager.destinations, args, "backup"
        )

        if manager.destinations:
            if args.file:
                manager.destinations_backup_file_name = args.file
            manager.backup_destinations()

            # Show summary with filter information
            dest_count = len(manager.destinations)
            filter_info = (
                " (filtered)" if hasattr(args, "filter") and args.filter else ""
            )
            print(
                f"Backed up {dest_count} destinations{filter_info} from list ID {args.destination_list_id} to: {manager.destinations_backup_file_name}"
            )
        else:
            logger.info("No destinations to backup")


if __name__ == "__main__":
    # Main parser
    parser = argparse.ArgumentParser(
        description="Cisco Secure Access Destination Management Tool"
    )

    # Create subparsers for main categories
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=True,
        metavar="{destination-lists,destinations}",
    )

    # Setup command parsers
    setup_destination_lists_parser(subparsers)
    setup_destinations_parser(subparsers)

    # Parse arguments
    args = parser.parse_args()

    logger.info("Starting Cisco Secure Access Destination Management Tool")

    try:
        if args.command == "destination-lists":
            handle_destination_lists(args)
        elif args.command == "destinations":
            handle_destinations(args)
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

    logger.info("Operation completed successfully")
