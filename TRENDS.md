# 논문 근거와 개발자 해석

조사 기준일: **2026-10-09 (Asia/Seoul)**. 확인 범위: 저자 원문 저장소 arXiv의 초록·제출 이력·comments·관련 DOI. 전문 실험·부록·코드 및 성능 재현은 확인하지 않았습니다. 최신 검색에 나온 일부 원문(2609.09625, 2609.32923)은 열기 실패로 설계 근거에서 제외했습니다. 아래는 완전한 최신 문헌 조사나 최신 순위가 아닙니다.

## Digital Twin AI: Opportunities and Challenges from Large Language Models to World Models

- 원문: https://arxiv.org/abs/2601.01321
- 발표/제출일: 2026-01-04
- 상태: arXiv preprint v1; 조회 페이지에 학회 채택 표기 없음
- 확인한 사실(초록): AI 통합을 modeling, mirroring, intervention, autonomous management의 네 단계로 정리합니다.
- 개발자 해석: 상태 동기화·시뮬레이션·검증·개입을 분리해 자동화의 책임 경계를 명확히 둡니다.

## Grounding Time-Series Foundation Models in Digital Twin Topology for Predictive Maintenance

- 원문: https://arxiv.org/abs/2609.40071
- 발표/제출일: 2026-09-30
- 상태: arXiv preprint v1; RESS 투고 표기, 게재 확정 아님
- 확인한 사실(초록): 동결 TSFM의 C-MAPSS RUL 평가와 물리 연결 구조를 이용한 융합을 제안합니다.
- 개발자 해석: 여러 센서의 연결과 운영 조건을 명시하고 입력 품질·후행 검증을 모델 평가와 분리하는 설계가 유용합니다.

## 이 프로그램의 적용

3D 표시 대신 각 공정을 독립된 FIFO 자원 큐로 계산합니다. 병렬 공정에서 처리 완료 순서가 바뀔 수 있으므로 다음 공정은 도착 시각으로 다시 정렬합니다. 계획 정지 중에는 처리를 중단하고 복구 후 남은 시간을 이어서 처리합니다. baseline과 candidate에 같은 작업 목록을 사용해 조건 변경의 효과를 비교합니다.

논문의 TSFM·임베딩·LLM·실험 모델을 재현한 것이 아닙니다. 표준 라이브러리 기반의 설명 가능한 오프라인 도구입니다. 논문 성능 수치나 물리 장비 검증을 주장하지 않습니다.
