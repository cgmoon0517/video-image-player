# Video & Image player, image sequence file saver  
## 목적 
비디오 파일 또는 이미지 파일을 연속적으로 재생하고, 필요한 경우 비디오 파일을 시퀀스 이미지 파일로 저장을 합니다.
## 실행하기
#### 파라미터 설명  
python main.py --help
#### 1. 비디오 재생 
##### 비디오의 fps를 이용하여 자동으로 계산된 속도로 비디오를 재생할 경우: 
python main.py --play_mode="video" 
##### 지연 시간을 24 msec로 적용하여 0.5배로 다운샘플링된 비디오를 재생할 경우: 
python main.py --play_mode="video" --delay_time=24 --resizing=True --resizing_ratio=0.5
##### 지연 시간을 1 msec로 적용하여 1.5배로 업샘플링된 비디오를 재생하고, 비디오 파일의 이미지 시퀀스 파일 포맷을 PNG로 설정하여 10 프레임 간격으로 저장할 경우: 
python main.py --play_mode="video" --delay_time=1 --resizing=True --resizing_ratio=1.5 --save=True --save_interval=10 --save_file_extension="PNG"
#### 2. 이미지 재생
#### 이미지를 재생할 경우:
python main.py --play_mode="image" --in_path="./data/image" 
#### 0.5배로 다운샘플링된 이미지를 재생할 경우:
python main.py --play_mode="image" --in_path="./data/image" --resizing=True --resizing_ratio=0.5
## 데이터 폴더 설명
- ./data/image: 재생하고자 하는 입력 이미지의 경로
- ./data/video: 재생하고자 하는 입력 비디오의 경로
- ./data/video_to_image: 비디오 파일을 이미지 시퀀스 파일로 저장할 경우, 파일이 저장되는 경로(시퀀스 파일명은 동영상 파일명을 기준으로 생성됨)
## 키보드 제어 
- 스페이스 바: 비디오 재생을 멈춤 
- 모든 키: 비디오 또는 이미지를 연속적으로 재생
- d 키: 다음 비디오 파일을 재생할 경우(비디오가 재생중일 경우에만 활성화됨)
- q 키: 종료 
## 필요 라이브러리
- click
- opencv
- 설치: pip install -r requirements.txt

