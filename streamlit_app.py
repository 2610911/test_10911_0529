import streamlit as st

# 1. 앱 페이지 설정
st.set_page_config(page_title="스트림릿 자판기", page_icon="🥤", layout="centered")

# 2. 자판기 데이터 초기화 (세션 상태 활용)
if "balance" not in st.session_state:
    st.session_state.balance = 0  # 투입 금액 잔액

if "inventory" not in st.session_state:
    # 음료수 이름: [가격, 재고, 아이콘]
    st.session_state.inventory = {
        "콜라": [1500, 5, "🥤"],
        "사이다": [1400, 3, "🥛"],
        "캔커피": [1000, 10, "☕"],
        "이온음료": [1200, 2, "💧"]
    }

if "history" not in st.session_state:
    st.session_state.history = []  # 구매 내역 로그

# --- 화면 UI 시작 ---
st.title("🥤 스트림릿 미니 자판기")
st.write("원하는 음료수를 선택하고 돈을 넣어주세요!")

# 3. 금액 투입 섹션
st.subheader("💰 금액 투입")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("+ 100원"):
        st.session_state.balance += 100
with col2:
    if st.button("+ 500원"):
        st.session_state.balance += 500
with col3:
    if st.button("+ 1,000원"):
        st.session_state.balance += 1000
with col4:
    if st.button("잔돈 반환"):
        if st.session_state.balance > 0:
            st.info(f"🪙 잔돈 {st.session_state.balance:,}원이 반환되었습니다.")
            st.session_state.balance = 0
        else:
            st.warning("반환할 잔돈이 없습니다.")

# 현재 잔액 표시
st.metric(label="현재 투입 금액", value=f"{st.session_state.balance:,} 원")

st.markdown("---")

# 4. 음료수 판매 섹션
st.subheader("🛒 음료수 목록")
menu_cols = st.columns(4)

for i, (name, info) in enumerate(st.session_state.inventory.items()):
    price, stock, icon = info
    with menu_cols[i]:
        st.markdown(f"### {icon} {name}")
        st.write(f"가격: **{price:,}원**")
        st.write(f"재고: {stock}개")
        
        # 구매 버튼 활성화 조건 체크
        if stock <= 0:
            st.button(f"{name} 품절", key=f"btn_{name}", disabled=True)
        else:
            if st.button(f"{name} 선택", key=f"btn_{name}"):
                # 잔액 부족 체크
                if st.session_state.balance < price:
                    st.error("❌ 잔액이 부족합니다! 돈을 더 넣어주세요.")
                else:
                    # 구매 처리
                    st.session_state.balance -= price
                    st.session_state.inventory[name][1] -= 1  # 재고 차감
                    st.success(f"🎉 {icon} {name}이(가) 나왔습니다!")
                    st.session_state.history.insert(0, f"{icon} {name} 구매 (-{price:,}원)")
                    st.rerun() # 화면 즉시 갱신

st.markdown("---")

# 5. 구매 내역 및 관리자 모드
st.subheader("📜 최근 이용 내역")
if st.session_state.history:
    for log in st.session_state.history[:5]:  # 최근 5개만 표시
        st.caption(log)
else:
    st.caption("아직 구매 내역이 없습니다.")

# 관리자 기능 (재고 채우기)
with st.expander("🛠️ 관리자 메뉴"):
    if st.button("모든 음료수 재고 가득 채우기 (5개씩)"):
        for name in st.session_state.inventory:
            st.session_state.inventory[name][1] = 5
        st.success("모든 음료수의 재고가 충전되었습니다!")
        st.rerun()