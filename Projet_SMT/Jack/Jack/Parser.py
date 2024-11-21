{
    "line": 1,
    "col": 1,
    "type": "class",
    "name": "Main",
    "classVarDecs": [],
    "subroutines": [
        {
            "line": 2,
            "col": 1,
            "kind": "function",
            "returnType": "void",
            "name": "main",
            "parameters": [],
            "body": {
                "varDecs": [],
                "statements": [
                    {
                        "type": "do",
                        "call": {
                            "type": "subroutineCall",
                            "classOrVar": "Output",
                            "subroutine": "printString",
                            "args": ["Hello, world!"]
                        }
                    },
                    {"type": "return", "value": null}
                ]
            }
        }
    ]
}
