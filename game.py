import os
import sys
from generator import Case, generate_case
from state import PlayerState
from utils import fmt, divider, numbered_list, calculate_score

def clear():
    os.system("cls" if os.name == "nt" else "clear")
def pause():
    input("\n  [Tekan Enter untuk melanjutkan / Press Enter to continue]")
def print_header(title: str, subtitle: str = ""):
    print()
    print(divider("═"))
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print(divider("═"))
def print_section(header: str):
    print()
    print(divider())
    print(f"  {header}")
    print(divider())
def select_language() -> str:
    clear()
    print_header("DETECTIVE GAME", "")
    while True:
        choice = input(
            "\n  Pilih bahasa / Select language:\n"
            "  1. Indonesia\n"
            "  2. English\n"
            "  > "
        ).strip()
        if choice == "1":
            return "id"
        elif choice == "2":
            return "en"
        else:
            print("Pilihan tidak valid / Invalid choice.")
def print_hud(case: Case, state: PlayerState, score: int):
    ui = case.lang["ui"]
    snap = state.status_snapshot()
    info = fmt(
        ui["score_info"],
        score=score,
        clues=snap["clues"],
        max_clues=snap["max_clues"],
        witnesses=snap["witnesses"],
        max_witnesses=snap["max_witnesses"],
    )
    print(f"\n {info}")
def visit_crime_scene(case: Case, state: PlayerState) -> int:
    ui = case.lang["ui"]
    print_section(ui["clue_header"])
    if not state.has_more_clues():
        print(f"\n {ui['already_visited']}")
        pause()
        return 0
    idx = state.scene_visits
    clue = case.clues[idx]
    state.scene_visits += 1
    state.clues_collected += 1
    state.clues_seen.append(clue)
    print(f"\n {clue}")
    print(f"\n {fmt(ui['clues_found'], current=state.clues_collected, total=state.scene_visits)}")
    if len(state.clues_seen) > 1:
        print(f"\n  ── Semua petunjuk sebelumnya / All previous clues ──")
        for i, c in enumerate(state.clues_seen[:-1], 1):
            print(f"  {i}. {c}")
    pause()
    return 30
def interview_witness(case: Case, state: PlayerState) -> int:
    ui = case.lang["ui"]
    print_section(ui["witness_header"])
    if not state.has_more_witnesses():
        print(f"\n {ui['already_met_witness']}")
        pause()
        return 0
    idx = state.witnesses_interviewed
    statement = case.witness_pool[idx]
    state.witnesses_interviewed += 1
    state.witness_statements.append(statement)
    print(f'\n "{statement}"')
    print("\n Catatan: Saksi tidak selalu jujur / Note: Witnesses may not always be truthful.")
    pause()
    return 20
def show_suspects(case: Case):
    ui = case.lang["ui"]
    print_section(ui["suspect_header"])
    print()
    print(numbered_list(case.suspects))
    pause()
def arrest_suspect(case: Case, state: PlayerState) -> bool:
    ui = case.lang["ui"]
    print_section(ui["arrest_header"])
    if not case.suspects:
        print(f"\n {ui['no_suspects']}")
        pause()
        return False
    print()
    print(numbered_list(case.suspects))
    print()
    while True:
        raw = input(f"  {ui['arrest_prompt']}").strip()
        if raw.isdigit():
            idx = int(raw) - 1
            if 0 <= idx < len(case.suspects):
                break
        print(f" {ui['invalid_choice']}")
    chosen = case.suspects[idx]
    print(f"\n {fmt(ui['arrest_confirm'], suspect=chosen)}")
    state.arrested = True
    state.arrested_suspect = chosen
    state.game_over = True
    return chosen == case.killer
def show_win(case: Case, state: PlayerState, score: int):
    ui = case.lang["ui"]
    clear()
    print_header(ui["title"])
    msg = fmt(ui["win_message"], killer=case.killer, score=score)
    print(msg)
    print()
def show_lose(case: Case, state: PlayerState):
    ui = case.lang["ui"]
    clear()
    print_header(ui["title"])
    msg = fmt(
        ui["lose_message"],
        suspect=state.arrested_suspect,
        killer=case.killer,
    )
    print(msg)
    print()
def main_menu(case: Case, state: PlayerState, score: int) -> str:
    ui = case.lang["ui"]
    clear()
    print_header(ui["title"], ui["subtitle"])
    print_hud(case, state, score)
    print_section(ui["menu_title"])
    print()
    print(numbered_list(ui["menu_items"]))
    print()
    while True:
        raw = input("  > ").strip()
        if raw in {"1", "2", "3", "4", "5"}:
            return raw
        print(f" {ui['invalid_choice']}")
def run_game():
    lang = select_language()
    case = generate_case(lang_code=lang, suspect_count=4)
    state = PlayerState(max_scene_visits=len(case.clues), max_witnesses=len(case.witness_pool))
    ui = case.lang["ui"]
    score = 1000
    clear()
    print_header(ui["title"], ui["subtitle"])
    print_section(ui["case_intro"])
    intro = fmt(
        ui["case_detail"],
        location=case.location,
        weapon=case.weapon,
        suspect_count=len(case.suspects),
    )
    print(f"\n  {intro}")
    pause()
    while not state.game_over:
        choice = main_menu(case, state, score)
        if choice == "1":
            penalty = visit_crime_scene(case, state)
            score = max(100, score - penalty)
        elif choice == "2":
            penalty = interview_witness(case, state)
            score = max(100, score - penalty)
        elif choice == "3":
            show_suspects(case)
        elif choice == "4":
            correct = arrest_suspect(case, state)
            final_score = calculate_score(
                state.clues_collected,
                state.max_scene_visits,
                state.witnesses_interviewed,
                state.max_witnesses,
            )
            if correct:
                show_win(case, state, final_score)
            else:
                show_lose(case, state)
        elif choice == "5":
            clear()
            print(f"\n  {ui['exit_message']}\n")
            sys.exit(0)
    while True:
        again = input("\n  Main lagi? / Play again? (y/n): ").strip().lower()
        if again == "y":
            run_game()
            return
        elif again == "n":
            clear()
            print(f"\n  {ui['exit_message']}\n")
            sys.exit(0)