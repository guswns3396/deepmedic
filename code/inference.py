import os
import pathlib

CODE_PATH = pathlib.Path(__file__).parent.absolute()
PACKAGE_PATH = CODE_PATH.parent.absolute()

# display required BIDS format
def displayBIDS() -> None:
	print("Please make sure the data is organized in the following fashion")
	print("myDataFolder/")
	print("\tSubject1/")
	print("\t\tanat/")
	print("\t\t\tSubject1_T1W.nii.gz")
	print("\t\t\tSubject1_FLAIR.nii.gz")

# modify modelConfig.cfg
def modifyMC() -> None:
	# get modelConfig.cfg path
	path_mc = str(PACKAGE_PATH)
	path_mc += "/deepmedic/inference_model/config/model/modelConfig.cfg"
	# find stop & append index
	with open(path_mc,'r') as file:
		content = file.read()
	index1 = content.find("folderForOutput = ")
	index2 = content.find("#  ================ MODEL PARAMETERS")
	# modify modelConfig.cfg output folder
	path_o = str(PACKAGE_PATH) + "/deepmedic/inference_model/output/"
	with open(path_mc,'w') as file:
		print(content[:index1 + len("folderForOutput = ")] + "\"" + path_o + "\"" + "\n", file=file)
		print(content[index2:], file=file)

# modify testConfig.cfg
def modifyTC() -> None:
	# get testConfig.cfg path
	path_tc = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/testConfig.cfg"
	# find stop & append index
	with open(path_tc,'r') as file:
		content = file.read()
	index1 = content.find("folderForOutput = ")
	substr = "#  [Optional] Path to a saved model, to load parameters from in the beginning of the session. If one is also specified using the command line, the latter will be used."
	index2 = content.find(substr)
	# modify testConfig.cfg output folder
	path_o = str(PACKAGE_PATH) + "/deepmedic/inference_model/output/"
	with open(path_tc,'w') as file:
		print(content[:index1 + len("folderForOutput = ")] + "\"" + path_o + "\"" + "\n", file=file)
		print(content[index2:], file=file)

# get absolute path to data
def getAbsolutePath(data_path: "path to directory of data") -> str:
	cwd = os.getcwd()
	os.chdir(data_path)
	data_path = os.getcwd()
	os.chdir(cwd)
	return data_path

# get list of subjects
def getSubjects(data_path: "path to directory of data") -> list:
	subjects = []
	dirlist = os.listdir(str(data_path))
	for file in dirlist:
		if os.path.isdir(str(data_path) + "/" + file):
			subjects.append(file)
	subjects.sort()
	return subjects

# modify names of prediction
def modifyPred(subjects: "list of subjects") -> None:
	path_pd = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/testNamesOfPredictions.cfg"
	# open cfg file for writing
	with open(path_pd,'w') as file:
		# write for each subject
		for subject in subjects:
			name = subject + "_WMH.nii.gz"
			print(name, file=file)

# modify test channels & prediction
def modifyCfgs(data_path: "path to directory of data") -> None:
	# channel cfgs
	path_flair = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_flair.cfg"
	path_t1w = str(PACKAGE_PATH) + "/deepmedic/inference_model/config/test/test_t1w.cfg"
	path_cfgs = [path_flair, path_t1w]
	# get all subjects
	subjects_all = getSubjects(data_path)
	subjects = []
	# make sure t1w and flair images are both present
	for subject in subjects_all:
		image_path = str(data_path) + "/" + subject + "/anat"
		hasT1W = os.path.isfile(image_path + "/" + subject + "_T1W.nii.gz")
		hasFLAIR = os.path.isfile(image_path + "/" + subject + "_FLAIR.nii.gz")
		if hasT1W and hasFLAIR:
			subjects.append(subject)
		else:
			print("Missing required image(s) for subject: " + subject)
	# modify channel cfgs
	modalities = ["FLAIR", "T1W"]
	for i in range(0, len(path_cfgs)):
		with open(path_cfgs[i],'w') as file:
			for subject in subjects:
				img = str(data_path) + "/" + subject + "/anat/" + subject + "_" + modalities[i] + ".nii.gz"
				print(img, file=file)
	# modify pred cfg
	modifyPred(subjects)

# run inference
def runInf() -> None:
	# get path to deepmedic
	path_dm = str(PACKAGE_PATH) + "/deepmedic"
	# prepare different parts of command
	run = path_dm + "/" + "deepMedicRun"
	model = "-model " +  path_dm + "/inference_model/config/model/modelConfig.cfg"
	test = "-test " + path_dm + "/inference_model/config/test/testConfig.cfg"
	load = "-load " + path_dm + "/inference_model/output/saved_models/train_t1w+flair/"
	load += "model_t1w+flair.train_t1w+flair.final.2019-11-01.11.44.09.274761.model.ckpt"
	dev = "-dev cuda"
	dev += input("Which GPU to use? ")
	# run command for inference
	# TODO: specify directory for out.txt
	os.system(run + " " +  model + " " + test + " " +  load + " " + dev + " >& " + str(PACKAGE_PATH) + "/out.txt &")
	print("Running inference. You can check the progress using 'cat out.txt | less'")
	print("Or 'jobs' to check if the process is still running")
