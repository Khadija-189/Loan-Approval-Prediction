import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# =====================
# LOAD DATA
# =====================
df = pd.read_csv("loan_data.csv")

X = df[["age", "salary", "credit_score", "loan_amount", "employment"]]
y = df["approved"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))

# =====================
# EMI Calculator
# =====================
def calculate_emi(principal, rate=0.12, years=5):
    monthly_rate = rate / 12
    months = years * 12
    emi = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -months)
    return emi

# =====================
# Prediction Function
# =====================
def predict_loan():
    try:
        age = int(entry_age.get())
        salary = float(entry_salary.get())
        credit = int(entry_credit.get())
        loan = float(entry_loan.get())
        employment = employment_var.get()

        prediction = model.predict([[age, salary, credit, loan, employment]])
        probability = model.predict_proba([[age, salary, credit, loan, employment]])

        approval_chance = probability[0][1] * 100
        emi = calculate_emi(loan)

        if prediction[0] == 1:
            result_label.config(text="✅ LOAN APPROVED", fg="#22c55e")
        else:
            result_label.config(text="❌ LOAN REJECTED", fg="red")

        details_label.config(
            text=f"Approval Probability: {approval_chance:.2f}%\n"
                 f"Estimated EMI (5 Years @12%): Rs {emi:,.0f}"
        )

    except:
        messagebox.showerror("Error", "Please enter valid information!")

# =====================
# UI
# =====================
root = tk.Tk()
root.title("Premium Loan Approval System")
root.geometry("900x750")
root.configure(bg="#0b1120")

header = tk.Label(root,
                  text="PREMIUM LOAN APPROVAL SYSTEM",
                  font=("Segoe UI", 24, "bold"),
                  bg="#0b1120",
                  fg="#38bdf8")
header.pack(pady=30)

frame = tk.Frame(root, bg="#111827", bd=0)
frame.pack(pady=20, padx=80, fill="both", expand=True)

def create_entry(label):
    tk.Label(frame, text=label,
             font=("Segoe UI", 14),
             bg="#111827", fg="white").pack(pady=(15,5))
    entry = tk.Entry(frame, font=("Segoe UI", 14), width=35)
    entry.pack()
    return entry

entry_age = create_entry("Age")
entry_salary = create_entry("Monthly Salary")
entry_credit = create_entry("Credit Score (300-850)")
entry_loan = create_entry("Loan Amount")

tk.Label(frame,
         text="Employment Status (1 = Employed, 0 = Unemployed)",
         font=("Segoe UI", 14),
         bg="#111827", fg="white").pack(pady=(15,5))

employment_var = tk.IntVar()
employment_menu = tk.OptionMenu(frame, employment_var, 0, 1)
employment_menu.config(font=("Segoe UI", 13))
employment_menu.pack()

predict_btn = tk.Button(frame,
                        text="Evaluate Loan",
                        command=predict_loan,
                        font=("Segoe UI", 15, "bold"),
                        bg="#2563eb",
                        fg="white",
                        width=25,
                        height=2)
predict_btn.pack(pady=30)

result_label = tk.Label(frame,
                        text="",
                        font=("Segoe UI", 20, "bold"),
                        bg="#111827")
result_label.pack(pady=10)

details_label = tk.Label(frame,
                         text="",
                         font=("Segoe UI", 14),
                         bg="#111827",
                         fg="#e5e7eb")
details_label.pack(pady=10)

accuracy_label = tk.Label(root,
                          text=f"Model Accuracy: {accuracy*100:.2f}%",
                          font=("Segoe UI", 12),
                          bg="#0b1120",
                          fg="gray")
accuracy_label.pack(pady=10)

footer = tk.Label(root,
                  text="Developed by Khadija",
                  font=("Segoe UI", 12, "italic"),
                  bg="#0b1120",
                  fg="#94a3b8")
footer.pack(side="bottom", pady=20)

root.mainloop()