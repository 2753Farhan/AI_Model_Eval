"""
Version information and utilities.
"""

__version__ = '1.0.0'
__version_info__ = (1, 0, 0)
__release__ = 'stable'


def get_version_string() -> str:
    """Get full version string."""
    return f"{__version__} ({__release__})"


def compare_versions(version1: str, version2: str) -> int:
    """Compare two version strings.
    
    Returns:
        -1 if version1 < version2
         0 if version1 == version2
         1 if version1 > version2
    """
    def parse_version(v):
        return tuple(map(int, (v.split("."))))
    
    v1 = parse_version(version1)
    v2 = parse_version(version2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


if __name__ == '__main__':
    print(f"AI Model Evaluation Framework v{get_version_string()}")
