@ARG //push arg 1  0-8
D=M
@1
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@SP //pop pointer 1 9-12
M=M-1
A=M
D=M
@THAT
M=D
@0 //push cons 0 13-18
D=A
@SP
AM=M+1
A=A-1
M=D
@THAT //pop that 0 19-30
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@1 //push cons 1 31-36
D=A
@SP
AM=M+1
A=A-1
M=D
@THAT //pop that 1 37-48
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG //push arg 0 49-57
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@2 //push cons 2 58-63
D=A
@SP
AM=M+1
A=A-1
M=D
@SP //sub 64-68
AM=M-1
D=M
A=A-1
M=M-D
@ARG //pop arg 0 69-80
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(MAIN_LOOP_START)
@ARG //push arg 0 81-89
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@SP //if goto compute element 90-93
M=M-1
@COMPUTE_ELEMENT
D;JNE
@END_PROGRAM //goto end program 94-95
0;JMP
(COMPUTE_ELEMENT)
@THAT //push that 0 96-104
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@THAT //push that 1 105-113
D=M
@1
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@SP //add 114-118
AM=M-1
D=M
A=A-1
M=D+M
@THAT //pop that 2 119-130
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@THAT //push pointer 1 131-137
D=M
@SP
A=M
M=D
@SP
M=M+1
@1 //push cons 1 138-143
D=A
@SP
AM=M+1
A=A-1
M=D
@SP //add 144-148
AM=M-1
D=M
A=A-1
M=D+M
@SP //pop pointer 1 149-152  !!!!!!!!!!!!!!!!!!
M=M-1
A=M
D=M
@THAT
M=D
@ARG //push arg 0 153-161
D=M
@0
A=A+D
D=M
@SP
AM=M+1
A=A-1
M=D
@1 //push cons 1 162-167
D=A
@SP
AM=M+1
A=A-1
M=D
@SP //sub 168-172
AM=M-1
D=M
A=A-1
M=M-D
@ARG //pop arg 0 173-184
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@MAIN_LOOP_START //goto mainloop 185-186
0;JMP   
(END_PROGRAM)
(END)
@END
0;JMP