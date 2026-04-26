from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import json

class ComfyUIImageGenParams(BaseModel):
    """
    ComfyUI API用の画像生成パラメーターモデルクラス
    
    ComfyUIワークフローに必要なパラメーターを保持
    """
    
    # ワークフロー定義
    workflow_json: Dict[str, Any] = Field(..., description="ComfyUIワークフロー JSON")
    # ワークフロー変更設定
    workflow_mod_json: Dict[str, Any] = Field(default=None, description="ComfyUIワークフロー 変更設定JSON")

    # ランダムプロンプト生成フラグ
    prompt_randomize: bool = Field(default=False, description="プロンプトをランダム生成するか(Trueの場合、ワークフロー上のプロンプトで生成)")

    # ランダムプロンプト用パラメーター（JSON形式）
    persona_json: Optional[Dict[str, Any]] = Field(default=None, description="ペルソナ定義 JSON")
    camera_angle_json: Optional[Dict[str, Any]] = Field(default=None, description="カメラアングル定義 JSON")
    wardrobe_json: Optional[Dict[str, Any]] = Field(default=None, description="衣装(wardrobe)定義 JSON")
    environment_json: Optional[Dict[str, Any]] = Field(default=None, description="環境(environment)定義 JSON")
    
    # 生成設定
    rating_level: Optional[int] = Field(default=None, ge=1, description="レーティングレベル (1以上)")
    batch_size: int = Field(default=1, ge=1, le=10, description="生成枚数")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "a beautiful landscape",
                "workflow_json": {
                    "1": {
                        "inputs": {
                            "seed": 8566257053, 
                            "steps": 20,
                            "cfg": 7.0
                        },
                        "class_type": "KSampler"
                    }
                },
                "persona_json": {
                    "age": 25,
                    "gender": "female",
                    "style": "anime"
                },
                "camera_angle_json": {
                    "angle": "frontal",
                    "distance": "medium"
                },
                "wardrobe_json": {
                    "clothing_type": "dress",
                    "color": "red"
                },
                "environment_json": {
                    "setting": "outdoor",
                    "time_of_day": "sunset"
                },
                "rating_level": 2,
                "batch_size": 1
            }
        }
    
    @classmethod
    def parse_json_fields(cls, data: dict) -> dict:
        """
        JSON文字列をdict に変換するためのヘルパーメソッド
        リクエストボディからJSON文字列として渡される場合に使用
        """
        json_fields = ['workflow_json', 'persona_json', 'camera_angle_json', 'wardrobe_json', 'environment_json']
        
        for field in json_fields:
            if field in data and isinstance(data[field], str):
                try:
                    data[field] = json.loads(data[field])
                except (json.JSONDecodeError, ValueError):
                    # 既にdictの場合はスキップ
                    pass
        
        return data
