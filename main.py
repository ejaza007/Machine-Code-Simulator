from Byte import *

def MakeMemory(FileName,SPRs): #Creates Memory, An array with length 8000, and copies the value from file to this memory

    Mem = []
    for i in range(65536):
        Mem.append(Byte(0, 0, 0, 0, 0, 0, 0, 0))


    F = open(FileName, "r")
    L = F.read().split(" ")
    for i in range(len(L)):
        Mem[i+2].Set(L[i])

    Mem[0]=IntToByte(1)
    Mem[1]=IntToByte(2+50+1+len(L))

    SPRs.SetCodeBase(2)
    SPRs.SetCodeLimit(2+len(L))
    SPRs.SetCodeCounter(2)

    SPRs.SetDataBase(3+len(L))
    SPRs.SetDataLimit(3+len(L))
    SPRs.SetDataCounter(3+len(L))

    SPRs.SetStackBase(4+len(L))
    SPRs.SetStackLimit(54+len(L))
    SPRs.SetStackCounter(4 + len(L))
    return Mem
def AllocateProcessToMemory(Memory,Filename): #Placeholder for the future
    return Memory
def ReadMemory(Memory,i): # returns the contents of our memory in the ith index
    return Memory[i]
def MakeGPRegisters(): #Creates 16 registers used for GPRs
    R = []
    for i in range(16):
        R.append(Register(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
    return R
def MakeSPRegisters():
    SpecialPR = SpecialPurposeRegisters()
    return SpecialPR
def PrintGPR(R): #Prints the contents of our set of 16 Registers (Meant for GPRs but can be used for SPRs)
        print("R0 : " + str(R[0])  + "    R1 :" + str(R[1]) +  "    R2 :" + str(R[2])  + "    R3 :" + str(R[3]))
        print("R4 : " + str(R[4])  + "    R5 :" + str(R[5]) +  "    R6 :" + str(R[6])  + "    R7 :" + str(R[7]))
        print("R8 : " + str(R[8])  + "    R9 :" + str(R[9]) +  "    R10:" + str(R[10]) + "    R11:" + str(R[11]))
        print("R12: " + str(R[12]) + "    R13:" + str(R[13]) + "    R14:" + str(R[14]) + "    R15:" + str(R[15]))
        print()
def PrintSPR(R):
    print("First         : " + str(R.GetFirstReg()) + "    CodeBase      : " + str(IntToRegister(R.GetCodeBase())) + "    CodeLimit    : " + str(IntToRegister(R.GetCodeLimit())) + "    CodeCounter  : " + str(IntToRegister(R.CodeCounter)))
    print("StackBase     : " + str(IntToRegister(R.GetStackBase())) + "    StackLimit    : " + str(IntToRegister(R.GetStackLimit())) + "    StackCounter : " + str(IntToRegister(R.GetStackCounter())) + "    DataBase     : " + str(IntToRegister(R.DataBase)))
    print("DataLimit     : " + str(IntToRegister(R.GetDataLimit())) + "    DataCounter   : " + str(IntToRegister(R.GetDataCounter())) + "    Flags        : " + str(R.Flags) + "    TwelvthReg   : " + str(R.TwelvthReg))
    print("ThirteenthReg : " + str(R.GetThirteenthReg()) + "    FourteenthReg : " + str(R.GetFourteenthReg()) + "    FifteenthReg : " + str(R.GetFifteenthReg()) + "    SixteenthReg : " + str(R.SixteenthReg))
    print()
    print("Overflow : " + str(R.GetFlagOverflow()))
    print("Zero     : " + str(R.GetFlagZero()))
    print("Sign     : " + str(R.GetFlagSign()))
    print("Carry    : " + str(R.GetFlagCarry()))
    print()
    print("_______________________________________________________________________________________________________________________________________________________________________________")

GPR = MakeGPRegisters()                 #General Purpose Registers Created
SPR = MakeSPRegisters()                 #Special Purpose Registers Created
Memory = MakeMemory("p0.txt",SPR)       #Memory Created, Data Copied to Memory, SPRs Adjusted accordingly

PC = 0                                  #Program Counter Created
IR = IntToByte(SPR.GetCodeBase())       #Instruction Register Created
END = Byte(1,1,1,1,0,0,1,1)             #The value of IR at which Execution will STOP

while ByteToInt(IR) != ByteToInt(END): # Fetch Execute Loop, ends when END value in IR

    PrintGPR(GPR)
    PrintSPR(SPR)
    MAR = SPR.GetCodeCounter()
    IR = ReadMemory(Memory, MAR)

    # the hexadecimal opcodes have been converted to int for the conditional statements
    # eg MOVI = 30 in hex but 48 in decimal

    if(ByteToInt(IR)==22):          #MOV
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        GPR[RegCode1] = GPR[RegCode2]                      # Executes MOV
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif(ByteToInt(IR)==23):         #ADD
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        Num = RegisterToInt(GPR[RegCode1]) + RegisterToInt(GPR[RegCode2])
        SPR.SetFlagsAL(Num)                                # Sets Flags
        GPR[RegCode1] = IntToRegister(Num)                 # Executes ADD
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif (ByteToInt(IR) == 24):  # SUB
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        Num = RegisterToInt(GPR[RegCode1]) - RegisterToInt(GPR[RegCode2])
        SPR.SetFlagsAL(Num)                                # Sets Flags
        GPR[RegCode1] = IntToRegister(Num)                 # Executes SUB
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif (ByteToInt(IR) == 25):  # MUL
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        Num =RegisterToInt(GPR[RegCode1]) * RegisterToInt(GPR[RegCode2])
        SPR.SetFlagsAL(Num)                                # Sets Flags
        GPR[RegCode1] = IntToRegister(Num)                 # Executes MUL
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif (ByteToInt(IR) == 26):  # DIV
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        Num = (int)(RegisterToInt(GPR[RegCode1]) / RegisterToInt(GPR[RegCode2]))
        SPR.SetFlagsAL(Num)                                # Sets Flags
        GPR[RegCode1] = IntToRegister(Num)                 # Executes DIV
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif (ByteToInt(IR) == 27):  # AND
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        GPR[RegCode1] = GPR[RegCode1].AND(GPR[RegCode2])   # Executes AND
        SPR.SetFlagsAL(RegisterToInt(GPR[RegCode1]))       # Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif (ByteToInt(IR) == 28):  # OR
        RegCode1 = ByteToInt(ReadMemory(Memory, MAR + 1))  # Gets Index of Register 1
        RegCode2 = ByteToInt(ReadMemory(Memory, MAR + 2))  # Gets Index of Register 2
        GPR[RegCode1] = GPR[RegCode1].OR(GPR[RegCode2])    # Executes OR
        SPR.SetFlagsAL(RegisterToInt(GPR[RegCode1]))       # Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter() + 3)
        PC += 3

    elif(ByteToInt(IR)==48):     #MOVI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        GPR[RegCode] = IntToRegister(Num)                                                     #Executes MOVI
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==49):     #ADDI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        GPR[RegCode] = IntToRegister(Num + RegisterToInt(GPR[RegCode]))                       #Executes ADDI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==50):     #SUBI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode] - Num))                       #Executes SUBI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==51):     #MULI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode] * Num))                       #Executes MULI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==52):     #DIVI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode] / Num))                       #Executes DIVI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==53):     #ANDI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        ToAnd = IntToRegister(Num)
        GPR[RegCode] = GPR[RegCode].AND(ToAnd)                                                #Executes ANDI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==54):     #ORI
        RegCode =  ByteToInt(ReadMemory(Memory,MAR+1))                                        #Checks which Register to Address
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
        ToOr = IntToRegister(Num)
        GPR[RegCode] = GPR[RegCode].OR(ToOr)                                                  #Executes ORI
        SPR.SetFlagsAL(Num)                                                                   #Sets Flags
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif(ByteToInt(IR)==55):     #BZ
        if(SPR.GetFlagZero()):
            Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
            Jump = IntToRegister(Num)
            SPR.SetCodeCounter(SPR.GetCodeCounter()+Jump)                                         #Executes BZ
            PC += Jump
        else:
            SPR.SetCodeCounter(SPR.GetCodeCounter() + 4)
            PC += 4

    elif(ByteToInt(IR)==56):     #BNZ
        if(not SPR.GetFlagZero()):
            Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
            Jump = IntToRegister(Num)
            SPR.SetCodeCounter(SPR.GetCodeCounter()+Jump)                                         #Executes BNZ
            PC += Jump
        else:
            SPR.SetCodeCounter(SPR.GetCodeCounter() + 4)
            PC += 4

    elif(ByteToInt(IR)==57):     #BC
        if(SPR.GetFlagCarry()):
            Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
            Jump = IntToRegister(Num)
            SPR.SetCodeCounter(SPR.GetCodeCounter()+Jump)                                         #Executes BC
            PC += Jump
        else:
            SPR.SetCodeCounter(SPR.GetCodeCounter() + 4)
            PC += 4

    elif(ByteToInt(IR)==58):     #BS
        if(SPR.GetFlagSign()):
            Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))   #Gets Value to insert in Register
            Jump = IntToRegister(Num)
            SPR.SetCodeCounter(SPR.GetCodeCounter()+Jump)                                         #Executes BS
            PC += Jump
        else:
            SPR.SetCodeCounter(SPR.GetCodeCounter() + 4)
            PC += 4

    elif(ByteToInt(IR)==59):     #JMP
        Num = 256*ByteToInt(ReadMemory(Memory,MAR+2)) + ByteToInt(ReadMemory(Memory,MAR+3))       #Gets Value to insert in Register
        Jump = IntToRegister(Num)
        SPR.SetCodeCounter(SPR.GetCodeCounter()+Jump)                                             #Executes JMP
        PC += Jump

    #CALL

    #ACT


    elif(ByteToInt(IR)==81):     #MOVL
        Imm = 256 * ByteToInt(ReadMemory(Memory, MAR + 2)) + ByteToInt(ReadMemory(Memory, MAR + 3)) #Gets Immediate Value
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))                                            #Gets Register Code
        BaseInt = RegisterToInt(SPR.GetDataBase())                                                  #Gets Data Base
        SPR.SetDataCounter(IntToRegister(BaseInt+Imm))                                              #Gets Memory Address
        Memory[RegisterToInt(SPR.GetDataCounter())] = GPR[RegCode]                                  #Executes MOVL
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif (ByteToInt(IR) == 82):  # MOVS
        Imm = 256 * ByteToInt(ReadMemory(Memory, MAR + 2)) + ByteToInt(ReadMemory(Memory, MAR + 3)) #Gets Immediate Value
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))                                            #Gets Register Code
        BaseInt = RegisterToInt(SPR.GetDataBase())                                                  #Gets Data Base
        SPR.SetDataCounter(IntToRegister(BaseInt + Imm))                                            #Gets Memory Address
        GPR[RegCode] = Memory[RegisterToInt(SPR.GetDataCounter())]                                  #Executes MOVS
        SPR.SetCodeCounter(SPR.GetCodeCounter()+4)
        PC += 4

    elif (ByteToInt(IR) == 113):  # SHL
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        SPR.SetFlagCarry(GPR[RegCode].bit15)                                                  #Sets Carry
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode])*2)                           #Executes SHL
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsRS(RegisterToInt(GPR[RegCode]))                                           #Sets Flags

    elif (ByteToInt(IR) == 114):  # SHR
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        SPR.SetFlagCarry(GPR[RegCode].bit0)                                                   #Sets Carry
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode]) / 2)                         #Executes SHR
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsRS(RegisterToInt(GPR[RegCode]))                                           #Sets Flags


    elif (ByteToInt(IR) == 115):  # RTL
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        SPR.SetFlagCarry(GPR[RegCode].bit15)                                                  #Sets Carry
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode]) * 2)                         #Executes RTL
        GPR[RegCode].bit0 = SPR.GetFlagCarry()                                                #Rotates Carry
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsRS(RegisterToInt(GPR[RegCode]))                                           #Sets Flags


    elif (ByteToInt(IR) == 116):  # RTR
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        SPR.SetFlagCarry(GPR[RegCode].bit0)                                                   #Sets Carry
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode]) / 2)                         #Executes RTR
        GPR[RegCode].bit15 = SPR.GetFlagCarry()                                               #Rotates Carry
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsRS(RegisterToInt(GPR[RegCode]))                                           #Sets Flags


    elif (ByteToInt(IR) == 117):  # INC
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode])+1)                           #Executes INC
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsAL(RegisterToInt(GPR[RegCode]))                                           #Sets Flags


    elif (ByteToInt(IR) == 118):  # DEC
        RegCode = ByteToInt(ReadMemory(Memory, MAR + 1))
        GPR[RegCode] = IntToRegister(RegisterToInt(GPR[RegCode]) - 1)                         #Executes DEC
        SPR.SetCodeCounter(SPR.GetCodeCounter()+2)
        PC += 2
        SPR.SetFlagsAL(RegisterToInt(GPR[RegCode]))                                           #Sets Flags



    #PUSH

    #POP

    #RETURN

    elif (ByteToInt(IR) == 242): #NOOP
        PC += 1

        #Command Executed, Back to Start of Loop



