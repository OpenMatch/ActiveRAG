import copy
from itertools import islice
from .prompt import Prompt
from .agent import *
from .group import *
from .plan import *
import json
from datetime import datetime
import traceback


def create_agent_group(prompt:Prompt): 
    empty_dict = {}
    group = AgentGroup(empty_dict)

    key_map = {
        'cot':          'reply',
        'anchoring':  'unknown_knowledge_reply',
        'associate':  'recite_knowledge_reply',
        'logician':     'logic_knowledge_reply',
        'cognition': 'fact_knowledge_reply',
    }

    for key, val in prompt.template.items():
        group.add_agent(Agent(template=val,key_map=key_map),key)
    return group

def create_plan(group:AgentGroup, init_input:dict)->Plan:
    '''
    init_input: A dict, whose key should match the variable in the template
    the init_input dict should include keys: question、choices_combined、passages
    '''
    
    plan = Plan(group)

    step1_output = plan.push_plan(
        SubPlan(
            agent=plan.agents.agent_dic['cot'],
            pre_func_name='padding_template',
            input=init_input,
            post_func_name='default'
        )
    )


    def prepare_first_round(self: Agent, input):
        self.TEMPLATE = self.template_list[1]
        input[self.name] = self.get_output()
        self.padding_template(input)

    plan.agents.agent_dic['anchoring'].   regist_fn(prepare_first_round,'prepare_first_round')
    plan.agents.agent_dic['associate'].   regist_fn(prepare_first_round,'prepare_first_round')
    plan.agents.agent_dic['logician'].      regist_fn(prepare_first_round,'prepare_first_round')
    plan.agents.agent_dic['cognition'].  regist_fn(prepare_first_round,'prepare_first_round')

    new_init_input = copy.deepcopy(init_input)
    # new_init_input['passages'] = init_input
    new_init_input['reply'] = step1_output

    plan.push_parallel_plan([
        SubPlan(
            agent=plan.agents.agent_dic['anchoring'],
            pre_func_name='padding_template',
            input=new_init_input,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['associate'],
            pre_func_name='padding_template',
            input=new_init_input,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['logician'],
            pre_func_name='padding_template',
            input=new_init_input,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['cognition'],
            pre_func_name='padding_template',
            input=new_init_input,
            post_func_name='default'
        )
    ])

    first_round_input = copy.deepcopy(init_input)
    first_round_input['reply'] = step1_output
    origin_cot = first_round_input

    multi_chain = plan.push_parallel_plan([
        SubPlan(
            agent=plan.agents.agent_dic['anchoring'],
            pre_func_name='prepare_first_round',
            input=origin_cot,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['associate'],
            pre_func_name='prepare_first_round',
            input=origin_cot,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['logician'],
            pre_func_name='prepare_first_round',
            input=origin_cot,
            post_func_name='default'
        ),
        SubPlan(
            agent=plan.agents.agent_dic['cognition'],
            pre_func_name='prepare_first_round',
            input=origin_cot,
            post_func_name='default'
        )
    ])

    return plan