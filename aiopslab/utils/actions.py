# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import importlib


def action(method):
    """
    Decorator to mark a method as an action.

    Args:
        method (function): The method to mark as an action.

    Returns:
        function: The decorated method.
    """
    method.is_action = True
    return method


def read_bug(method):
    """
    Decorator to mark a method as a read action.

    Args:
        method (function): The method to mark as a read action.

    Returns:
        function: The decorated method.
    """
    method.is_action = True
    method.action_type = "read"
    method.bug = True
    return method


def read(method):
    """
    Decorator to mark a method as a read action.

    Args:
        method (function): The method to mark as a read action.

    Returns:
        function: The decorated method.
    """
    method.is_action = True
    method.action_type = "read"
    method.bug = False
    return method


def write_bug(method):
    """
    Decorator to mark a method as a write action.

    Args:
        method (function): The method to mark as a write action.

    Returns:
        function: The decorated method.
    """
    method.is_action = True
    method.action_type = "write"
    method.bug = True
    return method


def write(method):
    """
    Decorator to mark a method as a write action.

    Args:
        method (function): The method to mark as a write action.

    Returns:
        function: The decorated method.
    """
    method.is_action = True
    method.action_type = "write"
    method.bug = False
    return method


def get_actions(
    task: str, subtype: str | None = None, incorrect_actions: list[str] | None = None
) -> dict:
    """
    Get all actions for the given task.
        key: action name
        value: docstring of the action

    Args:
        task (str): The name of the task.
        subtype (str): The subtype of the action (optional) (default: None).

    Returns:
        dict: A dictionary of actions for the given task.
    """

    if incorrect_actions is None:
        incorrect_actions = []

    class_name = task.title() + "Actions"
    module = importlib.import_module("aiopslab.orchestrator.actions." + task)
    class_obj = getattr(module, class_name)

    bugged_module = importlib.import_module(
        "aiopslab.orchestrator.bugged_actions." + task
    )
    bugged_class = getattr(bugged_module, class_name)

    actions = {
        method: getattr(class_obj, method).__doc__.strip()
        for method in dir(class_obj)
        if callable(getattr(class_obj, method))
        and getattr(getattr(class_obj, method), "is_action", False)
        and method not in incorrect_actions
    }

    bugged_actions = {
        method: getattr(bugged_class, method).__doc__.strip()
        for method in dir(bugged_class)
        if callable(getattr(bugged_class, method))
        and getattr(getattr(bugged_class, method), "is_action", False)
    }

    for bugs in incorrect_actions:
        if bugs not in bugged_actions.keys():
            raise ValueError(f"Action {bugs} is not in bugged_actions")

        actions[bugs] = bugged_actions[bugs]

        print(f"Replaced action {bugs} with bugged version")

    if subtype:
        actions = {
            method: doc
            for method, doc in actions.items()
            if getattr(getattr(class_obj, method), "action_type", None) == subtype
        }

    print("DONE")

    return actions
