def extract_text_from_adf(node):

    text_parts = []

    if isinstance(node, dict):

        if node.get("type") == "text":

            text_parts.append(
                node.get("text", "")
            )

        elif node.get("type") == "mention":

            text_parts.append(
                node.get("attrs", {})
                    .get("text", "")
            )

        for value in node.values():

            if isinstance(
                value,
                (dict, list)
            ):
                text_parts.append(
                    extract_text_from_adf(
                        value
                    )
                )

    elif isinstance(node, list):

        for item in node:

            text_parts.append(
                extract_text_from_adf(
                    item
                )
            )

    return "".join(text_parts)