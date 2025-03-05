# Prompts
DYNAMIC_STOP_PROMPT = """

Now, when you 99% sure you have completed the task, you may follow the instructions below to escape the autonomous loop.

When you have finished the task from the Human, output a special token: <DONE>
This will enable you to leave the autonomous loop.
"""
DYNAMIC_STOP_PROMPT_V2 = """
Now, when you 99% sure you have completed the task,or if you detect that you are trapped in a loop or encountering a situation where further progress is no longer possible (e.g., repetitive attempts yielding the same result or lack of actionable data to continue), you may follow the instructions below to escape the autonomous loop:
Output a special token: <DONE>
This will enable you to leave the autonomous loop. 
Note:This signifies that you have identified a potential deadlock, or the task cannot be effectively completed within the current constraints.
You should assess the following signs of a potential deadlock:
- Repeating the same task logic multiple times without achieving meaningful progress.  
- Encountering ambiguous or incomplete instructions that prevent task resolution.  
- Missing critical tools or resources required to complete the task.  
- Attempting to resolve an issue where the provided input does not allow for a valid solution.
Remember: As soon as you determine either task completion or a deadlock, output `<DONE>` to conclude your operations and exit the autonomous loop.
"""


# Make it able to handle multi input tools
DYNAMICAL_TOOL_USAGE = """
You have access to the following tools:
Output a JSON object with the following structure to use the tools

commands: {
    "tools": {
        tool1: "search_api",
        "params": {
            "query": "What is the weather in New York?",
            "description": "Get the weather in New York"
        }
        "tool2: "weather_api",
        "params": {
            "query": "What is the weather in Silicon Valley",
        }
        "tool3: "rapid_api",
        "params": {
            "query": "Use the rapid api to get the weather in Silicon Valley",
        }
    }
}

"""

########### FEW SHOT EXAMPLES ################
SCENARIOS = """
commands: {
    "tools": {
        tool1: "function",
        "params": {
            "input": "inputs",
            "tool1": "inputs"
        }
        "tool2: "tool_name",
        "params": {
            "parameter": "inputs",
            "tool1": "inputs"
        }
        "tool3: "tool_name",
        "params": {
            "tool1": "inputs",
            "tool1": "inputs"
        }
    }
}

"""


def tool_sop_prompt() -> str:
    return """
    You've been granted tools to assist users by always providing outputs in JSON format for tool usage. 
    Whenever a tool usage is required, you must output the JSON wrapped inside markdown for clarity. 
    Provide a commentary on the tool usage and the user's request and ensure that the JSON output adheres to the tool's schema.

    Here are some rules:
    Do not ever use tools that do not have JSON schemas attached to them.
    Do not use tools that you have not been granted access to.
    Do not use tools that are not relevant to the task at hand.
    Do not use tools that are not relevant to the user's request.
    All tool calls, regardless of the number of tools or the number of times each tool is called, must be combined into ONE JSON object.
    Do not generate multiple separate JSONs for each individual tool call



    Here are the guidelines you must follow:

    1. **Output Format**:
    - All outputs related to tool usage should be formatted as JSON.
    - The JSON should be encapsulated within triple backticks and tagged as a code block with 'json'.

    2. **Schema Compliance**:
    - Ensure that the JSON output strictly follows the provided schema for each tool.
    - Each tool's schema will define the structure and required fields for the JSON output.

    3. **Schema Example**:
    If a tool named `example_tool` with a schema requires `param1` and `param2`, your response should look like:
    ```json
    {
        "type": "function",
        "function": {
        "name": "example_tool",
        "parameters": {
            "param1": 123,
            "param2": "example_value"
        }
        }
    }
    ```
    If you want to use multiple tools ,or you need to call the same tool multiple times with different parameters,For example, if you want to use two tools, one tool named `example_tool` with a schema requiring `param1` and `param2`, and another tool named `example_tool2` that needs to be called twice - once with parameters `param3` and `param4`, and another time with `param5` and `param6` - your response should look like this:
    ```json
    {
        "type": "function",
        "functions": [
            {
                "name": "example_tool",
                "parameters": {
                    "param1": 123,
                    "param2": "value1"
                }
            },
            {
                "name": "example_tool2",
                "parameters": {
                    "param3": 456,
                    "param4": "value2"
                }
            },
            {
                "name": "example_tool2",
                "parameters": {
                    "param5": 789,
                    "param6": "value3"
                }
            }
        ]
    }
    ```
    Important Constraints:
    Prohibition of Separate JSON Outputs:
    Never split JSON calls into individual outputs. Multiple calls must always be merged into the functions list.
    For example, the below output with separate JSON blocks is INVALID and must NEVER occur:
    ```json
    {
    "type": "function",
    "function": {
        "name": "tool1",
        "parameters": { ... }
    }
    }
    ```
    ```json
    {
        "type": "function",
        "function": {
            "name": "tool2",
            "parameters": { ... }
        }
    }
    ```
    Please proceed with your task accordingly.
    """
