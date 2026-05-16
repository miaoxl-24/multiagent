from langchain_community.chat_models import ChatTongyi
from operator import add
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph,START,END
from config.load_key import load_key

nodes = ["supervisor", "travel", "couplet", "joke", "other"]

llm = ChatTongyi(
    model="qwen-plus",
    api_key=load_key("BAILIAN_API_KEY")
)

class State(TypedDict):  # 标注：7用法
    messages: Annotated[list[AnyMessage], add]
    type: str


def other_node(state: State):  # 标注：1个用法
    print(">>> other_node")
    writer = get_stream_writer()
    writer({"node", ">>> other_node"})
    return {
        "messages": [HumanMessage(content="我暂时无法回答这个问题")],
        "type": "other"
    }
def supervisor_node(state: State):
    print(">>> supervisor_node")
    writer = get_stream_writer()
    writer({"node", ">>>> supervisor_node"})
    prompt = """你是一个专业的客服助手，负责对用户的问题进行分类，并将任务分给其他Agent执行。
    如果用户的问题是和旅游路线规划相关的，那就返回 travel 。
    如果用户的问题是希望讲一个笑话，那就返回 joke 。
    如果用户的问题是希望对一个对联，那就返回 couplet 。
    如果是其他的问题，返回 other 。
    除了这几个选项外，不要返回任何其他的内容。
    """

    prompts = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": state["messages"][0]}
    ]
    if "type" in state:
        writer({"supervisor_step", f"已获得{state['type']} 智能体处理结果"})
        return {"type": END}

    else:
        response = llm.invoke(prompts)
        typeRes = response.content
        writer({"supervisor_step", f"问题分类结果: {typeRes}"})
        if typeRes in nodes:
            return {"type": typeRes}
        else:
            raise ValueError("type is not in (travel,joke,other,couplet)")

    return {}



def travel_node(state: State):
    print(">>> travel_node")
    writer = get_stream_writer()
    writer({"node", ">>>> travel_node"})

    return {
        "messages": [HumanMessage(content="travel_node")],
        "type": "travel"
    }
def joke_node(state: State):
    print(">>> joke_node")
    writer = get_stream_writer()
    writer({"node", ">>> joke_node"})



    system_prompt = "你是一个笑话大师，根据用户的问题，写一个不超过100个字的笑话。"

    prompts = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": state["messages"][0]}
        ]
    response = llm.invoke(prompts)
    writer({"joke_result": response.content})

    return {"messages": [HumanMessage(content=response.content)], "type": "joke"}




def couplet_node(state: State):
    print(">>> couplet_node")
    writer = get_stream_writer()
    writer({"node", ">>> couplet_node"})

    return {"messages": [HumanMessage(content="couplet_node")], "type": "couplet"}


def routing_func(state: State):
    if state["type"] == "travel":
        return "travel_node"
    elif state["type"] == "joke":
        return "joke_node"
    elif state["type"] == "couplet":
        return "couplet_node"
    elif state["type"] == END:
        return END
    else:
        return "other_node"


builder = StateGraph(State)


builder.add_node("supervisor_node", supervisor_node)
builder.add_node("travel_node", travel_node)
builder.add_node("joke_node", joke_node)
builder.add_node("couplet_node", couplet_node)
builder.add_node("other_node", other_node)

# 添加Edge
builder.add_edge(START, "supervisor_node")
builder.add_conditional_edges("supervisor_node", routing_func, path_map=["travel_node", "joke_node", "couplet_node", "other_node",END])
builder.add_edge(start_key="travel_node", end_key="supervisor_node")
builder.add_edge(start_key="joke_node", end_key="supervisor_node")
builder.add_edge(start_key="couplet_node", end_key="supervisor_node")
builder.add_edge(start_key="other_node", end_key="supervisor_node")
# 构建Graph
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 执行任务的测试代码
# 执行任务的测试代码
if __name__ == "__main__":
    config = {
        "configurable":{
            "thread_id": "1"
        }
    }

    for chunk in graph.stream( input={"messages": ["给我讲一个郭德纲的笑话"]}
        ,config=config
        ,stream_mode="custom"):
        print(chunk)