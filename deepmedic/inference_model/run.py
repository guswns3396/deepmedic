import os
import shutil

# ask user for path to their data
def getPathToData() -> str:
	print("Please make sure the data is organized in the following fashion")
	print("myDataFolder/")
	print("\tSubject1/")
	print("\t\tt1w.nii.gz")
	print("\t\tflair.nii.gz")
	path_d = input("Absolute path to data: ")
	if path_d[-1] != "/":
		path_d += "/"
	return path_d

# modify modelConfig.cfg
def modifyMC() -> None:
	# get modelConfig.cfg path
	path_mc = os.getcwd() + "/config/model/modelConfig.cfg"
	# find stop & append index
	modelConfig = open(path_mc, "r")
	content = ""
	for line in modelConfig:
		content += line
	index1 = content.find("folderForOutput = ")
	index2 = content.find("#  ================ MODEL PARAMETERS")
	modelConfig.close()
	# modify modelConfig.cfg output folder
	path_o = os.getcwd() + "/output/"
	modelConfig = open(path_mc, "w")
	print(content[:index1 + len("folderForOutput = ")] + "\"" +
		path_o + "\"" + "\n", file=modelConfig)
	print(content[index2:], file=modelConfig)
	modelConfig.close()

# modify testConfig.cfg
def modifyTC() -> None:
	# get testConfig.cfg path
	path_tc = os.getcwd() + "/config/test/testConfig.cfg"
	# find stop & append index
	testConfig = open(path_tc, "r")
	content = ""
	for line in testConfig:
		content += line
	index1 = content.find("folderForOutput = ")
	substr = "#  [Optional] Path to a saved model, to load parameters from in the beginning of the session. If one is also specified using the command line, the latter will be used."
	index2 = content.find(substr)
	testConfig.close()
	# modify testConfig.cfg output folder
	path_o = os.getcwd() + "/output/"
	testConfig = open(path_tc, "w")
	print(content[:index1 + len("folderForOutput = ")] + "\"" +
		path_o + "\"" + "\n", file=testConfig)
	print(content[index2:], file=testConfig)
	testConfig.close()

# modify names of prediction
def modifyPred(subs: "list of subjects") -> None:
	# get path to pred cfg
	path_pd = os.getcwd() + "/config/test/testNamesOfPredictions.cfg"
	# open cfg file for writing
	cfgFile = open(path_pd, "w")
	# write for each subject:
	for sub in subs:
		# get name of prediction
		name = "pred_" + sub + ".nii.gz"
		# write to cfg
		print(name, file=cfgFile)

# modify test channels & prediction
def modifyCfgs() -> None:
	# ask for path to data
	path_d = getPathToData()
	# channel cfgs
	path_flair = os.getcwd() + "/config/test/test_flair.cfg"
	path_t1w = os.getcwd() + "/config/test/test_t1w.cfg"
	path_cfgs = [path_flair, path_t1w]
	# modalities
	modal = ["flair", "t1w"]
	# get subjects
	subjects_all = os.listdir(path_d)
	subjects_all.sort()
	# get subjects for each modality
	subjects_mod = []
	for i in range(0, len(path_cfgs)):
		subs = []
		for sub in subjects_all:
			# get path of image for subject
			path = path_d + sub + "/" + modal[i] + ".nii.gz"
			# make sure file exists
			if os.path.isfile(path):
				subs.append(sub)
		subjects_mod.append(subs)
	# check if subjects match for all modalities
	for mod in subjects_mod:
		if subjects_mod[0] != mod:
			## TODO: show which image doesn't match
			raise ValueError("Images for all modalities must match!")
	print("Images for all modalities matched!")
	# extract path to image according to modality
	for i in range(0, len(path_cfgs)):
		# open cfg file for writing
		cfgFile = open(path_cfgs[i], "w")
		# write for each subject
		for sub in subjects_mod[0]:
			# get path of image for subject
			path = path_d + sub + "/" + modal[i] + ".nii.gz"
			# write to cfg
			print(path, file=cfgFile)
	# modify prediction cfg
	modifyPred(subjects_mod[0])

# ask user for path to deepmedic folder
def getPathToDM() -> str:
	path_d = input("Absolute path to deepmedic folder: ")
	if path_d[-1] != "/":
		path_d += "/"
	return path_d

# run inference
def runInf() -> None:
	# prepare different parts of command
	path_d = getPathToDM()
	run = path_d + "deepMedicRun"
	model = "-model " + os.getcwd() + "/config/model/modelConfig.cfg"
	test = "-test " + os.getcwd() + "/config/test/testConfig.cfg"
	load = "-load " + os.getcwd() + "/output/saved_models/train_t1w+flair/"
	load += "model_t1w+flair.train_t1w+flair.final.2019-11-01.11.44.09.274761.model.ckpt"
	# ask for which GPU to use
	dev = "-dev cuda" + input("Which GPU # to use? ")
	# run command for inference
	os.system(run + " " +  model + " " + test + " " +  load + " " + dev + " >& out.txt &")
	print("Running inference. You can check the progress using 'cat out.txt | less'")
	print("Or 'ps aux | grep -i myUserName' to check if the process is still running")

def main():
	modifyMC()
	modifyTC()
	modifyCfgs()
	print("Successfully modified channel & prediction configuration files!")
	runInf()
main()
