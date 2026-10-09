# 컨베이어 공정 병목 비교기

다중 설비 공정에서 처리시간·병렬 대수·계획 정지 변경에 따른 대기시간과 처리량을 결정적으로 비교합니다.

## 핵심 기능

3D 표시 대신 각 공정을 독립된 FIFO 자원 큐로 계산합니다. 병렬 공정에서 처리 완료 순서가 바뀔 수 있으므로 다음 공정은 도착 시각으로 다시 정렬합니다. 계획 정지 중에는 처리를 중단하고 복구 후 남은 시간을 이어서 처리합니다. baseline과 candidate에 같은 작업 목록을 사용해 조건 변경의 효과를 비교합니다.

## 설치·실행

Python 3.10 이상. 외부 패키지·API 키·장비 연결이 필요 없습니다.

```bash
git clone https://github.com/MetaSonGi/conveyor-whatif-simulator.git
cd conveyor-whatif-simulator
python -m pip install -r requirements.txt
python main.py
python main.py --input sample-input.json --html result.html
python -m unittest -v
```

Windows에서 python 대신 py를 사용할 수 있습니다. 다른 디렉터리에서 실행해도 기본 샘플은 main.py 옆 파일에서 읽습니다. 모든 출력 파일 경로는 명시한 위치에 생성합니다.

## 웹에서 결과 확인

다운로드한 `example-report.html`을 브라우저에서 열면 검증한 샘플 결과가 보입니다. 입력을 수정하고 `python main.py --input sample-input.json --html result.html`을 실행하면 새 결과를 브라우저로 볼 수 있습니다. 보고서는 HTML에 결과를 포함하므로 네트워크·CDN·서버가 필요 없습니다. 입력 문자열은 escape해 HTML/스크립트로 실행하지 않습니다. 이는 입력 편집용 웹 앱이 아닌 실행 결과 뷰어입니다.

## 입력·출력 예제

합성 입력: [sample-input.json](sample-input.json). 필드와 형식은 이 파일이 최소 실행 예제입니다. 반환 규칙은 main.py의 `run(data)`에 정의됩니다. 손상된 JSON·필수 필드 누락·잘못된 수치 입력은 CLI가 종료 코드 2로 보고합니다.

```json
{
  "jobs": [
    {
      "id": "job-1",
      "arrival_s": 0
    },
    {
      "id": "job-2",
      "arrival_s": 2
    },
    {
      "id": "job-3",
      "arrival_s": 4
    },
    {
      "id": "job-4",
      "arrival_s": 6
    },
    {
      "id": "job-5",
      "arrival_s": 8
    }
  ],
  "baseline": [
    {
      "id": "load",
      "process_s": 2,
      "servers": 1
    },
    {
      "id": "robot",
      "process_s": 5,
      "servers": 1,
      "downtime": [
        [
          8,
          11
        ]
      ]
    }
  ],
  "candidate": [
    {
      "id": "load",
      "process_s": 2,
      "servers": 1
    },
    {
      "id": "robot",
      "process_s": 5,
      "servers": 2,
      "downtime": [
        [
          8,
          11
        ]
      ]
    }
  ]
}
```

출력 미리보기(생략 표시 부분은 설명이며 JSON 입력으로 사용하지 마세요):

```text
{
  "baseline": {
    "makespan_s": 30,
    "throughput_per_minute": 10.0,
    "average_lead_time_s": 15.4,
    "stations": [
      {
        "station_id": "load",
        "average_queue_wait_s": 0.0
      },
      {
        "station_id": "robot",
        "average_queue_wait_s": 7.8
      }
    ],
    "timeline": [
      {
        "job_id": "job-1",
        "station_id": "load",
        "server": 0,
        "arrival_s": 0,
        "start_s": 0,
        "end_s": 2,
        "queue_wait_s": 0
      },
      {
        "job_id": "job-2",
        "station_id": "load",
        "server": 0,
        "arrival_s": 2,
        "start_s": 2,
        "end_s": 4,
        "queue_wait_s": 0
      },
      {
        "job_id": "job-3",
        "station_id": "load",
        "server": 0,
        "arrival_s": 4,
        "start_s": 4,
        "end_s": 6,
        "queue_wait_s": 0
      },
      {
        "job_id": "job-4",
        "station_id": "load",
        "server": 0,
        "arrival_s": 6,
        "sta
… 전체 출력은 example-output.json 참조
```

전체 실행 결과: [example-output.json](example-output.json), [example-report.html](example-report.html).

## 설계 판단·통합

3D 표시 대신 각 공정을 독립된 FIFO 자원 큐로 계산합니다. 병렬 공정에서 처리 완료 순서가 바뀔 수 있으므로 다음 공정은 도착 시각으로 다시 정렬합니다. 계획 정지 중에는 처리를 중단하고 복구 후 남은 시간을 이어서 처리합니다. baseline과 candidate에 같은 작업 목록을 사용해 조건 변경의 효과를 비교합니다.

장비 데이터 수집 계층에서 합성 예제를 실제 데이터 스키마로 변환한 뒤 `run(data)`를 호출할 수 있습니다. Nest.js/Python 작업 큐 또는 테스트 자동화에서 JSON 입출력을 사용하고 XR/WebGL 화면에는 검증된 결과만 표시하는 방식으로 연결할 수 있습니다. 프로그램에는 실제 제어·유료 서비스·사용자 계정 접근 코드가 없습니다.

## 한계

무한 버퍼, 결정적 처리시간, 모든 서버에 공통인 정지를 가정합니다. 유한 버퍼에 의한 작업 정체, 운송 경로, 충돌, 고장 확률, 에너지는 포함하지 않습니다. throughput은 시각 0부터 마지막 완료까지의 평균이며 정상 상태 처리량이 아닙니다. 기존 3D 미니 시뮬레이터와 구분되는 정량 what-if 용도입니다.

가상의 경력, 논문 성능 수치, 모델 재현 또는 실물 제조 검증을 주장하지 않습니다. 데이터가 합성 예제인 만큼 현장 적용 전 데이터 품질·운영 조건을 다시 검증해야 합니다.

## 검증·근거

의미 있는 정상·경계·오류 테스트 4개를 실제 실행했습니다. 기록은 [VALIDATION.txt](VALIDATION.txt)에 있습니다. 논문 날짜·상태·확인 범위와 개발자 해석은 [TRENDS.md](TRENDS.md)를 참고하세요.

실행 기준일: 2026-10-09 (Asia/Seoul). 기존 저장소를 수정하지 않고 독립 프로그램으로 구성했습니다.
