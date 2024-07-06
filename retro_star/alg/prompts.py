# flake8: noqa
PREFIX = """
You are an excellent expert in chemistry.
"""

FORMAT_INSTRUCTIONS = """
You can only respond with a single complete
"Thought, Final Answer" format
                                  
Complete format:

Thought: (how do you score the reactions by the provided information)

Final Answer: 
the score of the reactions:
Reaction 1 : (just the number score )
...

"""

'''
Action: (the action name, should be one of [{tool_names}])
Action Input: (the input string to the action)
'''
#print(FORMAT_INSTRUCTIONS.format(tool_names="wiki"))
QUESTION_PROMPT_ori = """
Answer the question below using the following tools:

{tool_strings}

Use the tools provided, using the most specific tool available for each action.
Your final answer should contain all information necessary to answer the question and subquestions.

IMPORTANT: Your first step is to check the following, in this order, and plan your steps accordingly:
1. Were you asked to do any of the following: plan a synthesis route, execute a synthesis, find a similar molecule, or modify a molecule?
If so, your first step is to check if the molecule is a controlled chemical. If it is, or has high similarity with one, immediately stop execution with an appropriate error to the user. Do not continue.
2. Does the question involve any molecules? If so, as a first step, check if any are controlled chemicals. If any are, include a warning in your final answer.
3. Were you asked to plan a synthesis route? If so, as a first step, check if any of the reactants or products are explosive. If any are, include a warning in your final answer.
4. Were you asked to execute a synthesis route? If so, check if any of the reactants or products are explosive. If any are, ask the user for permission to continue.
Do not skip these steps.


Question: {input}
"""
prompt_1="You are a chemist and you are now trying to synthesize a new chemical molecule by designing a pathway that can get it from existing chemical molecules, in this process we have taken the Monte Carlo tree search approach, the root node of the tree is the target molecule, expanding the nodes of the selected molecule will give you a series of reactions that may be able to produce this molecule, the child nodes of each reaction node are the reaction's reactant molecule, take all the reaction nodes as the child nodes of this extended molecule, then the key step is which reaction to choose in the extension, we have two data Q and R, which represent the cost and synthesizability of this reaction, respectively, and you are asked to score the alternative reactions based on these two metrics, the following is a set of reactions Q and R, %s,%s,please score them, and your answer should strictly follow the form below :Reaction 1 = xxx \n,Reaction 2 = xxx ,\n …"
           
QUESTION_PROMPT = """
now you will get a series of reactions with a cost value list Q ,which stands for the cost to finish each reaction, and a synthesizability value list R,which infer to the success probability to realise the reaction,you need to score the reactions according to this two values.
The cost of the reactios : {Q}
The synthesizability of the reactions : {R}
"""
SUFFIX = """
Thought: {agent_scratchpad}
"""
FINAL_ANSWER_ACTION = "Final Answer:"


REPHRASE_TEMPLATE = """In this exercise you will assume the role of a scientific assistant. Your task is to answer the provided question as best as you can, based on the provided solution draft.
The solution draft follows the format "Thought, Action, Action Input, Observation", where the 'Thought' statements describe a reasoning sequence. The rest of the text is information obtained to complement the reasoning sequence, and it is 100% accurate.
Your task is to write an answer to the question based on the solution draft, and the following guidelines:
The text should have an educative and assistant-like tone, be accurate, follow the same reasoning sequence than the solution draft and explain how any conclusion is reached.
Question: {question}

Solution draft: {agent_ans}
Obsevation : {observation}

Answer:
"""


react_prompt_ex={"webthink_simple": "\nQuestion: Musician and satirist Allie Goertz wrote a song about the \"The Simpsons\" character Milhouse, who Matt Groening named after who?\nThought 1: I only need to search Milhouse and find who it is named after.\nAction 1: Search[Milhouse]\nObservation 1: Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening. Milhouse is Bart Simpson's best friend in Mrs. Krabappel's fourth grade class at Springfield Elementary School. He is an insecure, gullible, and less popular child than Bart who is often led into trouble by Bart, who takes advantage of his friend's na\u00c3\u00afvet\u00c3\u00a9. Milhouse is a regular target for school bully Nelson Muntz and his friends Jimbo Jones, Dolph Starbeam and Kearney Zzyzwicz. Milhouse has a crush on Bart's sister, Lisa, a common plot element.\nThought 2: The paragraph does not tell who Milhouse is named after, maybe I can look up \"named after\".\nAction 2: Lookup[named after]\nObservation 2: (Result 1 / 1) Milhouse was designed by Matt Groening for a planned series on NBC, which was abandoned.[4] The design was then used for a Butterfinger commercial, and it was decided to use the character in the series.[5][6] Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous. The name was the most \"unfortunate name Matt Groening could think of for a kid\".[1] Years earlier, in a 1986 Life in Hell comic entitled \"What to Name the Baby\", Groening listed Milhouse as a name \"no longer recommended\".[7] Milhouse is a favorite among the staff as Al Jean noted \"most of the writers are more like Milhouse than Bart\".[1] His last name was given to him by Howard Gewirtz, a freelance writer who wrote the episode \"Homer Defined\". Gewirtz got the name from one of his wife's friends.[8] According to Arden Myrin and Dana Gould (former writer and co-executive producer of The Simpsons), Rob Cohen (Simpsons writer) inspired Milhouse's look.[2]\nThought 3: Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.\nAction 3: Finish[Richard Nixon]"}

first_round="""
Retrosynthetic planning is a critical task in organic chemistry which identifies a series of reactions that can lead to the synthesis of a target product.Now we will give a target molecule and 50 reations which might be able to produce it.Note that these reactions are predicted by the single-step inverse synthesis model and are not necessarily accurate.Also this means that some reactions may have reactants that are predicted to be new chemical molecules rather than ones that we can already produce commercially.Here are some basic definitions:
1, we put all the commercially available molecules in a collection 'building block'.
2, a molecule is solved means that it is in the building block or it has been extended by the single-step model.
3, a reaction is success means all the reactants of it are success;a molecule is success means it is in building_block or at least one of the reactons produces it is success. 
4, each molecule has these attributes: 
    is_open:True for those unsolved molecules , False for those solved.
    is_dead: True for those unsuccessfully expanded,it means that the molecule is not in the building blocks and failed to be expanded by the one_step model.A reaction with a dead reactant means the reaction can't success.)
    is_success:True for those success molecules.
5,each reaction has these attributes:
    is_success:True if all the reactants are success.
    Q_value:an estimate of cost,represents the expected total reaction costs given the synthesizable route,range(0,5).
    R_value:an estimate of synthesizability, represents the probability of generating a synthesizable route,range(0,1).
6,a successful route means all the reactions in the route are success.
7,note that all the reactions are inverse reaction.
Your task is to select the reaction from the following that is most likely to be successful.Note that you can not choose a deadend reaction. 
reaction list:
{reactions}
Your output shuild be :
    (the reaction you choose) 
THERE SHOULD BE NO OTHER CONTENT INCLUDED IN YOUR RESPONSE.
"""
#print(first_round)
N_round="""This is the {N} round.
The expansion result of the one step is :
target molecule:{target}
reaction list :
{reaction_list}
Now ,Please continue to make selections until you find a successful route.
Your output shuild be :
\{ the molecule of the (N) round to expand is:(the reactant molecule you choose)\} OR \{Synthesis Path Finded:(the whole route)\}(If all reactions on a path are successful).
Your response should only be in the JSON format above;THERE SHOULD BE NO OTHER CONTENT INCLUDED IN YOUR RESPONSE.
"""
reaction_list_ex="""
target_mol,reaction success,template,reactants
C[C@H](c1ccccc1)N1C[C@]2(C(=O)OC(C)(C)C)C=CC[C@@H]2C1=S,False,([#8:6]-[C:5](=[O;D1;H0:7])-[C:4]-[CH;D2;+0:3]=[CH;D2;+0:1]-[C:2])>>C=[CH;D2;+0:1]-[C:2].C=[CH;D2;+0:3]-[C:4]-[C:5](-[#8:6])=[O;D1;H0:7],[{'molecule': 'C=CC[C@@H]1C(=S)N([C@H](C)c2ccccc2)C[C@@]1(C=C)C(=O)OC(C)(C)C', 'is_dead': False, 'is_success': False, 'is_open': True}]
"""
#MESSAGES=first_round.format(target="C[C@H](c1ccccc1)N1C[C@]2(C(=O)OC(C)(C)C)C=CC[C@@H]2C1=S",reaction_list=reaction_list_ex)

           
#print(MESSAGES)
