from .group import AgentGroup
from .agent import Agent
from typing import List
import json

class SubPlan:

    def __init__(self, agent, pre_func_name=None, input=None, post_func_name=None, output=None) -> None:
        self.agent = agent
        self.pre_func_name = pre_func_name
        self.input = input 
        self.post_func_name = post_func_name
        self.output = self.agent if output == None else output
        self.relyon = None

    def get_output(self):
        return self.output
    
    def excute_pre_func(self):
        #prepare input
        if isinstance(self.input, Agent):
            self.relyon = self.input
            input = {self.relyon.name:self.input.get_output()}
            self.input = input
        elif isinstance(self.input, list):
            outputs = {}
            self.relyon = []
            for item in self.input:
                if isinstance(item, Agent):
                    self.relyon.append(item)
                    outputs[item.name] = item.get_output()
                else:
                    raise TypeError('if input is a list type, the variable in list should be consistent of type: Agent type')
            self.input = outputs
        elif isinstance(self.input, dict):
            for key, val in self.input.items():
                if isinstance(val,Agent):
                    self.input[key] = val.get_output()

        ret = self.agent.func_dic[self.pre_func_name](self.input)
        return ret
    
    def excute_post_func(self):
        ret = self.agent.func_dic[self.post_func_name]()
        self.output = ret
        return ret

def create_subplan(agent,pre_func,input,post_func):
    subplan = SubPlan(agent,pre_func,input,post_func)
    return subplan


class Plan:
    def __init__(self,agents: AgentGroup, plan_list=[]) -> None:
        self.agents:AgentGroup = agents
        self.plan_list:list[SubPlan] = []

    def init_plan(self):
        self.plan_list = []

    def push_plan(self,subplan:SubPlan):
        self.plan_list.append(subplan)
        return subplan.output

    def push_parallel_plan(self,subplan_list:List[SubPlan]):
        self.plan_list.append(subplan_list)
        output_list = [out.output for out in subplan_list]
        return output_list

    def pop_plan(self):
        #TODO
        pass

    def get_pre_plan(self):
        #TODO
        pass


    
    def excute(self):
        for plan in self.plan_list:
            if isinstance(plan,SubPlan):
                plan.excute_pre_func()
                self.agents.serial_send(plan.agent)
                plan.excute_post_func()
            elif isinstance(plan,list):
                parallel_agents = []
                for subplan in plan:
                    parallel_agents.append(subplan.agent)
                    subplan.excute_pre_func()
                self.agents.parallel_send(parallel_agents)
                for subplan in plan:
                    subplan.excute_post_func()
    
    def save_log(self,file_path):
        log = self.agents.save_all_messages(file_path)
        log['question_info'] = self.plan_list[0].input
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(json.dumps(log, ensure_ascii=False) + '\n')




