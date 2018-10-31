import common.config


class TestRoot(object):

    def test_name(self, client):
        result = client.get('/')
        assert result.status_code == 200
        assert isinstance(result.json, dict)
        assert result.json['service_name'] == common.config.get('rest', 'service_name')
        assert result.json['service_version'] == common.config.get('rest', 'service_version')
