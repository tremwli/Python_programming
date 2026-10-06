# __init__.py 파일 (패키지 초기화 파일)

# 1. 패키지를 import 할 때 실행되어야 하는 초기화 코드 ()
print("__init__")

# 2. ㅠㅐ키지 메타데이터 설정 (버전 정보, 작성자)
VERSION = "1.0.0"

# 패키지 re-export 
from mypackage.mymath import add
from .mymath import add
