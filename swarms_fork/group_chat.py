import os
from dotenv import load_dotenv
from swarm_models import OpenAIChat
from typing import Optional
from swarms.structs.groupchat import  *
from prompts.task import daily_regular_meeting_summarize
class AutoGroupMeeting(GroupChat):
    def __init__(
            self,
            preset_stopping_token=True,
            stopping_token:Optional[str] = None,
            stop_prompt:str=None,
            assistant_agent=None,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.preset_stopping_token=preset_stopping_token
        self.stopping_token = stopping_token
        self.stop_prompt = stop_prompt
        if self.stop_prompt is None:
            self.stop_prompt = """
           If you are sure that a conclusion has been reached for the topic of this discussion, please output a special token: <DONE> to end this meeting. (The meeting will only be confirmed as ended when all agents participating in the discussion have output <DONE>.)
            """
        self.assistant_agent=assistant_agent
        if preset_stopping_token is True:
            self.stopping_token = "<DONE>"

    def auto_run(self, task: str):
        """
        Run the group chat.

        Args:
            task (str): The initial message to start the chat.

        Returns:
            ChatHistory: The history of the chat.
        """
        try:

            if self.stopping_token is None or self.stop_prompt is None:
                raise
            logger.info(
                f"Starting chat '{self.name}' with task: {task}"
            )
            task = task + self.stop_prompt
            turn=0
            while(turn<3):
                current_turn = ChatTurn(
                    turn_number=turn, responses=[], task=task
                )
                for agent in self.agents:
                    if self.speaker_fn(
                            self.get_recent_messages(), agent
                    ) and agent.agent_name != 'ADMINISTRATIVE_ASSISTANT':
                        response = self._get_response_sync(
                            agent, task, turn
                        )
                        current_turn.responses.append(response)
                        self.chat_history.total_messages += 1
                        logger.debug(
                            f"Turn {turn}, {agent.name} responded"
                        )

                self.chat_history.turns.append(current_turn)
                # stop_count=0
                # for response in current_turn.responses:
                #     if self.stopping_token in response:
                #         stop_count+=1
                # if len(current_turn.responses) == stop_count:
                #     break;
                turn+=1

            task=daily_regular_meeting_summarize
            current_turn = ChatTurn(
                turn_number=turn, responses=[], task=task
            )
            response = self._get_response_sync(
                        self.assistant_agent, task, turn
                    )
            current_turn.responses.append(response)
            self.chat_history.total_messages += 1
            self.chat_history.turns.append(current_turn)
            return self.chat_history
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise e

    def _get_response_sync(
        self, agent: Agent, prompt: str, turn_number: int
    ) -> AgentResponse:
        """
        Get the response from an agent synchronously.

        Args:
            agent (Agent): The agent responding.
            prompt (str): The message triggering the response.
            turn_number (int): The current turn number.

        Returns:
            AgentResponse: The agent's response captured in a structured format.
        """
        try:
            # Provide the agent with information about the chat and other agents
            chat_info = f"Chat Name: {self.name}\nChat Description: {self.description}\nAgents in Chat: {[a.agent_name for a in self.agents]}"
            context = f"""You are {agent.agent_name} 
                        Conversation History: 
                        \n{chat_info}
                        Other agents: {[a.agent_name for a in self.agents if a != agent]}
                        Previous messages: {self.get_full_chat_history()}
                    
            """  # Updated line

            message = agent.send_agent_message(
                agent.agent_name, context + prompt
            )
            return AgentResponse(
                agent_name=agent.name,
                role=agent.system_prompt,
                message=message,
                turn_number=turn_number,
                preceding_context=self.get_recent_messages(3),
            )
        except Exception as e:
            logger.error(f"Error from {agent.name}: {e}")
            return AgentResponse(
                agent_name=agent.name,
                role=agent.system_prompt,
                message=f"Error generating response: {str(e)}",
                turn_number=turn_number,
                preceding_context=[],
            )
    def get_full_chat_history(self) -> list:
        """
        Get the full chat history formatted for agent context.

        Returns:
            str: The full chat history with sender names.
        """
        messages = []
        for turn in self.chat_history.turns:
            for response in turn.responses:
                messages.append(
                    f"{response.agent_name}: {response.message}"
                )
        return messages


if __name__ == "__main__":

    load_dotenv()


    # Model
    model = OpenAIChat(
        openai_api_key=os.getenv("OPENAI_API_KEY"), model_name="gpt-4o-mini", temperature=0.1,
        openai_api_base="https://api.mixrai.com/v1"
    )

    # Example agents
    agent1 = Agent(
        agent_name="Financial-Analysis-Agent",
        system_prompt="You are a friendly financial analyst specializing in investment strategies. Be approachable and conversational.",
        llm=model,
        max_loops=1,
        dynamic_temperature_enabled=True,
        user_name="swarms_corp",
        output_type="string",
        streaming_on=True,
    )

    agent2 = Agent(
        agent_name="Tax-Adviser-Agent",
        system_prompt="You are a tax adviser who provides clear, concise, and approachable guidance on tax-related queries.",
        llm=model,
        max_loops=1,
        dynamic_temperature_enabled=True,
        user_name="swarms_corp",
        output_type="string",
        streaming_on=True,
    )

    # agent3 = Agent(
    #     agent_name="Stock-Buying-Agent",
    #     system_prompt="You are a stock market expert who provides insights on buying and selling stocks. Be informative and concise.",
    #     llm=model,
    #     max_loops=1,
    #     dynamic_temperature_enabled=True,
    #     user_name="swarms_corp",
    #     retry_attempts=1,
    #     context_length=200000,
    #     output_type="string",
    #     streaming_on=True,
    # )

    agents = [agent1, agent2]

    chat = GroupChat(
        name="Investment Advisory",
        description="Financial, tax, and stock analysis group",
        agents=agents,
    )

    history = chat.run(
        "How to save on taxes for stocks, ETFs, and mutual funds?"
    )

    #print(history.model_dump_json(indent=2))

    print(chat.get_full_chat_history())