import pycorex.configs.app_init as app_pycorex
import logging
import re

def init_logging():
    """
    ロガー初期化
    """
    
    # pycorex初期化(ロガー設定)
    app_pycorex.init_app(__file__, "logger.json")

    # 色付き文字を除外する正規表現
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    class StripAnsiFilter(logging.Filter):
        """
        ログから色付き文字を除外するフィルタクラス
        """ 
        def filter(self, record): 
            record.msg = ansi_escape.sub('', str(record.msg)) 
            return True

    # ロガーハンドラにフィルタークラスを追加する
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler.addFilter(StripAnsiFilter())