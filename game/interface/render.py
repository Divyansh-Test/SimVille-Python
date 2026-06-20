
symbol = {
    2: ["stone", "◆"],
    1: ["wood", "♣"],
    0: ["floor", "·"],
    -5: ["marker", "×"],
    -1: ["empty", " "],
    101: ["agent1", "@"],
    102: ["agent1", "@"],
    103: ["agent1", "@"],
    
}



def render( rows, cols, layer0, layer1, layer2,marker):
  

    output = []
    

    for y in range(rows):

        row = ""

        for x in range(cols):

            if (x,y) == marker:
                row += " "+"*"+" "
                

            elif layer2[y][x] != -1:
                row +=" "+symbol[layer2[y][x]][1]+" "

            elif layer1[y][x] != -1:
                row +=" "+(symbol[layer1[y][x]])[1]+" "

            else:
                row +=" "+(symbol[layer0[y][x]])[1]+" "

        output.append(row)

    return output