import pytest
import irmark1 as m1
from irmark1.parts.transform import Lambda


def _get_sample_lambda():
    def f():
        return 1
    f.update = f
    return Lambda(f)


@pytest.fixture()
def vehicle():
    v = m1.Vehicle()
    v.add(_get_sample_lambda(), outputs=['test_out'])
    return v


def test_create_vehicle():
    v = m1.Vehicle()
    assert v.parts == []


def test_add_part():
    v = m1.Vehicle()
    v.add(_get_sample_lambda(), outputs=['test_out'])
    assert len(v.parts) == 1


def test_vehicle_run(vehicle):
    vehicle.start(rate_hz=20, max_loop_count=2)
    assert vehicle is not None


def test_should_raise_assertion_on_non_list_inputs_for_add_part():
    vehicle = m1.Vehicle()
    inputs = 'any'
    with pytest.raises(AssertionError):
        vehicle.add(_get_sample_lambda(), inputs=inputs)
        pytest.fail("inputs is not a list: %r" % inputs)


def test_should_raise_assertion_on_non_list_outputs_for_add_part():
    vehicle = m1.Vehicle()
    outputs = 'any'
    with pytest.raises(AssertionError):
        vehicle.add(_get_sample_lambda(), outputs=outputs)
        pytest.fail("outputs is not a list: %r" % outputs)


def test_should_raise_assertion_on_non_boolean_threaded_for_add_part():
    vehicle = m1.Vehicle()
    threaded = 'non_boolean'
    with pytest.raises(AssertionError):
        vehicle.add(_get_sample_lambda(), threaded=threaded)
        pytest.fail("threaded is not a boolean: %r" % threaded)