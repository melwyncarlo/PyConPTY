# This code is part of the PyConPTY python package.
# PyConPTY: A Python wrapper for the ConPTY (Windows Pseudo-console) API
# Copyright (C) 2025  MELWYN FRANCIS CARLO

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# For queries, contact me at: melwyncarlo@gmail.com


# pylint: disable=too-many-lines
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=use-implicit-booleaness-not-comparison-to-zero
# pylint: disable=use-implicit-booleaness-not-comparison-to-string


###############################################################################


import os
import time
import random
import concurrent.futures
import pytest
from pyconpty import ConPTY


###############################################################################


DEFAULT_NUMBER_OF_RERUNS = 10
I_RANGE = range(12, 0, -1)
DEFAULT_CONSOLE_ARGS_LIST = [None, ()]
FALSE_THEN_TRUE = [False, True]
TRUE_THEN_FALSE = [True, False]
TIMEDELTAS_LIST = [0.1, 0.01, 0]
INTERNALTIMEDELTAS_LIST = [100, 0.01, 1e-3, 0]


###############################################################################


def bgthread(thread_function, args, number_of_reruns):
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=os.cpu_count()
    ) as executor:
        futures = [
            executor.submit(
                thread_function, *((get_conpty_instance(args[0]),) + args[1:])
            )
            for i in range(number_of_reruns)
        ]
        for future in concurrent.futures.as_completed(futures):
            future.result()


def get_conpty_instance(arg):
    return None if arg is None else ConPTY(*arg)


def run_on_main_thread(function_name, args):
    function_name(*((get_conpty_instance(args[0]),) + args[1:]))


def run_on_bg_thread(
    function_name, args, number_of_reruns=DEFAULT_NUMBER_OF_RERUNS
):
    bgthread(function_name, args, number_of_reruns)


###############################################################################


def init(console):
    if console is None:
        console = ConPTY()
    assert console.lasterror == ConPTY.Error.NONE
    assert console.isinitialized
    assert console.lasterror == ConPTY.Error.NONE
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 80
    assert console.height == 24
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_init(console_args):
    run_on_main_thread(init, (console_args,))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_init_bgthread(console_args):
    run_on_bg_thread(init, (console_args,))


###############################################################################


def init_with_resize(console):
    if console is None:
        console = ConPTY(100, 50)
    assert console.isinitialized
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 100
    assert console.height == 50
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.resize(80, 40)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 80
    assert console.height == 40
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", [None, (100, 50)])
def test_init_with_resize(console_args):
    run_on_main_thread(init_with_resize, (console_args,))


@pytest.mark.parametrize("console_args", [None, (100, 50)])
def test_init_with_resize_bgthread(console_args):
    run_on_bg_thread(init_with_resize, (console_args,))


###############################################################################


def size_lower_bounds(console):
    if console is None:
        console = ConPTY(0, 0)
    assert console.isinitialized
    assert console.isinitialized
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 1
    assert console.height == 1
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.resize(0, 0)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 1
    assert console.height == 1
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", [None, (0, 0)])
def test_size_lower_bounds(console_args):
    run_on_main_thread(size_lower_bounds, (console_args,))


@pytest.mark.parametrize("console_args", [None, (0, 0)])
def test_size_lower_bounds_bgthread(console_args):
    run_on_bg_thread(size_lower_bounds, (console_args,))


###############################################################################


def size_upper_bounds(console):
    if console is None:
        console = ConPTY(40000, 40000)
    assert console.isinitialized
    assert console.lasterror == ConPTY.Error.NONE
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 32767
    assert console.height == 32767
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.resize(32768, 32768)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 32767
    assert console.height == 32767
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", [None, (40000, 40000)])
def test_size_upper_bounds(console_args):
    run_on_main_thread(size_upper_bounds, (console_args,))


@pytest.mark.parametrize("console_args", [None, (40000, 40000)])
def test_size_upper_bounds_bgthread(console_args):
    run_on_bg_thread(size_upper_bounds, (console_args,))


###############################################################################


def invalid_init_size(console):
    if console is None:
        console = ConPTY(80.0, 40)
    lasterror_checked = False
    if random.choice(TRUE_THEN_FALSE):
        assert console.lasterror == ConPTY.Error.CONSOLE_WIDTH_NOT_INT
        lasterror_checked = True
    assert not console.isinitialized
    assert console.lasterror == (
        ConPTY.Error.CONPTY_UNINITIALIZED
        if lasterror_checked
        else ConPTY.Error.CONSOLE_WIDTH_NOT_INT
    )
    assert console.width is None
    assert console.height is None
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.inputsent
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.waittocomplete()
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.resize("a", "b")
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.width is None
    assert console.height is None
    console = ConPTY(80, 40.0)
    assert not console.isinitialized
    assert console.lasterror == ConPTY.Error.CONSOLE_HEIGHT_NOT_INT
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width is None
    assert console.height is None
    assert not console.isinitialized
    console = ConPTY("80", 40)
    assert not console.isinitialized
    assert not console.isinitialized
    assert console.lasterror == ConPTY.Error.CONSOLE_WIDTH_NOT_INT
    assert console.width is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.height is None
    assert not console.isinitialized


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", [None, (80.0, 40)])
def test_invalid_init_size(console_args):
    run_on_main_thread(invalid_init_size, (console_args,))


@pytest.mark.parametrize("console_args", [None, (80.0, 40)])
def test_invalid_init_size_bgthread(console_args):
    run_on_bg_thread(invalid_init_size, (console_args,))


###############################################################################


def invalid_resize(console):
    if console is None:
        console = ConPTY()
    assert console.isinitialized
    assert console.isinitialized
    assert console.lasterror == ConPTY.Error.NONE
    assert console.lasterror == ConPTY.Error.NONE
    assert not console.resize(80.0, 40)
    assert console.lasterror == ConPTY.Error.CONSOLE_WIDTH_NOT_INT
    assert console.isinitialized
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 80
    assert console.lasterror == ConPTY.Error.NONE
    assert console.height == 24
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.resize(80, 40.0)
    assert console.lasterror == ConPTY.Error.CONSOLE_HEIGHT_NOT_INT
    assert console.width == 80
    assert console.height == 24
    assert not console.resize("80", 40)
    assert console.lasterror == ConPTY.Error.CONSOLE_WIDTH_NOT_INT
    assert console.lasterror == ConPTY.Error.NONE
    assert console.width == 80
    assert console.height == 24


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_invalid_resize(console_args):
    run_on_main_thread(invalid_resize, (console_args,))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_invalid_resize_bgthread(console_args):
    run_on_bg_thread(invalid_resize, (console_args,))


###############################################################################


def is_not_initialized_or_running(console):
    if console is None:
        console = ConPTY("a", "b")
    lasterror_checked = False
    if random.choice(TRUE_THEN_FALSE):
        assert console.lasterror == ConPTY.Error.CONSOLE_WIDTH_NOT_INT
        lasterror_checked = True
    assert not console.isinitialized
    assert console.lasterror == (
        ConPTY.Error.CONPTY_UNINITIALIZED
        if lasterror_checked
        else ConPTY.Error.CONSOLE_WIDTH_NOT_INT
    )
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.write("")
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.write("abc")
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.writeline("abc")
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.writelines(["abc"])
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.read() is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.readline() is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.readlines() is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.run("abc")
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert not console.kill()
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.processended
    assert console.lasterror == ConPTY.Error.CONPTY_UNINITIALIZED
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", [None, ("a", "b")])
def test_is_not_initialized_or_running(console_args):
    run_on_main_thread(is_not_initialized_or_running, (console_args,))


@pytest.mark.parametrize("console_args", [None, ("a", "b")])
def test_is_not_initialized_or_running_bgthread(console_args):
    run_on_bg_thread(is_not_initialized_or_running, (console_args,))


###############################################################################


def is_initialized_but_not_running(console):
    if console is None:
        console = ConPTY()
    assert console.isinitialized
    assert not console.write("")
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.write("abc")
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.writeline("abc")
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.writelines("abc")
    assert console.lasterror == ConPTY.Error.DATA_NOT_A_LIST_OF_STRINGS
    assert not console.writelines(["abc", 100])
    assert console.lasterror == ConPTY.Error.DATA_NOT_A_LIST_OF_STRINGS
    assert not console.writelines(["abc"])
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.read() is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.readline() is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.readlines() is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.kill()
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.exitcode is None


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_is_initialized_but_not_running(console_args):
    run_on_main_thread(is_initialized_but_not_running, (console_args,))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_is_initialized_but_not_running_bgthread(console_args):
    run_on_bg_thread(is_initialized_but_not_running, (console_args,))


###############################################################################


def run_errors(console):
    if console is None:
        console = ConPTY()
    assert console.isinitialized
    assert not console.run("abc")
    assert console.lasterror == ConPTY.Error.RUN_PROGRAM_NOT_FOUND
    assert console.exitcode is None
    assert not console.kill()
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run(1)
    assert console.lasterror == ConPTY.Error.COMMAND_NOT_A_STRING
    assert console.exitcode is None
    assert not console.run("a" * 32658)
    assert console.lasterror == ConPTY.Error.RUN_PROGRAM_NAME_TOO_LONG
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run("a" * 32767)
    assert console.lasterror == ConPTY.Error.COMMAND_LONGER_THAN_32766_CHARS
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run("abc", stripinput=1)
    assert console.lasterror == ConPTY.Error.STRIPINPUT_NOT_A_BOOLEAN
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run("abc", internaltimedelta="100")
    assert console.lasterror == ConPTY.Error.INTERNALTIMEDELTA_NOT_A_NUMBER
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run("abc", postenddelay=False)
    assert console.lasterror == ConPTY.Error.POSTENDDELAY_NOT_A_NUMBER
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.waittocomplete(waitfor="1")
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    assert not console.waittocomplete(waitfor=1, timedelta="0.1")
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER
    assert console.waittocomplete()
    assert console.lasterror == ConPTY.Error.NONE
    assert console.waittocomplete(waitfor=0)
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_run_errors(console_args):
    run_on_main_thread(run_errors, (console_args,))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
def test_run_errors_bgthread(console_args):
    run_on_bg_thread(run_errors, (console_args,))


###############################################################################


def run_error_program(console, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "error_program.exe"
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=0,
    )
    assert not console.isrunning
    assert console.exitcode == 0xC0000094  # STATUS_INTEGER_DIVIDE_BY_ZERO
    assert console.lasterror == ConPTY.Error.RUNTIME_ERROR


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_error_program(console_args, timedelta, internaltimedelta):
    run_on_main_thread(
        run_error_program, (console_args, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_error_program_bgthread(
    console_args, timedelta, internaltimedelta
):
    run_on_bg_thread(
        run_error_program, (console_args, timedelta, internaltimedelta)
    )


###############################################################################


def run_ipconfig(console, i, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert not console.isrunning
    assert console.run(
        "ipconfig",
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=(random.choice([0, 0.01])),
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode in [None, 0]
    assert console.lasterror in [
        ConPTY.Error.PROCESS_ALREADY_RUNNING,
        ConPTY.Error.RUNTIME_SUCCESS,
    ]
    if console.isrunning:
        while console.isrunning:
            time.sleep(
                (1, 0.5)[i % 2] / (10 ** (((i + (i % 2)) / 2) - (i % 2)))
            )
        assert not console.isrunning
        assert console.exitcode == 0
        assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS


@pytest.mark.repeat(2)
@pytest.mark.parametrize("i", I_RANGE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_ipconfig(console_args, i, timedelta, internaltimedelta):
    run_on_main_thread(
        run_ipconfig, (console_args, i, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("i", I_RANGE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST + [1e-4])
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_ipconfig_bgthread(console_args, i, timedelta, internaltimedelta):
    run_on_bg_thread(
        run_ipconfig, (console_args, i, timedelta, internaltimedelta), 2
    )


###############################################################################


def run_and_wait_ipconfig(console, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert not console.run("ipconfig", waitfor="-1", timedelta="-1")
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert not console.run("ipconfig", waitfor=-1, timedelta="-1")
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.run(
        "ipconfig",
        waitfor=-5,
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=(random.choice([0, 1e-4])),
    )
    assert console.waittocomplete(waitfor=-1, timedelta=timedelta)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    assert console.run(
        "ipconfig",
        waitfor=2.5,
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=(random.choice([0, 1e-4])),
    )
    assert console.waittocomplete(waitfor=-1, timedelta=timedelta)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_and_wait_ipconfig(console_args, timedelta, internaltimedelta):
    run_on_main_thread(
        run_and_wait_ipconfig, (console_args, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_and_wait_ipconfig_bgthread(
    console_args, timedelta, internaltimedelta
):
    run_on_bg_thread(
        run_and_wait_ipconfig, (console_args, timedelta, internaltimedelta)
    )


###############################################################################


def run_and_wait_very_slow_ipconfig(console, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.run(
        "ipconfig",
        waitfor=2.5,
        timedelta=5,
        internaltimedelta=internaltimedelta,
        postenddelay=100,
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS


@pytest.mark.repeat(1)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_and_wait_very_slow_ipconfig(console_args, internaltimedelta):
    run_on_main_thread(
        run_and_wait_very_slow_ipconfig, (console_args, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_run_and_wait_very_slow_ipconfig_bgthread(
    console_args, internaltimedelta
):
    run_on_bg_thread(
        run_and_wait_very_slow_ipconfig, (console_args, internaltimedelta), 1
    )


###############################################################################


def short_silent_program(console, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "short_silent_program.exe",
        ),
        internaltimedelta=internaltimedelta,
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.processended
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    if console.isrunning:
        assert console.lasterror == ConPTY.Error.NONE
        assert console.kill()
        assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_short_silent_program(console_args, internaltimedelta):
    run_on_main_thread(short_silent_program, (console_args, internaltimedelta))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_short_silent_program_bgthread(console_args, internaltimedelta):
    run_on_bg_thread(short_silent_program, (console_args, internaltimedelta))


###############################################################################


def long_silent_program(console, internaltimedelta, postenddelay):
    if console is None:
        console = ConPTY()
    assert console.run(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "long_silent_program.exe",
        ),
        waitfor=(0 if postenddelay == -1 else -1),
        internaltimedelta=internaltimedelta,
        postenddelay=postenddelay,
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    if postenddelay == -1:
        assert console.isrunning
        assert console.lasterror == ConPTY.Error.NONE
        assert console.kill()
        assert console.lasterror == ConPTY.Error.FORCED_TERMINATION
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == (1 if postenddelay == -1 else 0)
    assert console.lasterror == (
        ConPTY.Error.FORCED_TERMINATION
        if postenddelay == -1
        else ConPTY.Error.RUNTIME_SUCCESS
    )
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(2)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
@pytest.mark.parametrize("postenddelay", [-1, 100])
def test_long_silent_program(console_args, internaltimedelta, postenddelay):
    run_on_main_thread(
        long_silent_program, (console_args, internaltimedelta, postenddelay)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
@pytest.mark.parametrize("postenddelay", [-1, 100])
def test_long_silent_program_bgthread(
    console_args, internaltimedelta, postenddelay
):
    run_on_bg_thread(
        long_silent_program, (console_args, internaltimedelta, postenddelay), 2
    )


###############################################################################


def read_errors_init(console, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        "ipconfig",
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=10,
    )
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    return console


def read_errors_read(console, timedelta):
    assert console.read(max_bytes_to_read=1.0, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.MAX_READ_BYTES_NOT_AN_INT
    assert console.read(waitfor="1.0", timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    assert console.read(rawdata=0, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.RAWDATA_NOT_A_BOOLEAN
    assert console.read(timedelta="0.1") is None
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER
    assert console.read(trailingspaces=1, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.TRAILINGSPACES_NOT_A_BOOLEAN
    assert console.read(min_bytes_to_read=1.0, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.MIN_READ_BYTES_NOT_AN_INT
    assert (
        console.read(
            min_bytes_to_read=2, max_bytes_to_read=1, timedelta=timedelta
        )
        is None
    )
    assert console.lasterror == ConPTY.Error.MIN_MORE_THAN_MAX_READ_BYTES
    assert (
        console.read(
            min_bytes_to_read=-1, max_bytes_to_read=0, timedelta=timedelta
        )
        == ""
    )
    assert (
        console.read(
            min_bytes_to_read=0, max_bytes_to_read=0, timedelta=timedelta
        )
        == ""
    )
    assert console.lasterror == ConPTY.Error.NONE


def read_errors_readline(console, timedelta):
    assert console.readline(waitfor="1.0", timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    assert console.readline(rawdata=0, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.RAWDATA_NOT_A_BOOLEAN
    assert console.readline(timedelta="0.1") is None
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER


def read_errors_readlines(console, timedelta):
    assert (
        console.readlines(max_lines_to_read=1.0, timedelta=timedelta) is None
    )
    assert console.lasterror == ConPTY.Error.MAX_READ_LINES_NOT_AN_INT
    assert console.readlines(waitfor="1.0", timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    assert console.readlines(rawdata=0, timedelta=timedelta) is None
    assert console.lasterror == ConPTY.Error.RAWDATA_NOT_A_BOOLEAN
    assert console.readlines(timedelta="0.1") is None
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER
    assert (
        console.readlines(min_lines_to_read=1.0, timedelta=timedelta) is None
    )
    assert console.lasterror == ConPTY.Error.MIN_READ_LINES_NOT_AN_INT
    assert (
        console.readlines(
            min_lines_to_read=2, max_lines_to_read=1, timedelta=timedelta
        )
        is None
    )
    assert console.lasterror == ConPTY.Error.MIN_MORE_THAN_MAX_READ_LINES
    assert (
        console.readlines(
            min_lines_to_read=-1, max_lines_to_read=0, timedelta=timedelta
        )
        == []
    )
    assert (
        console.readlines(
            min_lines_to_read=0, max_lines_to_read=0, timedelta=timedelta
        )
        == []
    )
    assert console.lasterror == ConPTY.Error.NONE


def read_errors(console, timedelta, internaltimedelta):
    console = read_errors_init(console, timedelta, internaltimedelta)
    read_errors_read(console, timedelta)
    read_errors_readline(console, timedelta)
    read_errors_readlines(console, timedelta)


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_errors(console_args, timedelta, internaltimedelta):
    run_on_main_thread(
        read_errors, (console_args, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_errors_bgthread(console_args, timedelta, internaltimedelta):
    run_on_bg_thread(read_errors, (console_args, timedelta, internaltimedelta))


###############################################################################


def readlines(console, multiple_lines, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        "ipconfig",
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=10,
    )
    waitfor = random.choice([-1, 0, 1000])
    if multiple_lines:
        output = console.readlines(waitfor=waitfor, timedelta=timedelta)
        assert output is not None
        if not output:
            assert console.readlines(waitfor=-1, timedelta=timedelta)
    else:
        output = console.readline(waitfor=waitfor, timedelta=timedelta)
        assert output is not None
        if not output:
            assert console.readline(waitfor=-1, timedelta=timedelta)


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("multiple_lines", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_readlines(console_args, multiple_lines, timedelta, internaltimedelta):
    run_on_main_thread(
        readlines, (console_args, multiple_lines, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("multiple_lines", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_readlines_bgthread(
    console_args, multiple_lines, timedelta, internaltimedelta
):
    run_on_bg_thread(
        readlines, (console_args, multiple_lines, timedelta, internaltimedelta)
    )


###############################################################################


def read(console, trailingspaces, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "print_lines_of_text.exe",
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=100,
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    assert console.getoutput(
        trailingspaces=trailingspaces, timedelta=timedelta
    ) == (
        "This is line 1 with newline.\n"
        "This is line 2 with newline.\n"
        "This is line 3 with newline.\n"
        "\n"
        "This is line 5 with newline.\n"
        "This is line 6 WITHOUT newline."
    ) + (
        "     " if trailingspaces else ""
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read(
        waitfor=timedelta, trailingspaces=(not trailingspaces)
    ) == ("" if trailingspaces else "     ")
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("trailingspaces", TRUE_THEN_FALSE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read(console_args, trailingspaces, timedelta, internaltimedelta):
    run_on_main_thread(
        read, (console_args, trailingspaces, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("trailingspaces", TRUE_THEN_FALSE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_bgthread(
    console_args, trailingspaces, timedelta, internaltimedelta
):
    run_on_bg_thread(
        read, (console_args, trailingspaces, timedelta, internaltimedelta)
    )


###############################################################################


def read_and_kill(console, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.run(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "text_interaction.exe"
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
    )
    assert console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    assert (
        console.getoutput(timedelta=timedelta, trailingspaces=False)
        == "What is your name?"
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    assert console.kill()
    assert console.lasterror == ConPTY.Error.FORCED_TERMINATION
    assert console.exitcode == 1
    assert console.lasterror == ConPTY.Error.FORCED_TERMINATION
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.waittocomplete(waitfor=-1, timedelta=timedelta)
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_kill(console_args, timedelta, internaltimedelta):
    run_on_main_thread(
        read_and_kill, (console_args, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_kill_bgthread(console_args, timedelta, internaltimedelta):
    run_on_bg_thread(
        read_and_kill, (console_args, timedelta, internaltimedelta)
    )


###############################################################################


def read_and_resize(console, resize, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    if resize:
        assert console.resize(146 + 1, console.height)
    assert console.runandwait(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "print_long_line_of_text.exe",
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=100,
    )
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    output = console.getoutput(timedelta=timedelta)
    assert len(output) == (146 + int(not resize))
    assert output == (
        "This is a very long line of text of 146 characters, "
        + "containing five space charac"
        + ("\n" if not resize else "")
        + "ters at the end, and terminating without a newline character.     "
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("resize", FALSE_THEN_TRUE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_resize(console_args, resize, timedelta, internaltimedelta):
    run_on_main_thread(
        read_and_resize, (console_args, resize, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("resize", FALSE_THEN_TRUE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_resize_bgthread(
    console_args, resize, timedelta, internaltimedelta
):
    run_on_bg_thread(
        read_and_resize, (console_args, resize, timedelta, internaltimedelta)
    )


###############################################################################


def long_read(console, bulk_read, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.runandwait(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "print_many_lines_of_text.exe",
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
        postenddelay=100,
    )
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    if bulk_read:
        assert len(console.readlines()) == 100
        assert console.lasterror == ConPTY.Error.NONE
        assert console.readlines() == []
    else:
        for i in range(100):
            assert console.readline() == f"Log {100+i+1}: This is line {i+1}."
            assert console.lasterror == ConPTY.Error.NONE
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("bulk_read", FALSE_THEN_TRUE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_long_read(console_args, bulk_read, timedelta, internaltimedelta):
    run_on_main_thread(
        long_read, (console_args, bulk_read, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("bulk_read", FALSE_THEN_TRUE)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_long_read_bgthread(
    console_args, bulk_read, timedelta, internaltimedelta
):
    run_on_bg_thread(
        long_read, (console_args, bulk_read, timedelta, internaltimedelta)
    )


###############################################################################


def long_read_quick(console, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.run(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "print_many_lines_of_text.exe",
        ),
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
    )
    assert (
        len(
            console.readlines(
                waitfor=-1, timedelta=timedelta, min_lines_to_read=100
            )
        )
        == 100
    )
    assert console.lasterror == ConPTY.Error.NONE
    while not console.processended:
        time.sleep(timedelta)
    assert console.kill()
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    while console.isrunning:
        time.sleep(0.01)


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_long_read_quick(console_args, timedelta, internaltimedelta):
    run_on_main_thread(
        long_read_quick, (console_args, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("timedelta", [0])
@pytest.mark.parametrize("internaltimedelta", [0])
def test_long_read_quick_bgthread(console_args, timedelta, internaltimedelta):
    run_on_bg_thread(
        long_read_quick, (console_args, timedelta, internaltimedelta)
    )


###############################################################################


def read_and_write_part_1(console, stripinput, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert console.run(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "text_interaction.exe",
        ),
        stripinput=stripinput,
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
    )
    assert console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    return console


def read_and_write_part_2(console, stripinput, timedelta, internaltimedelta):
    assert console.readline() == ""
    assert console.getoutput(timedelta=timedelta) == "What is your name? "
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    assert console.read() == ""
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    assert console.write(
        "Mr. Melwyn Francis Carlo", waittillsent=True, waitfor=-1
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    if timedelta > 0.1 and internaltimedelta > 0.1:
        assert console.inputsent
    if not stripinput:
        assert (
            console.getoutput(timedelta=timedelta, min_bytes_to_read=1)
            == "Mr. Melwyn Francis Carlo"
        )
    assert console.write("\r\n")
    assert console.lasterror == ConPTY.Error.NONE
    while not console.inputsent:
        time.sleep(0.1)
    assert console.getoutput(timedelta=timedelta, min_bytes_to_read=10) == (
        ("\n" if not stripinput else "")
        + "Hi, Mr. Melwyn Francis Carlo! What's your age? "
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.exitcode is None
    assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
    if random.choice(TRUE_THEN_FALSE):
        assert not console.writeline(100)
        assert console.lasterror == ConPTY.Error.DATA_NOT_A_STRING
        assert console.writeline("100")
    else:
        assert console.sendinput("100")
    assert console.lasterror == ConPTY.Error.NONE
    output = console.getoutput(timedelta=timedelta, trailingspaces=False)
    possible_outputs_list = [
        "" if stripinput else "100\n",
        ("" if stripinput else "100\n")
        + "Hmm, so you will be 110 years old in 10 years.",
    ]
    assert output in possible_outputs_list
    if output == possible_outputs_list[0]:
        assert console.exitcode is None
        assert console.lasterror == ConPTY.Error.PROCESS_ALREADY_RUNNING
        assert (
            console.getoutput(timedelta=timedelta)
            == "Hmm, so you will be 110 years old in 10 years."
        )
        assert console.lasterror == ConPTY.Error.NONE


def read_and_write_part_3(console, timedelta):
    assert console.waittocomplete(timedelta=timedelta)
    assert console.lasterror == ConPTY.Error.NONE
    assert console.kill()
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS


def read_and_write(console, stripinput, timedelta, internaltimedelta):
    console = read_and_write_part_1(
        console, stripinput, timedelta, internaltimedelta
    )
    read_and_write_part_2(console, stripinput, timedelta, internaltimedelta)
    read_and_write_part_3(console, timedelta)


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("stripinput", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_write(
    console_args, stripinput, timedelta, internaltimedelta
):
    run_on_main_thread(
        read_and_write,
        (console_args, stripinput, timedelta, internaltimedelta),
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("stripinput", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_read_and_write_bgthread(
    console_args, stripinput, timedelta, internaltimedelta
):
    run_on_bg_thread(
        read_and_write,
        (console_args, stripinput, timedelta, internaltimedelta),
    )


###############################################################################


def write_notes(console, stripinput, timedelta, internaltimedelta):
    if console is None:
        console = ConPTY()
    assert not console.write("abc")
    assert console.lasterror == ConPTY.Error.NO_PROCESS_FOUND
    assert console.run(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "write_notes.exe"
        ),
        stripinput=stripinput,
        timedelta=timedelta,
        internaltimedelta=internaltimedelta,
    )
    console.write(100)
    assert console.lasterror == ConPTY.Error.DATA_NOT_A_STRING
    console.write("My Notes\n", waitfor=True)
    assert console.lasterror == ConPTY.Error.WAITFOR_NOT_A_NUMBER
    console.write("My Notes\n", timedelta=False)
    assert console.lasterror == ConPTY.Error.TIMEDELTA_NOT_A_NUMBER
    console.write("My Notes\n", waittillsent=0)
    assert console.lasterror == ConPTY.Error.WAITTILLSENT_NOT_A_BOOLEAN
    waitfor = random.choice([-1, 0, 1000])
    assert console.write("", waitfor=waitfor, timedelta=timedelta)
    input_notes = [
        "Today is Sunday.",
        "I have to do my chores.",
        "I have to telephone my friend.",
        " Hack the parental control system.",
        "  Munch on some jelly beans.",
    ]
    notes_total_length = sum(len(text) for text in input_notes)
    assert console.sendinput(
        input_notes[0], waitfor=waitfor, timedelta=timedelta
    )
    assert console.lasterror == ConPTY.Error.NONE
    assert console.writelines(
        input_notes[1:], waitfor=waitfor, timedelta=timedelta
    )
    assert console.lasterror == ConPTY.Error.NONE
    if random.choice(TRUE_THEN_FALSE):
        while not console.inputsent:
            time.sleep(0.1)
    output_notes = [
        f"Line #{str(i + 1).zfill(2)}: {note}"
        for i, note in enumerate(input_notes)
    ]
    io_notes = ([] if stripinput else input_notes) + output_notes
    if random.choice(TRUE_THEN_FALSE):
        assert console.getoutput(
            min_bytes_to_read=(notes_total_length * (1 if stripinput else 1))
        ) == "\n".join(io_notes + [""])
    else:
        assert console.readlines(min_lines_to_read=5, waitfor=-1) == io_notes
    assert console.lasterror == ConPTY.Error.NONE
    assert console.waittocomplete()
    assert console.kill()
    assert console.exitcode == 0
    assert console.lasterror == ConPTY.Error.RUNTIME_SUCCESS


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("stripinput", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_write_notes(console_args, stripinput, timedelta, internaltimedelta):
    run_on_main_thread(
        write_notes, (console_args, stripinput, timedelta, internaltimedelta)
    )


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("stripinput", FALSE_THEN_TRUE)
@pytest.mark.parametrize("timedelta", TIMEDELTAS_LIST)
@pytest.mark.parametrize("internaltimedelta", INTERNALTIMEDELTAS_LIST)
def test_write_notes_bgthread(
    console_args, stripinput, timedelta, internaltimedelta
):
    run_on_bg_thread(
        write_notes, (console_args, stripinput, timedelta, internaltimedelta)
    )


###############################################################################


def vts_display(console, enable_vts):
    if console is None:
        console = ConPTY()
    assert console.isinitialized
    assert not console.isrunning
    assert console.lasterror == ConPTY.Error.NONE
    if enable_vts:
        assert console.enablevts()
    else:
        if random.choice(TRUE_THEN_FALSE):
            assert console.disablevts()
        else:
            assert console.resetdisplay()


@pytest.mark.repeat(DEFAULT_NUMBER_OF_RERUNS)
@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("enable_vts", FALSE_THEN_TRUE)
def test_vts_display(console_args, enable_vts):
    run_on_main_thread(vts_display, (console_args, enable_vts))


@pytest.mark.parametrize("console_args", DEFAULT_CONSOLE_ARGS_LIST)
@pytest.mark.parametrize("enable_vts", FALSE_THEN_TRUE)
def test_vts_display_bgthread(console_args, enable_vts):
    run_on_bg_thread(vts_display, (console_args, enable_vts))


###############################################################################


if __name__ == "__main__":
    pytest.main()
