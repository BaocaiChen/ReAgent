from openai import OpenAI
from retro_star.alg.prompts import FORMAT_INSTRUCTIONS, QUESTION_PROMPT, REPHRASE_TEMPLATE, SUFFIX,PREFIX,first_round

def GPTCall(context):
    api_key = "sk-cy0sdvcMI2JB6vWo3c5968E29aFa44A1945e64E29c205320"
    #api_base = "https://api.xi-ai.cn/v1"
    api_base="http://202.120.38.225:38080/v1"
    client = OpenAI(api_key=api_key, base_url=api_base)
    completion = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="llama-3-8b_instruct_hf" ,
        messages=context,
        stop=["<|end_of_text|>", "<|eot_id|>"]
    )
    return completion.choices[0].message.content
if __name__=='__main__':
    context=[
        {"role": "system", "content": PREFIX},
        {"role": "user", "content": ''}
            ]
    print(context)
    print(GPTCall(context))
    # while True:
    #     #prompt=input()
    #     prompt="Please plan the synthesis of nitroglycerin."
    #     if prompt!='stop':
    #         Question=QUESTION_PROMPT.format(Q=[0.1,0.1,0.1],R=[0.5,0.6,0.7])
    #         context.append({"role": "user", "content":Question})
    #         response=(GPTCall(context))
    #         if "Final Answer" in response:
    #             context.append({"role":"assistant","content":response})
    #             print(response)

    #         else:
    #             print(GPTCall([   {"role": "system", "content": PREFIX},
    #                         {"role": "user", "content": FORMAT_INSTRUCTIONS},           
    #                         {"role":"user","content":REPHRASE_TEMPLATE.format(question=Question,agent_ans=response)}]))
                     
    #         print(context)
    #         break
             
    #     else:
    #         break
    #         #print(context)
