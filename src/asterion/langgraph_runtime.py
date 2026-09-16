"""Native LangGraph wiring, not a vendored substitute.

Install .[agent]. Its integration tests are separate from the reference runner.
No business side effects occur inside the human interrupt node.
"""
from __future__ import annotations
from pathlib import Path
from .models import ReviewRequest, RunRequest
from .workflow import State, discover, evaluate, intake, next_step, plan, rehearse, seal, event


def build_graph(checkpointer):
    from langgraph.graph import END, START, StateGraph
    from langgraph.types import interrupt

    def review(state: State) -> dict:
        raw = interrupt({"run_id": state["run_id"], "evidence_digest": state["evidence_digest"],
                         "question": "Approve this synthetic handoff capsule, not a production rollout?"})
        request = ReviewRequest.model_validate(raw)
        if request.expected_digest != state["evidence_digest"]:
            raise ValueError("stale or mismatched approval digest")
        status = "APPROVED" if request.decision == "approve" else "REJECTED"
        return {"review": request.model_dump(), "status": status,
                "events": event(state, "human_review", status=status)}

    graph = StateGraph(State)
    for name, node in [("intake", intake), ("discover", discover), ("plan", plan),
                       ("rehearse", rehearse), ("evaluate", evaluate), ("seal", seal), ("human_review", review)]:
        graph.add_node(name, node)
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "discover")
    graph.add_edge("discover", "plan")
    graph.add_edge("plan", "rehearse")
    graph.add_edge("rehearse", "evaluate")
    graph.add_conditional_edges("evaluate", next_step, {"plan": "plan", "seal": "seal"})
    graph.add_conditional_edges("seal", lambda s: "review" if s["status"] == "PENDING_REVIEW" else "done",
                                {"review": "human_review", "done": END})
    graph.add_edge("human_review", END)
    return graph.compile(checkpointer=checkpointer)


def invoke(database: Path, run_id: str, request: RunRequest | None = None,
           review_request: ReviewRequest | None = None) -> State:
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.types import Command
    database.parent.mkdir(parents=True, exist_ok=True)
    with SqliteSaver.from_conn_string(str(database)) as saver:
        graph = build_graph(saver)
        config = {"configurable": {"thread_id": run_id}, "recursion_limit": 100}
        if review_request is not None:
            value = Command(resume=review_request.model_dump())
        elif request is not None:
            value = {"run_id": run_id, "request": request.model_dump(), "events": []}
        else:
            raise ValueError("request or review_request required")
        graph.invoke(value, config=config)
        return dict(graph.get_state(config).values)
