"""
Timezone utilities for Philippines time handling
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Philippines timezone
PH_TZ = ZoneInfo('Asia/Manila')

def get_philippines_time():
    """Get current time in Philippines timezone."""
    return datetime.now(PH_TZ)

def format_philippines_time(dt=None):
    """Format datetime in Philippines timezone."""
    if dt is None:
        dt = get_philippines_time()
    elif dt.tzinfo is None:
        # Assume UTC if no timezone info
        dt = dt.replace(tzinfo=ZoneInfo('UTC')).astimezone(PH_TZ)
    else:
        dt = dt.astimezone(PH_TZ)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_philippines_time_for_db():
    """Get Philippines time formatted for database storage (store Philippines time in DB)."""
    # Store Philippines time directly in database for consistency
    ph_time = datetime.now(PH_TZ)
    return ph_time.strftime('%Y-%m-%d %H:%M:%S')

def parse_philippines_time(timestamp_str):
    """Parse timestamp string and convert to Philippines time.
    
    The database stores Philippines time directly, so we just need to parse
    the timestamp and add timezone info without any conversion.
    """
    try:
        if isinstance(timestamp_str, str):
            if 'T' in timestamp_str:
                # ISO format with T - check if it has timezone info
                if 'Z' in timestamp_str or '+' in timestamp_str or timestamp_str.count('-') > 2:
                    # Has timezone info, parse and convert to Philippines time
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    if dt.tzinfo:
                        dt = dt.astimezone(PH_TZ)
                    else:
                        dt = dt.replace(tzinfo=PH_TZ)
                else:
                    # No timezone info, treat as Philippines time
                    dt = datetime.fromisoformat(timestamp_str.replace('T', ' '))
                    dt = dt.replace(tzinfo=PH_TZ)
            else:
                # SQLite format - database stores Philippines time directly
                # Handle microseconds if present
                if '.' in timestamp_str:
                    # Remove microseconds for consistent parsing
                    timestamp_str = timestamp_str.split('.')[0]
                
                # Parse the timestamp (already in Philippines time)
                dt = datetime.fromisoformat(timestamp_str)
                
                # Database already stores Philippines time, so just add timezone info
                # No conversion needed - the timestamp is already correct
                dt = dt.replace(tzinfo=PH_TZ)
        else:
            # Already a datetime object
            dt = timestamp_str
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=PH_TZ)
            elif dt.tzinfo != PH_TZ:
                # Convert to Philippines time if it's in a different timezone
                dt = dt.astimezone(PH_TZ)
        
        # Final check - ensure timezone info is set
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=PH_TZ)
        
        return dt
    except Exception as e:
        print(f"Error parsing timestamp: {e}")
        return None

def format_philippines_time_display(timestamp_str):
    """Format timestamp for display in Philippines time."""
    ph_time = parse_philippines_time(timestamp_str)
    if ph_time:
        return ph_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    return timestamp_str

def format_philippines_time_ampm(timestamp_str):
    """Format timestamp for display in Philippines time with AM/PM."""
    ph_time = parse_philippines_time(timestamp_str)
    if ph_time:
        return ph_time.strftime('%Y-%m-%d %I:%M:%S %p')
    return timestamp_str

def get_philippines_time_plus_minutes(minutes):
    """Get Philippines time plus specified minutes."""
    return get_philippines_time() + timedelta(minutes=minutes)
