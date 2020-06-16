# agora-mask-detection
A custom image detection model over the Agora's 1-to-1 video call that predicts the probability that a person may or may not be wearing a mask

# Prerequisites

1. Agora.io developer account (with app ID)
2. Python3

# Process

Clone the repository and follow these steps:
1. Create an account on [agora.io](https://dashboard.agora.io). From the project manager create a new project and use the given app ID for this video call.
2. Open MaskDetection.py and paste your app ID over there along with a suitable channel name.
3. I have used a custom model that I trained myself, using ImageAI's custom prediction class following [these steps.](https://imageai.readthedocs.io/en/latest/custom/index.html). Download this model [here.](https://drive.google.com/file/d/1c0wq04EjRkhozQtOE7u73R4XtdbpVSVJ/view?usp=sharing)
4. Now open a sample agora video call [channel](http://sidsharma27.github.io) and paste the same app ID and channel name (as point 2) over there and click join
5. Run MaskDetection.py - this will take the frames from the video call and apply mask detection using ImageAI. 
6. The output i.e. mask/nomask will be displayed in the terminal where you run MaskDetection.py along with the probability of there being a mask/nomask.

# Sample Input and Output
**Input**

![in](https://user-images.githubusercontent.com/42168952/84763407-c4125d00-afe9-11ea-94d7-43d3b75cea8d.png)

**Output**

![Screenshot (183)](https://user-images.githubusercontent.com/42168952/84763706-43079580-afea-11ea-8336-2da1bcdfa289.png)

