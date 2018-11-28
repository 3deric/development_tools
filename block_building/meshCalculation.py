#rotation function by "BlackJack" from https://www.python-forum.de/viewtopic.php?t=7127
def rotateLeft(length, value):
    mask = 2**length - 1
    carry_pos = 2**(length - 1)
    return ((value << 1) | int(bool(value & carry_pos))) & mask

def createList():
    #bitmask values of unique meshes
    myBitmaskValues = []
    #bitmask values of permutations of unique meshes
    myPermutations = []
    #loop through all 256 possible cases
    for i in range(0,256):
        #convert the number to binary with 8 digits
        binary = format(i, '08b')
        #split the 8 digit binary into two 4 bit numbers
        p0 = int(binary[:4],2)
        p1 = int(binary[4:],2)
        #loop through all 3 rotation permutations
        for j in range(0, 3):
            # rotate lower and upper layer
            p0 = rotateLeft(4, p0)
            p1 = rotateLeft(4, p1)
            # combine lower and upper layer to a 8 bit binary
            result = int(str(format(p0, '04b')) + str(format(p1, '04b')),2)
            if result is not i:
                #if the result is not i, then add it to the permutation list
                myPermutations.append(result)
        #if i is not a permutation, then add it to the bitmask values
        if i not in myPermutations:
            myBitmaskValues.append(i)

    #print all unique meshes
    #this is for the ideal case, without different floor heights or special layers
    print("requried count of elements: "+ str(len(myBitmaskValues)))
    #loop throug all bitmask values
    for i in myBitmaskValues:
        #print the current bitmask value
        print (i)
        #convert it to binary
        binary = format(int(i) ,'08b')
        #split into two 4 bit numbers
        p0 = int(binary[:4],2)
        p1 = int(binary[4:],2)
        for j in range(0, 3, 1):     
            #rotate it to create the permutations and print the bitmask value and angle    
            #it always prints 3 permutations, there can be less
            p0 = rotateLeft(4, p0)
            p1 = rotateLeft(4, p1)  
            result = int(str(format(p0, '04b')) + str(format(p1, '04b')),2)
            print("     bitmask: " + str(result) + " at " + str((j+1) * 90)+ " deg" )

#execute the script
createList()     
