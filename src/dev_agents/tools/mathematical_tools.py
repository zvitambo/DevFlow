from agents import function_tool

@function_tool
def compute_factorial(n: int) -> dict:
    """Calculates the factorial of a non-negative integer.
    
    Args:
        n (int): The non-negative integer to compute factorial for
        
    Returns:
        dict: Computation status and result
    """
    print(f"🔧 TOOL CALLED: compute_factorial")
    print(f"   INPUT: n = {n}")

    if n < 0:
        result = {
            "status": "error",
            "error_message": "Factorial is not defined for negative numbers."
        }
        print(f"   OUTPUT: {result}")
        return result

    if n > 170:
        result = {
            "status": "error",
            "error_message": "Number too large. Factorial computation limited to n <= 170."
        }
        print(f"   OUTPUT: {result}")
        return result

    try:
        factorial_result = 1
        for i in range(2, n + 1):
            factorial_result *= i

        result = {
            "status": "success",
            "result": f"The factorial of {n} is {factorial_result}"
        }
        print(f"   OUTPUT: {result}")
        return result
    except Exception as e:
        result = {
            "status": "error",
            "error_message": f"Error computing factorial: {str(e)}"
        }
        print(f"   OUTPUT: {result}")
        return result


@function_tool
def compute_exponential(base: float, exponent: float) -> dict:
    """Calculates base raised to the power of exponent.
    
    Args:
        base (float): The base number
        exponent (float): The exponent
        
    Returns:
        dict: Computation status and result
    """
    print(f"🔧 TOOL CALLED: compute_exponential")
    print(f"   INPUT: base = {base}, exponent = {exponent}")

    try:
        result_value = base ** exponent

        if abs(result_value) > 1e308:
            result = {
                "status": "error",
                "error_message": "Result too large to compute."
            }
            print(f"   OUTPUT: {result}")
            return result

        result = {
            "status": "success",
            "result": f"{base} raised to the power of {exponent} is {result_value}"
        }
        print(f"   OUTPUT: {result}")
        return result
    except Exception as e:
        result = {
            "status": "error",
            "error_message": f"Error computing exponential: {str(e)}"
        }
        print(f"   OUTPUT: {result}")
        return result


@function_tool
def compute_fibonacci(n: int) -> dict:
    """Calculates the nth Fibonacci number (0-indexed).
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        dict: Computation status and result
    """
    print(f"🔧 TOOL CALLED: compute_fibonacci")
    print(f"   INPUT: n = {n}")

    if n < 0:
        result = {
            "status": "error",
            "error_message": "Fibonacci is not defined for negative positions."
        }
        print(f"   OUTPUT: {result}")
        return result

    if n > 1000:
        result = {
            "status": "error",
            "error_message": "Position too large. Fibonacci computation limited to n <= 1000."
        }
        print(f"   OUTPUT: {result}")
        return result

    try:
        if n == 0:
            fib_result = 0
        elif n == 1:
            fib_result = 1
        else:
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            fib_result = b

        result = {
            "status": "success",
            "result": f"The {n}th Fibonacci number is {fib_result}"
        }
        print(f"   OUTPUT: {result}")
        return result
    except Exception as e:
        result = {
            "status": "error",
            "error_message": f"Error computing Fibonacci: {str(e)}"
        }
        print(f"   OUTPUT: {result}")
        return result
