def format_headers(headers: dict) -> str:
    formatted_lines = []
    current_line = ""

    for key, value in headers.items():
        header_text = f"{key}: {value}"

        if len(header_text) > 120:
            formatted_lines.append(f"{header_text}, ")

        elif len(current_line) + len(header_text) + 2 > 120:
            formatted_lines.append(current_line.strip(", "))
            current_line = f"{header_text}, "

        else:
            current_line += f"{header_text}, "

    if current_line.strip(", "):
        formatted_lines.append(current_line.strip(", "))

    return "\n".join(formatted_lines)
