xhost +
docker run -it --rm --runtime nvidia --privileged --name jtf -v /home:/home -e DISPLAY=$DISPLAY -v /tmp/.X11-unix/:/tmp/.X11-unix tfaudio bash