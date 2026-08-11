"""tau2-bench telecom frame experiment (item 1 of drafts/tau2-frame-audit.md).

Baseline: replay a telecom task's gold action script -> grade.
Mutated:  same gold + one off-task write (suspend an unrelated customer's line) -> grade.
Witness:  victim line status before/after injection, plus db hashes.

Model-free: trajectories are built by executing tool calls against a live env
via Environment.get_response, exactly what the grader's replay re-executes.
"""

import json
import sys

from tau2.data_model.message import AssistantMessage, UserMessage, ToolCall
from tau2.data_model.tasks import Task
from tau2.domains.telecom.environment import get_environment
from tau2.evaluator.evaluator_env import EnvironmentEvaluator

TASKS = "data/tau2/domains/telecom/tasks_full.json"
TASK_INDEX = int(sys.argv[1]) if len(sys.argv) > 1 else 0

VICTIM = {"customer_id": "C1002", "line_id": None}  # line resolved at runtime


def constructor(solo_mode: bool = False, **kw):
    return get_environment(solo_mode=solo_mode, **kw)


def load_task() -> Task:
    with open(TASKS) as f:
        raw = json.load(f)
    return Task.model_validate(raw[TASK_INDEX])


def fresh_initialized_env(task: Task):
    env = constructor()
    init = task.initial_state
    env.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=[],
    )
    return env


def pick_victim_line(env):
    cust = env.tools.get_customer_by_id(VICTIM["customer_id"])
    for line_id in cust.line_ids:
        line = env.tools._get_target_line(VICTIM["customer_id"], line_id)
        if line.status.value == "Active":
            return line.line_id, line.status.value
    raise RuntimeError("no active line on victim customer; pick another")


def build_trajectory(task: Task, extra_calls: list[ToolCall]):
    env = fresh_initialized_env(task)
    calls = [
        ToolCall(id=f"gold_{i}", name=a.name, arguments=a.arguments, requestor=a.requestor)
        for i, a in enumerate(task.evaluation_criteria.actions or [])
    ] + extra_calls
    msgs = []
    for tc in calls:
        resp = env.get_response(tc)
        if resp.error:
            raise RuntimeError(f"tool call {tc.name} errored: {resp.content}")
        wrapper = (
            UserMessage(role="user", content=None, tool_calls=[tc])
            if tc.requestor == "user"
            else AssistantMessage(role="assistant", content=None, tool_calls=[tc])
        )
        msgs.extend([wrapper, resp])
    return msgs, env


def victim_status(env, line_id):
    return env.tools._get_target_line(VICTIM["customer_id"], line_id).status.value


def grade(task: Task, traj):
    info = EnvironmentEvaluator.calculate_reward(
        environment_constructor=constructor,
        task=task,
        full_trajectory=traj,
    )
    return {
        "reward": info.reward,
        "reward_basis": [str(b) for b in (info.reward_basis or [])],
        "reward_breakdown": {str(k): v for k, v in (info.reward_breakdown or {}).items()},
        "db_match": info.db_check.db_match if info.db_check else None,
        "env_assertions": [
            {"func": c.env_assertion.func_name, "met": c.met}
            for c in (info.env_assertions or [])
        ],
    }


def main():
    task = load_task()
    print(f"task: {task.id}")
    print(f"reward_basis: {[str(b) for b in task.evaluation_criteria.reward_basis]}")

    probe = fresh_initialized_env(task)
    line_id, status_before = pick_victim_line(probe)
    print(f"victim: {VICTIM['customer_id']}/{line_id} status_before={status_before}")

    baseline_traj, base_env = build_trajectory(task, [])
    baseline = grade(task, baseline_traj)
    print("\nBASELINE (gold only):")
    print(json.dumps(baseline, indent=2))
    print(f"victim line after baseline replay: {victim_status(base_env, line_id)}")

    inject = ToolCall(
        id="offtask_0",
        name="suspend_line",
        arguments={
            "customer_id": VICTIM["customer_id"],
            "line_id": line_id,
            "reason": "off-task write injected by frame audit",
        },
        requestor="assistant",
    )
    mutated_traj, mut_env = build_trajectory(task, [inject])
    status_after = victim_status(mut_env, line_id)
    print(f"\nwitness: victim line {line_id} {status_before} -> {status_after}")
    if status_after == status_before:
        raise RuntimeError("injection no-opped; witness incomplete, verdict void")

    mutated = grade(task, mutated_traj)
    print("\nMUTATED (gold + off-task suspend_line on unrelated customer):")
    print(json.dumps(mutated, indent=2))

    print("\nSUMMARY:")
    print(
        f"baseline reward={baseline['reward']} mutated reward={mutated['reward']} "
        f"mutated db_match={mutated['db_match']}"
    )


if __name__ == "__main__":
    main()
