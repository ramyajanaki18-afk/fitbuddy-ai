from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserPlan
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")

@router.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user": None})

@router.post("/generate", response_class=HTMLResponse)
def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    workout_plan = generate_workout_gemini(name, age, weight, goal, intensity)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    db_plan = UserPlan(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        workout_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    # நேராக result template-ஐ ரெண்டர் செய்கிறோம்
    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": db_plan,
        "workout_plan": workout_plan,
        "nutrition_tip": nutrition_tip
    })

@router.get("/result/{plan_id}", response_class=HTMLResponse)
def view_result(request: Request, plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(UserPlan).filter(UserPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": db_plan,
        "workout_plan": db_plan.workout_plan,
        "nutrition_tip": db_plan.nutrition_tip
    })

@router.post("/update/{plan_id}", response_class=HTMLResponse)
def update_plan(
    request: Request,
    plan_id: int,
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    db_plan = db.query(UserPlan).filter(UserPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    updated_workout = generate_workout_gemini(
        name=db_plan.name,
        age=db_plan.age,
        weight=db_plan.weight,
        goal=db_plan.goal,
        intensity=db_plan.intensity,
        feedback=feedback
    )

    db_plan.workout_plan = updated_workout
    db.commit()
    db.refresh(db_plan)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "user": db_plan,
        "workout_plan": updated_workout,
        "nutrition_tip": db_plan.nutrition_tip
    })

@router.get("/admin/users", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    users = db.query(UserPlan.id, UserPlan.name, UserPlan.goal, UserPlan.created_at).all()
    return templates.TemplateResponse("all_users.html", {"request": request, "users": users})