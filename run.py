import sys
from code import setup
from code import inference

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Not enough command line arguments")
	else:
		# setup venv & install dependencies
		if sys.argv[1] == '1' and len(sys.argv) == 2:
			setup.setupVenv()
			setup.addActivator()
			setup.activate()
			setup.install()
		# run inference
		elif sys.argv[1] == '2' and len(sys.argv) == 3:
			inference.displayBIDS()

			setup.activate()

			inference.modifyMC()
			inference.modifyTC()

			inference.modifyCfgs(inference.getAbsolutePath(sys.argv[2]))

			inference.runInf()
		else:
			print("Invalid command line argument(s)")
