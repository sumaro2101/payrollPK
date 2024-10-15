import re


def check_format_file(file_name: str) -> re.Match | None:
    result = re.match(r'^((.+)\.(?:jpeg|jpg|png|svg|ico))$',
                      file_name,
                      )
    return result
