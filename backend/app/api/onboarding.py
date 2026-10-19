"""Onboarding over HTTP: background steps, the adaptive diagnostic and the profile card.
Conflicts and invalid answers are AitaErrors, mapped to 409 / 422 by the app handler."""

from fastapi import APIRouter, BackgroundTasks, Body, Depends
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.onboarding import (
    STEP_MODELS,
    AnswerIn,
    AnswerOut,
    CardOut,
    DiagOut,
    LanguageIn,
    ProfilePatch,
    RecheckOut,
    StateOut,
    Step,
    SwitchOut,
)
from app.services.onboarding import recheck, service

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


@router.get("/state", response_model=StateOut, summary="Where the student is, for resume")
def get_state(current_user: User = Depends(get_current_active_user),
              db: Session = Depends(get_db)):
    return service.state(db, current_user)


@router.put("/steps/{step}", response_model=StateOut, summary="Save one background step")
def put_step(step: Step, body: dict | None = Body(None),
             current_user: User = Depends(get_current_active_user),
             db: Session = Depends(get_db)):
    try:
        data = STEP_MODELS[step].model_validate(body or {})
    except ValidationError as exc:
        raise RequestValidationError(exc.errors(include_url=False)) from exc
    return service.save_step(db, current_user, step, data)


@router.post("/diagnostic/next", response_model=DiagOut, summary="The current diagnostic item")
def diagnostic_next(current_user: User = Depends(get_current_active_user),
                    db: Session = Depends(get_db)):
    return service.next_item(db, current_user)


@router.post("/diagnostic/answer", response_model=AnswerOut, summary="Answer the current item")
def diagnostic_answer(req: AnswerIn, background_tasks: BackgroundTasks,
                      current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    return service.answer(db, current_user, req, background_tasks)


@router.post("/finish", response_model=CardOut, summary="Seed the learner model; the card")
def finish(background_tasks: BackgroundTasks,
           current_user: User = Depends(get_current_active_user),
           db: Session = Depends(get_db)):
    return service.finish(db, current_user, background_tasks)


@router.post("/language", response_model=SwitchOut, summary="Switch the study language")
def switch_language(req: LanguageIn, current_user: User = Depends(get_current_active_user),
                    db: Session = Depends(get_db)):
    return recheck.switch_language(db, current_user, req.language)


@router.post("/recheck/next", response_model=DiagOut, summary="The current language-check item")
def recheck_next(current_user: User = Depends(get_current_active_user),
                 db: Session = Depends(get_db)):
    return recheck.next_item(db, current_user)


@router.post("/recheck/answer", response_model=AnswerOut, summary="Answer a language-check item")
def recheck_answer(req: AnswerIn, background_tasks: BackgroundTasks,
                   current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    return recheck.answer(db, current_user, req, background_tasks)


@router.post("/recheck/finish", response_model=RecheckOut,
             summary="Seed the new language from its check")
def recheck_finish(current_user: User = Depends(get_current_active_user),
                   db: Session = Depends(get_db)):
    return recheck.finish(db, current_user)


@router.patch("/profile", response_model=CardOut, summary="Edit background answers")
def edit_profile(req: ProfilePatch, current_user: User = Depends(get_current_active_user),
                 db: Session = Depends(get_db)):
    return service.edit_profile(db, current_user, req)
