```markdown
# GP CALCULATOR

A web-based Grade Point (GP) Calculator built for university students on a 5-point grading scale. Students can register, enter their courses and scores, calculate their GP, view their result, and download a PDF result sheet.

---

## Live Demo
Coming soon — deploying to Railway

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0.4 |
| Database | Supabase (PostgreSQL) |
| Frontend | HTML + CSS + Vanilla JavaScript |
| PDF Export | xhtml2pdf |
| Language | Python 3.14.1 |

---

## Colour Scheme

| Element | Colour |
|---|---|
| Background | `#0a0a0a` (deep black) |
| Cards | `#111111` |
| Borders | `#222222` |
| Primary text | `#ffffff` |
| Secondary text | `#888888` |
| Accent | `#22c55e` (green) |

---

## Grading Logic (Nigerian 5-Point Scale)

| Score | Grade Point | Letter |
|---|---|---|
| 70–100 | 5 | A |
| 60–69 | 4 | B |
| 50–59 | 3 | C |
| 45–49 | 2 | D |
| 40–44 | 1 | E |
| 0–39 | 0 | F |

**GP Formula:** `GP = Σ(grade_point × credit_unit) / Σ(credit_units)`

### Class of Degree
| GP Range | Class |
|---|---|
| 4.50–5.00 | First Class |
| 3.50–4.49 | Second Class Upper |
| 2.40–3.49 | Second Class Lower |
| 1.50–2.39 | Third Class |
| 0.00–1.49 | Pass |

---

## Features

- User authentication — Signup, Login, Logout
- Student profile — Name, Matric Number, Department, Programme, Level
- Dynamic course input form — JavaScript generated rows
- Front-end validation — Score (0–100), Credit Unit (1–6)
- Live unit counter as courses are filled
- Confirm page — review before saving
- GP engine — calculates GP + Class of Degree
- Saves results to Supabase (PostgreSQL)
- Download result as PDF
- Responsive — works on mobile and desktop
- 1 semester limit per user

---

## Project Structure

```
gp_calculator_project/
├── accounts/
│   ├── models.py       # UserProfile model
│   ├── views.py        # signup, login, logout, dashboard
│   └── urls.py
├── calculator/
│   ├── models.py       # Semester + Course models
│   ├── views.py        # All calculator views + PDF
│   ├── utils.py        # GP engine
│   └── urls.py
├── core/
│   ├── views.py        # Landing page
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   └── calculator/
│       ├── setup.html
│       ├── courses.html
│       ├── confirm.html
│       ├── result.html
│       └── result_pdf.html
├── static/
│   └── css/
│       └── style.css
└── manage.py
```

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/Prudentdev-xyz/GP_CALCULATOR.git
cd GP_CALCULATOR
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root:
```
SECRET_KEY=your-secret-key
DATABASE_NAME=postgres
DATABASE_USER=your-supabase-user
DATABASE_PASSWORD=your-supabase-password
DATABASE_HOST=your-supabase-host
DATABASE_PORT=5432
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Run server
```bash
python manage.py runserver
```

---

## URL Structure

| URL | Description |
|---|---|
| `/` | Landing page |
| `/auth/signup/` | Register |
| `/auth/login/` | Login |
| `/auth/logout/` | Logout |
| `/auth/dashboard/` | Student dashboard |
| `/semester/setup/` | Semester setup form |
| `/semester/courses/` | Course input form |
| `/semester/confirm/` | Confirm courses |
| `/semester/<id>/result/` | GP result page |
| `/semester/<id>/pdf/` | Download PDF |

---

## Author

**AbdQoharr**
- GitHub: [@Prudentdev-xyz](https://github.com/Prudentdev-xyz)

---

## License
MIT License
