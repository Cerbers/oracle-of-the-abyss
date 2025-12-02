def check_for_title_line(line: str, filename: str) -> bool:
    """Check if the poem has a title line enclosed in quotes, all caps, 
    or if the first line is significantly shorter than the rest and coincides with file name."""

    stripped = line.strip()

    if stripped.startswith('"') and stripped.endswith('"'):
        return True

    if stripped.startswith("'") and stripped.endswith("'"):
        return True

    if stripped.isupper():
        return True

    if stripped == filename:
        return True

    return False
