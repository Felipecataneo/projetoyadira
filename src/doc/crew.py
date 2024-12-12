from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

# Uncomment the following line to use an example of a custom tool
# from crewai_taipy.tools.custom_tool import MyCustomTool

# Check our tools documentation for more information on how to use them
# from crewai_tools import SerperDevTool

from typing import Callable, Optional
from crewai.tasks.task_output import TaskOutput
# This will store the callback function from crewai_taipy
output_handler: Optional[Callable] = None

def register_output_handler(handler: Callable):
    """Register the output handler from crewai_taipy"""
    global output_handler
    output_handler = handler

def print_output(output: TaskOutput):
    """Bridge function to call Taipy's output handler"""
    if output_handler:
        output_handler(output)
    return output

@CrewBase
class Doc():
    """CrewaiTaipy crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff  # Optional hook to be executed before the crew starts
    def pull_data_example(self, inputs):
        # Example of pulling data from an external API, dynamically changing the inputs
        inputs['extra_data'] = "This is extra data"
        return inputs

    @after_kickoff  # Optional hook to be executed after the crew has finished
    def log_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Results: {output}")
        return output

    @agent
    def planejador_de_recuperacao(self) -> Agent:
        return Agent(
            config=self.agents_config['planejador_de_recuperacao'],
            verbose=True, 
			max_iter=5
        )

    @agent
    def pesquisador(self) -> Agent:
        return Agent(
            config=self.agents_config['pesquisador'],
            verbose=True, 
			max_iter=5
        )

    @agent
    def analista_de_relatorios(self) -> Agent:
        return Agent(
            config=self.agents_config['analista_de_relatorios'],
            verbose=True, 
			max_iter=5
        )

    @task
    def tarefa_pesquisa(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_pesquisa'],
            callback=print_output
        )

    @task
    def tarefa_relatorio(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_relatorio'],
            # output_file='report.md',
            callback=print_output
        )

    @task
    def tarefa_plano_recuperacao(self) -> Task:
        return Task(
            config=self.tasks_config['tarefa_plano_recuperacao'],
            # output_file='recovery_plan.md',
            callback=print_output,
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Doc crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
