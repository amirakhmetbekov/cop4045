import ast
import io
import tokenize


def line_number(input_file: str, output_file: str) -> None:
    """Read a text file and write its lines with line numbers to another file."""
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            lines = infile.readlines()

        with open(output_file, "w", encoding="utf-8") as outfile:
            for number, line in enumerate(lines, start=1):
                outfile.write(f"{number}. {line}")

    except Exception as error:
        print("Error processing the file:", error)
        raise


def parse_functions(filename: str) -> tuple:
    """Parse a Python file and return information about its functions."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        lines = source.splitlines(keepends=True)

        # Parse the Python source code
        tree = ast.parse(source)

        # Find locations of comments
        comment_columns = {}

        tokens = tokenize.generate_tokens(io.StringIO(source).readline)

        for token in tokens:
            if token.type == tokenize.COMMENT:
                line_number, column = token.start
                comment_columns[line_number] = column

        functions = []

        # Look at top-level functions in the file
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                function_line = node.lineno

                # Get the formal argument list from the function definition
                definition_line = lines[function_line - 1]
                left_parenthesis = definition_line.find("(")
                right_parenthesis = definition_line.rfind(")")
                arguments = definition_line[
                    left_parenthesis + 1:right_parenthesis
                ]

                code_lines = []

                # Get the function signature and body
                for current_number in range(node.lineno, node.end_lineno + 1):
                    current_line = lines[current_number - 1]

                    # Remove comments
                    if current_number in comment_columns:
                        column = comment_columns[current_number]
                        current_line = current_line[:column]

                    # Remove the newline and trailing spaces
                    current_line = current_line.rstrip()

                    # Do not include empty lines
                    if current_line.strip() != "":
                        code_lines.append(current_line)

                function_code = "\n".join(code_lines) + "\n"

                functions.append(
                    (
                        function_line,
                        function_name,
                        arguments,
                        function_code
                    )
                )

        # Sort alphabetically by function name
        functions.sort(key=lambda function: function[1])

        return tuple(functions)

    except Exception as error:
        print("Error processing the file:", error)
        raise


def main() -> None:
    """Test line_number and parse_functions on this Python source file."""
    source_file = __file__
    output_file = "p1_Akhmetbekov_Amir.txt"

    print("Amir Akhmetbekov")

    print("\nTesting line_number:")
    line_number(source_file, output_file)
    print("Created:", output_file)

    print("\nTesting parse_functions:")
    result = parse_functions(source_file)
    print(result)


if __name__ == "__main__":
    main()