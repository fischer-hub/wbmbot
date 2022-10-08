#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication
from src.app import MainWindow
from src import utils, worker



args = utils.arg_parse()


if args.cli:

    bot = worker.Worker()
    bot.args = worker.Args(args.headless_off, args.test, args.log, args.latency_wait, args.interval)    
    bot.test = args.test
    bot.log = args.log
    bot.cli = args.cli
    bot.running = True
    bot.yaml = args.yaml
    bot.experimental = args.experimental
    bot.run()

else:

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()