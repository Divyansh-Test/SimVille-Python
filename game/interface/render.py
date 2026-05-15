
symbol = {2:["stone", "🪨"], 1:["wood","🌳"], 0: ["Floor","🧱"], -5:["marker","❌"],-1:["empty",""],801:["agent1","😁"]}

def render(marker, rows, cols, layer0, layer1, layer2):
  

    output = []

    for y in rows:

        row = ""

        for x in cols:

            if (y, x) == marker:
                row += "❌"

            elif layer2[y][x] != -1:
                row +=""+ (symbol[layer2[y][x]])[1]+""

            elif layer1[y][x] != -1:
                row +=""+ (symbol[layer1[y][x]])[1]+""

            else:
                row +=""+ (symbol[layer0[y][x]])[1]+""

        output.append(row)

    return output