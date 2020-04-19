from .base_tools import BasicTools
from .const import *
import re


ANGLE_PATTERNS = {
    AT_LON: {
        'DMS_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                        (?P<deg>\d{3})  # Degrees
                        (?P<min>\d{2})  # Minutes
                        (?P<sec>\d{2}(\.\d+)?)  # Seconds
                        (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                        $  # End of the string
                       ''', re.VERBOSE),
        'DM_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+EW]?)  # Hemisphere prefix
                        (?P<deg>\d{3})  # Degrees
                        (?P<min>\d{2}(\.\d+)?)  # Minutes
                        (?P<hem_suffix>[EW]?)  # Hemisphere suffix
                        $  # End of the string
                       ''', re.VERBOSE)

    },
    AT_LAT: {
        'DMS_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
                        (?P<deg>\d{2})  # Degrees
                        (?P<min>\d{2})  # Minutes
                        (?P<sec>\d{2}(\.\d+)?)  # Seconds
                        (?P<hem_suffix>[NS]?)  # Hemisphere suffix
                        $  # End of the string
                       ''', re.VERBOSE),
        'DM_COMP': re.compile(r'''
                        ^  # Start of the string
                        (?P<hem_prefix>[-+NS]?)  # Hemisphere prefix
                        (?P<deg>\d{2})  # Degrees
                        (?P<min>\d{2}(\.\d+)?)  # Minutes
                        (?P<hem_suffix>[NS]?)  # Hemisphere suffix
                        $  # End of the string
                       ''', re.VERBOSE)
    }
}


class AngleBase(BasicTools):

    def __init__(self, ang_src=None, ang_type=None):
        BasicTools.__init__(self)
        self.ang_src = ang_src
        self.ang_type = ang_type
        self.ang_dd = None

    @staticmethod
    def dms_groups_to_dd(parts):
        if parts.group('hem_prefix') and parts.group('hem_suffix'):
            return
        else:
            d = int(parts.group('deg'))
            m = int(parts.group('min'))
            s = float(parts.group('sec'))
            h = parts.group('hem_prefix') + parts.group('hem_suffix')
            dd = d + m / 60 + s / 3600
            if h in ['W', 'S', '-']:
                dd = -dd
            return dd

    @staticmethod
    def dm_groups_to_dd(parts):
        if parts.group('hem_prefix') and parts.group('hem_suffix'):
            return
        else:
            d = int(parts.group('deg'))
            m = float(parts.group('min'))
            h = parts.group('hem_prefix') + parts.group('hem_suffix')
            dd = d + m / 60
            if h in ['W', 'S', '-']:
                dd = -dd
            return dd

    def compacted_format_to_dd(self, ang):
        ang_type_patterns = ANGLE_PATTERNS[self.ang_type]
        for pattern in ang_type_patterns:
            if ang_type_patterns[pattern].match(ang):
                parts = ang_type_patterns[pattern].search(ang)
                if pattern == 'DMS_COMP':
                    return self.dms_groups_to_dd(parts)
                elif pattern == 'DM_COMP':
                    return self.dm_groups_to_dd(parts)
