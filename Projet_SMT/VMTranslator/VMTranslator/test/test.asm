// Bootstrap
    @256
    D=A
    @SP
    M=D
	//Call Sys.init 0
    Code assembleur de {'type': 'Call', 'function': 'Sys.init', 'parameter': '0'}


//code de test\test.vm
	//push constant 7
        Code assembleur de {'line': 1, 'col': 1, 'type': 'push', 'segment': 'constant', 'parameter': '7'}

        @parameter
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        	//push constant 8
        Code assembleur de {'line': 2, 'col': 1, 'type': 'push', 'segment': 'constant', 'parameter': '8'}

        @parameter
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        	//add  
    Code assembleur de {'line': 3, 'col': 1, 'type': 'add'}

    @SP
    M=M-1
    A=M
    D=M
    A=A-1
    M=D+M
    