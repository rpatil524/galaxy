from galaxy_test.base.populators import (
    DatasetCollectionPopulator,
    DatasetPopulator,
    WorkflowPopulator,
)
from galaxy_test.driver import integration_util


class TestHistoriesApi(integration_util.IntegrationTestCase):
    dataset_populator: DatasetPopulator

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        super().handle_galaxy_config_kwds(config)

    def setUp(self):
        super().setUp()
        self.workflow_populator = WorkflowPopulator(self.galaxy_interactor)
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)
        self.dataset_collection_populator = DatasetCollectionPopulator(self.galaxy_interactor)

    def test_get_tags_workflows(self):
        response = self._test_get_tags(self._create_prefixes()["workflows"])
        self._assert_status_code_is(response, 200)

    def test_create_tag_workflows(self):
        response = self._test_create_tag(self._create_prefixes()["workflows"])
        self._assert_status_code_is(response, 200)

    def test_update_tag_workflows(self):
        response = self._test_update_tag(self._create_prefixes()["workflows"])
        self._assert_status_code_is(response, 200)

    def test_get_tag_workflows(self):
        response = self._test_get_tag(self._create_prefixes()["workflows"])
        self._assert_status_code_is(response, 200)

    def test_delete_tag_workflows(self):
        response = self._test_delete_tag(self._create_prefixes()["workflows"])
        self._assert_status_code_is(response, 200)

    def test_get_tags_histories(self):
        response = self._test_get_tags(self._create_prefixes()["histories"])
        self._assert_status_code_is(response, 200)

    def test_create_tag_histories(self):
        response = self._test_create_tag(self._create_prefixes()["histories"])
        self._assert_status_code_is(response, 200)

    def test_update_tag_histories(self):
        response = self._test_update_tag(self._create_prefixes()["histories"])
        self._assert_status_code_is(response, 200)

    def test_get_tag_histories(self):
        response = self._test_get_tag(self._create_prefixes()["histories"])
        self._assert_status_code_is(response, 200)

    def test_delete_tag_histories(self):
        response = self._test_delete_tag(self._create_prefixes()["histories"])
        self._assert_status_code_is(response, 200)

    def test_get_tags_histories_content(self):
        response = self._test_get_tags(self._create_prefixes()["histories_content"])
        self._assert_status_code_is(response, 200)

    def test_create_tag_histories_content(self):
        response = self._test_create_tag(self._create_prefixes()["histories_content"])
        self._assert_status_code_is(response, 200)

    def test_update_tag_histories_content(self):
        response = self._test_update_tag(self._create_prefixes()["histories_content"])
        self._assert_status_code_is(response, 200)

    def test_get_tag_histories_content(self):
        response = self._test_get_tag(self._create_prefixes()["histories_content"])
        self._assert_status_code_is(response, 200)

    def test_delete_tag_histories_content(self):
        response = self._test_delete_tag(self._create_prefixes()["histories_content"])
        self._assert_status_code_is(response, 200)

    def _create_prefixes(self):
        workflow_id = self._create_workflow()
        history_id = self._create_history()
        history_content_id = self._create_history_contents(history_id)
        prefixs = {
            "workflows": f"workflows/{workflow_id}",
            "histories": f"histories/{history_id}",
            "histories_content": f"histories/{history_id}/contents/{history_content_id}",
        }
        return prefixs

    def _test_get_tags(self, prefix):
        url = f"{prefix}/tags"
        response = self._get(url)
        return response

    def _test_create_tag(self, prefix):
        response = self._create_valid_tag(prefix)
        return response

    def _test_update_tag(self, prefix):
        response = self._create_valid_tag(prefix)
        tag_name = response.json()["user_tname"]
        url = f"{prefix}/tags/{tag_name}"
        tag_data = dict(value="updatedtagvalue")
        response = self._put(url, data=tag_data, json=True)
        return response

    def _test_get_tag(self, prefix):
        response = self._create_valid_tag(prefix)
        tag_name = response.json()["user_tname"]
        url = f"{prefix}/tags/{tag_name}"
        response = self._get(url)
        return response

    def _test_delete_tag(self, prefix):
        response = self._create_valid_tag(prefix)
        tag_name = response.json()["user_tname"]
        url = f"{prefix}/tags/{tag_name}"
        response = self._delete(url)
        return response

    def _create_valid_tag(self, prefix: str):
        url = f"{prefix}/tags/awesometagname"
        tag_data = dict(value="awesometagvalue")
        response = self._post(url, data=tag_data, json=True)
        return response

    def _create_history_contents(self, history_id):
        history_content_id = self.dataset_collection_populator.create_list_in_history(
            history_id, contents=["test_dataset"], direct_upload=True, wait=True
        ).json()["outputs"][0]["id"]
        return history_content_id

    def _create_history(self):
        history_id = self.dataset_populator.new_history()
        return history_id

    def _create_workflow(self):
        workflow = self.workflow_populator.load_workflow_from_resource(name="test_workflow_with_input_tags")
        workflow_id = self.workflow_populator.create_workflow(workflow)
        return workflow_id
