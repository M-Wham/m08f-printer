"""Tests for the CLI option surface the CUPS backend drives.

The backend (cups/m08f-backend) shells out to `m08f print <file>
--density D --cut C --feed F`. These tests pin the mapping from CLI
flags to printer.Options, complementing tests/test_cli.py (which already
covers --density/--cut pass-through)."""
from m08f import cli, config


def _capture(monkeypatch, tmp_path):
    """Patch print_file to record the Options it receives; isolate config."""
    captured = {}

    def fake_print_file(path, opts, device, baud, dpi):
        captured["path"] = path
        captured["density"] = opts.density
        captured["cut"] = opts.cut
        captured["feed_lines"] = opts.feed_lines
        captured["width_dots"] = opts.width_dots
        captured["device"] = device
        captured["baud"] = baud
        captured["dpi"] = dpi

    monkeypatch.setattr(cli.printer, "print_file", fake_print_file)
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "c.json")
    return captured


def test_feed_flag_maps_to_feed_lines(monkeypatch, tmp_path):
    captured = _capture(monkeypatch, tmp_path)
    f = tmp_path / "doc.pdf"; f.write_bytes(b"%PDF-1.4")
    rc = cli.main(["print", str(f), "--feed", "6"])
    assert rc == 0
    assert captured["feed_lines"] == 6


def test_defaults_when_no_flags(monkeypatch, tmp_path):
    captured = _capture(monkeypatch, tmp_path)
    f = tmp_path / "doc.pdf"; f.write_bytes(b"%PDF-1.4")
    rc = cli.main(["print", str(f)])
    assert rc == 0
    assert captured["density"] == 5
    assert captured["cut"] == "None"
    assert captured["feed_lines"] == 3


def test_width_dots_sourced_from_config(monkeypatch, tmp_path):
    captured = _capture(monkeypatch, tmp_path)
    f = tmp_path / "doc.pdf"; f.write_bytes(b"%PDF-1.4")
    rc = cli.main(["print", str(f)])
    assert rc == 0
    # config.load() supplies width_dots; default config must provide it.
    assert isinstance(captured["width_dots"], int)
    assert captured["width_dots"] > 0


def test_invalid_cut_is_rejected(monkeypatch, tmp_path):
    _capture(monkeypatch, tmp_path)
    f = tmp_path / "doc.pdf"; f.write_bytes(b"%PDF-1.4")
    import pytest
    with pytest.raises(SystemExit):  # argparse rejects bad choice
        cli.main(["print", str(f), "--cut", "Guillotine"])
