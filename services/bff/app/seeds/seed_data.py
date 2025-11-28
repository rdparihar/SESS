import json
from pathlib import Path
from datetime import datetime

from ..database import session_scope, Base, engine
from ..models import Team, User, Project, Runbook, PTO, Allocation


def load_fixtures():
    fixture_path = Path(__file__).parent / "fixtures.json"
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_seed():
    data = load_fixtures()
    Base.metadata.create_all(bind=engine)
    with session_scope() as session:
        teams = {}
        for record in data.get("teams", []):
            team = Team(name=record["name"], description=record.get("description"))
            session.add(team)
            teams[team.name] = team
        session.flush()

        users = {}
        for record in data.get("users", []):
            team = teams.get(record.get("team"))
            user = User(
                email=record["email"],
                name=record["name"],
                role=record.get("role"),
                team=team,
            )
            session.add(user)
            users[user.email] = user
        session.flush()

        projects = {}
        for record in data.get("projects", []):
            project = Project(
                name=record["name"],
                description=record.get("description"),
                team=teams.get(record.get("team")),
            )
            session.add(project)
            projects[project.name] = project
        session.flush()

        for record in data.get("runbooks", []):
            runbook = Runbook(
                title=record["title"],
                content=record["content"],
                project=projects.get(record.get("project")),
            )
            session.add(runbook)

        for record in data.get("pto", []):
            pto = PTO(
                user=users.get(record.get("user")),
                start_date=datetime.fromisoformat(record["start_date"]).date(),
                end_date=datetime.fromisoformat(record["end_date"]).date(),
            )
            session.add(pto)

        for record in data.get("allocations", []):
            allocation = Allocation(
                user=users.get(record.get("user")),
                project=projects.get(record.get("project")),
                percent=record["percent"],
            )
            session.add(allocation)

        print("Seed data applied")


if __name__ == "__main__":
    apply_seed()
