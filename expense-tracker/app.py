import base64
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend import ExpenseAgent
from sheets import GoogleSheetsClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

agent = ExpenseAgent()
sheets = GoogleSheetsClient()

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 5 * 1024 * 1024


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.post("/api/analyze", response_class=HTMLResponse)
async def analyze(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        return _err(f"Type non supporté : {file.content_type}")

    image_bytes = await file.read()
    if len(image_bytes) > MAX_SIZE_BYTES:
        return _err("Fichier trop volumineux (max 5 Mo).")

    data = agent.extract_from_bytes(image_bytes, file.content_type)
    image_data = f"{file.content_type}|{file.filename}|{base64.b64encode(image_bytes).decode()}"
    return _form(data, image_data)


@app.post("/api/submit", response_class=HTMLResponse)
async def submit(
    image_data:  str = Form(...),
    categorie:   str = Form(""),
    fournisseur: str = Form(""),
    date:        str = Form(""),
    montant_ttc: str = Form(""),
    tva:         str = Form(""),
    devise:      str = Form("EUR"),
    description: str = Form(""),
    confiance:   str = Form(""),
):
    try:
        media_type, filename, b64 = image_data.split("|", 2)
        image_bytes = base64.b64decode(b64)
    except Exception:
        return _err("Impossible de décoder l'image.")

    image_url = sheets.upload_image_to_drive(image_bytes, filename, media_type)
    sheets.append_expense({
        "categorie": categorie, "fournisseur": fournisseur, "date": date,
        "montant_ttc": montant_ttc or None, "tva": tva or None,
        "devise": devise, "description": description, "confiance": confiance or None,
    }, image_url)

    return f'<div class="success-box"><p> <strong>{fournisseur}</strong> — {montant_ttc} {devise} enregistré !</p><button onclick="location.reload()">Nouvelle dépense</button></div>'


@app.exception_handler(Exception)
async def on_error(request: Request, exc: Exception):
    return HTMLResponse(_err(str(exc)), status_code=500)


def _err(msg: str) -> str:
    return f'<div class="error-box"><p> {msg}</p></div>'


def _form(data: dict, image_data: str) -> str:
    v = lambda k: "" if data.get(k) is None else str(data.get(k))
    cats = ["restaurant", "transport", "hebergement", "carburant", "fournitures", "autre"]
    options = "".join(f'<option value="{c}" {"selected" if v("categorie")==c else ""}>{c}</option>' for c in cats)
    fields = [
        ("fournisseur", "Fournisseur",  "text",   ""),
        ("date",        "Date",         "text",   ""),
        ("montant_ttc", "Montant TTC",  "number", 'step="0.01"'),
        ("tva",         "TVA",          "number", 'step="0.01"'),
        ("devise",      "Devise",       "text",   ""),
        ("description", "Description",  "text",   ""),
        ("confiance",   "Confiance IA", "text",   "readonly"),
    ]
    inputs = "".join(
        f'<div class="field"><label>{lbl}</label><input type="{t}" name="{n}" value="{v(n)}" {extra}></div>'
        for n, lbl, t, extra in fields
    )
    return f'''<form hx-post="/api/submit" hx-target="#result" hx-swap="innerHTML">
    <input type="hidden" name="image_data" value="{image_data}">
    <div class="field"><label>Catégorie</label><select name="categorie">{options}</select></div>
    {inputs}
    <button type="submit"> Valider et enregistrer</button>
</form>'''