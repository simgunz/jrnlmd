import datetime
from unittest import mock

import pytest

from jrnlmd.jrnlmd import parse_input


def test_input_date_only():
    txt_input = "12 nov 2021:"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert topic is None
    assert note is None


def test_input_single_note_with_topic_only():
    txt_input = "topic1 is this"
    date, topic, note = parse_input(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert note is None


def test_input_single_note_with_topic():
    txt_input = "topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert date is None
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_single_note_with_date_and_topic():
    txt_input = "12nov2021: topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_single_note_with_date_with_space_and_topic():
    txt_input = "12 nov 2021: topic1 is this . a note"
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- a note\n" == note


def test_input_multiple_notes_with_date_and_topic():
    txt_input = (
        "12nov2021: topic1 is this . first bullet , second bullet , third bullet"
    )
    date, topic, note = parse_input(txt_input)
    assert "2021-11-12" == date
    assert "topic1 is this" == topic
    assert "- first bullet\n- second bullet\n- third bullet\n" == note


@mock.patch("jrnlmd.jrnlmd.input_from_editor")
def test_input_with_user_input(mock_input_from_editor):
    mock_input_from_editor.return_value = "a note"
    txt_input = "topic1 is this . @"
    _, _, note = parse_input(txt_input)
    assert "- a note\n" == note


@mock.patch("jrnlmd.jrnlmd.input_from_editor")
def test_input_with_multiple_user_input(mock_input_from_editor):
    mock_input_from_editor.side_effect = ["first note", "second note"]
    txt_input = "topic1 is this . @ , @"
    _, _, note = parse_input(txt_input)
    assert "- first note\n- second note\n" == note


@mock.patch("jrnlmd.jrnlmd.input_from_editor")
def test_input_with_multiline_user_input(mock_input_from_editor):
    mock_input_from_editor.return_value = "a note\non two lines"
    txt_input = "topic1 is this . @"
    _, _, note = parse_input(txt_input)
    assert "- a note\non two lines\n" == note
