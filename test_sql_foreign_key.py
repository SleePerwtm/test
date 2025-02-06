from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship
from typing import Annotated
from fastapi import Depends, FastAPI


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


class Classes(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, default=None)

    students: list["Student"] = Relationship(back_populates="cLass")


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, default=None)
    class_id: int = Field(foreign_key="classes.id")

    cLass: "Classes" = Relationship(back_populates="students")


@app.post("/class/", response_model=Classes)
def create_class(class_: Classes, session: Session = Depends(get_session)):
    session.add(class_)
    session.commit()
    session.refresh(class_)
    return class_


@app.post("/students/", response_model=Student)
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


if __name__ == "__main__":
    create_db_and_tables()

    import uvicorn

    uvicorn.run(app="test_sql_foreign_key:app", port=1234, reload=True)
