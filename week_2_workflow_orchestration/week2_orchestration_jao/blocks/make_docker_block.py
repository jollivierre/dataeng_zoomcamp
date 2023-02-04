
from prefect.infrastructure.docker import DockerContainer

#alternative for UI
docker_block = DockerContainer(
    image="jollie/prefect_jao:dataeng_jao",
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save("jao-dataeng-dockercnt", overwrite=True)

#docker_container_block = DockerContainer.load("jao-dataeng-dockercnt")