import json
#json
a_string=json.dumps(
    {
        "institution":"int8282",
        "protocolid":"ultimategame",
        "msgseq":[{
            "msgreceiver":"peter",
            "msgsender":"richard",
            "msgbody":{"mname":"offer","mvars":["2"]}
            },{
                "msgreceiver":"richard",
                "msgsender":"peter",
                "msgbody":{"mname":"acceptornot","mvars":["reject","2"]}
            }
        ]
    }
)

decode_data=json.loads(a_string)
print str(decode_data['msgseq'][1]['msgbody']['mvars'])


with open("/Users/cancui/workspace/LCCAnalysisSystem/agentstate.json","w") as f:
    json.dump(a_string,f)

with open("/Users/cancui/workspace/LCCAnalysisSystem/agentstate.json","r") as fo:
    da=json.load(fo)

    
