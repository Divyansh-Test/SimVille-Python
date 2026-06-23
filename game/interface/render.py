
symbol = {
    4: ["stone", "◆"],
    1: ["wood", "@"],
    0: ["floor", "·"],
    2:["tree","♣"],
    3:["animal","▼"]
    
}
from logger_config import get_logger
logger=get_logger(__name__)



def render( rows, cols, layer0, layer1, layer2,marker):
  

    output = []
    
    #logger.info(f"layer2{layer2}")
    for y in range(rows):

        row = ""

        for x in range(cols):

            if (x,y) == marker:
                row += " "+"*"+" "
                

            # elif layer2[y][x] != -1:
            #     row +=" "+symbol[layer2[y][x]][1]+" "

            elif layer1[y][x] != -1:
                row +=" "+(symbol[layer1[y][x]//100])[1]+" "

            else:
                row +=" "+(symbol[layer0[y][x]//100])[1]+" "

        output.append(row)

    return output