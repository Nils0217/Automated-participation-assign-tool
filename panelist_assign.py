import pandas as pd
import random

panels = {
    1: 'Name 1',
    2: 'Name 2',
    3: 'Name 3',
    4: "Name 4",
    5: 'Name 5'
}

def normalize(name):
    return " ".join(name.strip().split()).title()

def ask_panelist(prompt, exclude=None):
    while True:
        val = input(prompt).strip()
        if val.lower() == "na" or not val:
            return None
        if val.isdigit() and int(val) in panels:
            p = panels[int(val)]
            if p == exclude:
                print(f"  ⚠ Must be different from Panelist 1.")
            else:
                return p
        else:
            print(f"  ⚠ Not valid. Enter a number 1-5.")

def design_framework():
    panelist_display = "  " + "\n  ".join([f"{k}. {v}" for k, v in panels.items()])

    print("--- Panelist Assignment Tool ---")
    print(f"Available panelists:\n{panelist_display}\n")
    #print("Enter each user below. Type 'done' when finished.\n")

    user_list = []
    seen_names = set()
    i = 1

    while True:
        name_input = input(f"{i}. Your name: ").strip()

        if name_input.lower() == "done":
            if not user_list:
                print("No users entered. Exiting.")
                return
            break

        if not name_input:
            print("  ⚠ Name cannot be blank.\n")
            continue

        name = normalize(name_input)

        if name in seen_names:
            print(f"  ⚠ '{name}' already entered. Please enter a different name.\n")
            continue

        print(f"  Panelists: " + "  |  ".join([f"{k}. {v}" for k, v in panels.items()]))
        p1 = ask_panelist("  Panelist 1 (1-5, or 'na'): ")
        p2 = ask_panelist("  Panelist 2 fallback (1-5, or 'na'): ", exclude=p1) if p1 else None

        seen_names.add(name)
        user_list.append({"name": name, "p1": p1, "p2": p2})
        print()
        i += 1

    # Assign
    total = len(user_list)
    quota = total // len(panels) + 1
    p_counts = {p: 0 for p in panels.values()}
    final_assignments = {}

    # First pass — honour p1
    unassigned = []
    for user in user_list:
        name, p1, p2 = user["name"], user["p1"], user["p2"]
        if p1 and p_counts[p1] < quota:
            final_assignments[name] = p1
            p_counts[p1] += 1
        else:
            unassigned.append({"name": name, "p2": p2})

    # Second pass — try p2, then least loaded
    random.shuffle(unassigned)
    for user in unassigned:
        name, p2 = user["name"], user["p2"]
        if p2 and p_counts[p2] < quota:
            final_assignments[name] = p2
            p_counts[p2] += 1
        else:
            target = min(p_counts, key=p_counts.get)
            final_assignments[name] = target
            p_counts[target] += 1

    # Rebalance — no gap > 2
    for _ in range(200):
        max_p = max(p_counts, key=p_counts.get)
        min_p = min(p_counts, key=p_counts.get)
        if p_counts[max_p] - p_counts[min_p] <= 2:
            break
        moved = False
        for uname, assigned in final_assignments.items():
            if assigned == max_p:
                user_data = next(u for u in user_list if u["name"] == uname)
                if user_data["p1"] != max_p:
                    final_assignments[uname] = min_p
                    p_counts[max_p] -= 1
                    p_counts[min_p] += 1
                    moved = True
                    break
        if not moved:
            for uname, assigned in final_assignments.items():
                if assigned == max_p:
                    final_assignments[uname] = min_p
                    p_counts[max_p] -= 1
                    p_counts[min_p] += 1
                    break

    # Output CSV
    ordered = [u["name"] for u in user_list]
    df = pd.DataFrame(
        [(name, final_assignments[name]) for name in ordered],
        columns=["User Name", "Assigned Panelist"]
    )
    file_name = "panelist_assignment.csv"
    df.to_csv(file_name, index=False, encoding="utf-8-sig")

    print("\n--- Final Assignment ---")
    for p in panels.values():
        print(f"  {p}: {p_counts[p]} users")
    print(f"\n✓ Saved to '{file_name}'")

if __name__ == "__main__":
    design_framework()
