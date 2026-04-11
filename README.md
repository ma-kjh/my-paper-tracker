# 📚 My Paper Tracker

arXiv에서 관심 키워드의 최신 논문을 매일 자동으로 수집·정리하는 프로젝트.

## ⚙️ 동작 방식
- 매일 아침 9시(KST)에 GitHub Actions가 `fetch_papers.py` 실행
- `config.yml`의 키워드로 arXiv 검색 → `papers/YYYY-MM-DD.md`로 저장
- 상위 매칭 논문은 이메일로 알림 발송

## 🔧 설정
`config.yml`에서 키워드를 수정하세요.

## 📂 구조
- `fetch_papers.py` — 수집 스크립트
- `config.yml` — 키워드 설정
- `papers/` — 날짜별 수집 결과
- `.github/workflows/update.yml` — 자동화 워크플로우
