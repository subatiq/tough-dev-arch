from brokereg.registry import validate_event_schema

from src.tasks.events import AssigneeShuffled, TaskAdded, TaskCompleted
from hypothesis import given, settings, strategies as st

from src.users.events import UserCreated, UserUpdated


@settings(max_examples=1)
@given(st.builds(TaskAdded, id=st.uuids(), pub_id=st.uuids()))
def test_task_added(event: TaskAdded):
    validate_event_schema(event)


@settings(max_examples=1)
@given(st.builds(TaskCompleted, id=st.uuids(), pub_id=st.uuids()))
def test_task_completed(event: TaskCompleted):
    validate_event_schema(event)


@settings(max_examples=1)
@given(st.builds(AssigneeShuffled, id=st.uuids(), pub_id=st.uuids()))
def test_assignee_shuffled(event: AssigneeShuffled):
    validate_event_schema(event)


@settings(max_examples=1)
@given(st.builds(UserCreated, id=st.uuids(), pub_id=st.uuids()))
def test_user_created(event: UserCreated):
    validate_event_schema(event)


@settings(max_examples=1)
@given(st.from_type(UserUpdated))
def test_user_updated(event: UserUpdated):
    validate_event_schema(event)

