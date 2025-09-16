"""Command line CRM application for tracking student relationships."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

DEFAULT_DATA_PATH = Path(__file__).with_name("students.json")


def load_students(path: Path) -> List[dict]:
    """Return the list of students stored in *path*.

    The file is expected to contain a JSON array. If the file does not exist an
    empty list is returned. Each student dictionary is normalised so that the
    ``notes`` and ``tags`` keys are present.
    """

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError("Student data must be stored as a JSON list")

    return [_normalise_student(item) for item in data]


def save_students(path: Path, students: Iterable[dict]) -> None:
    """Write *students* back to *path* in a human readable format."""

    serialisable = [_normalise_student(student) for student in students]
    with path.open("w", encoding="utf-8") as fh:
        json.dump(serialisable, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def _normalise_student(raw: dict) -> dict:
    student = dict(raw)
    student.setdefault("notes", [])
    student.setdefault("tags", [])
    return student


def _format_table(headers: List[str], rows: List[List[str]]) -> str:
    widths = [len(column) for column in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(row: List[str]) -> str:
        return " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row))

    divider = "-+-".join("-" * width for width in widths)
    output = [format_row(headers), divider]
    output.extend(format_row(row) for row in rows)
    return "\n".join(output)


def _select_students(
    students: Iterable[dict],
    *,
    status: Optional[str] = None,
    stage: Optional[str] = None,
    tag: Optional[str] = None,
    owner: Optional[str] = None,
) -> List[dict]:
    results = []
    for student in students:
        if status and student.get("status", "").lower() != status.lower():
            continue
        if stage and student.get("stage", "").lower() != stage.lower():
            continue
        if owner and student.get("owner", "").lower() != owner.lower():
            continue
        if tag and tag.lower() not in {t.lower() for t in student.get("tags", [])}:
            continue
        results.append(student)
    return results


def _print_student_table(students: List[dict]) -> None:
    if not students:
        print("No students found.")
        return

    headers = ["ID", "Name", "Stage", "Status", "Owner", "Email", "Tags"]
    rows = []
    for student in students:
        full_name = "{} {}".format(
            student.get("first_name", "").strip(), student.get("last_name", "").strip()
        ).strip()
        tags = ", ".join(student.get("tags", [])) or "-"
        rows.append(
            [
                student.get("id", "-"),
                full_name or "-",
                student.get("stage", "-"),
                student.get("status", "-"),
                student.get("owner", "-"),
                student.get("email", "-"),
                tags,
            ]
        )

    print(_format_table(headers, rows))


def _generate_student_id(students: Iterable[dict]) -> str:
    prefix = "stu-"
    highest = 0
    for student in students:
        identifier = student.get("id", "")
        if identifier.startswith(prefix):
            try:
                value = int(identifier[len(prefix) :])
            except ValueError:
                continue
            highest = max(highest, value)
    return f"{prefix}{highest + 1:03d}"


def _search_students(students: Iterable[dict], query: str, field: Optional[str]) -> List[dict]:
    query_lower = query.lower()

    def candidate_values(student: dict) -> List[str]:
        values = []
        full_name = "{} {}".format(
            student.get("first_name", "").strip(), student.get("last_name", "").strip()
        ).strip()

        def maybe_add(key: str, value: Optional[str]) -> None:
            if value:
                values.append(value)

        if field is None or field == "name":
            maybe_add("name", full_name)
        if field is None or field == "email":
            maybe_add("email", student.get("email"))
        if field is None or field == "phone":
            maybe_add("phone", student.get("phone"))
        if field is None or field == "stage":
            maybe_add("stage", student.get("stage"))
        if field is None or field == "status":
            maybe_add("status", student.get("status"))
        if field is None or field == "owner":
            maybe_add("owner", student.get("owner"))
        if field is None or field == "tags":
            values.extend(student.get("tags", []))
        if field is None or field == "notes":
            for note in student.get("notes", []):
                if isinstance(note, dict):
                    maybe_add("note", note.get("content"))
                    maybe_add("note", note.get("author"))
                elif isinstance(note, str):
                    values.append(note)
        return values

    matches = []
    for student in students:
        for value in candidate_values(student):
            if query_lower in value.lower():
                matches.append(student)
                break
    return matches


def _print_student_details(student: dict) -> None:
    full_name = "{} {}".format(
        student.get("first_name", "").strip(), student.get("last_name", "").strip()
    ).strip()

    lines = [
        f"ID      : {student.get('id', '-')}",
        f"Name    : {full_name or '-'}",
        f"Email   : {student.get('email', '-')}",
        f"Phone   : {student.get('phone', '-')}",
        f"Status  : {student.get('status', '-')}",
        f"Stage   : {student.get('stage', '-')}",
        f"Owner   : {student.get('owner', '-')}",
        f"Tags    : {', '.join(student.get('tags', [])) or '-'}",
    ]

    print("\n".join(lines))

    notes = student.get("notes", [])
    print("Notes  :", end=" ")
    if not notes:
        print("(none)")
    else:
        print()
        for note in notes:
            if isinstance(note, dict):
                timestamp = note.get("timestamp", "-")
                author = note.get("author")
                author_part = f" ({author})" if author else ""
                content = note.get("content", "").strip() or "-"
                print(f"  - [{timestamp}]{author_part} {content}")
            else:
                print(f"  - {note}")


def handle_list(args: argparse.Namespace, students: List[dict]) -> bool:
    selected = _select_students(
        students,
        status=args.status,
        stage=args.stage,
        tag=args.tag,
        owner=args.owner,
    )
    _print_student_table(selected)
    return False


def handle_search(args: argparse.Namespace, students: List[dict]) -> bool:
    matches = _search_students(students, args.query, args.field)
    _print_student_table(matches)
    return False


def handle_info(args: argparse.Namespace, students: List[dict]) -> bool:
    student = next((s for s in students if s.get("id") == args.id), None)
    if not student:
        print(f"No student with id '{args.id}'", file=sys.stderr)
        return False
    _print_student_details(student)
    return False


def handle_add(args: argparse.Namespace, students: List[dict]) -> bool:
    identifier = _generate_student_id(students)
    student = {
        "id": identifier,
        "first_name": args.first_name,
        "last_name": args.last_name,
        "email": args.email,
        "phone": args.phone,
        "status": args.status,
        "stage": args.stage,
        "owner": args.owner,
        "tags": args.tag or [],
        "notes": [],
    }
    students.append(student)
    print(f"Created student {identifier} ({student['first_name']} {student['last_name']})")
    return True


def handle_update(args: argparse.Namespace, students: List[dict]) -> bool:
    student = next((s for s in students if s.get("id") == args.id), None)
    if not student:
        print(f"No student with id '{args.id}'", file=sys.stderr)
        return False

    changed = False
    for attr, value in {
        "first_name": args.first_name,
        "last_name": args.last_name,
        "email": args.email,
        "phone": args.phone,
        "status": args.status,
        "stage": args.stage,
        "owner": args.owner,
    }.items():
        if value is not None and student.get(attr) != value:
            student[attr] = value
            changed = True

    if args.tag is not None:
        student["tags"] = args.tag
        changed = True

    if changed:
        print(f"Updated student {args.id}")
    else:
        print("No changes applied")
    return changed


def handle_delete(args: argparse.Namespace, students: List[dict]) -> bool:
    for index, student in enumerate(students):
        if student.get("id") == args.id:
            removed = students.pop(index)
            full_name = "{} {}".format(
                removed.get("first_name", "").strip(), removed.get("last_name", "").strip()
            ).strip()
            print(f"Removed student {args.id} ({full_name or 'unknown'})")
            return True
    print(f"No student with id '{args.id}'", file=sys.stderr)
    return False


def handle_add_note(args: argparse.Namespace, students: List[dict]) -> bool:
    student = next((s for s in students if s.get("id") == args.id), None)
    if not student:
        print(f"No student with id '{args.id}'", file=sys.stderr)
        return False

    timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    note = {"timestamp": timestamp, "content": args.content.strip()}
    if args.author:
        note["author"] = args.author
    student.setdefault("notes", []).insert(0, note)
    print(f"Added note to {args.id}")
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Student CRM command line tool")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to the student data JSON file (defaults to students.json)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List students")
    list_parser.add_argument("--status", help="Filter by enrollment status")
    list_parser.add_argument("--stage", help="Filter by pipeline stage")
    list_parser.add_argument("--tag", help="Filter by a specific tag")
    list_parser.add_argument("--owner", help="Filter by relationship owner")
    list_parser.set_defaults(func=handle_list)

    search_parser = subparsers.add_parser("search", help="Search students")
    search_parser.add_argument("query", help="Text to look for")
    search_parser.add_argument(
        "--field",
        choices=["name", "email", "phone", "stage", "status", "owner", "tags", "notes"],
        help="Limit the search to a specific field",
    )
    search_parser.set_defaults(func=handle_search)

    info_parser = subparsers.add_parser("info", help="Display a single student")
    info_parser.add_argument("id", help="Student identifier")
    info_parser.set_defaults(func=handle_info)

    add_parser = subparsers.add_parser("add", help="Create a new student entry")
    add_parser.add_argument("first_name", help="First name")
    add_parser.add_argument("last_name", help="Last name")
    add_parser.add_argument("email", help="Primary email address")
    add_parser.add_argument("--phone", help="Phone number")
    add_parser.add_argument("--status", default="Prospect", help="Enrollment status")
    add_parser.add_argument("--stage", default="Inquiry", help="Pipeline stage")
    add_parser.add_argument("--owner", help="Relationship owner")
    add_parser.add_argument(
        "--tag",
        action="append",
        help="Assign a tag. Repeat for multiple tags",
    )
    add_parser.set_defaults(func=handle_add)

    update_parser = subparsers.add_parser("update", help="Update an existing student")
    update_parser.add_argument("id", help="Student identifier")
    update_parser.add_argument("--first-name", dest="first_name", help="First name")
    update_parser.add_argument("--last-name", dest="last_name", help="Last name")
    update_parser.add_argument("--email", help="Primary email address")
    update_parser.add_argument("--phone", help="Phone number")
    update_parser.add_argument("--status", help="Enrollment status")
    update_parser.add_argument("--stage", help="Pipeline stage")
    update_parser.add_argument("--owner", help="Relationship owner")
    update_parser.add_argument(
        "--tag",
        action="append",
        help="Replace existing tags. Repeat for multiple tags",
    )
    update_parser.set_defaults(func=handle_update)

    delete_parser = subparsers.add_parser("delete", help="Remove a student")
    delete_parser.add_argument("id", help="Student identifier")
    delete_parser.set_defaults(func=handle_delete)

    note_parser = subparsers.add_parser("add-note", help="Attach a note to a student")
    note_parser.add_argument("id", help="Student identifier")
    note_parser.add_argument("content", help="The note text")
    note_parser.add_argument("--author", help="Who wrote the note")
    note_parser.set_defaults(func=handle_add_note)

    return parser


def main(argv: Optional[List[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        students = load_students(args.data)
    except ValueError as error:
        parser.error(str(error))
        return

    changed = args.func(args, students)
    if changed:
        save_students(args.data, students)


if __name__ == "__main__":
    main()
