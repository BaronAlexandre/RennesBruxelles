import os
import pytest
from PIL import Image
from video.scenes import make_intro_clip, make_windows_clip
from video.constants import WINDOW_DELAYS, WINDOW_FREEZE_DURATION


def _dummy_asset(tmp_path):
    img = Image.new("RGB", (320, 240), "#ff0000")
    p = str(tmp_path / "intro.png")
    img.save(p)
    return p


def test_intro_clip_duration(tmp_path):
    clip = make_intro_clip(1920, 1080, asset_path=_dummy_asset(tmp_path))
    assert abs(clip.duration - 3.0) < 0.1


def test_intro_clip_frame_shape(tmp_path):
    clip = make_intro_clip(1920, 1080, asset_path=_dummy_asset(tmp_path))
    frame = clip.get_frame(0)
    assert frame.shape == (1080, 1920, 3)


def test_windows_clip_duration():
    clip = make_windows_clip(1920, 1080)
    expected = sum(WINDOW_DELAYS) + WINDOW_FREEZE_DURATION
    assert abs(clip.duration - expected) < 0.5


def test_windows_clip_frame_shape():
    clip = make_windows_clip(1920, 1080)
    frame = clip.get_frame(0)
    assert frame.shape == (1080, 1920, 3)


from video.scenes import make_blackout_clip, make_philosophical_clip
from video.constants import BLACKOUT_DURATION, CHAR_DELAY, PHILOSOPHICAL_QUESTION, THINK_DURATION, FADE_DURATION


def test_blackout_clip_duration():
    clip = make_blackout_clip(1920, 1080)
    assert abs(clip.duration - BLACKOUT_DURATION) < 0.01


def test_blackout_clip_is_black():
    clip = make_blackout_clip(1920, 1080)
    assert clip.get_frame(0).max() == 0


def test_philosophical_clip_duration():
    expected = len(PHILOSOPHICAL_QUESTION) * CHAR_DELAY + 0.5 + THINK_DURATION + FADE_DURATION
    clip = make_philosophical_clip(1920, 1080)
    assert abs(clip.duration - expected) < 0.5


def test_philosophical_clip_frame_shape():
    clip = make_philosophical_clip(1920, 1080)
    assert clip.get_frame(0).shape == (1080, 1920, 3)


from video.scenes import make_announcement_clip
from video.constants import LINE_DELAY, ANNOUNCEMENT_LINES


def test_announcement_clip_frame_shape():
    clip = make_announcement_clip(1920, 1080)
    assert clip.get_frame(0).shape == (1080, 1920, 3)


def test_announcement_clip_duration():
    clip = make_announcement_clip(1920, 1080)
    # text phase + map fade + hold >= 6s
    assert clip.duration >= 6.0
