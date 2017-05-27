import re
from sre_parse import Pattern

with open("/Users/cancui/workspace/LCCAnalysisSystem/resources/phpgameprotocols/ultimategame.inst","r") as protocol:
    protocollines=protocol.readlines()

    pattern_n=re.compile(r'^\\n&')
    search_n=re.findall(pattern_n, protocollines[0])
    print search_n
    
    linepoint=0
    agent=( )
    print type(agent)
    while linepoint<len(protocollines):
        if "::=" in protocollines[linepoint]:
            print "yes"
            l=linepoint+1
            agent=agent + (l,)
        else:
            print "no"
        linepoint+=1
    
  
        