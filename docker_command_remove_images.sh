sudo docker rmi --force $(sudo docker images -q '{$1}' | uniq)
