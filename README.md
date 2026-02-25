# Automated-participation-assign-tool
Automation using python

# Panelist Assignment Tool

A command-line tool that collects user names and panelist preferences, then automatically assigns each user to a panelist as evenly as possible.

---

## Requirements

- Python 3.7+
- pandas

Install dependencies:
```bash
pip install pandas
```

---

## How to Run

```bash
python panelist_assign.py
```

---

## Usage

When the tool starts, it displays the available panelists and prompts each user to enter their information one at a time.

**Example session:**
```
--- Panelist Assignment Tool ---
Available panelists (Insert your panelist's name):
    1: 'Name 1',
    2: 'Name 2',
    3: 'Name 3',
    4: "Name 4",
    5: 'Name 5'

Enter each user below. Type 'done' when finished.

1. Your name: Alice
  Panelist 1 (1-5, or 'na'): 2
  Panelist 2 fallback (1-5, or 'na'): 4

2. Your name: Bob
  Panelist 1 (1-5, or 'na'): na

3. Your name: done

--- Final Assignment ---
  Name 1: 0 users
  Name 2: 1 users
  ...

✓ Saved to 'panelist_assignment.csv'
```

### Input Rules

| Field | What to type |
|---|---|
| Your name | Any name. Cannot be blank or a duplicate. |
| Panelist 1 | A number `1–5` for your preferred panelist, or `na` for no preference. |
| Panelist 2 fallback | A number `1–5` (different from Panelist 1) as a backup, or `na`. Only asked if Panelist 1 was given. |
| Finish | Type `done` at the name prompt when all users are entered. |

---

## Assignment Logic

1. **Honour Panelist 1** — if a user selected a preferred panelist and that panelist is not over quota, they are assigned there.
2. **Try Panelist 2** — if Panelist 1 is full, the tool tries the fallback panelist.
3. **Random assignment** — if neither preference can be fulfilled (or no preference was given), the user is assigned to whichever panelist currently has the fewest users.
4. **Rebalance** — after all assignments, if the gap between the most and least loaded panelist exceeds 2, users without strong preferences are moved around until the distribution is balanced.

---

## Output

A CSV file named `panelist_assignment.csv` is saved in the same directory, with two columns:

| User Name | Assigned Panelist |
|---|---|
| Alice | Ramon Zapata |
| Bob | Kyle O'Neil |

---

## Updating the Panelist List

To change the panelists, edit the `panels` dictionary at the top of `panelist_assign.py`:

```python
panels = {
    1: 'Name 1',
    2: 'Name 2',
    3: 'Name 3',
    4: "Name 4",
    5: 'Name 5'
}
```
