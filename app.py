from flask import Flask, render_template, request, redirect, url_for, flash

from database import session
from model_database import Portfolio
from ai_service import generate_text


app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")


@app.get("/portfolio")
def portfolio_list():
    query = session.query(Portfolio)

    portfolio = query.all()
    session.close()

    return render_template(
        "portfolio_list.html",
        portfolio=portfolio,
        q="",
        sort="newest",
        viewed=None
    )


@app.route("/portfolio/new", methods=["GET", "POST"])
def portfolio_new():
    if request.method == "POST":
        ime = (request.form.get("ime") or "").strip()
        prezime = (request.form.get("prezime") or "").strip()
        godini = (request.form.get("godini") or "").strip()
        nasoka = (request.form.get("nasoka") or "").strip()
        vestini = (request.form.get("vestini") or "").strip()

        if not ime or not prezime or not godini or not nasoka or not vestini:
            flash("Име, презиме, години, насока и вештини се задолжителни.", "error")
            return render_template("manage.html", portfolio=None)

        portfolio = Portfolio(
            ime=ime,
            prezime=prezime,
            godini=godini,
            nasoka=nasoka,
            vestini=vestini,
        )
        session.add(portfolio)
        session.commit()
        return redirect(url_for("manage2", portfolio_id=portfolio.id))

    return render_template("manage.html", portfolio=None)



@app.get("/portfolio/<int:portfolio_id>")
def manage2(portfolio_id: int):
    portfolio = session.get(Portfolio, portfolio_id)
    if not portfolio:
        return "Не постои портфолио со ова ИД", 404
    return render_template("manage2.html", portfolio=portfolio)


@app.route("/portfolio/<int:portfolio_id>/edit", methods=["GET", "POST"])
def portfolio_edit(portfolio_id: int):
    portfolio = session.get(Portfolio, portfolio_id)
    portfolio.kratko_bio = request.form.get("kratko_bio")
    portfolio.proekti_iskustva = request.form.get("proekti_iskustva")
    if not portfolio:
        return "Не постои место со ова ИД", 404

    if request.method == "POST":
        ime = (request.form.get("ime") or "").strip()
        prezime = (request.form.get("prezime") or "").strip()
        godini = (request.form.get("godini") or "").strip()
        nasoka = (request.form.get("nasoka") or "").strip()
        vestini = (request.form.get("vestini") or "").strip()

        if not ime or not prezime or not godini or not nasoka or not vestini:
            flash("Име, презиме, години, насока и вештини се задолжителни.", "error")
            return render_template("manage.html", portfolio=None)


        portfolio.ime = ime
        portfolio.prezime = prezime
        portfolio.godini = godini
        portfolio.nasoka = nasoka
        portfolio.vestini = vestini

        session.commit()
        return redirect(url_for("manage2", portfolio_id=portfolio.id))

    return render_template("manage.html", portfolio=portfolio)


@app.post("/portfolio/<int:portfolio_id>/delete")
def portfolio_delete(portfolio_id: int):
    portfolio = session.get(Portfolio, portfolio_id)
    if not portfolio:
        return "Не постои место со ова ИД", 404
    session.delete(portfolio)
    session.commit()
    return redirect(url_for("portfolio_list"))



@app.route("/ai/rewrite/<int:portfolio_id>", methods=['POST'])
def ai_rewrite(portfolio_id):
    portfolio = session.get(Portfolio, portfolio_id)

    if not portfolio:
        return "Портфолиото не е пронајдено", 404

    current_text = portfolio.kratko_bio

    if not current_text or len(current_text.strip()) < 3:
        return "Грешка: Нема зачувано текст во базата за да се преправи. Прво внеси и зачувај текст.", 400

    tone = request.form.get('tone', 'student')
    base_instruction = f"Rewrite the following Macedonian text: '{current_text}'."

    if tone == 'professional':
        style_instruction = "Make it professional, formal, suitable for LinkedIn. Use sophisticated business vocabulary."
    elif tone == 'short':
        style_instruction = "Summarize it into maximum 1 or 2 short sentences. Be direct."
    else:
        style_instruction = "Make it sound like a friendly, enthusiastic university student. Casual tone."

    final_prompt = (
        f"{base_instruction} {style_instruction} "
        "Keep the output in Macedonian language only. "
        "Do not add introductory text like 'Here is the rewrite'."
    )

    try:
        new_text = generate_text(final_prompt)
        portfolio.kratko_bio = new_text
        session.commit()

    except Exception as e:
        return f"Настана грешка со AI: {str(e)}"

    return redirect(url_for('manage', portfolio_id=portfolio.id))

@app.get("/portfolio/view/<int:portfolio_id>")
def view_portfolio(portfolio_id):
    portfolio = session.get(Portfolio, portfolio_id)
    return render_template("portfolio_detail.html", portfolio=portfolio)

@app.post("/portfolio/delete/<int:portfolio_id>")
def delete_portfolio(portfolio_id):
    portfolio = session.get(Portfolio, portfolio_id)
    if portfolio:
        session.delete(portfolio)
        session.commit()
    return redirect(url_for("portfolio_list"))



if __name__ == "__main__":
    app.run(debug=True)



    4214214341321