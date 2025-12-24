from dataclasses import dataclass
from flask.wrappers import Response
from typing import Any, Dict, Optional, Union
from http import HTTPStatus
from app.models.response.base import BaseResponse

@dataclass
class SuccessResponse(BaseResponse):
    """
    APIの成功レスポンスを表現するデータクラス
    
    Attributes
    ----------
    data : Any
        レスポンスのメインデータ
    message : Optional[str]
        成功メッセージ（任意）
    meta : Optional[Dict[str, Any]]
        ページネーションなどの追加情報
    """
    
    data: Any
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        レスポンスボディとして返却可能なDict形式に変換する
        
        Returns
        -------
        
        Dict[str, Any]
            成功レスポンスのDict形式
        """
        
        result = {"data": self.data}
        
        if self.message is not None:
            result["message"] = self.message
        
        if self.meta is not None:
            result["meta"] = self.meta
            
        return result
    
    @classmethod
    def ok(
        cls, 
        data: Any, 
        message: Optional[str] = None, 
        meta: Optional[Dict[str, Any]] = None, 
        status: Union[int, HTTPStatus] = HTTPStatus.OK) -> Response:
        """
        SuccessResponse インスタンスを生成する
        
        Parameters
        ----------
        data : Any
            レスポンスのメインデータ
        message : Optional[str]
            成功メッセージ
        meta : Optional[Dict[str, Any]]
            ページネーションなどの追加情報
        status : int | HTTPStatus
            HTTPステータスコード
        
        Returns
        -------
        Response
            Flaskのレスポンスオブジェクト
        """
        
        return cls(data=data, message=message, meta=meta).to_response(status)