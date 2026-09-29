def calculate(a: float, b: float, operation: str):
    if operation == "add":
        return a+b
    elif operation == "sub":
        return a-b
    elif operation == "mul":
        return a*b
    elif operation == "div":
        if b == 0:
            return "can't divide by zero"
        return a/b
    else:
        return "invalid operation"

calculate_tool = {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"执行两个数之间的运算",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{
                        "type":"number",
                        "description":"输入的第一个数字",
                    },
                    "b":{
                        "type":"number",
                        "description":"输入的第二个数字"
                    },
                    "operation":{
                        "type":"string",
                        "enum":["add","sub","mul","div"],
                        "description":"运算类型"
                    }
                },
                "required":["a","b","operation"],
            }
        }

    }
