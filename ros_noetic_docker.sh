xhost +
docker run --rm -it --privileged --network="host" --env DISPLAY=$DISPLAY --name data_collection \
-v /tmp/.X11-unix:/tmp/.X11-unix -v /home/$USER/catkin_ws:/root/catkin_ws \
-v /home/$USER/Repos/evsts-data-collection-tools:/root/evsts-data-collection \
-v /home/$USER/Datasets:/root/Datasets \
prabinrath/ubuntu-ros1:data_collection bash
