from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("invoices.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    conn = get_db_connection()

    invoices = conn.execute(
        "SELECT * FROM invoices"
    ).fetchall()

    status_counts = conn.execute("""
    SELECT status, COUNT(*) as count
    FROM invoices
    GROUP BY status
""").fetchall()

    conn.close()


    return render_template(
        "index.html",
        invoices=invoices,
        status_counts=status_counts
    )

@app.route("/add", methods=["POST"])
def add_invoice():

    invoice_number = request.form["invoice_number"]
    client_name = request.form["client_name"]
    amount = request.form["amount"]
    invoice_date = request.form["invoice_date"]
    due_date = request.form["due_date"]

    # Check for duplicate invoice number
    conn = get_db_connection()

    existing_invoice = conn.execute(
        "SELECT id FROM invoices WHERE invoice_number = ?",
        (invoice_number,)
    ).fetchone()

    conn.close()

    if existing_invoice:
        return "Error: Invoice number already exists. Please use a different invoice number."

    # Validation
    

    # Validation
    flag_reason = None

    if not client_name.strip():
        flag_reason = "Missing client name"
    elif not amount.strip():
        flag_reason = "Amount is required"
    else:
        try:
            if float(amount) <= 0:
                flag_reason = "Amount must be greater than zero"
        except ValueError:
            flag_reason = "Amount must be a valid number"

    # Decide status
    if flag_reason:
        status = "Quarantine"
    else:
        status = "Draft"

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO invoices
        (invoice_number, client_name, amount, invoice_date, due_date, status, flag_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice_number,
        client_name,
        amount,
        invoice_date,
        due_date,
        status,
        flag_reason
    ))

    conn.commit()
    conn.close()

    return redirect("/")

# DELETE INVOICE
@app.route("/delete/<int:invoice_id>")
def delete_invoice(invoice_id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM invoices WHERE id = ?",
        (invoice_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# EDIT INVOICE
@app.route("/edit/<int:invoice_id>", methods=["GET", "POST"])
def edit_invoice(invoice_id):

    conn = get_db_connection()

    if request.method == "POST":

        invoice_number = request.form["invoice_number"]
        client_name = request.form["client_name"]
        amount = request.form["amount"]
        invoice_date = request.form["invoice_date"]
        due_date = request.form["due_date"]

        conn.execute("""
            UPDATE invoices
            SET invoice_number = ?,
                client_name = ?,
                amount = ?,
                invoice_date = ?,
                due_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            invoice_number,
            client_name,
            amount,
            invoice_date,
            due_date,
            invoice_id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    invoice = conn.execute(
        "SELECT * FROM invoices WHERE id = ?",
        (invoice_id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", invoice=invoice)


# UPDATE STATUS
# UPDATE STATUS
# UPDATE STATUS
@app.route("/update_status/<int:invoice_id>", methods=["POST"])
def update_status(invoice_id):

    new_status = request.form["status"]

    conn = get_db_connection()

    invoice = conn.execute(
        "SELECT * FROM invoices WHERE id = ?",
        (invoice_id,)
    ).fetchone()

    current_status = invoice["status"]

    allowed_transitions = {
        "Draft": ["Quarantine"],
        "Quarantine": ["Approved"],
        "Approved": ["Sent"],
        "Sent": ["Paid"],
        "Paid": []
    }

    if new_status in allowed_transitions[current_status]:

        conn.execute("""
            UPDATE invoices
            SET status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_status, invoice_id))

        conn.execute("""
            INSERT INTO status_log
            (invoice_id, old_status, new_status, changed_by)
            VALUES (?, ?, ?, ?)
        """, (
            invoice_id,
            current_status,
            new_status,
            "Admin"
        ))

        conn.commit()

    conn.close()

    return redirect("/")
# VIEW STATUS HISTORY
@app.route("/history/<int:invoice_id>")
def history(invoice_id):

    conn = get_db_connection()

    history = conn.execute("""
        SELECT * FROM status_log
        WHERE invoice_id = ?
        ORDER BY changed_at ASC
    """, (invoice_id,)).fetchall()

    conn.close()

    return render_template("history.html", history=history)

# START FLASK SERVER
if __name__ == "__main__":
    app.run(debug=True)
# START FLASK SERVER
if __name__ == "__main__":
    app.run(debug=True)



# START FLASK SERVER
if __name__ == "__main__":
    app.run(debug=True)