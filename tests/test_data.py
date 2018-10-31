import math


class TestData(object):

    def test_calculation_1(self, client):
        result = client.get('data?lat=45&lng=5')
        assert result.status_code == 200
        assert isinstance(result.json, dict)
        assert math.isclose(
            result.json['result'], 1657.142857142857,
            abs_tol=1e-6
        )

    def test_calculation_2(self, client):
        result = client.get('data?lat=42.13&lng=8.24')
        assert result.status_code == 200
        assert isinstance(result.json, dict)
        assert math.isclose(
            result.json['result'], 1903.1428571428569,
            abs_tol=1e-6
        )

    def test_outofbound(self, client):
        result = client.get('data?lat=52.34&lng=-12.04')
        assert result.status_code == 403

    def test_invalid_1(self, client):
        result = client.get('data?lat=42.13')
        assert result.status_code == 400

    def test_invalid_2(self, client):
        result = client.get('data?lat=aaa&lng=8.24')
        assert result.status_code == 400
