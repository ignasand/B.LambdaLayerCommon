from os.path import dirname, abspath
from typing import Optional, List, Dict

from aws_cdk.aws_lambda import Runtime
from aws_cdk.core import Stack, DockerImage, BundlingDockerImage
from b_cfn_lambda_layer.lambda_layer import LambdaLayer
from b_cfn_lambda_layer.package_version import PackageVersion


class Layer(LambdaLayer):
    def __init__(
            self,
            scope: Stack,
            name: str,
            additional_pip_install_args: Optional[str] = None,
            dependencies: Optional[Dict[str, PackageVersion]] = None,
            docker_image: Optional[DockerImage] = None,
    ) -> None:
        super().__init__(
            scope,
            name,
            source_path=self.get_source_path(),
            code_runtimes=self.runtimes(),
            include_source_path_directory=True,
            additional_pip_install_args=additional_pip_install_args,
            dependencies=dependencies,
            # Ensure Python 3.8 matches everywhere.
            docker_image=docker_image or BundlingDockerImage.from_registry('python:3.8')
        )

    @staticmethod
    def get_source_path() -> str:
        return dirname(abspath(__file__))

    @staticmethod
    def runtimes() -> Optional[List[Runtime]]:
        return [
            Runtime.PYTHON_3_6,
            Runtime.PYTHON_3_7,
            # Even though this layer supports more python versions,
            # It is recommended to use Python 3.8.
            Runtime.PYTHON_3_8
        ]
