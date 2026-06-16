"""m08f command-line interface."""
import argparse
import sys
from m08f import config, printer, transport, escpos

def _probe(args) -> int:
    cfg = config.load()
    candidates = [115200, 38400, 19200, 9600]
    test = escpos.initialize() + escpos.density(5)
    test += escpos.raster_block(16, 24, b"\xff" * (16 * 24))
    test += escpos.feed(4)
    for baud in candidates:
        try:
            with transport.open_port(cfg["device"], baud) as port:
                port.send(test)
        except transport.PrinterNotFound as e:
            print(e, file=sys.stderr)
            return 1
        ans = input(f"Baud {baud}: did a clean black bar print? [y/N] ").strip().lower()
        if ans == "y":
            cfg["baud"] = baud
            config.save(cfg)
            print(f"Saved baud={baud}. Config: {config.CONFIG_PATH}")
            return 0
    print("No baud rate produced clean output. Try adjusting paper/printer mode.",
          file=sys.stderr)
    return 1

def _calibrate(args) -> int:
    cfg = config.load()
    test_width_dots = 2000
    width_bytes = (test_width_dots + 7) // 8
    bar = escpos.initialize() + escpos.density(cfg.get("density", 5))
    bar += escpos.raster_block(width_bytes, 48, b"\xff" * (width_bytes * 48))
    bar += escpos.feed(4)
    try:
        with transport.open_port(cfg["device"], cfg["baud"]) as port:
            port.send(bar)
    except transport.PrinterNotFound as e:
        print(e, file=sys.stderr)
        return 1
    val = input("Measured printed bar width in DOTS (count or width_mm * dpi): ").strip()
    cfg["width_dots"] = int(val)
    config.save(cfg)
    print(f"Saved width_dots={val}. Config: {config.CONFIG_PATH}")
    return 0

def _status(args) -> int:
    cfg = config.load()
    print("m08f printer status")
    for k, v in cfg.items():
        print(f"  {k}: {v}")
    return 0

def _print(args) -> int:
    cfg = config.load()
    opts = printer.Options(
        density=args.density,
        cut=args.cut,
        feed_lines=args.feed,
        width_dots=cfg["width_dots"],
    )
    try:
        printer.print_file(args.file, opts, cfg["device"], cfg["baud"], cfg["dpi"])
    except transport.PrinterNotFound as e:
        print(e, file=sys.stderr)
        return 1
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="m08f", description="M08F thermal printer driver")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("print", help="print a PDF or image")
    pp.add_argument("file")
    pp.add_argument("--density", type=int, default=5)
    pp.add_argument("--cut", choices=["None", "Partial", "Full"], default="None")
    pp.add_argument("--feed", type=int, default=3)
    pp.set_defaults(func=_print)

    sub.add_parser("probe", help="detect baud rate").set_defaults(func=_probe)
    sub.add_parser("status", help="show saved config").set_defaults(func=_status)
    sub.add_parser("calibrate", help="measure printable width").set_defaults(func=_calibrate)
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
