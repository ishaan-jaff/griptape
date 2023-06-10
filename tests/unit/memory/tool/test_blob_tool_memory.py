from griptape.artifacts import BlobArtifact, ListArtifact
from griptape.drivers import MemoryBlobToolMemoryDriver
from griptape.memory.tool import BlobToolMemory
from tests.mocks.mock_tool.tool import MockTool


class TestBlobToolMemory:
    def test_init(self):
        memory = BlobToolMemory(driver=MemoryBlobToolMemoryDriver())

        assert memory.id == BlobToolMemory.__name__

        memory = BlobToolMemory(id="MyMemory", driver=MemoryBlobToolMemoryDriver())

        assert memory.id == "MyMemory"

    def test_process_output(self):
        memory = BlobToolMemory(id="MyMemory", driver=MemoryBlobToolMemoryDriver())
        artifact = BlobArtifact(b"foo", name="foo")
        output = memory.process_output(MockTool().test, artifact)

        assert output.to_text().startswith(
            'Output of "MockTool.test" was stored in memory "MyMemory" with the following artifact namespace:'
        )

        assert memory.driver.load(artifact.id) == [artifact]

    def test_process_output_with_many_artifacts(self):
        memory = BlobToolMemory(id="MyMemory", driver=MemoryBlobToolMemoryDriver())

        assert memory.process_output(
            MockTool().test, ListArtifact([BlobArtifact(b"foo", name="foo")])
        ).to_text().startswith(
            'Output of "MockTool.test" was stored in memory "MyMemory" with the following artifact namespace:'
        )