from agora_community_sdk import AgoraRTC
from imageai.Prediction.Custom import CustomImagePrediction
import os

client = AgoraRTC.create_watcher("<insert app id here>", "chromedriver.exe")
client.join_channel("naynika")

users = client.get_users() # Gets references to everyone participating in the call

user1 = users[0] # Can reference users in a list

binary_image = user1.frame # Gets the latest frame from the stream as a PIL image

#with open("test.jpg") as f:
#    f.write(str(binary_image)) # Can write to file
binary_image.save("in.png") #Replace test.png with your file name
execution_path = os.getcwd() #Returns current working directory of the project

prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "model_ex-068_acc-0.900000.h5"))
prediction.setJsonPath(os.path.join(execution_path, "model_class.json"))
prediction.loadModel(num_objects=3)

predictions, probabilities = prediction.predictImage(os.path.join(execution_path, "in.png"))    

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)

client.unwatch() #Ends the stream
