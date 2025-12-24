from abc import ABC, abstractmethod
from flask import jsonify
from flask.wrappers import Response
from typing import Dict, Any, Union
from http import HTTPStatus

class BaseResponse(ABC):
    """
    APIレスポンスの基底クラス
    """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        各レスポンス固有のDictを返す
        """
        pass
    
    def to_response(self, status: Union[int, HTTPStatus]) -> Response:
        """
        Flask レスポンスを返す
        """
        
        return jsonify(self.to_dict()), status