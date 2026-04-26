import libcore_hng.utils.app_logger as app_logger
from pycorex.comfyui_client import ComfyUIClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from pycorex.utils.pony_prompt_generator import PonyPromptGenerator
from pycorex.utils.workflow_editor import WorkflowEditor
from pycorex.utils.workflow_mod import WorkflowMod
from app.models.comfyui_image_gen_params import ComfyUIImageGenParams

class ComfyUIImageGenerator:
    """
    ComfyUIを使用した画像生成のコア処理を担当する
    """

    def __init__(self, base_url: str, timeout_seconds: int, polling_interval: int):
        """
        コンストラクタ
        
        Parameters
        ----------
        base_url : str
            ComfyUI APIのエンドポイントURL
        timeout_seconds : int
            ComfyUI APIのタイムアウト設定
        polling_interval : int
            ComfyUI APIのポーリング設定

        """
        # ComfyUIClientを初期化
        self.client = ComfyUIClient(
            base_url=base_url, 
            timeout_seconds=timeout_seconds, 
            polling_interval=polling_interval
        )
        app_logger.info(f"[ComfyUIImageGenerator] ComfyUIClient initialized.")
    
    def apply_prompt_context(params: ComfyUIImageGenParams):
        """
        ワークフローをPromptContextの内容に準じて変更する

        Parameters
        ----------
        params : ComfyUIImageGenParams
            画像生成パラメーターモデル
        
        Returns
        -------
        Dict[str, Any]
            生成結果
        """

        # PonyPromptGeneratorのインスタンスを作成
        pony_generator = PonyPromptGenerator(
            persona_conf=params.persona_json,
            camera_conf=params.camera_angle_json,
            wardrobe_conf=params.wardrobe_json,
            environment_conf=params.environment_json
        )
        # PromptContextを生成
        prompt_context = pony_generator.generate_prompt(
            rating_level=PonyPromptGenerator.RatingLevel.SAFE,
        )

        # ワークフロー修正定義
        modification_list = WorkflowMod.create_modifications(
            prompt_context=prompt_context, 
            mod_config=params.workflow_mod_json,
            batch_size=2
        )

        # WorkflowEditorを使用してワークフローに修正を適用
        return WorkflowEditor.apply_modifications(params.workflow_json, modification_list)
    
    def generate(self, params: ComfyUIImageGenParams):
        """
        画像生成処理を実行する
        
        Parameters
        ----------
        params : ComfyUIImageGenParams
            画像生成パラメーターモデル
        
        Returns
        -------
        Dict[str, Any]
            生成結果
        """
    
        try:
            
            # ワークフローを取得
            workflow = params.workflow_json
            
            # プロンプトのランダム生成有無判定
            if params.prompt_randomize:
                
                # ワークフロー変更
                app_logger.info(f"[ComfyUIImageGenerator] Applying prompt context to workflow... ")
                workflow = self.apply_prompt_context(params)
                app_logger.info(f"[ComfyUIImageGenerator] Successfully applied prompt context to workflow. ")

            # ワークフロー実行
            app_logger.info(f"[ComfyUIImageGenerator] Generating image... ")
            response = self.client.run_workflow(workflow_data=workflow)
            app_logger.info(f"[ComfyUIImageGenerator] Image generation completed. result_count={len(response['result'])}")
            
            # 実行結果を返す
            return response
        
        except NoCandidatesError as e:
            app_logger.error(e)
            raise e
        except Exception as e:
            app_logger.error(e)
            raise e
