# 引入单元测试相关模块
import unittest
from unittest.mock import patch

from MapUtils import MapUtils  # 假设mapapi是文件名，MapUtils是类名


# 创建测试类，继承自unittest.TestCase
class TestMapUtils(unittest.TestCase):

    # 在每个测试之前运行，初始化MapUtils对象
    def setUp(self):
        self.map_utils = MapUtils()
        # 假设密钥是 'YOUR_AMAP_KEY'
        self.map_utils.amap_key = 'YOUR_AMAP_KEY'

    # 测试成功获取坐标的情况
    @patch('mapapi.requests.get')
    def test_get_location_coordinate_success(self, mock_get):
        # 模拟返回的JSON数据
        mock_response = {
            "status": "1",
            "geocodes": [
                {"location": "123.456,78.901"}
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        # 调用函数
        result = self.map_utils.get_location_coordinate("某地", "某市")

        # 断言结果是否正确
        self.assertEqual(result, "123.456,78.901")
        # 断言是否调用了预期的URL
        mock_get.assert_called_once_with(
            "https://restapi.amap.com/v3/geocode/geo?address=某地&city=某市&key=YOUR_AMAP_KEY"
        )

    # 测试无法获取坐标的情况
    @patch('mapapi.requests.get')
    def test_get_location_coordinate_fail(self, mock_get):
        # 模拟返回的JSON数据
        mock_response = {
            "status": "0",
            "info": "错误信息"
        }
        mock_get.return_value.json.return_value = mock_response

        # 调用函数
        result = self.map_utils.get_location_coordinate("某地", "某市")

        # 断言结果是否为None
        self.assertIsNone(result)


# 入口函数
if __name__ == '__main__':
    unittest.main()