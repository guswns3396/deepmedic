import unittest
import sys
import setup
import inference
from io import StringIO
from unittest.mock import patch

CODE_PATH = setup.pathlib.Path(__file__).parent.absolute()
PACKAGE_PATH = CODE_PATH.parent.absolute()
DATA_PATH = str(PACKAGE_PATH) + "/data"

class TestSetup(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		print("SETTING UP CLASS")
		print("-"*20)
		'''
		setup.setupVenv()
		setup.addActivator()
		setup.activate()
		setup.install()
		'''
		print("DONE")

	@classmethod
	def tearDownClass(cls):
		print("TEARING DOWN CLASS")
		print("-"*20)
		cwd = setup.os.getcwd()
		print("Current directory:", cwd)
		print("Changing directory to package directory:", PACKAGE_PATH)
		setup.os.chdir(PACKAGE_PATH)
		print("Removing venv")
		setup.os.system("rm -rf env/")
		print("Changing directory:", cwd)
		setup.os.chdir(cwd)
		print("DONE")

	def setUp(self):
		print("SETTING UP")
		print("Path to code directory:", CODE_PATH)
		print("Path to package directory:", PACKAGE_PATH)
		print("Path to data directory:", DATA_PATH)

		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		setup.os.system("mkdir data")
		setup.os.chdir(cwd)
		print("Changed directory to:",cwd)

		print("DONE")

	def tearDown(self):
		print("TEARING DOWN")

		# reset config files
		cmd = "git checkout -- "
		config_path = "/deepmedic/inference_model/config"
		cmd += str(PACKAGE_PATH) + config_path

		setup.os.system(cmd + "/model/modelConfig.cfg")
		setup.os.system(cmd + "/test/testConfig.cfg")
		setup.os.system(cmd + "/test/testNamesOfPredictions.cfg")
		setup.os.system(cmd + "/test/test_flair.cfg")
		setup.os.system(cmd + "/test/test_t1w.cfg")

		# erase test data
		cwd = setup.os.getcwd()
		print("Current directory:", cwd)
		print("Changing directory to package directory:", PACKAGE_PATH)
		setup.os.chdir(PACKAGE_PATH)
		print("Removing data")
		setup.os.system("rm -rf data/")
		print("Changing directory:", cwd)
		setup.os.chdir(cwd)

		print("DONE")

	def test_displayBIDS_displaysText(self):
		print("ARRANGE - DISPLAYBIDS")
		print("-"*20)
		print("ACT - DISPLAYBIDS")
		print("-"*20)
		output = ""
		with patch("sys.stdout", new=StringIO()) as fake_out:
			inference.displayBIDS()
			output = fake_out.getvalue()

		print("ASSERT - DISPLAYBIDS")
		expected = "Please make sure the data is organized in the following fashion\n"
		expected += "myDataFolder/\n" + "\tSubject1/\n" + "\t\tanat/\n"
		expected += "\t\t\tSubject1_T1W.nii.gz\n" + "\t\t\tSubject1_FLAIR.nii.gz\n"
		self.assertEqual(expected, output)

	def test_modifyMC_modifiesOutputFolder(self):
		print("ARRANGE - MODIFYMC")
		print("-"*20)
		path_mc = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/model/modelConfig.cfg"
		print("Path to MC:", path_mc)

		print("ACT - MODIFYMC")
		print("-"*20)
		inference.modifyMC()

		print("ASSERT - MODIFYMC")
		print("-"*20)
		old = "\"/ifs/loni/faculty/farshid/img/members/jack/dmtest/deepmedic/trial_3_pipeline/output/\""
		with open(path_mc,'r') as f:
			content = f.read()
		index1 = content.find("folderForOutput = ")
		index2 = content.find("#  ================ MODEL PARAMETERS")
		new = content[index1 + len("folderForOutput = "):index2]
		print(old)
		print(new)
		self.assertNotEqual(old, new)

	def test_modifyTC_modifiesOutputFolder(self):
		print("ARRANGE - MODIFYTC")
		print("-"*20)
		path_tc = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/testConfig.cfg"
		print("Path to TC:", path_tc)

		print("ACT - MODIFYTC")
		print("-"*20)
		inference.modifyTC()

		print("ASSERT - MODIFYTC")
		print("-"*20)
		old = "\"/ifs/loni/faculty/farshid/img/members/jack/dmtest/deepmedic/trial_3_pipeline/output/\""
		with open(path_tc,'r') as f:
			content = f.read()
		index1 = content.find("folderForOutput = ")
		substr = "#  [Optional] Path to a saved model, to load parameters from in the beginning of the session. If one is also specified using the command line, the latter will be used."
		index2 = content.find(substr)
		new = content[index1 + len("folderForOutput = "):index2]
		print(old)
		print(new)
		self.assertNotEqual(old, new)

	def test_getAbsolutePath_getsAbsolutePathToDirectory(self):
		print("ARRANGE - GETABSOLUTEPATH")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
		relative_path = "../dm_package/./data"

		print("ACT - GETABSOLUTEPATH")
		print("-"*20)
		output = inference.getAbsolutePath(relative_path)
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ASSERT - GETABSOLUTEPATH")
		print("-"*20)
		expected = str(PACKAGE_PATH) + "/data"
		self.assertEqual(expected,output)

	def test_getSubjects_getsAllSubjectFolders(self):
		print("ARRANGE - GETSUBJECTS")
		print("-"*20)	
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - GETSUBJECTS")
		print("-"*20)
		output = inference.getSubjects(DATA_PATH)

		print("ASSERT - GETSUBJECTS")
		print("-"*20)
		expected = subjects
		self.assertEqual(expected,output)

	def test_modifyCfgs_modifiesPred_all(self):
		print("ARRANGE - MODIFYCFGS (MODIFIESPRED_ALL)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_FLAIR.nii.gz")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIESPRED_ALL)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIESPRED_ALL)")
		print("-"*20)
		path_pred = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/testNamesOfPredictions.cfg"
		with open(path_pred) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = []
		for subject in subjects:
			expected.append(subject + "_WMH.nii.gz")
		self.assertEqual(expected, output)

	def test_modifyCfgs_modifiesPred_combination(self):
		print("ARRANGE - MODIFYCFGS (MODIFIESPRED_COMBINATION)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
		setup.os.system("touch data/sub-01/anat/sub-01_FLAIR.nii.gz")
		setup.os.system("touch data/sub-01/anat/sub-01_T1W.nii.gz")
		setup.os.system("touch data/sub-02/anat/sub-02_FLAIR.nii.gz")
		setup.os.system("touch data/sub-03/anat/sub-03_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIESPRED_COMBINATION)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIESPRED_COMBINATION)")
		print("-"*20)
		path_pred = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/testNamesOfPredictions.cfg"
		with open(path_pred) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = ["sub-01_WMH.nii.gz"]
		self.assertEqual(expected, output)

	def test_modifyCfgs_modifesT1w_all(self):
		print("ARRANGE - MODIFYCFGS (MODIFIEST1W_ALL)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_FLAIR.nii.gz")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIEST1W_ALL)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIEST1W_ALL)")
		print("-"*20)
		path_t1w = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_t1w.cfg"
		with open(path_t1w) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = []
		for subject in subjects:
			expected.append(DATA_PATH + "/" + subject + "/anat/" + subject + "_T1W.nii.gz")
		self.assertEqual(expected, output)

	def test_modifyCfgs_modifesT1w_combination(self):
		print("ARRANGE - MODIFYCFGS (MODIFIEST1W_COMBINATION)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
		setup.os.system("touch data/sub-01/anat/sub-01_FLAIR.nii.gz")
		setup.os.system("touch data/sub-01/anat/sub-01_T1W.nii.gz")
		setup.os.system("touch data/sub-02/anat/sub-02_FLAIR.nii.gz")
		setup.os.system("touch data/sub-03/anat/sub-03_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIEST1W_COMBINATION)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIEST1W_COMBINATION)")
		print("-"*20)
		path_t1w = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_t1w.cfg"
		with open(path_t1w) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = [DATA_PATH + "/sub-01/anat/sub-01_T1W.nii.gz"]
		self.assertEqual(expected, output)

	def test_modifyCfgs_modifesFlair_all(self):
		print("ARRANGE - MODIFYCFGS (MODIFIESFLAIR_ALL)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_FLAIR.nii.gz")
			setup.os.system("touch data/" + subject + "/anat/" + subject + "_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIESFLAIR_ALL)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIESFLAIR_ALL)")
		print("-"*20)
		path_flair = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_flair.cfg"
		with open(path_flair) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = []
		for subject in subjects:
			expected.append(DATA_PATH + "/" + subject + "/anat/" + subject + "_FLAIR.nii.gz")
		self.assertEqual(expected, output)

	def test_modifyCfgs_modifesFlair_combination(self):
		print("ARRANGE - MODIFYCFGS (MODIFIESFLAIR_COMBINATION)")
		print("-"*20)
		# make test data folder
		cwd = setup.os.getcwd()
		print("Current directory:",cwd)
		setup.os.chdir(PACKAGE_PATH)
		print("Changed directory to:", PACKAGE_PATH)
		print("Creating data directory")
		subjects = ["sub-01","sub-02","sub-03"]
		for subject in subjects:
			setup.os.mkdir("data/" + subject)
			setup.os.mkdir("data/" + subject + "/anat")
		setup.os.system("touch data/sub-01/anat/sub-01_FLAIR.nii.gz")
		setup.os.system("touch data/sub-01/anat/sub-01_T1W.nii.gz")
		setup.os.system("touch data/sub-02/anat/sub-02_FLAIR.nii.gz")
		setup.os.system("touch data/sub-03/anat/sub-03_T1W.nii.gz")
		setup.os.chdir(cwd)
		print("Changed directory to:", cwd)

		print("ACT - MODIFYCFGS (MODIFIESFLAIR_COMBINATION)")
		print("-"*20)
		inference.modifyCfgs(DATA_PATH)

		print("ASSERT - MODIFYCFGS (MODIFIESFLAIR_COMBINATION)")
		print("-"*20)
		path_flair = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_flair.cfg"
		with open(path_flair) as f:
			content = f.read()
		output = content.split("\n")
		output.pop()
		expected = [DATA_PATH + "/sub-01/anat/sub-01_FLAIR.nii.gz"]
		self.assertEqual(expected, output)

if __name__ == "__main__":
	unittest.main()
