# NiFi Flow 백업 및 복원 가이드

## 1. Flow 백업 방법 - NiFi UI를 통한 Template 생성

1. NiFi UI 접속: https://localhost:8443/nifi
2. Process Group 선택
3. 우클릭 → "Create Template"
4. Template 이름 입력 (예: ad-impression-flow)
5. 상단 메뉴 → Templates → Download

## 2. Flow 복원 방법 - NiFi UI를 통한 Template Import

1. 새 NiFi 환경에서 UI 접속
2. Canvas에서 우클릭 → Upload template → Template XML 파일 선택
3. 상단 메뉴 → Template → Browse → Canvas 로 Drag → Upload 한 Template 선택
