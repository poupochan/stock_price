import streamlit as st
import yfinance as yf

st.set_page_config(page_title="米国株検索", page_icon="📈")

st.title("📈 米国株データ検索")
st.write("米国株のティッカーを入力してください")

symbol = st.text_input(
    "ティッカー",
    value="AVGO"
).strip().upper()

if st.button("検索", type="primary"):
    if not symbol:
        st.warning("ティッカーを入力してください")
    else:
        try:
            with st.spinner("データ取得中..."):
                stock = yf.Ticker(symbol)
                info = stock.info

                # 株価を取得
                price = info.get("currentPrice")
                if price is None:
                    price = info.get("regularMarketPrice")

                if price is None:
                    price = stock.fast_info.get("lastPrice")

                # 株価が取れない場合は直近の履歴を確認
                if price is None:
                    history = stock.history(period="5d")
                    if not history.empty:
                        price = float(history["Close"].dropna().iloc[-1])

                eps = info.get("trailingEps")
                per = info.get("trailingPE")
                forward_per = info.get("forwardPE")

            if price is None and eps is None and per is None:
                st.error("データを取得できませんでした。")
                st.info(
                    "ティッカーを確認してください。"
                    "取得制限や通信エラーの可能性もあります。"
                )
            else:
                st.subheader(
                    info.get("longName") or symbol
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "株価（USD）",
                    f"${price:,.2f}" if price is not None else "取得不可"
                )
                col2.metric(
                    "実績PER",
                    f"{per:.2f}倍" if per is not None else "取得不可"
                )
                col3.metric(
                    "実績EPS",
                    f"${eps:.2f}" if eps is not None else "取得不可"
                )

                st.write(
                    "予想PER：",
                    f"{forward_per:.2f}倍"
                    if forward_per is not None else "取得不可"
                )

                st.caption(
                    "データ提供元：Yahoo Finance（yfinance経由）。"
                    "数値は遅延・欠損する場合があります。"
                )

        except Exception as e:
            st.error("データ取得中にエラーが発生しました。")
            st.code(str(e))
