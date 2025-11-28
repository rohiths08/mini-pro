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

        Function:

        `[Function signature]`



        Description:

        [Explain what it does.]



        Args:

        - `name (type)`: Description.



        Returns:

        - `type`: Description.



        Raises:

        - `ExceptionType`: When it happens (if any).



        Logic Explanation:

        [Step-by-step explanation.]



        Time Complexity:

        `O(n)` or similar.



        Example:

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
        You are a code explanation expert. Explain the following {language} code in a clear, well-formatted way.
        
        CRITICAL FORMATTING RULES:
        1. Use proper Markdown with clear section headers (##)
        2. Add BLANK LINES between ALL sections and paragraphs
        3. Write complete sentences in proper paragraphs
        4. Use bullet points (-) for lists with proper spacing
        5. Use inline code (`backticks`) for variable/function names
        6. Use code blocks (```) for code examples
        7. Keep paragraphs concise (2-3 sentences max)
        8. ALWAYS add a blank line after headers before content
        9. ALWAYS add a blank line between list items and paragraphs
        
        REQUIRED STRUCTURE:
        
        ## Overview
        
        Write 2-3 complete sentences explaining what this code does overall. Make sure each sentence is clear and well-formed.
        
        ## Code Breakdown
        
        ### Function/Component Name
        
        - **Purpose**: Write a complete sentence explaining what it does
        - **Parameters**: List each parameter with its type and purpose in complete sentences
        - **Return value**: Write a complete sentence about what it returns
        - **Key operations**: 
          - Step 1: Complete sentence
          - Step 2: Complete sentence
          - Step 3: Complete sentence
        
        ## Data Flow
        
        Explain the flow in complete sentences and use arrows for clarity:
        
        - Input: `parameterName` → Processing step → Output: `returnValue`
        - Describe each step in a complete sentence
        
        ## Key Points
        
        - Write each point as a complete, clear sentence
        - Include important implementation details
        - Mention performance considerations if relevant
        - Note any design patterns used
        
        ## Potential Issues
        
        - Write each issue as a complete sentence
        - Mention edge cases to watch for
        - Note common pitfalls
        - Provide suggestions for improvement
        
        EXAMPLE OUTPUT FORMAT:
        
        ## Overview
        
        This function calculates the factorial of a number using recursion. It's a classic example of a recursive algorithm that demonstrates how a function can call itself to solve a problem.
        
        ## Code Breakdown
        
        ### factorial(n)
        
        - **Purpose**: This function calculates n! (n factorial) by recursively multiplying numbers from n down to 1.
        - **Parameters**: `n` (number) - The number to calculate factorial for, should be a non-negative integer.
        - **Return value**: The function returns the factorial result as a number.
        - **Key operations**:
          - First, it checks if n equals 0 or 1, which are the base cases.
          - If the base case is true, it returns 1 immediately.
          - Otherwise, it multiplies n by the result of calling factorial(n - 1).
        
        ## Data Flow
        
        The function follows this flow:
        
        - Input: `n` → Check if base case (n === 0 or n === 1) → If true, return 1
        - If false → Calculate `n * factorial(n-1)` → Return the result
        - The recursion continues until reaching the base case.
        
        ## Key Points
        
        - This implementation uses recursion instead of iteration, which is more elegant but less efficient.
        - The time complexity is O(n) because it makes n recursive calls.
        - The space complexity is also O(n) due to the call stack storing each recursive call.
        
        ## Potential Issues
        
        - There is no input validation, so negative numbers will cause infinite recursion and stack overflow.
        - Very large numbers (above ~10000) may cause stack overflow errors.
        - Consider using an iterative approach for better performance and to avoid stack issues.
        
        NOW EXPLAIN THIS CODE:
        
        ```{language}
        {code}
        ```
        
        REMEMBER: 
        - Write in complete, clear sentences
        - Add blank lines between ALL sections
        - Add blank lines between paragraphs
        - Make the output easy to read!
        """
    ).strip()


def build_test_prompt(code: str, language: str) -> str:
    """Prompt for unit test synthesis."""

    return dedent(
        f"""
        You are a test generation expert. Generate comprehensive unit tests for the EXACT code provided below.
        
        CRITICAL RULES:
        1. Analyze the PROVIDED CODE carefully
        2. Generate tests ONLY for the functions/classes in the provided code
        3. DO NOT generate tests for example code or hypothetical functions
        4. Use the testing framework appropriate for {language}
        5. Include test cases for:
           - Normal/happy path scenarios
           - Edge cases
           - Error conditions
           - Boundary values
        
        TESTING FRAMEWORK BY LANGUAGE:
        - JavaScript/TypeScript: Jest or Vitest
        - Python: pytest or unittest
        - Java: JUnit
        - C#: NUnit or xUnit
        - Go: testing package
        - Ruby: RSpec
        
        OUTPUT FORMAT:
        - Start with necessary imports
        - Group related tests in describe/test blocks
        - Use clear, descriptive test names
        - Include assertions for expected outputs
        - Add comments explaining complex test scenarios
        
        EXAMPLE OUTPUT STRUCTURE:
        
        ```{language}
        // Import testing framework
        import {{ describe, it, expect }} from 'vitest'
        
        // Import the function to test
        import {{ functionName }} from './module'
        
        describe('functionName', () => {{
          it('should handle normal input correctly', () => {{
            const result = functionName(normalInput)
            expect(result).toBe(expectedOutput)
          }})
          
          it('should handle edge case: empty input', () => {{
            const result = functionName('')
            expect(result).toBe(expectedForEmpty)
          }})
          
          it('should throw error for invalid input', () => {{
            expect(() => functionName(invalidInput)).toThrow()
          }})
        }})
        ```
        
        NOW GENERATE TESTS FOR THIS EXACT CODE:
        
        ```{language}
        {code}
        ```
        
        REMEMBER:
        - Test ONLY the code shown above
        - Use the function/class names from the provided code
        - Cover all important scenarios
        - Make tests clear and maintainable
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
        
        NODE ID RULES (VERY IMPORTANT):
        - Node IDs MUST be simple alphanumeric only (no underscores, no spaces, no special chars)
        - Use camelCase for multi-word IDs: callFib, nCheck, returnN (NOT Call_Fib, N_Check, Return_N)
        - Keep IDs short: A, B, C, Start, End, Check, Process, etc.
        - VALID IDs: Start, End, checkUser, processData, A1, B2
        - INVALID IDs: Call_Fib, N_Check, Return_N, check-user, process data
        
        NODE LABEL RULES (CRITICAL):
        6. Keep node labels short and descriptive
        7. Use square brackets [text] for process nodes
        8. Use double parentheses ((text)) for start/end nodes
        9. Use curly braces {{{{text}}}} for decision nodes
        10. Use proper arrow syntax: --> for connections
        11. Use |text| for edge labels on decision branches
        12. CRITICAL QUOTE RULES:
            - If a label contains quotes, slashes, or special characters, wrap the ENTIRE label in double quotes
            - CORRECT: redirect["Redirect to /login"]
            - CORRECT: update["Set user.name = 'John'"]
            - WRONG: redirect[Redirect to "/login"]
            - WRONG: update[Set user.name = 'John']
        13. For simple labels without special chars, no quotes needed:
            - CORRECT: process[Process Data]
            - CORRECT: check{{Valid?}}
        
        CORRECT Example (start response exactly like this):
        flowchart TD
            Start((Start)) --> getInput[Get Input]
            getInput --> checkValid{{Valid?}}
            checkValid -->|Yes| processData["arr[i] = data"]
            checkValid -->|No| showError[Show Error]
            processData --> End((End))
            showError --> End

        WRONG Examples (DO NOT do this):
        - Using underscores: Call_Fib, N_Check, Return_N
        - Using spaces: call fib, n check
        - Using hyphens: call-fib, n-check
        - Unquoted special chars: Process[arr[i] = 1], redirect[Go to "/login"]
        - Starting with: ```mermaid
        - Ending with: ```
        - Adding any markdown formatting

        Code to convert:
        ```{language}
        {code}
        ```

        Generate ONLY the flowchart code starting with "flowchart TD" and nothing else.
        Remember: Use camelCase for node IDs, wrap labels with special characters in double quotes!
        """
    ).strip()
