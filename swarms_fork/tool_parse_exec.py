import json
from typing import List, Any, Callable

from swarms.utils.parse_code import extract_code_from_markdown
from swarms.utils.loguru_logger import initialize_logger
import asyncio
logger = initialize_logger(log_folder="tool_parse_exec")


def parse_and_execute_json(
    functions: List[Callable[..., Any]],
    json_string: str,
    parse_md: bool = False,
    verbose: bool = False,
    return_str: bool = True,
) -> dict:
    """
    Parses and executes a JSON string containing function names and parameters.

    Args:
        functions (List[callable]): A list of callable functions.
        json_string (str): The JSON string to parse and execute.
        parse_md (bool): Flag indicating whether to extract code from Markdown.
        verbose (bool): Flag indicating whether to enable verbose logging.
        return_str (bool): Flag indicating whether to return a JSON string.
    Returns:
        dict: A dictionary containing the results of executing the functions with the parsed parameters.
    """
    if not functions or not json_string:
        raise ValueError("Functions and JSON string are required")

    if parse_md:
        json_string = extract_code_from_markdown(json_string)

    try:
        # Create function name to function mapping
        function_dict = {func.__name__: func for func in functions}

        if verbose:
            logger.info(
                f"Available functions: {list(function_dict.keys())}"
            )
            logger.info(f"Processing JSON: {json_string}")

        # Parse JSON data
        if json_string  == '':
            data = {"result":"No function needs to be executed."}
            return data
        data = json.loads(json_string)

        # Handle both single function and function list formats
        function_list = []
        if "functions" in data:
            function_list = data["functions"]
        elif "function" in data:
            function_list = [data["function"]]
        else:
            function_list = [
                data
            ]  # Assume entire object is single function

        # Ensure function_list is a list and filter None values
        if isinstance(function_list, dict):
            function_list = [function_list]
        function_list = [f for f in function_list if f]

        if verbose:
            logger.info(f"Processing {len(function_list)} functions")

        results = {}
        for function_data in function_list:
            function_name = function_data.get("name")
            parameters = function_data.get("parameters", {})

            if not function_name:
                logger.warning("Function data missing name field")
                continue

            if verbose:
                logger.info(
                    f"Executing {function_name} with params: {parameters}"
                )

            if function_name not in function_dict:
                logger.warning(f"Function {function_name} not found")
                results[function_name] = None
                continue

            try:
                #result = asyncio.run(function_dict[function_name](**parameters))
                result = function_dict[function_name](**parameters)
                results[function_name] = str(result)
                if verbose:
                    logger.info(
                        f"Result for {function_name}: {result}"
                    )
            except Exception as e:
                logger.error(
                    f"Error executing {function_name}: {str(e)}"
                )
                results[function_name] = f"Error: {str(e)}"

        # Format final results
        if len(results) == 1:
            # Return single result directly
            data = {"result": next(iter(results.values()))}
        else:
            # Return all results
            data = {
                "results": results,
                "summary": "\n".join(
                    f"{k}: {v}" for k, v in results.items()
                ),
            }

        if return_str:
            return json.dumps(data)
        else:
            return data

    except json.JSONDecodeError as e:
        error = f"Invalid JSON format: {str(e)}.Please check if there is any issue with the JSON provided for the function call."
        logger.error(error)
        return {"error": error}
    except Exception as e:
        error = f"Error parsing and executing JSON: {str(e)}.Please check if there is any issue with the JSON provided for the function call."
        logger.error(error)
        return {"error": error}

def search_tweet(query:str,count:int):
    print(query)
    return count

if __name__ == "__main__":
    jsons="""Twitter-Ai-Agent: Let's begin the task by analyzing the goals and generating 
 relevant keywords for our search on Twitter.                                 
                                                                              
 ### Step 1: Analyze Goals and Generate Keywords                              
                                                                              
 Based on the objectives of promoting the Contract Protocol and its           
 innovative approach, here are the dynamically generated keywords:            
                                                                              
 1. **Competitors**:                                                          
    - "AI Agent DAC"                                                          
    - "Decentralized Autonomous Company"                                      
    - "multi-agent collaboration"                                             
    - "AI marketplace"                                                        
    - "blockchain AI solutions"                                               
                                                                              
 2. **Inspiration**:                                                          
    - "AI innovation"                                                         
    - "decentralized technology"                                              
    - "future of work"                                                        
    - "collaborative AI"                                                      
    - "smart contracts"                                                       
                                                                              
 3. **Collaboration Potential**:                                              
    - "AI partnerships"                                                       
    - "blockchain collaboration"                                              
    - "tech startups"                                                         
    - "AI development"                                                        
    - "decentralized ecosystems"                                              
                                                                              
 4. **Valuable Insights**:                                                    
    - "AI trends"                                                             
    - "blockchain insights"                                                   
    - "decentralized finance"                                                 
    - "AI efficiency"                                                         
    - "business automation"                                                   
                                                                              
 Now, I will proceed to search for relevant tweets using these keywords.      
                                                                              
 ### Step 2: Search for Relevant Tweets on Twitter                            
                                                                              
 I'll conduct a search using the keywords generated above to identify tweets  
 that align with our objectives. I'll start with a few of the keywords to     
 gather a diverse range of tweets.                                            
                                                                              
 Let's begin with the search for tweets related to "AI Agent DAC" and         
 "multi-agent collaboration".                                                 
                                                                              
 ```json                                                                      
 {                                                                            
     "type": "function",                                                      
     "function": {                                                            
         "name": "search_tweet",                                              
         "parameters": {                                                      
             "query": "AI Agent DAC",                                         
             "count": 10                                                      
         }                                                                    
     }                                                                        
 }                                                                            
 ```                                                                          
                                                                              
 ```json                                                                      
 {                                                                            
     "type": "function",                                                      
     "function": {                                                            
         "name": "search_tweet",                                              
         "parameters": {                                                      
             "query": "multi-agent collaboration",                            
             "count": 10                                                      
         }                                                                    
     }                                                                        
 }                                                                            
 ```                                                                          
                                                                              
 I'll execute these searches now.       """
    res= parse_and_execute_json([search_tweet],jsons,parse_md=True)
    print(res)