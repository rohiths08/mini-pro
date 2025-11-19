from textwrap import dedent


def build_doc_prompt(
    code: str,
    language: str,
    file_name: str = "code",
    include_examples: bool = True,
    include_api: bool = True,
) -> str:
    """Prompt used for documentation generation."""

    return dedent(
        f"""
        Follow this format:

        ### Function

        `[Function signature]`



        ### Description

        [Explain what it does.]



        ### Args

        - `name (type)`: Description.



        ### Returns

        - `type`: Description.



        ### Raises

        - `ExceptionType`: When it happens (if any).



        ### Logic Explanation

        [Step-by-step explanation.]



        ### Time Complexity

        `O(n)` or similar.



        ### Example

        ```{language}
        >>> [Code Example]

        [Expected Output]
        ```



        ---

        Now document the following function only:

        ```{language}
        {code}
        ```
        """
    ).strip()


def build_explain_prompt(code: str, language: str) -> str:
    """Prompt for code explanation."""

    return dedent(
        f"""
        Explain the following {language} code for an intermediate developer. Cover:
        - What each major block does
        - How data flows through the code
        - Non-obvious implementation details or optimizations
        - Potential pitfalls or assumptions

        Code:
        ```{language}
        {code}
        ```
        """
    ).strip()


def build_test_prompt(code: str, language: str) -> str:
    """Prompt for unit test synthesis."""

    return dedent(
        f"""
        Generate table-driven unit tests for the following {language} code.
        Requirements:
        - Prefer the testing framework idiomatic to {language}
        - Cover success and failure paths
        - Include assertions for outputs and side-effects
        - Highlight any mocks or fixtures that are required

        Code:
        ```{language}
        {code}
        ```
        """
    ).strip()


def build_optimize_prompt(code: str, language: str) -> str:
    """Prompt for optimization suggestions."""

    return dedent(
        f"""
        Review the {language} snippet below and propose targeted optimizations.
        For each suggestion include:
        - Problem/inefficiency being addressed
        - Updated code if applicable
        - Impact on readability, performance, or resource usage

        Code:
        ```{language}
        {code}
        ```
        """
    ).strip()


def build_flowchart_prompt(code: str, language: str) -> str:
    """Prompt for flowchart instructions (Mermaid)."""

    return dedent(
        f"""
        Convert the following {language} code into a Mermaid flowchart compatible with Mermaid v11.12.1.
        
        CRITICAL FORMATTING RULES:
        1. DO NOT wrap your response in markdown code blocks
        2. DO NOT use backticks (```) anywhere in your response
        3. DO NOT write "```mermaid" or "```" at all
        4. Start your response IMMEDIATELY with "flowchart TD" or "graph TD"
        5. Use proper Mermaid syntax for nodes and connections
        6. Keep node labels short and descriptive
        7. Use square brackets [text] for process nodes
        8. Use double parentheses ((text)) for start/end nodes
        9. Use curly braces {{{{text}}}} for decision nodes
        10. Use proper arrow syntax: --> for connections
        
        CORRECT Example (start response exactly like this):
        flowchart TD
            Start((Start)) --> Input[Get Input]
            Input --> Check{{Valid?}}
            Check -->|Yes| Process[Process Data]
            Check -->|No| Error[Show Error]
            Process --> End((End))
            Error --> End

        WRONG Examples (DO NOT do this):
        - Starting with: ```mermaid
        - Ending with: ```
        - Adding any markdown formatting

        Code to convert:
        ```{language}
        {code}
        ```

        Generate ONLY the flowchart code starting with "flowchart TD" and nothing else:
        """
    ).strip()
