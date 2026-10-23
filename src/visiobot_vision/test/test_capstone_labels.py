"""Exercise the real detection callback without a ROS installation."""

import ast
from pathlib import Path
from types import SimpleNamespace
import threading
import time

import pytest


def load_callback():
    """Load only the callback; its ROS annotation is not needed for this test."""
    source = Path(__file__).parents[1] / 'visiobot_vision/day30_capstone_node.py'
    tree = ast.parse(source.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef)
                and n.name == 'YoloCapstoneNode')
    callback = next(n for n in node.body if isinstance(n, ast.FunctionDef)
                    and n.name == '_yolo_callback')
    for argument in callback.args.args:
        argument.annotation = None
    namespace = {'time': time}
    exec(compile(ast.Module(body=[callback], type_ignores=[]), str(source), 'exec'),
         namespace)
    return namespace['_yolo_callback']


@pytest.mark.parametrize('label', ['person', 'person_1', 'person_standing_2', 'human_42'])
def test_person_labels_from_detector_trigger_servo(label):
    state = invoke_callback(label)
    assert state.state == 'SERVO'
    assert state.handoff_triggered is True
    assert state._height == 100.0


@pytest.mark.parametrize('label', ['truck_1', 'car_2', 'person_not_a_track'])
def test_other_classes_do_not_trigger_servo(label):
    state = invoke_callback(label)
    assert state.state == 'PATROL'
    assert state.handoff_triggered is False


def invoke_callback(label):
    running = threading.Event()
    running.set()
    logger = SimpleNamespace(warn=lambda message: None)
    state = SimpleNamespace(is_running=running, state='PATROL',
                            allowed_classes={'person', 'person_standing', 'human'},
                            handoff_triggered=False, get_logger=lambda: logger)
    hypothesis = SimpleNamespace(class_id=label, score=1.0)
    bbox = SimpleNamespace(center=SimpleNamespace(position=SimpleNamespace(x=320.0)),
                           size_y=100.0)
    detection = SimpleNamespace(results=[SimpleNamespace(hypothesis=hypothesis)], bbox=bbox)
    load_callback()(state, SimpleNamespace(detections=[detection]))
    return state
