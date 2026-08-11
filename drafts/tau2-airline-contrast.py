"""Airline contrast for the tau2 frame experiment (item 3, exonerating half).

Same injection shape as telecom: replay gold, then gold + one off-task write
(cancel an unrelated reservation). Airline reward_basis includes DB, so the
full-hash comparison should zero the reward.
"""

import json

from tau2.data_model.message import AssistantMessage, ToolCall
from tau2.data_model.tasks import Task
from tau2.domains.airline.environment import get_environment
from tau2.evaluator.evaluator_env import EnvironmentEvaluator

TASK_INDEX = 7
VICTIM_RESERVATION = "4WQ150"  # untouched by gold (gold touches XEHM4B, 59XX6W)


def constructor(solo_mode: bool = False, **kw):
    return get_environment(solo_mode=solo_mode, **kw)


def fresh_initialized_env(task: Task):
    env = constructor()
    init = task.initial_state
    env.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=[],
    )
    return env


def build_trajectory(task: Task, extra_calls: list[ToolCall]):
    env = fresh_initialized_env(task)
    calls = [
        ToolCall(
            id=f"gold_{i}",
            name=a.name,
            arguments=a.arguments,
            requestor=a.requestor,
        )
        for i, a in enumerate(task.evaluation_criteria.actions or [])
    ] + extra_calls
    msgs = []
    for tc in calls:
        resp = env.get_response(tc)
        if resp.error:
            raise RuntimeError(f"tool call {tc.name} errored: {resp.content}")
        msgs.extend(
            [AssistantMessage(role="assistant", content=None, tool_calls=[tc]), resp]
        )
    return msgs, env


def reservation_status(env, reservation_id):
    res = env.tools.get_reservation_details(reservation_id)
    return getattr(res, "status", None) or ("cancelled" if not res.flights else "active")


def grade(task: Task, traj):
    info = EnvironmentEvaluator.calculate_reward(
        environment_constructor=constructor, task=task, full_trajectory=traj
    )
    return {
        "reward": info.reward,
        "reward_basis": [str(b) for b in (info.reward_basis or [])],
        "reward_breakdown": {str(k): v for k, v in (info.reward_breakdown or {}).items()},
        "db_match": info.db_check.db_match if info.db_check else None,
    }


def main():
    with open("data/tau2/domains/airline/tasks.json") as f:
        task = Task.model_validate(json.load(f)[TASK_INDEX])
    print(f"task: {task.id}")
    print(f"reward_basis: {[str(b) for b in task.evaluation_criteria.reward_basis]}")

    baseline_traj, _ = build_trajectory(task, [])
    print("\nBASELINE (gold only):")
    print(json.dumps(grade(task, baseline_traj), indent=2))

    probe = fresh_initialized_env(task)
    before = probe.tools.get_reservation_details(VICTIM_RESERVATION)
    print(f"\nvictim reservation {VICTIM_RESERVATION} flights before: {len(before.flights)}")

    inject = ToolCall(
        id="offtask_0",
        name="cancel_reservation",
        arguments={"reservation_id": VICTIM_RESERVATION},
        requestor="assistant",
    )
    mutated_traj, mut_env = build_trajectory(task, [inject])
    after = mut_env.tools.get_reservation_details(VICTIM_RESERVATION)
    print(f"witness: victim status after: {after.status if hasattr(after, 'status') else after}")

    print("\nMUTATED (gold + off-task cancel of unrelated reservation):")
    print(json.dumps(grade(task, mutated_traj), indent=2))


if __name__ == "__main__":
    main()
