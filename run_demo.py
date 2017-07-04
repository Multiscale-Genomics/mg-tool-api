import sys
import demos
import importlib
import pycompss_mock

if __name__ == '__main__':
    demoname = sys.argv[1]
    try:
        demo = importlib.import_module("demos.{}".format(demoname))
    except ImportError:
        sys.stderr.write("ERROR: Couldn't run demo {}.".format(demoname))
        sys.exit(1)

    demo.main()
