# Liveliness Detection Using a Dynamically Changing UI and Iris Tracking

We are building a dynamically changing interface and an iris tracking algorithm which can understand the liveliness (actual person vs his photo or video being shown to the camera) of a person based on his eye’s responses to the UI, without compromising on the usability of the UI itself.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

OpenCV 3.3+ (Python)

```
Windows Installation:
https://docs.opencv.org/3.3.1/d5/de5/tutorial_py_setup_in_windows.html

Linux Installation:
https://www.learnopencv.com/install-opencv3-on-ubuntu/
```

NodeJS 8+

```
Windows Installation:
(Has an easy executable file installation)
https://nodejs.org/en/download/ 

Linux Installation:
https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04
```

Android Studio 2+ (preferably 3+)

```
https://developer.android.com/studio/
(Their website covers everything)
```

### Installing

Steps to get youself a personal copy of the project running on your machine

Clone the project repo to your local machine

```
git clone git@github.com:rohitbhaskar/face_liveliness_detection.git
```

Get into the server directory with the node code

```
cd face_liveliness_detection/server/node_server
```

Run the nodeJS script

```
node index.js
```

Open a new terminal/command prompt, and run the following commang to get your device ip

```
Windows: ipconfig
Linux: ifconfig
```

Open client/android_app inside Android Studio. Go to "Camera2VideoFragment.java".
Now edit line numbers 122 and 982 with your ip address

```
socket = IO.socket("http://192.168.1.2:6000");

HttpFileUpload hfu = new HttpFileUpload("http://192.168.1.2:5000/upload", "my file title","my file description", new File(filePath), suddenImageId);

{your ip adress in place of 192.168.1.2}
```

Install the app in your phone

```
Install using apk generated after build
or
Connect phone to directly install while android studui builds and runs the app
```

You are now good to go! Open the app and click the 'Make Payment' Button to test it out.

## Built With

* [NodeJS](https://nodejs.org/) - The web framework used
* [Android](https://developer.android.com/studio/) - Android App Development
* [Socket.io](https://socket.io/) - Web sockets for comm
* [OpenCV](https://opencv.org/) - Image processing library

## Authors

* **Rohit Bhaskar** - *Initial work* - [LinkedIn](https://in.linkedin.com/in/rohitb1vs10)
* **Billie Thompson** - *Initial work* - [LinkedIn](https://www.linkedin.com/in/tanay-shah-74095359)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) {when its ready :p)} file for details

