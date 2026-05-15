
symbol = {2:["stone", "#"], 1:["wood","*"], 0: ["Floor","."], -5:["marker","X"],-1:["empty",""],801:["agent1","@"]}

def  get_info(layer0,layer1,layer2,x,y):
   return {"layer0":symbol[layer0[x][y]][0],"layer1":symbol[layer1[x][y]][0],"layer2":symbol[layer2[x][y]][0]}
  