from m08f import cli, config

def test_status_prints_config(capsys, monkeypatch, tmp_path):
    monkeypatch.setattr(config, "CONFIG_PATH", tmp_path / "c.json")
    rc = cli.main(["status"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "/dev/ttyACM0" in out
    assert "baud" in out

def test_print_invokes_print_file(monkeypatch, tmp_path):
    called = {}
    def fake_print_file(path, opts, device, baud, dpi):
        called["path"] = path
        called["density"] = opts.density
        called["cut"] = opts.cut
    monkeypatch.setattr(cli.printer, "print_file", fake_print_file)
    f = tmp_path / "doc.pdf"
    f.write_bytes(b"%PDF-1.4")
    rc = cli.main(["print", str(f), "--density", "7", "--cut", "Full"])
    assert rc == 0
    assert called["path"] == str(f)
    assert called["density"] == 7
    assert called["cut"] == "Full"
