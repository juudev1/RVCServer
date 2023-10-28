# RVC server for multiple processing

The idea of ​​this project is to split audio files into several parts and send them to an RVC server.
The server processes that audio and returns the converted audio to us.
All parts come together at the end of the conversion on the client.

Your client must have client.py and indicate the URL of the model and the audio file.
For the client it is not necessary to install anything yet.
Then run client.py with `python3 client.py`

On the server you need to install uvicorn, fastapi, python-multipart and jrvc.
The audios received from the request are automatically deleted after conversion.
The converted audios are saved in the audio outputs folder and deleted after response.
The downloaded model is automatically deleted after conversion.

This is a beta version, there are several bugs that are not being fixed.
Run with the server with `uvicorn server:app --reload --host=0.0.0.0 --port=8000`

Create as many servers as you want and then add them in client.py

I have the idea of ​​making a conversion client in which everyone connected can let their cpu or gpu be used for conversions of other users, in this way a shared service is created.
But it's just an idea, I don't see how to develop it now and if it's worth it.