from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import json_text, now_iso, run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"

load_lab_env(ROOT)


def create_transcript(version: str, model: str) -> dict[str, Any]:
    artifact_version = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = f"{version}_gemini_ui_{timestamp}"
    return {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": "gemini",
        "model": model,
        "system_prompt": str(SYSTEM_PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": 5,
        "max_tool_rounds": 4,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def start_conversation(version: str, model: str) -> None:
    transcript = create_transcript(version, model)
    st.session_state.transcript = transcript
    st.session_state.history = []
    st.session_state.transcript_path = TRANSCRIPTS_DIR / f"{transcript['transcript_id']}.transcript.json"
    write_transcript(st.session_state.transcript_path, transcript)


@st.cache_resource
def gemini_provider() -> Any:
    return make_provider("gemini")


def save_transcript() -> None:
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)


def render_json(value: Any) -> None:
    st.code(json_text(value, max_chars=12000), language="json")


def render_turn(turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.markdown(turn["user"])

    with st.chat_message("assistant"):
        status = turn.get("status", "unknown")
        if status == "provider_error":
            st.error(turn.get("error", "Unknown provider error"))
        else:
            st.markdown(turn.get("assistant_text") or "No response text returned.")

        label = f"Execution trace: {len(turn.get('tool_events', []))} tool call(s)"
        with st.expander(label, expanded=bool(turn.get("tool_events"))):
            st.caption(f"Status: {status} | Started: {turn.get('started_at', 'unknown')}")
            for round_data in turn.get("rounds", []):
                st.markdown(f"**Round {round_data['round']}**")
                if round_data.get("assistant_text"):
                    st.caption("Gemini tool-planning response")
                    st.write(round_data["assistant_text"])
                for event in round_data.get("tool_results", []):
                    result = event.get("result")
                    has_error = isinstance(result, dict) and "error" in result
                    heading = f"{'Error' if has_error else 'Result'}: `{event['tool']}`"
                    (st.error if has_error else st.success)(heading)
                    left, right = st.columns(2)
                    with left:
                        st.caption("Arguments")
                        render_json(event.get("args", {}))
                    with right:
                        st.caption("Output")
                        render_json(result)


def main() -> None:
    st.set_page_config(page_title="Gemini Research Agent", page_icon="G", layout="wide")
    st.markdown(
        """
        <style>
          .block-container { max-width: 1100px; padding-top: 2rem; }
          [data-testid="stSidebar"] { border-right: 1px solid #e5e7eb; }
          .stChatMessage { border-radius: 12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("Gemini Research Agent")
        st.caption("Gemini API only. Tool execution stays local.")
        version = st.text_input("Artifact version", value="v3")
        model = st.text_input("Gemini model", value="gemini-3.5-flash-lite")
        st.divider()
        if st.button("New conversation", use_container_width=True):
            start_conversation(version.strip() or "ui", model.strip() or "gemini-3.5-flash-lite")
            st.rerun()

    if "transcript" not in st.session_state:
        start_conversation(version.strip() or "ui", model.strip() or "gemini-3.5-flash-lite")

    transcript = st.session_state.transcript
    st.title("Research workspace")
    st.caption("Requests, Gemini responses, tool traces, outputs, and errors are saved after each turn.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Provider", "Gemini")
    col2.metric("Turns", len(transcript["turns"]))
    col3.metric("Tool calls", sum(len(turn.get("tool_events", [])) for turn in transcript["turns"]))
    st.caption(f"Transcript: `{st.session_state.transcript_path.relative_to(ROOT)}`")

    for turn in transcript["turns"]:
        render_turn(turn)

    prompt = st.chat_input("Ask the research agent")
    if not prompt:
        return

    turn: dict[str, Any] = {
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini is reasoning and running tools..."):
            try:
                messages = [
                    {"role": "system", "content": SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")},
                    *trim_history(st.session_state.history, transcript["history_window"]),
                    {"role": "user", "content": prompt},
                ]
                declarations = load_tool_declarations(TOOLS_PATH)
                result = run_model_tool_loop(
                    provider=gemini_provider(),
                    messages=messages,
                    tools=to_openai_tools(declarations),
                    model=transcript["model"],
                    max_tool_rounds=transcript["max_tool_rounds"],
                )
                turn.update(result)
                st.markdown(result["assistant_text"] or "No response text returned.")
            except Exception as exc:
                turn.update({
                    "status": "provider_error",
                    "error": f"{type(exc).__name__}: {exc}",
                })
                st.error(turn["error"])

    turn["ended_at"] = now_iso()
    transcript["turns"].append(turn)
    if turn["status"] != "provider_error":
        st.session_state.history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": turn["assistant_text"] or ""},
        ])
    save_transcript()
    st.rerun()


if __name__ == "__main__":
    main()
