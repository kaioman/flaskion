from dataclasses import dataclass
from flask.wrappers import Response
from typing import Any, Optional, Dict, Union
from http import HTTPStatus
from app.models.response.base import BaseResponse
from app.core.errors import ErrorEnumProtocol
from app.core.error_messages import get_error_message

@dataclass
class ErrorResponse(BaseResponse):
    """
    APIエラーレスポンスクラス
    
    Attributes
    ----------
    errors : str
        エラーコード
    message : str
        エラーメッセージ
    details : Optional[Dict[str, Any]]
        バリデーションエラー等の追加情報。任意で指定
    """ 
    
    errors: str
    message: str
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        レスポンスボディとして返却可能なDictに変換する
        
        Returns
        -------
        
        Dict[str, Any]
            エラーレスポンスのDict形式
        """
        
        data = {
            "errors": self.errors,
            "message": self.message,
        }
        if self.details is not None:
            data["details"] = self.details
        return data
        
    @classmethod
    def from_error(cls, err_enum: ErrorEnumProtocol, status: Union[int, HTTPStatus], details: Optional[Dict[str, Any]]=None) -> Response:
        """
        エラー情報を元に ErrorResponse インスタンスを生成する
        
        Parameters
        ----------
        err_enum : BaseErrorEnum
            エラーコードとメッセージを持つEnumメンバー
        status : int | HTTPStatus
            HTTPステータスコード
        details : Optional[Dict[str, Any]]
            バリデーションエラーなどの追加情報
        
        Returns
        -------
        Response
            Flaskのレスポンスオブジェクト
        """
        return cls(
            errors=err_enum.value,
            message=get_error_message(err_enum),
            details=details
        ).to_response(status)