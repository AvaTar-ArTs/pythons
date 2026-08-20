from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer_prompt_cli import transcribe_segment, analyze_transcript


def test_transcribe_uses_new_sdk(tmp_path):
    fake_audio = tmp_path / "seg.mp4"
    fake_audio.write_bytes(b"fake")

    mock_seg = MagicMock()
    mock_seg.start = 0.0
    mock_seg.end = 5.0
    mock_seg.text = "hello world"

    mock_transcript = MagicMock()
    mock_transcript.segments = [mock_seg]

    with patch("analyzer_prompt_cli.client") as mock_client:
        mock_client.audio.transcriptions.create.return_value = mock_transcript
        result = transcribe_segment(str(fake_audio))

    mock_client.audio.transcriptions.create.assert_called_once()
    kwargs = mock_client.audio.transcriptions.create.call_args.kwargs
    assert kwargs["model"] == "whisper-1"
    assert "hello world" in result


def test_analyze_uses_new_sdk():
    mock_completion = MagicMock()
    mock_completion.choices[0].message.content = "Analysis result"

    with patch("analyzer_prompt_cli.client") as mock_client:
        mock_client.chat.completions.create.return_value = mock_completion
        result = analyze_transcript("some transcript text")

    mock_client.chat.completions.create.assert_called_once()
    kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert kwargs["model"] in ("gpt-4o", os.getenv("ANALYZER_MODEL", "gpt-4o"))
    assert result == "Analysis result"
