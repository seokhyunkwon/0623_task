from datetime import datetime
from html import escape
from urllib.parse import quote_plus

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text


st.set_page_config(page_title="Baseball Records", page_icon="B", layout="wide")


def make_engine(user: str, password: str, host: str, port: int, database: str):
    safe_password = quote_plus(password)
    url = f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{database}?charset=utf8mb4"
    return create_engine(url, pool_pre_ping=True)


@st.cache_data(ttl=30)
def read_sql(user: str, password: str, host: str, port: int, database: str, query: str) -> pd.DataFrame:
    engine = make_engine(user, password, host, port, database)
    try:
        return pd.read_sql(text(query), con=engine)
    finally:
        engine.dispose()


def run_query(query: str) -> pd.DataFrame:
    return read_sql(db_user, db_password, db_host, db_port, db_name, query)


def inject_style():
    st.markdown(
        """
        <style>
        .stApp, [data-testid="stAppViewContainer"] {
            background: #ffffff;
            color: #111111;
        }
        [data-testid="stHeader"] {
            background: #ffffff;
        }
        [data-testid="stSidebar"] {
            background: #f6f6f6;
        }
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: #111111;
        }
        [data-testid="stSidebar"] input {
            background: #ffffff;
            color: #111111;
        }
        .block-container {
            max-width: 1240px;
            padding-top: 24px;
        }
        h1, h2, h3, p, div, span {
            letter-spacing: 0;
        }
        .league-header {
            border-top: 3px solid #2f2f2f;
            border-bottom: 1px solid #d8d8d8;
            padding: 18px 0 14px;
            margin-bottom: 18px;
        }
        .league-title {
            font-size: 30px;
            font-weight: 800;
            color: #111;
            margin: 0;
        }
        .league-subtitle {
            font-size: 14px;
            color: #666;
            margin-top: 6px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
            margin: 14px 0 22px;
        }
        .summary-card {
            border: 1px solid #d9d9d9;
            border-radius: 4px;
            padding: 14px 16px;
            background: #fff;
        }
        .summary-label {
            color: #666;
            font-size: 13px;
            font-weight: 700;
        }
        .summary-value {
            color: #111;
            font-size: 28px;
            font-weight: 800;
            margin-top: 4px;
        }
        button[role="tab"] p {
            color: #222222 !important;
            font-weight: 800;
        }
        button[role="tab"][aria-selected="true"] p {
            color: #ff3b3b !important;
        }
        button[role="tab"]:hover p {
            color: #111111 !important;
        }
        button[role="tab"][aria-selected="true"]:hover p {
            color: #ff3b3b !important;
        }
        .section-title {
            display: flex;
            align-items: baseline;
            gap: 14px;
            margin: 20px 0 10px;
        }
        .section-title strong {
            font-size: 24px;
            color: #111;
        }
        .section-title span {
            color: #cfcfcf;
            font-size: 22px;
            font-weight: 800;
        }
        .stat-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 18px;
            background: #fff;
            border-top: 1px solid #7a7a7a;
        }
        .stat-table th {
            background: #f2f2f2;
            color: #111;
            font-size: 17px;
            font-weight: 800;
            padding: 12px 10px;
            border-bottom: 1px solid #d6d6d6;
            text-align: center;
            white-space: nowrap;
        }
        .stat-table td {
            padding: 10px 10px;
            border-bottom: 1px solid #e1e1e1;
            text-align: center;
            color: #333;
            white-space: nowrap;
        }
        .stat-table td.name {
            text-align: left;
            font-weight: 800;
            color: #333;
        }
        .stat-table td.rank {
            color: #111;
            font-weight: 800;
        }
        .stat-table td.highlight,
        .stat-table th.highlight {
            background: #f8eeee;
            color: #111;
            font-weight: 800;
        }
        .score-away {
            color: #47799b;
            font-weight: 900;
        }
        .score-home {
            color: #b65b66;
            font-weight: 900;
        }
        .muted-cell {
            color: #777;
            font-weight: 700;
        }
        .empty-box {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 24px;
            color: #666;
            background: #fff;
        }
        @media (max-width: 760px) {
            .summary-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .stat-table {
                font-size: 14px;
            }
            .stat-table th,
            .stat-table td {
                padding: 8px 6px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_title(main: str, sub: str = ""):
    st.markdown(
        f'<div class="section-title"><strong>{escape(main)}</strong><span>{escape(sub)}</span></div>',
        unsafe_allow_html=True,
    )


def summary_cards(items):
    cards = "".join(
        f'<div class="summary-card"><div class="summary-label">{escape(label)}</div>'
        f'<div class="summary-value">{escape(value)}</div></div>'
        for label, value in items
    )
    st.markdown(f'<div class="summary-grid">{cards}</div>', unsafe_allow_html=True)


def render_table(df: pd.DataFrame, columns, highlight: str | None = None, name_cols=None, html_cols=None):
    if df.empty:
        st.markdown('<div class="empty-box">표시할 데이터가 없습니다.</div>', unsafe_allow_html=True)
        return

    name_cols = set(name_cols or [])
    html_cols = set(html_cols or [])
    header = "".join(
        f'<th class="{"highlight" if key == highlight else ""}">{escape(label)}</th>'
        for key, label in columns
    )

    rows = []
    for _, row in df.iterrows():
        cells = []
        for key, _label in columns:
            value = "" if pd.isna(row.get(key, "")) else row.get(key, "")
            value = str(value) if key in html_cols else escape(str(value))
            klass = []
            if key == highlight:
                klass.append("highlight")
            if key in name_cols:
                klass.append("name")
            if key == "rank":
                klass.append("rank")
            cells.append(f'<td class="{" ".join(klass)}">{value}</td>')
        rows.append(f"<tr>{''.join(cells)}</tr>")

    st.markdown(
        f'<table class="stat-table"><thead><tr>{header}</tr></thead><tbody>{"".join(rows)}</tbody></table>',
        unsafe_allow_html=True,
    )


def format_rate(value) -> str:
    if pd.isna(value):
        return "-"
    return f"{float(value):.3f}".replace("0.", ".")


def format_game_back(value) -> str:
    if value == 0:
        return "-"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


def format_date_label(value) -> str:
    if pd.isna(value):
        return "-"
    date = pd.to_datetime(value)
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    return f"{date.month:02d}.{date.day:02d}({weekdays[date.weekday()]})"


def score_text(away_score, home_score):
    away_class = "score-away"
    home_class = "score-home"
    if away_score > home_score:
        away_class = "score-home"
        home_class = "score-away"
    return (
        f'<span class="{away_class}">{away_score}</span>'
        f'<span class="muted-cell"> vs </span>'
        f'<span class="{home_class}">{home_score}</span>'
    )


def make_standings(teams: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for team in teams.itertuples(index=False):
        team_matches = matches[(matches["away_team_id"] == team.team_id) | (matches["home_team_id"] == team.team_id)]
        wins = losses = draws = scored = allowed = 0
        results = []

        for game in team_matches.sort_values(["match_date", "match_id"]).itertuples(index=False):
            is_away = game.away_team_id == team.team_id
            own = game.away_final_score if is_away else game.home_final_score
            opp = game.home_final_score if is_away else game.away_final_score
            scored += own
            allowed += opp
            if own > opp:
                wins += 1
                results.append("승")
            elif own < opp:
                losses += 1
                results.append("패")
            else:
                draws += 1
                results.append("무")

        games = wins + losses + draws
        rate = wins / (wins + losses) if wins + losses else None
        streak = "-"
        if results:
            last = results[-1]
            streak_count = 0
            for result in reversed(results):
                if result == last:
                    streak_count += 1
                else:
                    break
            streak = f"{streak_count}{last}"

        rows.append(
            {
                "team_id": team.team_id,
                "team_name": team.team_name,
                "G": games,
                "W": wins,
                "L": losses,
                "D": draws,
                "PCT": rate,
                "R": scored,
                "RA": allowed,
                "DIFF": scored - allowed,
                "STREAK": streak,
            }
        )

    standings = pd.DataFrame(rows)
    if standings.empty:
        return standings

    standings = standings.sort_values(["PCT", "W", "DIFF"], ascending=[False, False, False]).reset_index(drop=True)
    leader_w = standings.loc[0, "W"]
    leader_l = standings.loc[0, "L"]
    standings["GB"] = ((leader_w - standings["W"]) + (standings["L"] - leader_l)) / 2
    standings["rank"] = range(1, len(standings) + 1)
    standings["PCT"] = standings["PCT"].apply(format_rate)
    standings["GB"] = standings["GB"].apply(format_game_back)
    return standings


def make_team_score_ranking(team_scores: pd.DataFrame) -> pd.DataFrame:
    if team_scores.empty:
        return team_scores
    df = team_scores.sort_values(["total_score", "avg_score"], ascending=[False, False]).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)
    df["AVG"] = df["avg_score"].map(lambda value: f"{value:.2f}")
    return df


def make_batter_ranking(players: pd.DataFrame) -> pd.DataFrame:
    batters = players[players["AB"].notna() & (players["AB"] > 0)].copy()
    if batters.empty:
        return batters

    batters["AVG_VALUE"] = batters["H"] / batters["AB"]
    batters = batters.sort_values(["AVG_VALUE", "H", "HR"], ascending=[False, False, False]).reset_index(drop=True)
    batters["rank"] = range(1, len(batters) + 1)
    batters["AVG"] = batters["AVG_VALUE"].apply(format_rate)
    int_cols = ["G", "PA", "AB", "R", "H", "2B", "3B", "HR", "RBI"]
    for col in int_cols:
        batters[col] = batters[col].fillna(0).astype(int)
    return batters


def make_match_rows(matches: pd.DataFrame) -> pd.DataFrame:
    if matches.empty:
        return matches

    df = matches.copy()
    df["date_label"] = df["match_date"].apply(format_date_label)
    df["time"] = "-"
    df["score"] = df.apply(lambda row: score_text(row["away_final_score"], row["home_final_score"]), axis=1)
    df["winner_text"] = df["winner"].map(lambda value: f'<span class="muted-cell">{escape(str(value))}</span>')
    return df.sort_values(["match_date", "match_id"], ascending=[False, False])


inject_style()

with st.sidebar:
    st.header("DB 접속")
    db_host = st.text_input("Host", value="127.0.0.1")
    db_port = st.number_input("Port", value=3306, step=1)
    db_name = st.text_input("Database", value="baseball2")
    db_user = st.text_input("User", value="root")
    db_password = st.text_input("Password", value="1234", type="password")

    if st.button("새로고침"):
        st.cache_data.clear()
        st.rerun()


queries = {
    "teams": "SELECT team_id, team_name, founded_year FROM teams ORDER BY team_id",
    "players": """
        SELECT
            p.player_id,
            p.player_name,
            p.back_number,
            p.birth_year,
            p.position,
            p.team_id,
            COALESCE(t.team_name, '무소속') AS team_name,
            bs.games AS G,
            bs.plate_appearances AS PA,
            bs.at_bats AS AB,
            bs.runs AS R,
            bs.hits AS H,
            bs.doubles AS `2B`,
            bs.triples AS `3B`,
            bs.home_runs AS HR,
            bs.rbi AS RBI
        FROM players p
        LEFT JOIN teams t ON p.team_id = t.team_id
        LEFT JOIN batting_stats bs ON bs.player_id = p.player_id
        ORDER BY t.team_name, p.position, p.player_name
    """,
    "matches": """
        SELECT
            m.match_id,
            m.match_date,
            m.away_team_id,
            m.home_team_id,
            away.team_name AS away_team,
            home.team_name AS home_team,
            s.stadium_name,
            s.location AS stadium_location,
            m.away_final_score,
            m.home_final_score,
            CASE
                WHEN m.away_final_score > m.home_final_score THEN away.team_name
                WHEN m.away_final_score < m.home_final_score THEN home.team_name
                ELSE '무승부'
            END AS winner
        FROM matches m
        JOIN teams away ON away.team_id = m.away_team_id
        JOIN teams home ON home.team_id = m.home_team_id
        JOIN stadiums s ON s.stadium_id = m.stadium_id
        ORDER BY m.match_date DESC, m.match_id DESC
    """,
    "stadiums": """
        SELECT
            s.stadium_id,
            s.stadium_name,
            s.location,
            COUNT(m.match_id) AS game_count
        FROM stadiums s
        LEFT JOIN matches m ON m.stadium_id = s.stadium_id
        GROUP BY s.stadium_id, s.stadium_name, s.location
        ORDER BY game_count DESC, s.stadium_name
    """,
    "team_scores": """
        SELECT
            t.team_name,
            COUNT(*) AS games,
            SUM(x.score) AS total_score,
            ROUND(AVG(x.score), 2) AS avg_score
        FROM (
            SELECT away_team_id AS team_id, away_final_score AS score FROM matches
            UNION ALL
            SELECT home_team_id AS team_id, home_final_score AS score FROM matches
        ) x
        JOIN teams t ON t.team_id = x.team_id
        GROUP BY t.team_id, t.team_name
        ORDER BY total_score DESC
    """,
    "position_age": """
        SELECT
            position,
            COUNT(*) AS player_count,
            ROUND(AVG(YEAR(CURDATE()) - birth_year), 1) AS avg_age
        FROM players
        GROUP BY position
        ORDER BY player_count DESC, position
    """,
    "lineups": """
        SELECT
            ml.match_id,
            m.match_date,
            ml.player_id,
            ml.team_id,
            t.team_name,
            p.player_name,
            ml.batting_order,
            ml.starting_position,
            ml.is_starter
        FROM match_lineups ml
        JOIN matches m ON m.match_id = ml.match_id
        JOIN teams t ON t.team_id = ml.team_id
        JOIN players p ON p.player_id = ml.player_id
        ORDER BY m.match_date DESC, ml.match_id DESC, t.team_name, ml.batting_order
    """,
}


try:
    teams = run_query(queries["teams"])
    players = run_query(queries["players"])
    matches = run_query(queries["matches"])
    stadiums = run_query(queries["stadiums"])
    team_scores = run_query(queries["team_scores"])
    position_age = run_query(queries["position_age"])
    lineups = run_query(queries["lineups"])
except Exception as exc:
    st.error("DB에서 데이터를 가져오지 못했습니다.")
    st.caption(str(exc))
    st.info("MariaDB/MySQL이 켜져 있고, `baseball2` DB에 `batting_stats` 테이블이 추가되어 있는지 확인하세요.")
    st.stop()


standings = make_standings(teams, matches)
team_score_rank = make_team_score_ranking(team_scores)
batter_rank = make_batter_ranking(players)
match_rows = make_match_rows(matches)

st.markdown(
    """
    <div class="league-header">
        <p class="league-title">BASEBALL RECORDS</p>
        <div class="league-subtitle">Baseball DB 데이터를 기록실 형태로 정리했습니다.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

summary_cards(
    [
        ("팀", f"{len(teams):,}"),
        ("선수", f"{len(players):,}"),
        ("타자 기록", f"{len(batter_rank):,}"),
        ("경기", f"{len(matches):,}"),
    ]
)

tab_team, tab_player, tab_games, tab_stadium = st.tabs(["팀 순위", "선수 순위", "경기 결과", "구장"])

with tab_team:
    section_title("팀 순위")
    col1, col2 = st.columns([1.05, 1])

    with col1:
        st.markdown("#### 승률")
        render_table(
            standings,
            [
                ("rank", "순위"),
                ("team_name", "팀명"),
                ("G", "경기"),
                ("W", "승"),
                ("L", "패"),
                ("D", "무"),
                ("PCT", "승률"),
                ("GB", "게임차"),
                ("STREAK", "연속"),
            ],
            highlight="PCT",
            name_cols={"team_name"},
        )

    with col2:
        st.markdown("#### 득점")
        render_table(
            team_score_rank,
            [
                ("rank", "순위"),
                ("team_name", "팀명"),
                ("games", "G"),
                ("total_score", "R"),
                ("AVG", "평균득점"),
            ],
            highlight="AVG",
            name_cols={"team_name"},
        )

    section_title("포지션", "평균나이")
    position_view = position_age.copy()
    position_view["rank"] = range(1, len(position_view) + 1)
    position_view["avg_age"] = position_view["avg_age"].map(lambda value: f"{value:.1f}")
    render_table(
        position_view,
        [
            ("rank", "순위"),
            ("position", "포지션"),
            ("player_count", "선수"),
            ("avg_age", "AVG AGE"),
        ],
        highlight="avg_age",
        name_cols={"position"},
    )

with tab_player:
    section_title("선수 순위", "타율")
    col1, col2, col3 = st.columns(3)
    team_filter = col1.selectbox("팀", ["전체"] + sorted(batter_rank["team_name"].unique().tolist()))
    position_filter = col2.selectbox("포지션", ["전체"] + sorted(batter_rank["position"].unique().tolist()))
    keyword = col3.text_input("선수명")

    filtered_batters = batter_rank.copy()
    if team_filter != "전체":
        filtered_batters = filtered_batters[filtered_batters["team_name"] == team_filter]
    if position_filter != "전체":
        filtered_batters = filtered_batters[filtered_batters["position"] == position_filter]
    if keyword:
        filtered_batters = filtered_batters[
            filtered_batters["player_name"].str.contains(keyword, case=False, na=False)
        ]
    filtered_batters = filtered_batters.reset_index(drop=True)
    filtered_batters["rank"] = range(1, len(filtered_batters) + 1)

    render_table(
        filtered_batters,
        [
            ("rank", "순위"),
            ("player_name", "선수명"),
            ("team_name", "팀명"),
            ("AVG", "AVG"),
            ("G", "G"),
            ("PA", "PA"),
            ("AB", "AB"),
            ("R", "R"),
            ("H", "H"),
            ("2B", "2B"),
            ("3B", "3B"),
            ("HR", "HR"),
            ("RBI", "RBI"),
        ],
        highlight="AVG",
        name_cols={"player_name", "team_name"},
    )

with tab_games:
    section_title("경기 결과", "스코어")
    col1, col2 = st.columns(2)
    team_options = ["전체"] + sorted(set(match_rows["away_team"]).union(set(match_rows["home_team"])))
    stadium_options = ["전체"] + stadiums["stadium_name"].sort_values().tolist()
    selected_team = col1.selectbox("경기 팀", team_options)
    selected_stadium = col2.selectbox("경기장", stadium_options)

    filtered_matches = match_rows.copy()
    if selected_team != "전체":
        filtered_matches = filtered_matches[
            (filtered_matches["away_team"] == selected_team) | (filtered_matches["home_team"] == selected_team)
        ]
    if selected_stadium != "전체":
        filtered_matches = filtered_matches[filtered_matches["stadium_name"] == selected_stadium]

    render_table(
        filtered_matches,
        [
            ("date_label", "날짜"),
            ("time", "시간"),
            ("away_team", "원정"),
            ("score", "스코어"),
            ("home_team", "홈"),
            ("stadium_name", "구장"),
            ("winner_text", "승리팀"),
        ],
        highlight="score",
        name_cols={"away_team", "home_team", "stadium_name"},
        html_cols={"score", "winner_text"},
    )

with tab_stadium:
    section_title("구장", "경기 수")
    stadium_view = stadiums.copy()
    stadium_view["rank"] = range(1, len(stadium_view) + 1)
    render_table(
        stadium_view,
        [
            ("rank", "순위"),
            ("stadium_name", "구장명"),
            ("location", "지역"),
            ("game_count", "경기"),
        ],
        highlight="game_count",
        name_cols={"stadium_name", "location"},
    )

    section_title("라인업", "출전 명단")
    if lineups.empty:
        st.markdown('<div class="empty-box">match_lineups 테이블에 데이터가 없습니다.</div>', unsafe_allow_html=True)
    else:
        lineup_view = lineups.copy()
        lineup_view["starter_status"] = lineup_view["is_starter"].map(lambda value: "선발" if value == 1 else "교체")
        lineup_view["date_label"] = lineup_view["match_date"].apply(format_date_label)
        render_table(
            lineup_view.head(30),
            [
                ("date_label", "날짜"),
                ("team_name", "팀명"),
                ("batting_order", "타순"),
                ("player_name", "선수명"),
                ("starting_position", "POS"),
                ("starter_status", "구분"),
            ],
            highlight="batting_order",
            name_cols={"team_name", "player_name"},
        )
