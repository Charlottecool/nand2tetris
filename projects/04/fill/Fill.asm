// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//(LOOP) //READ KEY
//	@KBD
//	D=M
//	@WHITESETUP
//	D;JEQ
//	@BLACKSETUP
//	0;JMP
//(BLACKSETUP)
//	@SCREEN
//	D=A
//	@i
//	M=D
//(BLACKLOOP)
//	@i
//	A=M
//	M=-1
//	@i
//	M=M+1
//	@i
//	D=M
//	@KBD
//	D=D-A
//	@LOOP
//	D;JEQ
//	@BLACKLOOP
//	0;JMP
//(WHITESETUP)
//	@SCREEN
//	D=A
//	@i
//	M=D
//(WHITELOOP)
//	@i
//	A=M
//	M=0
//	@i
//	M=M+1
//	@i
//	D=M
//	@KBD
//	D=D-A
//	@LOOP
//	D;JEQ
//	@WHITELOOP
//	0;JMP

(LOOP)
	@KBD
	D=M
	@WHITESET
	D;JEQ
	@BLACKSET
	0;JMP
(BLACKSET)
	@SCREEN
	D=A
	@i
	M=D
(BLACKLOOP)
	@i
	A=M
	M=-1
	@i
	M=M+1
	@i
	D=M
	@KBD
	D=D-A
	@LOOP
	D;JEQ
	@BLACKLOOP
	0;JMP
(WHITESET)
	@SCREEN
	D=A
	@i
	M=D
(WHITELOOP)
	@i
	A=M
	M=0
	@i
	M=M+1
	@i
	D=M
	@KBD
	D=D-A
	@LOOP
	D;JEQ
	@WHITELOOP
	0;JMP
























































































































	




































































































































































































































































































